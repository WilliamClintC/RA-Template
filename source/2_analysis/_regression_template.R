# ===========================================================================
# Task: <task_name>
# Author: William Clinton Co
# Date: <YYYY-MM-DD>
# Updated: <YYYY-MM-DD>
#
# Purpose:
#   <One-sentence description of what this script does.>
#
# Inputs:  data/1_derived/<dataset>/
# Outputs: output/2_analysis/tables/<table>.tex
#          output/2_analysis/figures/<figure>.pdf
# Log:     output/2_analysis/<task_name>/<task_name>.log
#
# Notes:
#   - Run from the project root: Rscript source/2_analysis/<task>/<task>.R
#   - All paths are relative to the project root.
# ===========================================================================

library(here)          # project-root-relative paths
library(tidyverse)
library(haven)
library(fixest)        # feols() for OLS / IV / FE regressions
library(modelsummary)  # regression tables

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
sink(here("output/2_analysis/<task_name>/<task_name>.log"), split = TRUE)
start_time <- proc.time()

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
df <- read_dta(here("data/1_derived/<dataset>/<dataset>.dta"))
# df <- read_csv(here("data/1_derived/<dataset>/<dataset>.csv"))

# ---------------------------------------------------------------------------
# 2. Variable construction
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 3. Regressions
# ---------------------------------------------------------------------------

# Baseline OLS
m1 <- feols(y ~ x1 + x2, data = df, vcov = "hetero")

# With fixed effects
m2 <- feols(y ~ x1 + x2 | fe_var, data = df, cluster = ~cluster_var)

# IV
# m3 <- feols(y ~ x2 | fe_var | x1 ~ instrument, data = df, cluster = ~cluster_var)

# ---------------------------------------------------------------------------
# 4. Export regression table
# ---------------------------------------------------------------------------
dir.create(here("output/2_analysis/<task_name>"), showWarnings = FALSE, recursive = TRUE)

modelsummary(
  list("OLS" = m1, "FE" = m2),
  stars    = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
  gof_map  = c("nobs", "r.squared", "adj.r.squared"),
  output   = here("output/2_analysis/tables/tbl_<task_name>.tex")
)

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
dir.create(here("output/2_analysis/figures"), showWarnings = FALSE, recursive = TRUE)

# p <- ggplot(df, aes(x = x1, y = y)) +
#   geom_point(alpha = 0.4) +
#   geom_smooth(method = "lm") +
#   theme_bw()
# ggsave(here("output/2_analysis/figures/fig_<task_name>.pdf"), p,
#        width = 6, height = 4)

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
elapsed <- proc.time() - start_time
message(sprintf("Done. Elapsed: %.1f sec", elapsed["elapsed"]))
sink()
