"""
rename_output.py  –  Quarto post-render hook
=============================================
Renames the rendered PDF to: YYYY-MM-DD_<Title>.pdf
Runs automatically after `quarto render` via _quarto.yml.
"""
import os
import re
import datetime
from pathlib import Path

today = datetime.date.today().strftime("%Y-%m-%d")

project_dir = Path(os.environ.get("QUARTO_PROJECT_DIR", Path(__file__).parent))

# Locate the source .qmd (skip directories)
qmd_path = None
doc_path_str = os.environ.get("QUARTO_DOCUMENT_PATH", "")
if doc_path_str:
    p = Path(doc_path_str)
    if p.is_file():
        qmd_path = p
if qmd_path is None:
    for f in sorted(project_dir.glob("*.qmd")):
        if f.is_file():
            qmd_path = f
            break

# Extract title from the .qmd YAML front matter
title_slug = "report"
if qmd_path and qmd_path.exists():
    content = qmd_path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if m:
        raw = m.group(1).strip().strip("\"'")
        # Sanitize: remove characters that are invalid in filenames, collapse spaces to hyphens
        raw = re.sub(r'[<>:"/\\|?*]', '', raw)
        title_slug = re.sub(r'\s+', '-', raw.strip())

# The default PDF output has the same stem as the .qmd file
original = qmd_path.with_suffix(".pdf") if qmd_path else project_dir / "_report_template.pdf"
new_name = original.parent / f"{today}_{title_slug}.pdf"

if original.exists():
    if original.resolve() != new_name.resolve():
        if new_name.exists():
            new_name.unlink()
        original.rename(new_name)
        print(f"[post-render] Renamed: {original.name}  ->  {new_name.name}")
    else:
        print(f"[post-render] Output already correctly named: {new_name.name}")
else:
    print(f"[post-render] Warning: expected PDF not found at {original}")
