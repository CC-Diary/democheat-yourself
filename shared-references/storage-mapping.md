# 原 Skill 存储到 SuperC 知识库的映射

评分、盲预测、复盘和 rubric bump 逻辑保留；只替换它们读写的存储位置。

| 原 Skill 名称 | SuperC 唯一存储位置 | 内容边界 |
|---|---|---|
| `benchmark.md` | `knowledge_base/对标账号/对标账号索引.md` | 对标账号、样本、拆出的借鉴模式；不算 SuperC 已发布数据 |
| `audience.md` | `knowledge_base/账号策略/受众画像.md` | 从真实评论和复盘派生的受众判断；标注证据来源 |
| `script_patterns.md` | `knowledge_base/文案口语/script_patterns.md` | 已验证和待验证的写作结构、句式和节奏 |
| `rubric_notes.md` | `knowledge_base/爆款规律/rubric_notes.md` | 当前评分公式和维度定义；不得写真实播放等实绩 |
| `candidates.md` | `knowledge_base/选题池/candidates.md` | 待做选题；不得伪装成已发布内容 |
| `rubric-memo.md` | `knowledge_base/爆款规律/rubric-memo.md` | rubric 升级用的证据和观察；不进入盲评分白名单 |
| `.cheat-state.json` | `knowledge_base/账号策略/运行状态.json` | 当前模式、版本、队列和流程状态；根目录可保留兼容镜像 |
| `content.db` | `knowledge_base/数据复盘/content.db` | 从真实发布主表重建的查询缓存，不是事实来源 |

## 唯一真源

`knowledge_base/数据复盘/` 是已发布文案和真实数据的事实来源。其他文件只能引用它、提炼规律或生成候选，不能反向覆盖事实。

`content.db` 只能由主表重建或 upsert，禁止直接把预测、草稿、对标样本写入数据库。数据库污染时，删除后从主表重建，不影响原始记录。

## 评分与进化的路径替换

- `cheat-score` / `cheat-predict`：读取 `knowledge_base/爆款规律/rubric_notes.md`；盲评分仍禁止读取 `数据复盘/`、`rubric-memo.md` 和 `受众画像.md`。
- `cheat-retro`：从 `数据复盘/` 读取真实结果，观察写入 `爆款规律/rubric-memo.md`，确认后的通用规则才更新 `rubric_notes.md`。
- `cheat-bump`：使用 `数据复盘/` 的真实样本重打，更新 `rubric_notes.md`；升级证据留在 `rubric-memo.md`。
- `cheat-seed` / `cheat-recommend` / `cheat-trends`：读写 `选题池/candidates.md`，同时参考 `对标账号/`、`文案口语/` 和 `账号策略/`。
- `cheat-learn-from`：只写 `对标账号/`、`文案口语/` 和必要的 `爆款规律/` 定性信号，禁止写 `数据复盘/`。
