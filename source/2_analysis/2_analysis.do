/*===========================================================================
  source/analysis/<task>/<task>.do  –  Regressions and statistics

  Inputs:  data/0_raw/<dataset>/           (if calling raw directly)
           data/1_derived/<dataset>/        (primary: cleaned datasets)
  Outputs: output/2_analysis/tables/        (regression tables)
           output/2_analysis/figures/       (plots)
           data/1_derived/<task>/           (final collapsed dataset, if needed)
  Log:     output/2_analysis/<task>/<task>.log

  Notes:
    - Name this folder verb+noun, e.g. sumstats_main, regs_main.
    - Save temp datasets to temp/2_analysis/<task>/.
    - Use relative paths only.
===========================================================================*/

* log using "output/2_analysis/<task>/<task>.log", replace text

* --- your code here ---

* log close

