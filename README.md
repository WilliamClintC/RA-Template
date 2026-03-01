# Project Repository

Structure follows **Gentzkow & Shapiro (2014)** and the associated internal RA manual.
References: [Code and Data Guide](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf) · [GS Lab RA Manual](https://github.com/gslab-econ/ra-manual/wiki)

---

## Directory Structure

```
project/
│
├── source/                         # All code scripts
│   ├── raw/
│   │   └── <task_name>/            # e.g., process_redfin_raw/
│   ├── derived/
│   │   └── <task_name>/            # e.g., preclean_redfin/
│   └── analysis/
│       └── <task_name>/            # e.g., sumstats_main/
│
├── data/                           # All datasets (standalone names)
│   ├── raw/
│   │   └── <dataset_name>/         # e.g., redfin_dta/
│   ├── derived/
│   │   └── <dataset_name>/         # e.g., redfin_event_trees/
│   └── analysis/
│       └── <task_name>/            # rare — final datasets for replication
│
├── output/                         # Generated outputs (mirrors source/ names)
│   ├── raw/
│   │   └── <task_name>/            # logs from raw tasks
│   ├── derived/
│   │   └── <task_name>/            # logs + sanity-check tables
│   └── analysis/
│       └── <task_name>/            # tables (.tex/.csv) and figures (.eps/.pdf)
│
├── temp/                           # Intermediate files (safe to delete, don't sync)
│   ├── raw/
│   │   └── <task_name>/
│   ├── derived/
│   │   └── <task_name>/
│   └── analysis/
│       └── <task_name>/
│
├── docs/
│   └── weekly_reports/
│       └── <your_name>/            # versioned weekly progress reports
│
├── Documentation/                  # Reference PDFs and project docs
└── README.md
```

---

## Pipeline Logic

```
data/raw/  ──►  source/derived/<task>/  ──►  data/derived/  ──►  source/analysis/<task>/  ──►  output/analysis/
```

- **`source/raw/`** tasks: ingest and lightly process raw data → write to `data/raw/`
- **`source/derived/`** tasks: clean and transform → write to `data/derived/`
- **`source/analysis/`** tasks: regressions, tables, figures → write to `output/analysis/`

---

## Key Rules

| Rule | Description |
|------|-------------|
| **Separate by function** | `source/raw/` → `source/derived/` → `source/analysis/` |
| **Mirror task names** | `source/raw/<task>/` logs go to `output/raw/<task>/`; temp to `temp/raw/<task>/` |
| **Standalone data names** | `data/` folders use dataset names, not task names — they're shared across tasks |
| **Relative paths only** | Never hardcode `/Users/yourname/...`; always use paths relative to project root |
| **Always log** | Every script writes a log to the corresponding `output/<stage>/<task>/` folder |
| **Don't sync temp/** | `temp/` is excluded from Dropbox and version control |

---

## Naming Conventions

- All folder and file names: **lowercase with underscores** (`preclean_redfin`, not `PrecleanRedfin`)
- Task folders: **verb + noun** describing what the script does (`process_redfin_raw`, `sumstats_main`)
- Script named same as its folder: `source/raw/process_redfin_raw/process_redfin_raw.do`
- Variables: lowercase with underscores (`sg_poi_id` not `SafeGraphID`)

---

## Workflow Example

```bash
# From the project root:
stata-mp -e do ./source/raw/process_redfin_raw/process_redfin_raw.do
stata-mp -e do ./source/derived/preclean_redfin/preclean_redfin.do
stata-mp -e do ./source/analysis/sumstats_main/sumstats_main.do
```

Each script uses relative paths internally, e.g.:
```stata
use "../../data/raw/redfin_dta/redfin.dta"
log using "../../output/raw/process_redfin_raw/process_redfin_raw.log", replace
```

---

## Weekly Reports

Save progress reports to `docs/weekly_reports/<your_name>/`.
Naming: `<task_or_purpose>_<your_name>_<YYYY-MM-DD>.pdf`
Also version to the project Dropbox under `/docs/weekly_reports/<your_name>/`.
