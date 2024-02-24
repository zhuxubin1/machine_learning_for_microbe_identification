# Script name: Figure4.R
# Purpose: Used to generate representational images required by Figure4.
# Author: Zhu Xubin
# Date Created: 2024-02-17


# Load dependencies ----------------------

library(ggplot2)
library(tidyverse)
library(dplyr)
library(stringi)
source("toolbox.R")

# Import Data ----------------------

load("RData/Figure4.RData")

# Generation of subplots ------------------------------

## 1.Multi-classification bar chart ----------------------

F1_multi_barplot(F1_multi_PCA, "PCA+LDA")
F1_multi_barplot(F1_multi_RF, "RF")
