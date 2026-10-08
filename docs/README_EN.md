<h1 align="center">CC's AI Diary</h1>

<h3 align="center">Turn content creation into a calibratable experiment · Knowledge-Base Edition</h3>

<p align="center">
  <a href="../README.md">简体中文</a>
  &nbsp;·&nbsp;
  <strong>English</strong>
  &nbsp;·&nbsp;
  <a href="../LICENSE">MIT</a>
</p>

---

## In one line

Turn every post into a **controlled experiment**: score → blind-predict → publish → retro → upgrade your formula.
The more you post, the sharper your judgment gets.

## The problem it solves

Most creators are stuck in one loop:

> Publish → check the numbers → learn nothing → post again by gut feeling

Someone who shipped 200 pieces isn't necessarily sharper than someone who shipped 5 — because nothing ever gets **logged**. This tool keeps the books for you and lets your judgment evolve on its own.

## What's new (Knowledge-Base Edition)

**1. Account knowledge base `knowledge_base/` (the headline feature)**

Created automatically at init, with 6 categories that keep all your account material in one place:

```
knowledge_base/
├── 对标账号/ (benchmarks)       what your competitors are doing
├── 文案口语/ (voice)            your tone & writing templates
├── 爆款规律/ (viral patterns)   breakdowns & scoring rules
├── 选题池/   (topic pool)       candidate topics
├── 数据复盘/ (data retro)       history & retrospectives
└── 账号策略/ (account strategy) positioning, pivot, monetization
```

Before writing, picking topics, or doing a retro — check here first. No more digging through chat history for material.

**2. Three companion protocols** (`shared-references/`)
- `data-integrity-protocol.md` — single source of truth for retros
- `voice-calibration-protocol.md` — read real published copy before writing
- `storage-mapping.md` — file ↔ directory mapping

**3. New templates & tools**
- New in `templates/`: account audit, knowledge-base index (monetization diagnosis & viral-pattern methodology live in `docs/05`, `docs/04`)
- `tools/upsert_published_record.py` — publish-record helper

**4. Chinese how-to docs** (`docs/01-05`)
5-min quickstart / client data checklist / FAQ / viral-pattern methodology / monetization diagnosis

## Three iron rules

1. **Blind prediction** — write the prediction before seeing any data; once written it's locked by a hook and can't be changed.
2. **Upgrade = full re-scoring** — when the formula changes, all history is re-scored; the new ranking must match reality ≥80% and pass an independent AI audit.
3. **The rubric is a workbench, not a museum** — refuted observations are deleted; git history is the archive.

## Install

```bash
git clone https://github.com/CC-Diary/democheat-yourself.git
cd cheat-yourself
bash install.sh
```

Claude Code · Codex (`bash install.sh --codex`) · Both (`bash install.sh --all`)
Uninstall: `bash uninstall.sh` (your content data is untouched)

## Usage

Inside your content project, say "**初始化**" (init), then answer five questions.
Daily: `打分` (score) · `启动预测` (start prediction) · `拍了` (shot) · `已发布` (shipped) · `复盘` (retro) · `状态` (status) · `推荐选题` (find topic) · `升级公式` (bump rubric)

## Open-source notice

This project is an improved work based on open-source, released under **MIT**.
Core methodology adapted from **XBuilderLAB's open-source project `cheat-on-content`** (MIT).
Free to use, modify, and distribute — including commercial and closed-source use. Your data stays local.

## License

MIT
