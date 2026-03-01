# source/analysis/

Code scripts for **analysis tasks** — tables, figures, regressions.

Each task gets its own subfolder: `source/analysis/<task_name>/`

## What belongs here

- Scripts that read from `data/raw/` and/or `data/derived/` (upstream)
- Scripts that produce tables (.tex, .csv, .xlsx) and figures (.eps, .pdf)
- Output files go to `output/analysis/<task_name>/`
- Final datasets (if needed for future replication) go to `data/analysis/<task_name>/`
- Temp/intermediate files go to `temp/analysis/<task_name>/`

## Example

```
source/analysis/sumstats_main/
    sumstats_main.do    ← produces output/analysis/sumstats_main/table1.tex
```
