# AI 洞察日报 · 站点

> 一个每天自动更新的 AI 资讯站。基于 **Hugo + Hextra** 构建，部署在 **GitHub Pages**，完全免费。

**🌐 在线访问：https://siweimidu.github.io/ai-daily-site/**

---

## 📖 这是什么

这是 AI 洞察日报的**展示前端**。它每天自动从后端仓库拉取日报内容，渲染成一个带侧边栏归档、全文搜索、暗色模式的静态网站。

**它和另外两个仓库的关系：**

| 仓库 | 角色 | 技术 |
|---|---|---|
| **[CloudFlare-AI-Insight-Daily](https://github.com/siweimidu/CloudFlare-AI-Insight-Daily)** | **后端**：抓数据、调 AI、生成日报 | Cloudflare Workers |
| **ai-daily-site**（本仓库） | **前端**：把日报展示成网站 | Hugo + GitHub Pages |

数据流向：

```
后端 Worker（每天 08:00 生成日报）
        │  写入 daily/2026-10-13.md
        ▼
CloudFlare-AI-Insight-Daily 仓库
        │  GitHub Actions 每天 09:00 拉取
        ▼
本仓库 content/cn/ 目录 → Hugo 构建 → GitHub Pages 上线
```

> 你只需要维护**后端仓库**，这个站会自动跟着更新。

---

## ✨ 功能特性

| 特性 | 说明 |
|---|---|
| 📚 **自动归档** | 日报按月份自动分组到侧边栏，可折叠浏览 |
| 🔍 **全文搜索** | 基于 FlexSearch，支持 `Ctrl/Cmd + K` 唤起 |
| 🌓 **暗色模式** | 支持浅色 / 深色 / 跟随系统三种模式 |
| 📱 **响应式** | 手机、平板、桌面自适应 |
| ⚡ **零成本** | 纯静态站，GitHub Pages 免费托管 |
| 🎨 **自动同步** | 每天定时拉取后端内容并重新构建部署 |

---

## 🚀 部署你自己的站点

### 第 1 步：Fork 或新建仓库

推荐直接点右上角 **Fork**，然后改名成你喜欢的仓库名。

如果你的 GitHub 用户名不是 `siweimidu`，Fork 后需要改两处配置（见第 3 步）。

### 第 2 步：启用 GitHub Pages

1. 进入仓库 **Settings → Pages**
2. **Source** 选择 **GitHub Actions**（不要选 "Deploy from a branch"）
3. 保存

### 第 3 步：修改配置指向你的内容源

**改 `hugo.yaml`：**

```yaml
title: AI 洞察日报          # 改成你的站点名
params:
  description: 你的站点描述
```

**改 `.github/workflows/build-book.yaml`**，把源仓库指向你的后端：

```yaml
on:
  workflow_dispatch:
    inputs:
      source_repo:
        default: '你的用户名/CloudFlare-AI-Insight-Daily'   # 改这里
      source_branch:
        default: 'main'
```

### 第 4 步：触发首次构建

1. 进入 **Actions** 标签页
2. 左侧选 **Update Content from Daily Notes** → 点 **Run workflow**
3. 填源仓库地址，运行
4. 等它跑完，会自动触发 **Deploy Hugo site to Pages**
5. 完成后访问 `https://你的用户名.github.io/你的仓库名/`

---

## 📁 目录结构

```
content/cn/                 # 日报内容（自动生成，不用手改）
├── _index.md               #   首页
├── 2026-10/                #   按月份归档
│   ├── _index.md           #     月度索引
│   └── 2026-10-13.md       #     单篇日报
└── tags/                   #   标签页

layouts/                    # Hugo 模板覆盖
├── partials/toc.html       #   侧边栏目录
├── robots.txt              #   SEO 配置
└── _default/_markup/       #   Markdown 渲染规则

scripts/
└── update_home.py          # 更新首页描述与链接

assets/css/custom.css       # 自定义样式
hugo.yaml                   # 站点主配置
.github/workflows/
├── build-book.yaml         # 拉取后端内容并提交
└── pages.yaml              # 构建并部署到 Pages
```

---

## 🔄 两个自动化流程

### 1. 拉取内容（build-book.yaml）

- **触发时机**：每天 UTC 01:00（北京时间 09:00）+ 手动触发
- **做什么**：克隆后端仓库 → 读取 `daily/*.md` → 转成 Hugo 格式 → 提交到 `content/cn/`

**为什么是 09:00？** 后端在 08:00 生成日报，晚一小时确保内容已就绪。

> 想改成别的频率，编辑 `build-book.yaml` 里的 `cron` 表达式。
> 在线工具：https://crontab.guru

### 2. 构建部署（pages.yaml）

- **触发时机**：`build-book` 完成后、`main` 分支有推送、手动触发
- **做什么**：安装 Hugo → 构建静态文件 → 部署到 GitHub Pages

---

## 🛠 本地预览

想在自己电脑上改样式、看效果：

**前置要求：** [Hugo Extended](https://gohugo.io/installation/) 0.147.9+ 和 [Go](https://go.dev/dl/) 1.24+

```bash
git clone https://github.com/siweimidu/ai-daily-site.git
cd ai-daily-site
hugo server -D
```

打开 http://localhost:1313/ai-daily-site/ 即可预览，改文件会实时刷新。

---

## ❓ 常见问题

<details>
<summary><b>站点显示 404</b></summary>

检查顺序：

1. **Settings → Pages** 的 Source 是不是选了 **GitHub Actions**
2. **Actions** 里 `Deploy Hugo site to Pages` 最近一次是否成功
3. 首次部署需要几分钟，稍等再看

</details>

<details>
<summary><b>站点没有内容 / 只有旧内容</b></summary>

1. 去 **Actions → Update Content from Daily Notes → Run workflow** 手动跑一次
2. 确认后端仓库的 `daily/` 目录里确实有 `.md` 文件
3. 检查 `build-book.yaml` 里的 `source_repo` 是不是指向了正确的后端仓库

</details>

<details>
<summary><b>构建报错 "partial adx.html not found"</b></summary>

`layouts/partials/toc.html` 里残留了上游的广告组件引用。删掉这一行即可：

```
{{ partial "adx.html" }}
```

</details>

<details>
<summary><b>中文被推到 /cn/ 子路径下</b></summary>

`hugo.yaml` 缺少中文默认语言配置。加上：

```yaml
defaultContentLanguage: zh
defaultContentLanguageInSubdir: false
languages:
  zh:
    languageCode: zh-CN
    contentDir: content/cn
    languageName: 简体中文
    weight: 1
```

</details>

<details>
<summary><b>Workflow 显示 failed 但看不到任何步骤</b></summary>

通常是 YAML 语法问题（比如 heredoc 内容顶格写，破坏了块标量）。本地用 `python -c "import yaml;yaml.safe_load(open('.github/workflows/x.yaml'))"` 验证。

本仓库已把内嵌的 Python 逻辑抽到 `scripts/update_home.py`，避免这个问题。

</details>

---

## 🎨 自定义

| 想改什么 | 改哪里 |
|---|---|
| 站点标题 | `hugo.yaml` 的 `title` |
| 副标题/描述 | `content/cn/_index.md` |
| 导航菜单 | `hugo.yaml` 的 `menu.main` |
| 配色和样式 | `assets/css/custom.css` |
| 首页卡片 | `content/cn/_index.md` 里的 `{{< cards >}}` |
| 页脚 | 在 `hugo.yaml` 的 `params.footer` 配置 |

---

## 🔗 相关链接

| 链接 | 说明 |
|---|---|
| [后端仓库](https://github.com/siweimidu/CloudFlare-AI-Insight-Daily) | 日报生成逻辑 |
| [后端 API](https://ai-daily.352388732.workers.dev) | 直接访问 Worker |
| [RSS 订阅](https://ai-daily.352388732.workers.dev/rss?days=7) | 订阅日报 |
| [Hextra 主题文档](https://imfing.github.io/hextra/) | 主题用法 |
| [Hugo 文档](https://gohugo.io/documentation/) | 静态站生成器 |

---

## 📄 License

MIT
