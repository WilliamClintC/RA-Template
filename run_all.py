"""
run_all.py  –  Master pipeline script
======================================
Runs every stage of the pipeline in order.
Supports Stata (.do), R (.R), and Jupyter notebooks (.ipynb).

Usage (from the project root):
    python run_all.py              # run everything
    python run_all.py --stage 0    # run only 0_raw
    python run_all.py --stage 1    # run only 1_derived
    python run_all.py --stage 2    # run only 2_analysis
    python run_all.py --dry-run    # print what would run, don't execute

Pipeline (Franklin Qian RA Manual convention):
    Stage 0  →  source/0_raw/<task>/        Ingest raw data
    Stage 1  →  source/1_derived/<task>/    Clean and process
    Stage 2  →  source/2_analysis/<task>/   Regressions and output

Script types:
    .do      →  stata-mp -e do <file>
    .R       →  Rscript <file>
    .ipynb   →  jupyter nbconvert --to notebook --execute --inplace <file>
"""

import argparse
import datetime
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration  –  edit these to match your system
# ---------------------------------------------------------------------------
STATA_EXE  = "stata-mp"          # or "stata-se", "stata" — must be on PATH
RSCRIPT_EXE = "Rscript"          # must be on PATH
JUPYTER_EXE = "jupyter"          # must be on PATH

# ---------------------------------------------------------------------------
# Pipeline definition
# Each stage is a list of scripts to run in order, relative to project root.
# Scripts starting with "_" are templates and are automatically skipped.
# ---------------------------------------------------------------------------
PIPELINE = {
    0: {
        "name": "0_raw",
        "description": "Ingest and assemble raw data",
        "scripts": [
            # "source/0_raw/<task>/<task>.do",
            # "source/0_raw/<task>/<task>.py",
        ],
    },
    1: {
        "name": "1_derived",
        "description": "Clean and process data",
        "scripts": [
            # "source/1_derived/<task>/<task>.do",
            # "source/1_derived/<task>/<task>.py",
        ],
    },
    2: {
        "name": "2_analysis",
        "description": "Regressions, statistics, tables, figures",
        "scripts": [
            # "source/2_analysis/<task>/<task>.do",
            # "source/2_analysis/<task>/<task>.R",
            # "source/2_analysis/<task>/<task>.ipynb",
        ],
    },
}

# Directories that must exist before running
REQUIRED_DIRS = [
    "data/0_raw",
    "data/1_derived",
    "output/0_raw",
    "output/1_derived",
    "output/2_analysis/tables",
    "output/2_analysis/figures",
    "temp",
    "docs/weekly_reports",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.resolve()


def setup_logging() -> logging.Logger:
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = ROOT / f"output/run_all_{date_str}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
    )
    logger = logging.getLogger("run_all")
    logger.info(f"Log file: {log_path.relative_to(ROOT)}")
    return logger


def setup_git_hooks(logger: logging.Logger) -> None:
    """Point git's hooksPath at the tracked hooks/ directory."""
    result = subprocess.run(
        ["git", "config", "core.hooksPath", "hooks"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode == 0:
        logger.info("Git hooks configured: core.hooksPath=hooks")
    else:
        logger.warning(f"Could not configure git hooks: {result.stderr.strip()}")


def ensure_dirs(logger: logging.Logger) -> None:
    for d in REQUIRED_DIRS:
        path = ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        if not keep.exists():
            keep.touch()
    logger.info("Required directories verified.")


def check_executables(logger: logging.Logger) -> None:
    missing = []
    for name, exe in [("Stata", STATA_EXE), ("Rscript", RSCRIPT_EXE), ("Jupyter", JUPYTER_EXE)]:
        if shutil.which(exe) is None:
            missing.append(f"  {name}: '{exe}' not found on PATH")
    if missing:
        logger.warning("Some executables not found (scripts of that type will fail):\n" + "\n".join(missing))


def run_script(script: str, logger: logging.Logger, dry_run: bool = False) -> bool:
    """Run a single script. Returns True on success, False on failure."""
    path = ROOT / script
    ext  = path.suffix.lower()
    name = Path(script).name

    # Skip templates (underscore prefix)
    if name.startswith("_"):
        logger.info(f"  SKIP (template)  {script}")
        return True

    if not path.exists():
        logger.error(f"  NOT FOUND        {script}")
        return False

    # Build command
    if ext == ".do":
        cmd = [STATA_EXE, "-e", "do", str(path)]
    elif ext == ".r":
        cmd = [RSCRIPT_EXE, "--vanilla", str(path)]
    elif ext == ".ipynb":
        cmd = [
            JUPYTER_EXE, "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=600",
            str(path),
        ]
    else:
        logger.warning(f"  UNKNOWN TYPE     {script} — skipping")
        return True

    logger.info(f"  RUN [{ext[1:].upper():6}]  {script}")
    if dry_run:
        logger.info(f"  CMD              {' '.join(cmd)}")
        return True

    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        logger.error(f"  FAILED (exit {result.returncode})  {script}")
        return False

    logger.info(f"  OK               {script}")
    return True


def run_stage(stage_id: int, logger: logging.Logger, dry_run: bool = False) -> bool:
    stage   = PIPELINE[stage_id]
    scripts = stage["scripts"]
    logger.info("")
    logger.info(f"{'='*60}")
    logger.info(f"Stage {stage_id}: {stage['name']}  –  {stage['description']}")
    logger.info(f"{'='*60}")

    all_ok = True
    for script in scripts:
        ok = run_script(script, logger, dry_run=dry_run)
        if not ok:
            all_ok = False
            logger.error(f"Stopping pipeline — failed at: {script}")
            return False          # fail fast

    return all_ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full research pipeline.")
    parser.add_argument(
        "--stage", type=int, choices=[0, 1, 2],
        help="Run only this stage (0=raw, 1=derived, 2=analysis).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print commands without executing them.",
    )
    args = parser.parse_args()

    # Must run from project root
    os.chdir(ROOT)

    logger   = setup_logging()
    dry_tag  = "  [DRY RUN]" if args.dry_run else ""
    logger.info(f"run_all.py — {datetime.datetime.now():%Y-%m-%d %H:%M}{dry_tag}")
    logger.info(f"Project root: {ROOT}")

    setup_git_hooks(logger)
    ensure_dirs(logger)
    check_executables(logger)

    stages = [args.stage] if args.stage is not None else list(PIPELINE.keys())
    start  = datetime.datetime.now()

    for stage_id in stages:
        ok = run_stage(stage_id, logger, dry_run=args.dry_run)
        if not ok:
            logger.error("Pipeline aborted.")
            sys.exit(1)

    elapsed = datetime.datetime.now() - start
    logger.info("")
    logger.info(f"Pipeline complete. Elapsed: {elapsed}")


if __name__ == "__main__":
    main()
