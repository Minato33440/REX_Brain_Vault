#!/usr/bin/env python3
"""wrapup.py - v0 会話要点抽出スクリプト (Mem0 なし)

設計合意 (2026-05-19, ミナト × Rex):
  - 入力 = raw/YYYY-M-D.md (手動ペースト済みセッション) + .wrapup_state.json (チェックポイント)
  - 差分抽出: 前回処理済み行以降だけを Haiku に 1 回渡す (前回サマリは渡さない)
  - 送る前にローカルでデデュープ (Claude.ai の thinking ヘッダ二重コピー等)
  - Haiku が差分を「結果が出たトピック単位」に内部分割し、各単位に 要点 + 流れ を出力
  - 出力 = personal/dialogues/YYYY-MM-DD-HHMM-<topic>.md に地層追記
  - 真実の源は raw/。state が消えても raw から復旧できる。
  - 既定はプレビュー (dry-run)。--write で初めてファイル書込 & チェックポイント前進。

使い方 (セッション原文は raw/session/ に置く。ファイル名だけで解決):
  python wrapup.py 2026-5-19.md                 # プレビュー (書込なし)
  python wrapup.py 2026-5-19.md --write          # 確定 (追記 + state 更新)
  python wrapup.py 2026-5-19.md --write --new "mem0_design"  # 別スレ = 新ファイル
  python wrapup.py 2026-5-19.md --keep-open      # 末尾の未完ブロックを次回に残す
  (raw/session/foo.md や絶対パスでも可)

環境変数 (.env 自動読込: REX_Brain_Vault/.env → リポルート/.env → CWD/.env の順):
  ANTHROPIC_API_KEY  必須
  WRAPUP_MODEL       任意。既定 claude-haiku-4-5-20251001。別 Haiku を使うなら上書き。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

# tools/ の親 = REX_Brain_Vault をベースにする
BASE = Path(__file__).resolve().parent.parent
SESSION_DIR = BASE / "raw" / "session"          # セッション原文ルート
STATE_PATH = BASE / "personal" / ".wrapup_state.json"
DIALOGUES_DIR = BASE / "personal" / "dialogues"


def load_env() -> None:
    """依存追加なしの簡易 .env ローダ。既存の環境変数は上書きしない (export が優先)。"""
    for cand in (BASE / ".env", BASE.parent / ".env", Path.cwd() / ".env"):
        if not cand.exists():
            continue
        for line in cand.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_env()
DEFAULT_MODEL = os.environ.get("WRAPUP_MODEL", "claude-haiku-4-5-20251001")

TS_RE = re.compile(r"^\s*\d{1,2}:\d{2}\s*$")  # Claude.ai のビート (例: 6:31, 10:38)


# ---------- state ----------
def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------- raw 読取 ----------
def dedup_lines(lines: list[str]) -> list[str]:
    """直前の非空行と完全一致する行を落とす (隣接重複のみ。離れた繰り返しは残す)。"""
    out: list[str] = []
    prev_nonblank = None
    for ln in lines:
        s = ln.strip()
        if s and s == prev_nonblank:
            continue
        out.append(ln)
        if s:
            prev_nonblank = s
    return out


def read_delta(raw_path: Path, processed_line: int, keep_open: bool):
    """processed_line 行目以降を返す。keep_open なら最後の timestamp 境界までに切り詰める。"""
    all_lines = raw_path.read_text(encoding="utf-8").splitlines()
    total = len(all_lines)
    delta = all_lines[processed_line:]
    end_line = total

    if keep_open:
        last_ts = None
        for i, ln in enumerate(delta):
            if TS_RE.match(ln):
                last_ts = i
        if last_ts is None:
            return "", processed_line, processed_line  # 完結ブロック無し → 次回へ
        delta = delta[: last_ts + 1]
        end_line = processed_line + last_ts + 1

    delta = dedup_lines(delta)
    return "\n".join(delta).strip(), processed_line, end_line


# ---------- 抽出 ----------
PROMPT = """以下は人間(ミナト)と Claude(Rex)の会話ログの一区間です。
ログには Claude.ai のタイムスタンプ行 (例: 6:31) や思考要約行が混ざっています。

この区間を「議論に結果・合意・結論が出たトピック」単位に内部分割し、
各単位について次を抽出してください:
  - title: その単位の短い見出し (日本語可)
  - timestamp: その単位の直前にある「行全体がタイムスタンプだけの行」(Claude.ai の
               ターン区切り。例: その行に 6:31 とだけある) の値。文章中で言及されて
               いる時刻 (例「## 6:31 を…」「13:50 のファイル」) は絶対に使わない。
               該当する区切り行が無ければ空文字 ""。
  - points: 事実・決定・preference の箇条書き (高速参照用、簡潔に)
  - flow:  その合意/結論に至った流れ・ニュアンスを 2-4 文の段落で

原文に無い固有名詞・比喩・用語を創作しないこと。要点も流れも原文に根拠のある内容だけ。
ラフでよい。網羅や水増しはしない。零れた要点を化石化する感覚で。
抽出結果は必ず save_segments ツールで返すこと。

--- 会話ログ ---
"""

EXTRACT_TOOL = {
    "name": "save_segments",
    "description": "抽出した会話の要点を構造化して返す",
    "input_schema": {
        "type": "object",
        "properties": {
            "segments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "単位の短い見出し"},
                        "timestamp": {
                            "type": "string",
                            "description": "直前の『行全体が時刻だけの行』の値。文章中で言及された時刻は使わない。無ければ空",
                        },
                        "points": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "事実・決定・preference の箇条書き",
                        },
                        "flow": {"type": "string", "description": "合意/結論に至った流れ 2-4 文"},
                    },
                    "required": ["title", "points", "flow"],
                },
            }
        },
        "required": ["segments"],
    },
}


def call_claude(delta_text: str, model: str) -> list[dict]:
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic SDK 未導入: pip install anthropic")

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY を読む
    try:
        msg = client.messages.create(
            model=model,
            max_tokens=8000,
            tools=[EXTRACT_TOOL],
            tool_choice={"type": "tool", "name": "save_segments"},
            messages=[{"role": "user", "content": PROMPT + delta_text}],
        )
    except anthropic.APIError as e:
        sys.exit(
            f"Anthropic API エラー (model={model}): {e}\n"
            f"よくある原因: クレジット残高不足 / モデル名不正 / APIキー無効。"
        )
    if msg.stop_reason == "max_tokens":
        print("警告: 出力が max_tokens で打ち切られた。差分が大きすぎる可能性。", file=sys.stderr)
    for block in msg.content:
        if block.type == "tool_use":
            return block.input.get("segments", [])
    # 透明性優先: tool 呼び出しが無ければ捨てずに生テキストを残す
    raw = "".join(getattr(b, "text", "") for b in msg.content)
    return [{"title": "(抽出失敗・生出力)", "points": [], "flow": raw}]


# ---------- 整形 ----------
def slugify(s: str) -> str:
    s = re.sub(r"[\\/:*?\"<>|]", "", s).strip().replace(" ", "_")
    return s[:40] or "untitled"


def parse_date(raw_path: Path) -> str:
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", raw_path.name)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    return dt.date.today().isoformat()


def render(segments: list[dict], beat: str) -> str:
    parts = []
    for seg in segments:
        ts = (seg.get("timestamp") or "").strip() or beat  # raw 時刻優先、無ければ実行時刻
        parts.append(f"## {ts} {seg.get('title', '(no title)')}\n")
        pts = seg.get("points") or []
        if pts:
            parts.append("### 要点\n" + "\n".join(f"- {p}" for p in pts) + "\n")
        flow = seg.get("flow", "").strip()
        if flow:
            parts.append("### 流れ\n" + flow + "\n")
    return "\n".join(parts)


# ---------- main ----------
def main() -> None:
    try:  # Windows コンソールの日本語文字化け対策
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="v0 会話要点抽出 (プレビュー既定)")
    ap.add_argument("raw", help="raw ファイル (REX_Brain_Vault からの相対 or 絶対)")
    ap.add_argument("--write", action="store_true", help="確定: 追記 + state 更新")
    ap.add_argument("--new", metavar="TOPIC", help="別スレ: 新しい dialogue ファイルを作る")
    ap.add_argument("--keep-open", action="store_true", help="末尾の未完ブロックを次回へ残す")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    raw_path = Path(args.raw)
    if not raw_path.is_absolute():
        cand = BASE / args.raw
        raw_path = cand if cand.exists() else SESSION_DIR / args.raw
    if not raw_path.exists():
        sys.exit(f"raw が見つからない: {raw_path}")

    rel_key = str(raw_path.relative_to(BASE)).replace("\\", "/") if BASE in raw_path.parents else str(raw_path)
    state = load_state()
    entry = state.get(rel_key, {"line": 0, "dialogue": None})

    delta, start, end = read_delta(raw_path, entry["line"], args.keep_open)
    if not delta:
        print(f"[{rel_key}] 未処理の完結ブロック無し (processed={entry['line']})。何もしない。")
        return

    print(f"[{rel_key}] 行 {start+1}..{end} を抽出 (model={args.model})\n")
    segments = call_claude(delta, args.model)

    # タイムスタンプ検証: delta 内に「行まるごとが時刻だけ」の区切り行として
    # 実在する値のみ採用。文章中で言及された時刻 (自己言及的な会話で頻発) は
    # 破棄し、空にして実行時刻へ fallback させる。
    valid_ts = {ln.strip() for ln in delta.splitlines() if TS_RE.match(ln)}
    for seg in segments:
        if (seg.get("timestamp") or "").strip() not in valid_ts:
            seg["timestamp"] = ""

    date = parse_date(raw_path)
    if args.new or not entry.get("dialogue"):
        topic = slugify(args.new) if args.new else slugify(segments[0].get("title", "session"))
        hhmm = dt.datetime.now().strftime("%H%M")
        dialogue_rel = f"personal/dialogues/{date}-{hhmm}-{topic}.md"
    else:
        dialogue_rel = entry["dialogue"]
    dialogue_path = BASE / dialogue_rel

    beat = dt.datetime.now().strftime("%H:%M")
    body = render(segments, beat)

    if not args.write:
        print("=" * 60)
        print(f"DRY RUN (書込なし / checkpoint 据置)  ->  {dialogue_rel}")
        print("=" * 60)
        print(body)
        print("=" * 60)
        print("確定するなら同じコマンドに --write を付けて再実行。")
        return

    DIALOGUES_DIR.mkdir(parents=True, exist_ok=True)
    if not dialogue_path.exists():
        header = f"# {date} {slugify(args.new) if args.new else segments[0].get('title','session')}\n\nsource: [[{rel_key}]]\n\n"
        dialogue_path.write_text(header, encoding="utf-8")
    with dialogue_path.open("a", encoding="utf-8") as f:
        f.write(body + "\n")

    state[rel_key] = {"line": end, "dialogue": dialogue_rel}
    save_state(state)
    print(f"書込完了 -> {dialogue_rel}  / checkpoint: {entry['line']} -> {end}")


if __name__ == "__main__":
    main()
