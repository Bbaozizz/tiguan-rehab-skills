# 报告 JSON 契约

`scripts/render_report.py` 接收 UTF-8 JSON 对象。不接收客户真实姓名或其他可识别信息。

```json
{
  "client_label": "合成案例 A",
  "assessment_date": "2026-07-31",
  "primary_goal": "连续办公时更自在地转头",
  "baseline": ["在相同坐姿下，向右转到某位置出现熟悉不适"],
  "session_findings": ["当次处理后动作范围变化，该方向值得继续验证"],
  "life_action": "不适出现前起身并重新调整前臂支撑",
  "next_retest": "在相同时段、坐姿和记录方式下复测",
  "boundaries": ["当次变化不等于长期疗效"]
}
```

必填字符串：`client_label`、`assessment_date`、`primary_goal`、`life_action`、`next_retest`。

必填非空字符串数组：`baseline`、`session_findings`、`boundaries`。

渲染器会对所有内容做 HTML 转义，并生成可用浏览器打印或另存为 PDF 的自包含 HTML。
