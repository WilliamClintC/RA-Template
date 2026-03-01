# source/raw/

Code scripts for **raw data processing** tasks.

Each task gets its own subfolder: `source/raw/<task_name>/`

## What belongs here

- Scripts that read from `data/raw/<dataset>/` (raw source files)
- Scripts that convert, import, or lightly process raw data
- The output data goes to `data/raw/<output_dataset>/`
- Log files go to `output/raw/<task_name>/`

## Example

```
source/raw/process_redfin_raw/
    process_redfin_raw.do    ← main script (named same as folder)
```

Run from the project root using a relative path:
```
stata-mp -e do ./source/raw/process_redfin_raw/process_redfin_raw.do
```
