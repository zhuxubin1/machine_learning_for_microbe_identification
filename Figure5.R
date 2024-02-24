# Script name: Figure5.R
# Purpose: Used to generate representational images required by Figure5.
# Author: Zhu Xubin
# Date Created: 2024-02-17


# Load dependencies ----------------------

library(ggplot2)
library(tidyverse)
library(dplyr)
library(stringi)
source("toolbox.R")

# Import Data ----------------------

load("RData/Figure5.RData")

# Generation of subplots ------------------------------

F1_Hierarchical_barplot(F1_Hierarchical_data)
