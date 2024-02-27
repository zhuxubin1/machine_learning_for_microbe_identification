# Script name: FigureS6-7.R
# Purpose: The script is used to generate the evaluation results of the dimensionality
#           reduction models in Figure S6 and Figure S7. Includes LDA plots for models
#           trained using Single and Merged datasets, and LDA plots for evaluating
#           effects using hierarchical classification models at each classification level.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(ggpubr)
require(gridExtra)
require(stringi)
require(ggfortify)
source("toolbox.R")

# Import Data ----------------------

load("RData/Universal_variable.RData")
load("RData/FigureS6-7.RData")

# Generation of subplots ------------------------------

## 1.LDA scatter ----------------------

for (i in 1:length(scatter)) {
  data_name <- scatter[[i]]$name
  data_name_list <- strsplit(data_name, '_')
  t <- data_name_list[[1]][2]
  c <- data_name_list[[1]][3]
  
  scatter_plot(as.data.frame(scatter[[i]]), LDA[i, ], t, c)
}
