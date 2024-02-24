# Script name: FigureS4.R
# Purpose: Used to generate representational images required by Figure S4.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

library(ggplot2)
library(dplyr)
library(readxl)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS4.RData")

# Generation of subplots ------------------------------

## 1.bubble plot ----------------------

bubble_plot(bubble_Single, "Single")
bubble_plot(bubble_Merged, "Merged")
