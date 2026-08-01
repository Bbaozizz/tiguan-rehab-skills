# 体观康复 Skills

简体中文 | [English](README.en.md)

> 面向认真解决客户问题的康复专业人员。让 AI 接走整理、记录、呈现和复盘工作，不替代临床判断与责任。

[![Version](https://img.shields.io/badge/version-0.1.1-17352D.svg?style=flat-square)](VERSION)
[![skills.sh](https://skills.sh/b/Bbaozizz/tiguan-rehab-skills)](https://skills.sh/Bbaozizz/tiguan-rehab-skills)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-B1462F.svg?style=flat-square)](LICENSE)

**支持：WorkBuddy（macOS 本机实测，Windows 使用原生 PowerShell 安装器与 CI）、Claude Code、Codex，以及其他支持 Agent Skills 的工具。**

这是由 [体观运动康复](https://tiguanrehab.cn/) 创建的公开 Skill 工具箱。首批将已在真实康复服务中重复出现的整理、呈现和复盘环节，抽成 2 个可安装、可验证的 Skills。

**v0.1.1：** 新增 WorkBuddy 一键安装器。提供 `/tiguan-rehab` 统一入口与 `/tiguan-assessment-session-design` 评估课设计工作流，包含脱敏输入、合成案例、可打印报告和隐私/临床边界。

[快速开始](#快速开始) · [安装](#安装) · [能力一览](#能力一览) · [完整使用手册](docs/getting-started.md) · [开源路线图](#开源路线图) · [更新日志](https://github.com/Bbaozizz/tiguan-rehab-skills/releases)

![体观康复 Skills 链接图](docs/skill-map.svg)

## 这套 Skills 解决什么问题

康复师不缺测试、手法和动作，但专业过程常常无法被客户理解，也难以在下一次服务中继续复测。这套 Skills 先处理六类非临床重复劳动：

| 真实工作场景 | 当前可得到什么 |
| --- | --- |
| 信息很多，评估课前仍然只能从“哪里不舒服”开始 | 脱敏事实卡与证明已读材料的开场问题 |
| 专业参数很多，客户不知道和自己有什么关系 | 客户能理解、下次能重复的功能基线 |
| 当场有变化，容易被说成“找到原因” | 支持什么、不能证明什么的证据边界 |
| 课后一次丢给客户太多动作 | 一个能回到生活、带回信息的主行动 |
| 评估过程只停留在康复师脑中 | 客户提醒草稿与可打印评估摘要 |
| 不知道该用哪个 Skill | 统一入口读取当前上下文并路由 |

## 快速开始

安装完成后，在支持 Skills 的 Agent 中直接输入：

```text
/tiguan-rehab 我有一位脱敏客户，主要想解决连续办公后转头不适。
请帮我把已有信息变成一节可复测的评估课。
```

`/tiguan-rehab` 会读取当前对话，路由到已发布的具体 Skill。已经知道需求时，直接调用：

```text
/tiguan-assessment-session-design 以下是脱敏客户信息：……
请输出课前问题、客户可理解基线、复测结构、一个生活行动和报告草稿。
```

## 能力一览

| 状态 | 入口 | 主要产出 |
| --- | --- | --- |
| 已实现 | `/tiguan-rehab` | 新手引导、任务前路由、任务后导航 |
| 已实现 | `/tiguan-assessment-session-design` | 事实卡、开场问题、可复测基线、生活行动、提醒与评估报告 |
| 计划中 | 课后质询 | 从治疗师的脱敏课后口述中追问知行差值 |
| 计划中 | 课后交付 | 客户小结、家作、下次复测与进度记录 |
| 计划中 | 客户与进度 | 分阶段基线、阶段复盘与生活/运动转移 |
| 计划中 | 经营分析 | 服务、日程、客户与经营事实的脱敏分析 |

“计划中”不等于已可下载，也不会被主入口路由。

## 安装

### WorkBuddy 一键安装

WorkBuddy 当前不在通用 `skills` 安装器的 Agent 列表中，因此按系统提供专用命令。

#### macOS

在“终端”复制下面这一条命令：

```bash
curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
```

#### Windows

在 PowerShell 复制下面这一条命令；不需要另装 Node、Git 或 WSL：

```powershell
irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
```

安装器只管理 `~/.workbuddy/skills/tiguan-rehab` 与 `~/.workbuddy/skills/tiguan-assessment-session-design`，不会删除或改写其他 Skill。完成后刷新或重启 WorkBuddy，在“我安装的”中确认两个 Skill 已启用，然后输入 `/tiguan-rehab 新手入门`。

### 其他支持 Agent Skills 的工具

```bash
npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all
```

这条通用命令会安装到安装器已经支持的 Agent；它不负责 WorkBuddy。安装后回到 Agent，输入 `/tiguan-rehab 新手入门` 即可开始。

### Claude Code 插件市场

```bash
claude plugin marketplace add Bbaozizz/tiguan-rehab-skills
claude plugin install tiguan-rehab@tiguan-rehab-skills
```

只想安装评估课能力时，可使用：

```bash
claude plugin install tiguan-assessment-session-design@tiguan-rehab-skills
```

### 本地安装

克隆仓库后，在仓库根目录执行：

```bash
npx -y skills add . --all
```

也可以把 `skills/` 下的两个 Skill 目录复制到 Agent 所支持的 Skills 目录。

### 本地构建发布包

```bash
bash tools/build-skills.sh
```

产物位于 `dist/skills/`，包含独立 Skill zip 和总包。

### 更新

已安装时，可以直接对 Agent 说：

```text
更新体观康复 Skills
```

主入口会根据当前运行环境提示对应命令。WorkBuddy macOS 使用：

```bash
curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
```

WorkBuddy Windows 使用：

```powershell
irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
```

其他已被通用安装器支持的 Agent 使用：

```bash
npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all
```

更新只同步该仓库的两个 Skills，不应改动使用者生成的报告、案例文件或其他 Skills。WorkBuddy 的安装位置是 `~/.workbuddy/skills`。版本变化见 [GitHub Releases](https://github.com/Bbaozizz/tiguan-rehab-skills/releases)。

## 它怎样工作

```text
脱敏的真实任务
  ↓
/tiguan-rehab 读取上下文，只路由到已发布能力
  ↓
一个 Skill 完成整理、设计、呈现或复盘
  ↓
康复师审核、在真实场景执行并带回复测结果
```

价值在于把一次真实任务推进到可验证的下一步，不在于一次性生成一份看起来完整的报告。

## 隐私与临床边界

- 不上传客户数据库、原始录音/转写、完整私信、可识别影像、联系方式、密钥或业务写入脚本。
- 使用者负责脱敏、知情、数据保存和当地法规合规。
- AI 可整理、生成草稿和提醒遗漏；不诊断、不定检查/动作/剂量、不替临床专业人员决定进阶。
- 生成文件、测试通过或完成本地安装，都不等于真实客户使用有效。
- 这套 Skills 不是紧急医疗、诊断、处方或临床监督服务。

## 开源路线图

| 批次 | 状态 | 能力 |
| --- | --- | --- |
| 0 | 已发布 | 仓库首页、使用手册、链接图、安装/构建/CI/Release 链路 |
| 1 | 已发布 | 评估课设计 Skill（问卷、基线、复测、提醒、可打印报告） |
| 2 | 计划中 | 课后质询/复盘 Skill |
| 3 | 计划中 | 课后交付 Skill 组 |
| 4 | 计划中 | 客户基线、阶段评估与进度追踪 |
| 5 | 计划中 | 工作室脱敏经营分析 |

后续每个 Skill 都必须经过：去身份/路径 → 标准化输入输出 → 合成案例 → 隐私/临床边界 → 失败处理 → 独立安装试跑。

## 项目结构

```text
tiguan-rehab-skills/
├── README.md                # 价值、快速开始、安装与路线图
├── docs/                   # 新手手册与链接图
├── skills/                 # 已实现、可安装的 Skills
│   ├── tiguan-rehab/
│   └── tiguan-assessment-session-design/
├── .claude-plugin/         # Claude Code 插件定义
├── tools/                  # 构建与发布门禁
└── tests/                  # 公开合同与渲染器测试
```

## 链接方式

- **仓库内部链接**：README 目录、相对文件、手册和 Skill 源文件，用于不离开 GitHub 完成理解。
- **能力索引链接**：[skills.sh 仓库页](https://skills.sh/Bbaozizz/tiguan-rehab-skills) 读取每个 `SKILL.md`，展示独立能力与安装命令。
- **下载链接**：[GitHub Releases](https://github.com/Bbaozizz/tiguan-rehab-skills/releases) 包含每个 Skill 的独立 zip 与总包。
- **仓库首页链接**：README 串起安装、使用手册、路线图、Release 和品牌官网，不再另造一个必经网页。
- **品牌链接**：[体观运动康复](https://tiguanrehab.cn/) 负责说明业务与专业背景，不与 Skill 安装混成一个链路。

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE) 许可证：可用于个人使用、学习、研究与非商业项目；公开衍生作品需注明来源，商业用途需单独授权。

真实客户数据、内部业务库、凭证和私有工作流不属于本仓库的公开范围。

作者：[体观运动康复](https://tiguanrehab.cn/) · GitHub：[`Bbaozizz/tiguan-rehab-skills`](https://github.com/Bbaozizz/tiguan-rehab-skills)
