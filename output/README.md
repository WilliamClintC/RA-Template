# output/

All **generated outputs** (logs, tables, figures) live here, **mirroring the `source/` structure**.

| Subfolder | Contents |
|-----------|----------|
| `raw/` | Log files from raw processing tasks |
| `derived/` | Log files and sanity-check tables from derived tasks |
| `analysis/` | Final tables (.tex, .csv, .xlsx) and figures (.eps, .pdf) from analysis tasks |

## Mirroring

Task names mirror `source/` exactly:

```
source/raw/process_redfin_raw/    →   output/raw/process_redfin_raw/
source/derived/preclean_redfin/   →   output/derived/preclean_redfin/
source/analysis/sumstats_main/    →   output/analysis/sumstats_main/
```

This makes it trivial to find all outputs for any given task.

## Always save log files

Every script execution should write a log to the corresponding `output/<stage>/<task>/` folder.

- Stata: `log using "../../output/raw/process_redfin_raw/process_redfin_raw.log", replace`
- R/Python: redirect stdout/stderr to the matching output folder
