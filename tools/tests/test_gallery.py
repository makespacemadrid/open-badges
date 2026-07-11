from badgegen import gallery
from badgegen.config import Settings


def test_scan_report(tmp_path):
    settings = Settings(repo_root=tmp_path)
    out = gallery.write_scan_report(settings, [
        {"slug": "badge-a", "file": "badge-a.png", "roundness": 0.9566,
         "issues": ["flattened-circle"], "judge_score": 2, "judge_issues": ["texto roto"]},
        {"slug": "badge-b", "file": "badge-b.png", "roundness": 0.999,
         "issues": [], "judge_score": None, "judge_issues": []},
    ])
    html = out.read_text(encoding="utf-8")
    assert out == tmp_path / "review" / "scan-report.html"
    assert 'src="../badge-a.png"' in html
    assert "0.9566" in html and "flattened-circle" in html and "texto roto" in html
    assert "badge-b" in html


def test_review_gallery(tmp_path):
    settings = Settings(repo_root=tmp_path)
    out = gallery.write_review(settings, [
        {"slug": "badge-a", "current": "badge-a.png", "candidates": [
            {"file": "candidates/badge-a/01-gemini.png", "qc_ok": True,
             "roundness": 0.998, "provider": "gemini", "model": "gemini-2.5-flash-image"},
            {"file": "candidates/badge-a/02-gemini.png", "qc_ok": False,
             "roundness": 0.92, "provider": "gemini", "model": "gemini-2.5-flash-image"},
        ]},
    ])
    html = out.read_text(encoding="utf-8")
    assert 'src="../candidates/badge-a/01-gemini.png"' in html
    assert "python -m badgegen promote badge-a candidates/badge-a/01-gemini.png" in html
    assert 'class="qc bad"' in html and 'class="qc good"' in html
    assert 'src="../badge-a.png"' in html  # la actual, para comparar
