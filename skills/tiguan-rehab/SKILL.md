---
name: tiguan-rehab
description: 体观康复公开 Skills 的统一入口和动态路由器。当用户不确定该用哪个体观 Skill、第一次使用工具箱、提交了一个脱敏的康复工作流任务，或完成一轮后想判断下一步时使用。
---

# 体观康复 Skills 入口

读取当前对话中已有的目标、材料、约束和上一轮结果，然后只选择当前最适合的一个已发布 Skill。不要让用户先学会工具名。

## 模式

### 新手入门

当用户说“新手入门”或第一次使用时：

1. 说明只需提交当前真实任务，无需记住 Skill 名。
2. 提醒先去除姓名、联系方式、影像标识、机构 ID 和完整病历等可识别信息。
3. 给出一个最小示例：

   ```text
   /tiguan-rehab 我有一位脱敏客户，主要想解决连续办公后转头不适。
   帮我设计一节让他被看见、看得懂基线、能带回生活的评估课。
   ```

4. 继续处理用户已提交的任务，不要在教程结束后再让他重复背景。

### 任务前路由

当用户说“更新体观康复 Skills”或“升级体观 Skills”时：

- 如果当前 Skill 的基础目录位于 `.workbuddy/skills`，根据当前操作系统提供 WorkBuddy 专用安装命令。macOS/Linux：

  ```bash
  curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
  ```

  Windows PowerShell：

  ```powershell
  irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
  ```

- 其他已被通用安装器支持的 Agent，重新运行 `npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all`；
- 更新只同步本工具箱的 Skills，不改动用户生成的报告、案例文件或其他 Skills。

| 用户意图 | 路由 | 边界 |
| --- | --- | --- |
| 设计首评/体验评估课，整理课前信息、客户可见基线、现场复测、生活转移动作或评估报告 | `/tiguan-assessment-session-design` | 只处理脱敏输入；不代替临床判断 |
| 课后质询、治疗记录、客户进度、工作室经营 | 说明属于开源路线图，当前公开包尚未发布对应 Skill | 不伪装成已安装、不调用私有工作流 |
| 紧急医疗、诊断、处方、剂量或进阶决定 | 不路由给任何公开 Skill | 说明应由有资质的临床专业人员处理 |

路由时只说一句：

> 这个任务由 `/tiguan-assessment-session-design` 处理，因为你现在要设计的是一节可被理解和复测的评估课。

然后立即执行对应 Skill，不要再展示工具目录。

### 任务后导航

完成一轮后，先复述已得到的具体产物和尚未验证的部分。如果用户有新结果，按新结果继续当前 Skill；不要为了“串起来”调用一个还没发布的 Skill。

## 公共边界

- 使用脱敏材料或合成案例。
- 区分客户自述、康复师判断、AI 推断和待验证假设。
- AI 可整理、结构化、提醒遗漏和生成草稿；不做诊断、不替专业人员定动作/剂量、不判定进阶。
- 生成文件、模板或测试通过，都不等于真实客户闭环。
