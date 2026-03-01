# source/derived/

Code scripts for **data cleaning and transformation** tasks.

Each task gets its own subfolder: `source/derived/<task_name>/`

## What belongs here

- Scripts that read from `data/raw/<dataset>/` (upstream)
- Scripts that clean, reshape, or transform data for analysis use
- Output data goes to `data/derived/<output_dataset>/`
- Log files and summary stats go to `output/derived/<task_name>/`
- Temp/intermediate datasets go to `temp/derived/<task_name>/`

## Pipeline position

```
data/raw/  →  source/derived/<task>/  →  data/derived/
```

Derived folders sit between raw and analysis in the data pipeline.
