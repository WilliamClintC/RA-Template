/* =============================================================================
   ANALYSIS MASTER SCRIPT
   
   Purpose : Runs all analysis steps from the clean data file to final
             tables and figures. Execute this script to reproduce all
             results in the paper.
   
   Steps   : 1. Clear output and temp directories
             2. Run each analysis sub-script in order
   
   Inputs  : ../input/       (link/copy of build/output – read only)
   Outputs : ../output/      (figures .eps/.pdf, tables .tex/.txt)
   Temp    : ../temp/        (logs, intermediate results – safe to delete)
   
   Gentzkow & Shapiro (2014) Rule: All file references should be local
   (../input/...) so the directory is portable across machines.
============================================================================= */

clear all
set more off

* --------------------------------------------------------------------------- *
* Paths (relative – keep this portable, Rule C)
* --------------------------------------------------------------------------- *
global analysis "../"
global input    "${analysis}input/"
global code     "${analysis}code/"
global output   "${analysis}output/"
global temp     "${analysis}temp/"

* --------------------------------------------------------------------------- *
* Clear outputs (uncomment when ready to enforce full reproducibility)
* --------------------------------------------------------------------------- *
* shell rmdir /S /Q "${output}"
* shell mkdir "${output}"
* shell rmdir /S /Q "${temp}"
* shell mkdir "${temp}"

* --------------------------------------------------------------------------- *
* Run sub-scripts in order
* --------------------------------------------------------------------------- *
* do "${code}01_summary_stats.do"
* do "${code}02_regressions.do"
* do "${code}03_figures.do"
* do "${code}04_tables.do"
