# analysis/input

Contains the **clean data** needed for analysis.

- Populate by copying (or symlinking) files from `build/output/`.
- Use local relative references in code: `../input/filename.dta`
- This keeps the analysis directory fully portable across machines.
