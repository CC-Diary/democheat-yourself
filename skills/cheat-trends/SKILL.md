---
name: cheat-trends
description: 把候选素材整理成候选池：读用户粘贴（或用户自建源）的输入 → 去重 + 粗打分 + 写入 candidates.md。**绝大部分人没有候选池——这是让"我没素材"问题在 onboarding 第二步就消失的钥匙**。触发词："抓热点"/"补充候选池"/"今天有什么可做的"/"找选题"。本仓库不内置第三方热点抓取源。
argument-hint: [— sources: <comma-separated>] [— max-per: 20]
allowed-tools: Bash(*), Read, Write, Edit, Glob, WebFetch, Skill
---

# /cheat-trends — 候选池补充

来源模式：读用户粘贴 / 用户自建 source 的输入 → 去重 → 粗打分 → 写入 `candidates.md`。

> ⚠️ 本仓库**不内置**任何第三方热点抓取源（不含 aihot / 微博热搜 / 知乎热榜 / TrendRadar 等）。
> 唯一内置来源是 `manual-paste`。要接自己的源见 [shared-references/data-source-routing.md](../../shared-references/data-source-routing.md)。

## Overview

```
[用户：抓热点 / 补充候选池]
  ↓
[Phase 0: 读 .cheat-state.json 拿 enabled sources]
  ↓
[Phase 1: 对每个来源取输入]
  ↓
[Phase 2: normalize 到 candidate-schema]
  ↓
[Phase 3: 去重（vs candidates / predictions / trends-history）]
  ↓
[Phase 4: 对每个新 item 粗打分（调 cheat-score 内联逻辑）]
  ↓
[Phase 5: 排序 + 询问用户哪些加入 candidates.md]
  ↓
[Phase 6: 写入 + 更新 trends-history.jsonl 缓存]
```

## Constants

- **TREND_SOURCES = ["manual-paste"]** — 启用来源列表（内置仅 manual-paste；用户可自建并在此登记）
- **LOOKBACK_HOURS = 24** — 参考最近 N 小时的素材
- **MAX_PER_SOURCE = 20** — 每个来源最多 N 条
- **DEDUPE = true** — 去重开关
- **AUTO_SCORE = true** — 整理后自动调 cheat-score 粗打分
- **MIN_COMPOSITE_TO_SUGGEST = 6.0** — 低于此分的不推荐用户加入候选池（仍写入 trends-history 避免下次重复推）

> 💡 调用时覆盖：`/cheat-trends — sources: manual-paste,<你的自建源> — max-per: 10`

## Inputs

| 必填 | 来源 |
|---|---|
| `.cheat-state.json` | 默认 sources |
| `adapters/trend-sources/<name>.md` | 自建源的可选实现描述（本仓库默认无内置源） |
| `candidates.md` | 去重对照 |
| `predictions/*.md` | 去重对照（已发的不再推） |
| `.cheat-cache/trends-history.jsonl` | 历史素材去重缓存 |

## Workflow

### Phase 0: 读启用的来源

```python
# 伪代码
state = read('.cheat-state.json')
enabled_sources = args.sources or state.get('enabled_trend_sources', ['manual-paste'])
```

如来源为空 → 输出引导：

```
你目前没有启用任何候选来源。

最简单的方式（默认就有）：
- 直接跑：/cheat-trends
  然后把你今天看到的候选 URL / 标题粘进来（每行一条），我来去重 + 粗打分。

要接自己的源：
- 写 adapters/trend-sources/<name>.md，再登记到 .cheat-state.json 的 enabled_trend_sources
- 详见 shared-references/data-source-routing.md
```

### Phase 1-2: 取输入 + normalize

对每个来源取输入（实际是 Bash / 询问用户 / WebFetch）：

| 来源 | 实现机制 |
|---|---|
| `manual-paste`（内置） | 询问用户："粘贴你今天的候选 URL/标题列表（每行一条）" → 解析每行，对 URL 做 WebFetch 补 snippet |
| 用户自建源 | 读其 `adapters/trend-sources/<name>.md` 描述的方式取数；可用性由用户自己保证 |

每个来源输出符合 [candidate-schema.md](../../shared-references/candidate-schema.md) 的 items。

**优雅降级**：单来源失败 → skip，**不抛异常**，在汇总里说明：
```
✅ manual-paste: 5 条（用户输入）
⚠️  <自建源>: 跳过（用户未配置 / 端点不可用）
```

### Phase 3: 去重

按 [candidate-schema.md](../../shared-references/candidate-schema.md) 的"去重协议"：

1. 对每个 item 算 id（`sha256(source_type + normalized_title + url_path)[:12]`）
2. 检查 `candidates.md` 已含此 id → 跳过
3. 检查 `predictions/*.md` 已含此 id → 跳过
4. 检查 `.cheat-cache/trends-history.jsonl` 已含此 id 且 `rejected_at != null` → 跳过

去重统计写到汇总报告里。

### Phase 4: 粗打分

`AUTO_SCORE=true` 时，对每条新 item：
1. 用 item 的 `snapshot_text` 作为输入
2. 按当前 rubric 给 7 维打分（**不**调 `/cheat-score` 子 skill 走 IO；inline 复用打分逻辑）
3. 算 composite
4. 给一句 rationale

**注意**：粗打分 ≠ 正式预测。预测必须基于最终稿（用户改过的），这里的打分只是"是否值得展开写"的粗筛。

`AUTO_SCORE=false` 时，items 写入 candidates.md 时 composite=null，需要后续手动 `/cheat-score`。

### Phase 5: 排序 + 询问

按 composite 降序，过滤掉 composite < `MIN_COMPOSITE_TO_SUGGEST` 的：

```
✅ 候选整理完成。统计：
- manual-paste: 5 条（用户输入）

去重后剩 5 条新 item。
粗打分后 3 条 composite ≥ 6.0：

| # | 标题 | source | composite | bucket | rationale |
|---|---|---|---|---|---|
| 1 | 为什么我们都讨厌主动联系朋友 | manual-paste | 8.4 | 30-100w | ER+QL 双 5，AB 普适 |
| 2 | "她不一样"的一千种变体 | manual-paste | 8.1 | 30-100w | MS 候选维度高 |
| 3 | ...... |

哪些加入 candidates.md？
- 全部加 → 回 "all"
- 选几个 → 回 "1, 3, 5"
- 都不要 → 回 "none"（这些会被记到 trends-history 避免下次重复推）
```

### Phase 6: 落盘

用户响应后：
1. 选中的 items → 按 [candidate-schema.md](../../shared-references/candidate-schema.md) 的"Markdown 表示"格式追加到 `candidates.md`
2. 所有拿到的 items（不管选中与否）→ append 到 `.cheat-cache/trends-history.jsonl`：
   ```jsonl
   {"id": "...", "title": "...", "source": "...", "snapshot_at": "...", "rejected_at": null|"<ISO>", "fetched_at": "<ISO>"}
   ```

### Phase 7: 状态更新

```json
{
  "last_trends_run_at": "<ISO>",
  "last_trends_added_count": 5
}
```

## Key Rules

1. **不抛异常**。单来源失败 → skip + 报告。无可用来源 → 走 manual-paste 询问用户
2. **manual-paste 永远在**。它是唯一内置来源，也是兜底——必须能跑
3. **去重是硬约束**。同 id 不重复推；用户拒绝过的 6 个月内不再推
4. **粗打分要诚实标注**。在 candidates.md 的 entry 里标 `composite (rough, snapshot-based)`，避免与 prediction 的精打分混淆
5. **不直接进 predictions/**。trends 只产 candidates，predict 是另一个动作
6. **不代接第三方源**。本仓库不内置、不背书、不提供第三方热点源的接入说明

## Refusals

- 「帮我直接抓微博 / 知乎 / 抖音的实时热榜」 → 拒绝。本仓库不内置第三方热点抓取源（抓取合规 + 授权边界由用户自负）。改为引导用户**手动粘贴**，或自建源
- 「跳过去重，把所有抓到的都写进去」 → 拒绝。会污染候选池，下次 recommend 时排序失效
- 「跳过粗打分，直接写 raw 标题」 → 允许（`AUTO_SCORE=false`），但提示用户后续需要 `/cheat-score` 才能进 recommend 池

## Integration

- 上游：用户配置 `.cheat-state.json` 的 `enabled_trend_sources` 数组
- 下游：`/cheat-recommend` 直接读 `candidates.md` 排序——trends 写完，recommend 立刻看到
- 与 `/cheat-init`：onboarding Q4 选"没有候选池"的用户被引导到这里
- 与 `/cheat-status`：status 看板显示"上次补充候选池：X 天前 / 待清理候选池：Y 条"

## 自建源实现注意事项

若用户/维护者新增一个 source，`adapters/trend-sources/<name>.md` 必须文档化以下：
1. **依赖**：API key / cookie / package
2. **取数接口**：调用方式（python script path / shell command / API endpoint）
3. **输出 schema**：必须符合 candidate-schema.md
4. **失败模式**：常见错误 + 优雅降级行为
5. **稳定性等级**：★ 1-5 颗星

⚠️ **接入第三方源前，请自行确认其用户协议 / robots / 著作权 / 商用授权边界。**
