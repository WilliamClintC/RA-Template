# source/

All **code scripts** live here, organized by pipeline stage.

| Subfolder | Purpose |
|-----------|---------|
| `raw/` | Scripts that read raw source data and produce cleaned datasets in `data/raw/` |
| `derived/` | Scripts that transform `data/raw/` inputs into derived datasets in `data/derived/` |
| `analysis/` | Scripts that consume `data/raw/` and/or `data/derived/` to produce tables and figures in `output/analysis/` |

## Naming tasks

Each task gets its own subfolder named **`verb_noun`** (lowercase, underscores) — e.g., `process_redfin_raw`, `preclean_redfin`, `sumstats_main`.

The task name mirrors across `source/`, `output/`, and (if needed) `temp/`:

```
source/raw/process_redfin_raw/   ← code lives here
output/raw/process_redfin_raw/   ← logs and outputs mirror here
temp/raw/process_redfin_raw/     ← temp files if needed
```

Data output folders in `data/` use **standalone dataset names** (not mirrored) because they are shared across multiple downstream tasks.
