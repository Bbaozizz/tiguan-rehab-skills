#!/usr/bin/env python3
"""Render a de-identified assessment summary as printable standalone HTML."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


REQUIRED_STRING_FIELDS = (
    "client_label",
    "assessment_date",
    "primary_goal",
    "life_action",
    "next_retest",
)
REQUIRED_LIST_FIELDS = ("baseline", "session_findings", "boundaries")


def load_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("report input must be a JSON object")

    for field in REQUIRED_STRING_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")

    for field in REQUIRED_LIST_FIELDS:
        value = payload.get(field)
        if not isinstance(value, list) or not value:
            raise ValueError(f"{field} must be a non-empty list")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise ValueError(f"{field} items must be non-empty strings")
    return payload


def escaped(value: str) -> str:
    return html.escape(value.strip(), quote=True)


def render_list(items: list[str]) -> str:
    return "\n".join(f"<li>{escaped(item)}</li>" for item in items)


def render_html(payload: dict[str, Any]) -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%2317352d'/%3E%3Cpath d='M14 18h36v8H36v24h-8V26H14z' fill='%23f3efe4'/%3E%3C/svg%3E\">
  <title>{escaped(payload['client_label'])} | 评估摘要</title>
  <style>
    :root {{ --paper:#f3efe4; --ink:#17352d; --muted:#6a736d; --line:#b9b6aa; --mark:#b1462f; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:#d9d5ca; color:var(--ink); font-family:\"Noto Serif SC\",\"Songti SC\",serif; line-height:1.7; }}
    .toolbar {{ position:sticky; top:0; display:flex; justify-content:flex-end; padding:12px 20px; background:#17352ded; z-index:2; }}
    button {{ border:1px solid #f3efe4; background:transparent; color:#f3efe4; padding:8px 14px; cursor:pointer; font:inherit; }}
    main {{ width:min(210mm, calc(100% - 28px)); min-height:297mm; margin:24px auto; padding:22mm 18mm; background:var(--paper); box-shadow:0 18px 50px #17352d22; }}
    header {{ display:grid; grid-template-columns:1fr auto; gap:24px; border-top:7px solid var(--ink); border-bottom:1px solid var(--ink); padding:18px 0; }}
    .eyebrow {{ margin:0 0 8px; color:var(--mark); font:700 12px/1.2 ui-monospace,monospace; letter-spacing:.12em; }}
    h1 {{ margin:0; font-size:32px; line-height:1.2; }}
    .meta {{ text-align:right; color:var(--muted); font-size:13px; }}
    .goal {{ margin:28px 0; padding:20px 22px; border-left:5px solid var(--mark); background:#ece6d8; font-size:21px; }}
    section {{ display:grid; grid-template-columns:116px 1fr; gap:24px; padding:22px 0; border-top:1px solid var(--line); }}
    h2 {{ margin:0; font-size:15px; letter-spacing:.08em; }}
    p, ul {{ margin:0; }}
    ul {{ padding-left:1.2em; }}
    .boundary {{ color:var(--muted); font-size:13px; }}
    footer {{ margin-top:28px; padding-top:14px; border-top:1px solid var(--ink); color:var(--muted); font-size:12px; }}
    @page {{ size:A4; margin:0; }}
    @media print {{ body {{ background:#fff; }} .toolbar {{ display:none; }} main {{ margin:0; box-shadow:none; }} }}
    @media (max-width:640px) {{ main {{ padding:28px 22px; }} header,section {{ grid-template-columns:1fr; }} .meta {{ text-align:left; }} }}
  </style>
</head>
<body>
  <div class=\"toolbar\"><button type=\"button\" onclick=\"window.print()\">打印 / 导出 PDF</button></div>
  <main>
    <header>
      <div><p class=\"eyebrow\">TIGUAN / ASSESSMENT SUMMARY</p><h1>评估摘要</h1></div>
      <div class=\"meta\"><strong>{escaped(payload['client_label'])}</strong><br>{escaped(payload['assessment_date'])}</div>
    </header>
    <div class=\"goal\">{escaped(payload['primary_goal'])}</div>
    <section><h2>可复测基线</h2><ul>{render_list(payload['baseline'])}</ul></section>
    <section><h2>本次观察</h2><ul>{render_list(payload['session_findings'])}</ul></section>
    <section><h2>回到生活</h2><p>{escaped(payload['life_action'])}</p></section>
    <section><h2>下次复测</h2><p>{escaped(payload['next_retest'])}</p></section>
    <section class=\"boundary\"><h2>边界说明</h2><ul>{render_list(payload['boundaries'])}</ul></section>
    <footer>本文档由 AI 辅助整理，必须由负责的康复专业人员审核。它不是诊断、处方或长期结果承诺。</footer>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_html(payload), encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(f"rendered: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
