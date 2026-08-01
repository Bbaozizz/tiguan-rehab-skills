# 体观康复 Skills

简体中文 | [English](README.en.md)

> 让真正的康复，不再被埋没。

[![Version](https://img.shields.io/badge/version-0.1.2-17352D.svg?style=flat-square)](VERSION)
[![skills.sh](https://skills.sh/b/Bbaozizz/tiguan-rehab-skills)](https://skills.sh/Bbaozizz/tiguan-rehab-skills)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-B1462F.svg?style=flat-square)](LICENSE)

**支持：WorkBuddy（macOS 本机实测，Windows 使用原生 PowerShell 安装器与 CI）、Claude Code、Codex，以及其他支持 Agent Skills 的工具。**

这是由 [体观运动康复](https://tiguanrehab.cn/) 创建的公开 Skill 组合。面向康复学生、医院/机构内康复师、个人门店康复师与机构负责人，帮助他们把知识带进实践、把专业判断变成可验证的服务，并让这些价值能被客户、团队和市场理解。

AI 用于补足表达、记录、分析、运营与复盘，不替代人的专业判断、临床责任和组织决策。

**当前可下载：** 2 个已发布 Skill。**长期方向：** 围绕康复同行完整的学习、实践、服务、表达与经营路径，逐步开放更深的认知型 Skills。规划中的能力不等于已经可安装。

**v0.1.2：** 课前输入升级为 10 题全选择问卷，并增加 Q01–Q10 字段映射。保留 WorkBuddy 一键安装、合成案例、可打印报告和隐私/临床边界。

[完整能力地图](#完整能力地图) · [快速开始](#快速开始) · [安装](#安装) · [能力一览](#能力一览) · [完整使用手册](docs/getting-started.md) · [开源路线图](#开源路线图) · [更新日志](https://github.com/Bbaozizz/tiguan-rehab-skills/releases)

![体观康复 Skills 完整能力地图与当前开放状态](docs/skill-map.svg)

## 这套 Skills 解决什么问题

康复同行面对的很多困难，表面上是缺技术、缺模板、缺表达、缺流量或缺管理工具；真正的断点往往是：知识没有进入实践，专业判断没有变成可验证的过程，或者真实价值没有被他人理解。

这套 Skills 不是报告生成器合集，而是把 AI 放到关键判断点上，帮助使用者完成一次明显的认知转变，再回到真实场景验证。

## 完整能力地图

这张地图先按康复同行的完整真实路径设计，不受当前已发布能力限制。

| 真实阶段 | 表面问题 | 常见错误归因 | 真实问题 | 期望的认知转变 |
| --- | --- | --- | --- | --- |
| 学习与入行 | 学了很多，还是不敢做 | 还缺更多课程和技术 | 知识没有进入真实判断与反馈循环 | 学会不等于能在具体情境中判断 |
| 接触客户 | 不知道先问什么 | 缺一份更完整的问卷 | 没有判断哪些信息会改变安全、目标和下一步 | 收集信息是为了支持决策，不是填满资料 |
| 评估与目标对齐 | 测试很多仍然没有方向 | 测得不够全、技术不够高级 | 缺少客户目标、可复测基线和假设优先级 | 评估是可验证的服务过程，不是测试堆叠 |
| 方案与阶段设计 | 不知道如何写完整方案 | 缺标准模板或动作库 | 在证据不足时过早确定长期答案 | 方案是可调整的阶段性假设，不是一次写完的处方 |
| 治疗与训练 | 当场做了很多 | 项目越多越专业 | 没有围绕主假设控制变量和复测 | 当次服务的价值在于推动判断，不在项目数量 |
| 课后管理 | 记录、解释和家作很费力 | 缺更漂亮的报告和更强的自动化 | 重点没被压缩成客户能执行、下次能验证的行动 | 课后交付是把一个改变带回生活，不是复述整堂课 |
| 复评与阶段决策 | 不知道何时进阶、调整或停止 | 指标变好就该升级，没变就是方案失败 | 没有提前定义同条件复测和决策门槛 | 复评不是证明自己做对，而是决定下一步 |
| 结束、转诊与长期关系 | 担心客户离开 | 留得越久就越成功 | 没有区分继续价值、独立能力、转诊与结束 | 好的康复可能以客户不再依赖为结果 |
| 实践复盘 | 知道问题，下次仍然会犯 | 只是当时忘了或执行力不足 | 计划中的“知”没有和现场的“行”对照 | 复盘不是总结，而是抓住知行错配 |
| 专业表达与获客 | 专业没人看懂 | 不懂流量、不会营销 | 专业判断没有被转译成他人能理解和验证的价值 | 表达不是包装专业，而是让专业证据可见 |
| 执业与组织经营 | 忙、乱、留不住人或难管理 | 缺软件、缺流量或团队执行力差 | 责任、阶段、交付标准和经营事实不清 | AI 先补足可见性与反馈，不替代经营决策 |

### 四个长期能力簇

上面的阶段不会一行拆成一个 Skill。它们将按反复出现的核心认知问题，聚类成四个长期能力方向：

| 能力簇 | 要完成的认知转变 | 主要覆盖 |
| --- | --- | --- |
| 实践认知校准 | 从“我以为自己会/不会”，转向“证据显示我具体卡在哪” | 学习、入职、单次实践、课后质询、角色转型 |
| 可验证服务设计 | 从“堆测试、动作和方案”，转向“目标—基线—假设—复测—阶段决策” | 客户接触、评估、方案、治疗、课后、复评和结束 |
| 专业价值可见化 | 从“表达就是包装或营销”，转向“让真实判断和证据被特定对象理解” | 客户沟通、团队协作、案例表达、内容获客 |
| 执业系统诊断 | 从“所有问题都是技术、流量或执行力问题”，转向“找出专业、交付、表达、协作和经营的真实断点” | 个人执业、单人门店、机构协作与质量管理 |

### 为什么不会无限拆 Skill

公开 Skill 只拆到“一个独立、反复出现的关键判断”这一层。

- 问卷、报告、通知、家作、复评表等输出形式，作为 Skill 内部模式或模板。
- 学生、机构康复师、个人门店康复师和机构负责人的差异，作为同一能力中的角色分支。
- 数据读取、文件渲染、系统写入等确定性操作，作为脚本或可选适配器。
- 只有当一项能力对应新的真实任务、新的核心判断和可独立验证的认知转变时，才新增公开 Skill。

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

| 状态 | 入口 / 能力方向 | 作用 |
| --- | --- | --- |
| 已实现 | `/tiguan-rehab` | 新手引导、任务前路由、任务后导航 |
| 已实现 | `/tiguan-assessment-session-design` | “可验证服务设计”的第一个公开实现：事实卡、目标、基线、假设、复测、生活行动和报告草稿 |
| 规划中 | 实践认知校准 | 用脱敏实践材料对照自我认知与真实做法，找到知行错配和下一个验证动作 |
| 规划中 | 可验证服务设计的后续能力 | 逐步覆盖方案、课后转移、阶段复评、结束与转诊；是扩展现有 Skill 还是新增 Skill，以实际验证决定 |
| 规划中 | 专业价值可见化 | 把已确认的判断和证据转译为客户、团队或公众能理解的表达 |
| 规划中 | 执业系统诊断 | 从个人执业、门店或机构事实中识别真正断点，不把问题一律归因于技术、流量或执行力 |

“规划中”表示已进入完整能力地图，将逐步设计、测试和开放；它不等于已可下载，也不会被主入口伪装成已发布能力。

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
当前角色 + 脱敏的真实任务
  ↓
/tiguan-rehab 读取目标、材料和约束
  ↓
只路由到当前最适合的一个已发布 Skill
  ↓
完成一次关键认知转变 + 一个可验证的下一步
  ↓
使用者审核、在真实场景执行并带回新证据
```

不要为了“串起来”一次调用所有 Skill。价值在于把当前最关键的问题挖深，不在于一次性填满所有环节。

## 隐私与临床边界

- 不上传客户数据库、原始录音/转写、完整私信、可识别影像、联系方式、密钥或业务写入脚本。
- 使用者负责脱敏、知情、数据保存和当地法规合规。
- AI 可整理、生成草稿和提醒遗漏；不诊断、不定检查/动作/剂量、不替临床专业人员决定进阶。
- 生成文件、测试通过或完成本地安装，都不等于真实客户使用有效。
- 这套 Skills 不是紧急医疗、诊断、处方或临床监督服务。

## 开源路线图

| 能力方向 | 状态 | 开放边界 |
| --- | --- | --- |
| 统一入口、安装、使用手册与发布链路 | 已发布 | 当前可用 |
| 评估课设计 | 已发布 | 可验证服务设计的第一个公开实现 |
| 实践认知校准 | 规划中 | 优先探索身份与自我认知、脱敏实践对照、知行错配和下一个验证动作 |
| 可验证服务设计后续能力 | 规划中 | 方案、课后转移、阶段复评、结束与转诊 |
| 专业价值可见化 | 规划中 | 客户、团队和公众三类对象下的专业转译与证据表达 |
| 执业系统诊断 | 规划中 | 个人执业、单人门店、机构协作与质量管理 |

规划中的能力会逐步出现，但不预先把每个工作步骤命名为 Skill。每个新 Skill 都必须经过：核心认知问题 → 角色与触发场景 → 合成/脱敏案例 → 隐私与临床边界 → 失败处理 → 独立安装与真实任务试跑。

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
