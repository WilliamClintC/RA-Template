"""
rename_output.py - Quarto post-render hook

Renames the rendered PDF to: YYYY-MM-DD_<Title>.pdf

Resolution order (most reliable first):
  1. QUARTO_DOCUMENT_PATH env var (set by Quarto when rendering a single doc).
  2. The `render:` list in _quarto.yml (source of truth for project renders).

The previous fallback (first *.qmd in alphabetical order) was brittle and
broke whenever an extra qmd file was added to the directory.
"""
import os
import re
import datetime
from pathlib import Path

today = datetime.date.today().strftime("%Y-%m-%d")

project_dir = Path(os.environ.get("QUARTO_PROJECT_DIR", Path(__file__).parent))


def find_render_targets():
    """Parse _quarto.yml for the list of qmd files this project renders."""
    qy = project_dir / "_quarto.yml"
    if not qy.exists():
        return []
    text = qy.read_text(encoding="utf-8")
    targets = []
    in_render = False
    render_indent = None
    for line in text.splitlines():
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("render:"):
            in_render = True
            render_indent = indent
            continue
        if in_render:
            # Exit the render block when indentation drops back to or below render's level
            if indent <= render_indent and not stripped.startswith("-"):
                in_render = False
                continue
            m = re.match(r'-\s*["\']?([^"\']+\.qmd)["\']?', stripped)
            if m:
                targets.append(project_dir / m.group(1))
    return targets


def get_title(qmd_path):
    """Extract the title from qmd YAML front matter; sanitize for filenames."""
    if not qmd_path.exists():
        return None
    text = qmd_path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1).strip().strip("\"'")
    raw = re.sub(r'[<>:"/\\|?*]', '', raw)
    return re.sub(r'\s+', '-', raw.strip())


def rename_one(qmd_path):
    """Rename the PDF corresponding to this qmd file."""
    if not qmd_path.exists():
        print(f"[post-render] Skip: source qmd not found: {qmd_path.name}")
        return False
    pdf_path = qmd_path.with_suffix(".pdf")
    if not pdf_path.exists():
        print(f"[post-render] Skip: PDF not produced for {qmd_path.name}")
        return False
    title = get_title(qmd_path) or qmd_path.stem
    new_name = pdf_path.parent / f"{today}_{title}.pdf"
    if pdf_path.resolve() == new_name.resolve():
        print(f"[post-render] Already correctly named: {new_name.name}")
        return True
    if new_name.exists():
        new_name.unlink()
    pdf_path.rename(new_name)
    print(f"[post-render] Renamed: {pdf_path.name}  ->  {new_name.name}")
    return True


def main():
    # Primary: explicit document path from Quarto
    doc_path_str = os.environ.get("QUARTO_DOCUMENT_PATH", "")
    if doc_path_str and Path(doc_path_str).is_file():
        rename_one(Path(doc_path_str))
        return

    # Fallback: read _quarto.yml
    targets = find_render_targets()
    if not targets:
        print("[post-render] Warning: no render targets found in _quarto.yml")
        return
    for t in targets:
        rename_one(t)


if __name__ == "__main__":
    main()
