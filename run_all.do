/*===========================================================================
  run_all.do  –  Stata master script

  Called by run_all.py as part of the pipeline, or run standalone:
      stata-mp -e do run_all.do

  To run the full pipeline (Stata + R + Jupyter), use:
      python run_all.py

  Pipeline stages handled by this file:
    Stage 0  →  source/0_raw/<task>/<task>.do    Ingest raw data
    Stage 1  →  source/1_derived/<task>/<task>.do  Clean and process
    Stage 2  →  source/2_analysis/<task>/<task>.do  Stata analysis only
               (R and Jupyter analysis scripts are run by run_all.py)

  Notes:
    - Uses relative paths throughout; never hard-code absolute paths.
    - Each task logs to output/<stage>/<task>/.
    - See README.md and run_all.py for the full pipeline definition.
===========================================================================*/

* --------------------------------------------------------------------------
* 0. Setup
* --------------------------------------------------------------------------
clear all
set more off
version 17                  // minimum Stata version for reproducibility

* Working directory must be the project root when this file is invoked.
* Interactively: cd to project root, then: do run_all.do
* Batch mode:    stata-mp -e do run_all.do

* Ensure required directories exist
foreach dir in "data/0_raw" "data/1_derived" ///
               "output/0_raw" "output/1_derived" ///
               "output/2_analysis/tables" "output/2_analysis/figures" ///
               "temp" "docs/weekly_reports" {
    capture mkdir "`dir'"
}

* Master log (date-stamped)
local date_str = string(year(today())) + string(month(today()), "%02.0f") ///
               + string(day(today()), "%02.0f")
log using "output/run_all_`date_str'.log", replace text

di "========================================================"
di " run_all.do — `c(current_date)' `c(current_time)'"
di "========================================================"

* --------------------------------------------------------------------------
* 1. Raw  –  Ingest and assemble raw data
*    source/0_raw/<task>/<task>.do → data/0_raw/<dataset>/
* --------------------------------------------------------------------------
di _newline "--- Stage: 0_raw ---"
do "source/0_raw/0_build.do"

* --------------------------------------------------------------------------
* 2. Derived  –  Clean and process data
*    source/1_derived/<task>/<task>.do → data/1_derived/<dataset>/
* --------------------------------------------------------------------------
di _newline "--- Stage: 1_derived ---"
do "source/1_derived/1_clean.do"

* --------------------------------------------------------------------------
* 3. Analysis  –  Regressions, statistics, tables, figures
*    source/2_analysis/<task>/<task>.do → output/2_analysis/
* --------------------------------------------------------------------------
di _newline "--- Stage: 2_analysis ---"
do "source/2_analysis/2_analysis.do"
do "source/2_analysis/3_output.do"

* --------------------------------------------------------------------------
* Done
* --------------------------------------------------------------------------
di _newline "========================================================"
di " All stages completed successfully."
di "========================================================"
log close
