/*===========================================================================
  source/raw/<task>/<task>.do  –  Ingest and assemble raw data

  Inputs:  data/0_raw/<dataset>/        (original raw files)
  Outputs: data/0_raw/<dataset>/        (converted/appended files)
  Log:     output/0_raw/<task>/<task>.log

  Notes:
    - Never modify the original source files in data/raw/.
    - Name this folder verb+noun, e.g. process_redfin_raw.
    - Save log files to output/raw/<task>/.
    - Use relative paths only.
===========================================================================*/

* log using "output/0_raw/<task>/<task>.log", replace text

* --- your code here ---

* log close

