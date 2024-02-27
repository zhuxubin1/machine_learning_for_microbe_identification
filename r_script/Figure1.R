# Script name: Figure1.R
# Purpose: The script was used to generate AuNPs characterization images in Figure 1,
#           including particle size histogram, UV-Vis absorption spectrum and zeta 
#           potential histogram.
# Author: Zhu Xubin
# Date Created: 2024-02-15


# Load dependencies ----------------------

require(readxl)
require(dplyr)
require(stringi)
require(ggplot2)
source("toolbox.R")

# Import Data ----------------------

load("RData/Figure1.RData")

# Generation of subplots ------------------------------

## 1.Size plot ----------------------
AuNPs_size_plotdata <- table_add_avg_sd(AuNPs_size, "size")
AuNPs_size_plot(AuNPs_size_plotdata)

## 2.UV-Vis spectrum ----------------------
AuNPs_wave_plot(AuNPs1_wave, "#452a3d", "AuNPs1")
AuNPs_wave_plot(AuNPs2_wave, "#a07673", "AuNPs2")
AuNPs_wave_plot(AuNPs3_wave, "#eed5b7", "AuNPs3")


## 3.zeta potential ----------------------
AuNPs_zeta_plotdata <- table_add_avg_sd(AuNPs_zeta, "zeta")
AuNPs_zeta_plot(AuNPs_zeta_plotdata)
