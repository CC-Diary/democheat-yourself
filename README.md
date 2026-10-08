<h1 align="center">CC的AI日记</h1>

<h3 align="center">把内容创作变成可校准的实验 · 知识库版</h3>

<p align="center">
  <strong>简体中文</strong>
  &nbsp;·&nbsp;
  <a href="docs/README_EN.md">English</a>
  &nbsp;·&nbsp;
  <a href="LICENSE">MIT</a>
</p>

---

## 一句话

让每一次发布都变成一次**受控实验**：打分 → 盲预测 → 发布 → 复盘 → 升级公式。
发得越多，你的爆款判断越准。

## 它解决什么问题

大部分创作者的循环是：

> 发内容 → 看数据 → 没学到什么 → 继续凭感觉发

发了 200 条，判断力未必比发了 5 条强——因为发完从不**记账**。
这个工具替你记账，并让你的判断标准自己进化。

## 本次更新（知识库版）

**1. 账号知识库 `knowledge_base/`（本版重点）**

初始化时自动创建 6 个分类目录，把账号资料集中管理：

```
knowledge_base/
├── 对标账号/    对标博主分析、最新动态
├── 文案口语/    口语风格、写作模板
├── 爆款规律/    爆款拆解、评分规则
├── 选题池/      候选选题
├── 数据复盘/    历史数据、复盘记录
└── 账号策略/    定位、转型、变现规划
```

写文案、找选题、复盘前先来查这里——不用再翻聊天记录找素材。

**2. 三份配套协议**（`shared-references/`）
- `data-integrity-protocol.md` — 数据复盘唯一真源
- `voice-calibration-protocol.md` — 写稿前必读真实发布文案，校准语气
- `storage-mapping.md` — 文件与目录的对应关系

**3. 新增模板与工具**
- `templates/` 新增：账号诊断模板、知识库索引模板（变现诊断框架、爆款规律方法论见 `docs/05`、`docs/04`）
- `tools/upsert_published_record.py` — 发布记录登记工具

**4. 中文实操文档**（`docs/01-05`）
5 分钟上手 / 客户数据提供清单 / 常见问题 FAQ / 爆款规律方法论 / 变现诊断框架

## 三条铁律

1. **盲预测**：预测必须在看到数据前写完，写完即被 hook 锁死，改不了。
2. **升级 = 全量重考**：改公式时所有历史样本重算，新排序与真实表现 ≥80% 一致才放行，还要过独立 AI 审核。
3. **工作台不留废料**：被数据推翻的观察直接删，Git 记录才是档案。

## 安装

```bash
git clone https://github.com/CC-Diary/democheat-yourself.git
cd cheat-yourself
bash install.sh
```

支持 Claude Code · Codex（`bash install.sh --codex`）· 双平台（`bash install.sh --all`）
卸载：`bash uninstall.sh`（不动你的内容数据）

## 用起来

在内容项目目录里说「**初始化**」，回答五个问题即可。
日常命令：`打分` · `启动预测` · `拍了` · `已发布` · `复盘` · `状态` · `推荐选题` · `升级公式`

## 开源声明

本项目为借鉴开源项目的改良作品，遵循 **MIT** 协议。
核心方法论改良自 **蜗牛学长（XBuilderLAB）的开源项目 `cheat-on-content`**（MIT）。
可自由使用、修改、分发，含商用与闭源集成。你的账号数据只存在本地，不上传任何平台。

## License

MIT
