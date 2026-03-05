/*===========================================================================
  source/derived/<task>/<task>.do  –  Clean and process data

  Inputs:  data/0_raw/<dataset>/           (upstream raw datasets)
  Outputs: data/1_derived/<dataset>/        (cleaned / transformed datasets)
  Log:     output/1_derived/<task>/<task>.log

  Notes:
    - derived/ tasks take raw/ as input and deliver to analysis/.
    - Name this folder verb+noun, e.g. preclean_redfin.
    - Save any sanity-check summary stats to output/derived/<task>/.
    - Use relative paths only.
===========================================================================*/

* log using "output/1_derived/<task>/<task>.log", replace text

* --- your code here ---

* log close

