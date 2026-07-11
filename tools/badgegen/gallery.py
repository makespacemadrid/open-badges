"""Galerías HTML estáticas (file://): informe de scan y revisión de candidatos."""
from __future__ import annotations

import html
from pathlib import Path

from badgegen.config import Settings

_CSS = """
body{background:#111;color:#eee;font-family:system-ui,sans-serif;margin:2rem}
h1{font-size:1.4rem}h2{font-size:1.1rem;border-top:1px solid #333;padding-top:1rem}
img{background:repeating-conic-gradient(#222 0 25%,#333 0 50%) 0 0/24px 24px;border-radius:8px}
table{border-collapse:collapse}td,th{padding:.4rem .8rem;border-bottom:1px solid #333;text-align:left}
.issue{background:#7a2020;border-radius:4px;padding:0 .4rem;margin-right:.3rem;font-size:.85em}
.qc{font-weight:bold;padding:0 .4rem;border-radius:4px}.qc.good{background:#1c5c2e}.qc.bad{background:#7a2020}
.cand{display:inline-block;vertical-align:top;margin:.5rem;text-align:center}
code{background:#222;padding:.2rem .4rem;border-radius:4px;font-size:.8em}
button{margin-top:.3rem;cursor:pointer}
"""

_COPY_JS = """
function copyCmd(btn){
  const cmd = btn.dataset.cmd;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(cmd).then(()=>{btn.textContent='copiado ✓';});
  } else { window.prompt('Copia el comando:', cmd); }
}
"""


def _page(title: str, body: str) -> str:
    return (
        f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
        f"<style>{_CSS}</style><script>{_COPY_JS}</script></head><body>"
        f"<h1>{html.escape(title)}</h1>{body}</body></html>"
    )


def write_scan_report(settings: Settings, rows: list[dict]) -> Path:
    parts = ["<table><tr><th></th><th>slug</th><th>redondez</th><th>issues</th><th>juez</th></tr>"]
    for row in rows:
        issues = "".join(f'<span class="issue">{html.escape(i)}</span>' for i in row["issues"])
        judge = ""
        if row.get("judge_score") is not None:
            j_issues = ", ".join(html.escape(i) for i in row.get("judge_issues", []))
            judge = f"{row['judge_score']}/5 {j_issues}"
        parts.append(
            f'<tr><td><img src="../{html.escape(row["file"])}" width="96"></td>'
            f'<td><code>{html.escape(row["slug"])}</code></td>'
            f"<td>{row['roundness']:.4f}</td><td>{issues or '—'}</td><td>{judge or '—'}</td></tr>"
        )
    parts.append("</table>")
    return _write(settings, "scan-report.html", _page("badgegen · informe de scan", "".join(parts)))


def write_review(settings: Settings, items: list[dict]) -> Path:
    parts = []
    for item in items:
        parts.append(f'<h2><code>{html.escape(item["slug"])}</code></h2>')
        if item.get("current"):
            parts.append(
                f'<div class="cand"><img src="../{html.escape(item["current"])}" width="180">'
                f"<div>actual</div></div>"
            )
        for cand in item["candidates"]:
            qc_class = "good" if cand["qc_ok"] else "bad"
            qc_label = "QC ok" if cand["qc_ok"] else "QC ✗"
            cmd = f"python -m badgegen promote {item['slug']} {cand['file']}"
            parts.append(
                f'<div class="cand"><img src="../{html.escape(cand["file"])}" width="180">'
                f'<div><span class="qc {qc_class}">{qc_label}</span> {cand["roundness"]:.3f} '
                f'· {html.escape(cand["provider"])}</div>'
                f'<div><button data-cmd="{html.escape(cmd)}" onclick="copyCmd(this)">copiar promote</button></div>'
                f"</div>"
            )
    return _write(settings, "review.html", _page("badgegen · candidatos", "".join(parts)))


def _write(settings: Settings, name: str, content: str) -> Path:
    settings.review_dir.mkdir(parents=True, exist_ok=True)
    path = settings.review_dir / name
    path.write_text(content, encoding="utf-8")
    return path
