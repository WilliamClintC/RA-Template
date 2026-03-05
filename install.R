# -----------------------------------------------------------------------
# install.R  –  RA Template
# R version: 4.x
#
# Usage (quick install, no lockfile):
#   source("install.R")
#
# Preferred (full reproducibility with exact versions):
#   install.packages("renv")
#   renv::restore()          # reads renv.lock
#
# After adding a package here, update the lockfile:
#   renv::snapshot()
# -----------------------------------------------------------------------

pkgs <- c(
  # ----- Data wrangling ------------------------------------------------
  "tidyverse",       # dplyr, ggplot2, tidyr, readr, purrr, stringr, forcats
  "data.table",      # fast large-data manipulation
  "haven",           # read Stata .dta, SPSS .sav, SAS .sas7bdat
  "readxl",          # read .xlsx
  "writexl",         # write .xlsx without Java dependency
  "janitor",         # clean_names(), tabyl()

  # ----- Econometrics & statistics -------------------------------------
  "fixest",          # OLS, IV, Poisson with high-dimensional FE (feols, feglm)
  "lfe",             # felm() – alternative FE estimator
  "sandwich",        # robust & clustered standard errors
  "lmtest",          # coeftest()
  "AER",             # IV regression, many applied-econ datasets
  "ivreg",           # ivreg() two-stage least squares

  # ----- Output: tables ------------------------------------------------
  "modelsummary",    # regression tables to .tex, .docx, .html
  "knitr",           # kable() for Quarto / R Markdown
  "kableExtra",      # kable styling and LaTeX options
  "stargazer",       # LaTeX regression tables (legacy)

  # ----- Visualization -------------------------------------------------
  "ggplot2",         # (included in tidyverse; listed explicitly for clarity)
  "ggthemes",        # additional ggplot2 themes
  "scales",          # axis formatting helpers
  "patchwork",       # combine ggplot2 panels

  # ----- Geospatial ----------------------------------------------------
  "sf",              # simple features for R
  "tigris",          # US Census shapefiles
  "tidycensus",      # Census API wrapper

  # ----- Utilities -----------------------------------------------------
  "here",            # here() for project-root-relative paths
  "glue",            # string interpolation
  "fs",              # file system operations
  "tictoc"           # timing code blocks
)

new_pkgs <- pkgs[!(pkgs %in% installed.packages()[, "Package"])]
if (length(new_pkgs) > 0) install.packages(new_pkgs)
message("All packages installed.")
