# Script name: FigureS4.R
# Purpose: The script is used to generate the results of the binary model evaluation
#           in Figure S4. Includes model P-R bubble charts using Single data sets and
#           Merged data sets.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(dplyr)
require(readxl)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS4.RData")

# Generation of subplots ------------------------------

## 1.bubble plot ----------------------

bubble_plot(bubble_Single, "Single")
bubble_plot(bubble_Merged, "Merged")
