# Script name: FigureS1.R
# Purpose: Used to generate representational images required by Figure S1.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

library(ggplot2)
library(readxl)
library(dplyr)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS1.RData")

# Generation of subplots ------------------------------

## 1.Grain size comparison histogram ----------------------

size_comparison_histogram(df)
zeta_comparison_histogram(df)
wavelength_comparison_histogram(df)
