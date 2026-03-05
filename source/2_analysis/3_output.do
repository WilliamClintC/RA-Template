/*===========================================================================
  source/analysis/<output_task>/<output_task>.do  –  Export tables & figures

  Inputs:  data/1_derived/<dataset>/       (cleaned datasets)
           data/1_derived/<task>/           (collapsed final datasets)
  Outputs: output/2_analysis/tables/        (.tex, .csv, .xlsx)
           output/2_analysis/figures/       (.pdf, .png)
  Log:     output/2_analysis/<output_task>/<output_task>.log

  Notes:
    - Variable names: lowercase, underscore-separated (e.g. sg_poi_id).
    - Use informative, self-explanatory variable names.
    - Use relative paths only.
===========================================================================*/

* log using "output/2_analysis/<output_task>/<output_task>.log", replace text

* --- your code here ---

* log close

