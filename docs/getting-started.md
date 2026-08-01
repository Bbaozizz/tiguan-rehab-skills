# 体观康复 Skills 新手入门

这套 Skills 不要求你先学一套 AI 方法。你只需要提交当前的真实任务，但必须先把客户信息脱敏。

## 1. 安装

WorkBuddy macOS 从 GitHub 一键安装或更新：

```bash
curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
```

WorkBuddy Windows 在 PowerShell 中运行；不需要另装 Node、Git 或 WSL：

```powershell
irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
```

安装器只替换它管理的两个体观 Skill，保留 `~/.workbuddy/skills` 中的其他内容。完成后刷新或重启 WorkBuddy，在“我安装的”中确认两个 Skill 已启用。

其他已被通用 `skills` 安装器支持的 Agent 使用：

```bash
npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all
```

本地克隆后，也可以在仓库根目录执行：

```bash
npx -y skills add . --all
```

安装后重启或刷新 Agent 的 Skills 列表。如果你使用的是 WorkBuddy，不要运行带 `--agent workbuddy` 的通用安装命令；它目前不识别 WorkBuddy，请使用上面的专用一键安装器。如果是其他不受支持的 Agent，再把 `skills/tiguan-rehab/` 和 `skills/tiguan-assessment-session-design/` 复制到该 Agent 的 Skills 目录。

之后只要对 Agent 说“更新体观康复 Skills”，主入口会引导重新运行远程安装命令。它不应修改你自己生成的报告或其他 Skills。

## 2. 第一次怎么用

直接输入：

```text
/tiguan-rehab 新手入门
```

或者直接带上任务：

```text
/tiguan-rehab 我想为一位脱敏客户设计一节评估课。
他最在意的是连续办公后向右转头不适，下午更明显。
我要先得到课前问题、可复测基线和一个生活行动。
```

主入口会路由到 `/tiguan-assessment-session-design`。它已经读到的背景不需要再说一遍。

## 3. 提交什么

可以提交：

- 内置 10 题课前问卷的 Q01–Q10 脱敏选项答案；
- 脱敏后的客户主要目标；
- 工作、生活、运动或睡眠中的具体场景；
- 客户自己对问题的理解；
- 康复师已经确定的专业计划与限制；
- 希望输出的形式：对话简报、客户提醒、Markdown 报告或可打印 HTML。

不要提交：

- 真实姓名、电话、微信、身份证明、出生日期、住址；
- 可识别影像、完整私信、完整录音/转写或完整病历；
- 密钥、token、数据库或内部账号 ID。

如果还没有问卷，让 Agent 读取 `assets/intake-questionnaire-template.md`。它是 10 题全选择模板：Q03 根据主场景分支且最多选 2 项，Q09 会引用 Q08 的训练时段，Q10 只收集客户还能提供的资料。正式问卷不计时，也不把“没有资料”当成“没有风险”。

## 4. 你会得到什么

`/tiguan-assessment-session-design` 默认交付：

1. 脱敏事实卡；
2. 已知、客户相信、康复师已判断、待验证四层；
3. 开场问题；
4. 客户可理解基线和相同条件复测；
5. 不替代临床计划的验证结构；
6. 一个生活转移行动；
7. 客户提醒与评估报告草稿；
8. 未知、风险和下次复测。

## 5. 生成可打印报告

使用合成示例测试：

```bash
python3 skills/tiguan-assessment-session-design/scripts/render_report.py \
  --input skills/tiguan-assessment-session-design/examples/synthetic-report-input.json \
  --output /tmp/tiguan-assessment-report.html
```

用浏览器打开 HTML，目检后点击“打印 / 导出 PDF”。

## 6. 怎样判断这次用得对不对

不要用“报告已生成”当成成功。至少检查：

- 客户是否能看到自己的具体生活问题；
- 基线是否可以在相同条件复测；
- 当次变化是否没有被夸大成唯一原因或长期结果；
- 生活行动是否只有一个主焦点；
- 康复师是否已审核所有临床和客户面向内容；
- 实际执行后是否带回了复测信息。

最后一项才是真实业务闭环；本地构建、安装或合成案例通过不能代替它。
