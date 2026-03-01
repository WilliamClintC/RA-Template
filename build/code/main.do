/* =============================================================================
   BUILD MASTER SCRIPT
   
   Purpose : Runs all data build steps from raw inputs to a clean analysis file.
             Execute this script to reproduce the entire data build from scratch.
   
   Steps   : 1. Clear output and temp directories
             2. Run each build sub-script in order
   
   Inputs  : ../input/       (raw data – never modified)
   Outputs : ../output/      (clean data ready for analysis)
   Temp    : ../temp/        (intermediate files – safe to delete)
   
   Gentzkow & Shapiro (2014) Rule: This script should clear ../temp/ and
   ../output/ at the start so all output is known to come from current code.
============================================================================= */

clear all
set more off

* --------------------------------------------------------------------------- *
* Paths (relative – keep this portable, Rule C)
* --------------------------------------------------------------------------- *
global build    "../"
global input    "${build}input/"
global code     "${build}code/"
global output   "${build}output/"
global temp     "${build}temp/"

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
* do "${code}01_import.do"
* do "${code}02_clean.do"
* do "${code}03_merge.do"
