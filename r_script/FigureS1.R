# Script name: FigureS1.R
# Purpose: The script was used to generate the results of microbial interaction 
#           with AuNPs in Figure S1, including the histogram of hydrated particle
#           size, the histogram of zeta potential, and the histogram of maximum 
#           absorption wavelength.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(readxl)
require(dplyr)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS1.RData")

# Generation of subplots ------------------------------

## 1.Grain size comparison histogram ----------------------

size_comparison_histogram(df)
zeta_comparison_histogram(df)
wavelength_comparison_histogram(df)
