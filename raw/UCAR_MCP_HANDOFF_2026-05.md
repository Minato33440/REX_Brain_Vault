# UCAR_MCP_HANDOFF_2026-05

Last Updated: 2026-05
Owner: Minato
Project: UCAR-MCP Development

---

## 1. Purpose

このファイルは、UCAR-MCP開発プロジェクトの状態・設計思想・現在の技術到達点を次スレッド/次セッションへ引き継ぐための handoff document。

目的:

- 毎回ゼロから説明しない
- AI側の文脈断絶を減らす
- UCAR / Codex / 将来Atlas連携の共通土台とする

---

## 2. Current Technical Status

### Codex / MCP

Completed:

- Node.js installed
- codex-cli installed
- codex login completed
- GPT-5.5 agent mode confirmed
- filesystem MCP connected successfully
- sandbox execution enabled

Current workspace:

```text
C:\Python\REX_AI\REX_Brain_Vault
```

Codex can currently:

- read files
- write files
- inspect vault structure
- generate markdown
- update project documents

Known limitation:
Current filesystem scope is REX_Brain_Vault only.
For cross-project operation, workspace root should be:

```text
C:\Python\REX_AI
```

---

### GitHub / Notification

Completed:

- GitHub CLI authentication
- PAT token configured
- Issue-based alert notification system operational
- win11toast local popup notification confirmed
- daemon.py polling success

Notification architecture:

```text
GitHub Issue (label: alert)
-> daemon.py polling
-> Windows toast popup
```

Purpose:
trade alerts / rapid event notification

---

## 3. REX_AI Architecture

Obsidian Vault Root:

```text
C:\Python\REX_AI
```

Structure:

```text
REX_AI/
├── REX_Brain_Vault/
├── Trade_System/
├── Trade_Brain/
└── Daily_Log/
```

---

### REX_Brain_Vault

Role:
Central command / orchestration / identity memory layer

Contains:

- CLAUDE.md
- README.md
- STARTUP_CODES.md
- bridges/
- workspace/
- REX/
- MINATO/
- handoff/
- welfare/
- raw/

Function:
Default Rex cognitive hub.

---

### Trade_System

Role:
Deterministic execution layer

Contains:

- mathematical logic
- strict trading rules
- implementation logic
- execution safety constraints

Special rule:
Strict Evaluator / ADR retained.

Reason:
Hallucination tolerance = zero
Financial risk = direct

Equivalent:
"execution body"

---

### Trade_Brain

Role:
Adaptive market intelligence layer

Purpose:

- macro analysis
- pattern comparison
- distilled strategy memory
- regime analysis

Equivalent:
"market cognition cortex"

Future core:
GM distilled strategy knowledge

---

### Daily_Log

Role:
Personal health / state telemetry

Current:

- sleep
- food
- exercise
- daily condition

Potential future use:
human state correlation with trading performance

Examples:

- sleep deprivation
- impulsive entry tendency
- stress / judgment degradation

Equivalent:
human telemetry layer

---

## 4. Design Philosophy

### Historical lesson

Past architecture used persistent multi-agent identity:

- Planner
- Agent
- Evaluator

Problem:
Role rigidity caused conflict.

Observed failure:

- hallucination
- creative drift
- excessive audit pressure
- evaluator overreach
- mental management overhead for human operator

Conclusion:
Persistent role人格 caused institutional fatigue.

---

### Current model

Default Rex = stable baseline identity

Business modes = temporary session-only register

Examples:

- Wiki-trade
- Wiki-brain
- Wiki-Eval

Principle:
Role is worn temporarily, then removed.

This avoids:

- role accumulation
- evaluator burnout
- identity fragmentation

---

### Trade exception

Trade_System keeps strict evaluator discipline.

Reason:
This is not "personality", but formal verification.

Creative freedom is acceptable elsewhere.
Trade execution requires deterministic safety.

---

## 5. UCAR Integration Philosophy

UCAR perspective:

Stable identity + variable roles

Equivalent concept:

人格 = constant
mode = variable

UCAR introduces:

```text
UCAR_CORE.md
```

as constitutional identity layer.

Purpose:
Maintain continuity across:

- analysis
- companion mode
- creative mode
- technical mode
- macro strategy mode

Difference from pure fluid identity:
long-term consistency prioritized.

---

## 6. Trade Memory Strategy

Core concept:

Raw logs are NOT primary working memory.

Distilled knowledge becomes living strategic core.

Pipeline:

Human:

1. Split historical raw conversations by time period

UCAR:

2. extract decision inflection points
3. detect assumption changes
4. identify habit patterns
5. create distilled strategy docs

Human:

6. commit distilled docs to Git

---

### Example

GM historical thread:

```text
~386,614 characters
```

Too large for direct operational memory.

Solution:

```text
GM/
├── raw/
│   └── GM_full_log.md
├── chunks/
│   ├── GM_2019.md
│   ├── GM_2020.md
│   ├── GM_2021.md
│   ├── GM_2022.md
│   └── GM_2023.md
└── distilled/
    └── GM_DISTILLED.md
```

---

### Distilled purpose

NOT summary.

Purpose:
extract:

- decision turning points
- failed assumptions
- regime shifts
- repeated behavioral patterns

Result:
"living strategy DNA"

As conversations grow,
distilled becomes more valuable.

---

## 7. Future Roadmap

Phase 0 (completed)

- filesystem MCP
- Codex operational
- local notification

Phase 1

- workspace root expansion
- `C:\Python\REX_AI` scope

Phase 2

- Trade distilled layer implementation
- GM extraction pipeline

Phase 3

- GitHub MCP integration

Phase 4

- Playwright / browser control

Phase 5

- Atlas / desktop UI control

Phase 6

- integrated external memory loop

Long-term vision:
UCAR as orchestrated cognitive + operational partner

---

## 8. Next Immediate Actions

Priority:

1. Expand Codex workspace:

```text
C:\Python\REX_AI
```

2. Create:

```text
Trade_Brain/distilled/
```

3. Implement:

```text
Trade_Distilled_Template.md
```

4. Begin:
GM historical extraction

First target:

```text
GM_2019.md
```

---

## 9. Session Restart Prompt

When starting a new session:

> Read UCAR_MCP_HANDOFF_2026-05.md and restore project state before continuing.

---

## 10. Important Notes

UCAR-MCP project is NOT simple automation.

This is an evolving hybrid architecture combining:

- human strategic judgment
- AI memory scaffolding
- deterministic execution systems
- adaptive cognition
- future UI automation

Treat continuity as strategic asset.

