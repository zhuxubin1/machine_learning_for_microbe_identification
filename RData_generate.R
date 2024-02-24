# Script name: RData_generate.R
# Purpose: Load the data table into the RData file
# Author: Zhu Xubin
# Date Created: 2024-02-15


# Load dependencies ----------------------

library(readxl)
library(openxlsx)
library(stringi)
library(dplyr)
source("toolbox.R")

# Import Data ----------------------

load("RData/Universal_variable.RData")


# Figure 1 ------------------------------

AuNPs_size <- read_xlsx("../AuNPs_characterization/data/AuNPs_size.xlsx")
AuNPs1_wave <- read_xlsx("../AuNPs_characterization/data/AuNPs1_curve.xlsx")
AuNPs2_wave <- read_xlsx("../AuNPs_characterization/data/AuNPs2_curve.xlsx")
AuNPs3_wave <- read_xlsx("../AuNPs_characterization/data/AuNPs3_curve.xlsx")
AuNPs_zeta <- read_xlsx("../AuNPs_characterization/data/Zeta_potential.xlsx")

save(AuNPs_size, AuNPs_zeta, AuNPs1_wave, AuNPs2_wave, AuNPs3_wave,
     file = "RData/Figure1.RData")



# Figure 3 ------------------------------

## 1.ROC curve data ----------------------

ROC_xBlank_all <- ROC_data_load("xBlank", "all")
save_ROC <- list(ROC_xBlank_all = ROC_xBlank_all)

for (c in concentration){
  for (s in species){
    df_name <- sprintf("ROC_%s_%s", s, c)
    ROC <- assign(df_name, ROC_data_load(s, c))
    save_ROC[[df_name]] <- ROC
  }
}
save(save_ROC, file = "RData/Figure3_ROC.RData")

## 2.AUROC & AUPR Error bar diagram ----------------------

AUROC_data_Single <- read_xlsx("../AUROC+AUPR/AUROC_Single.xlsx")
AUPR_data_Single <- read_xlsx("../AUROC+AUPR/AUPR_Single.xlsx")
AUROC_data_Merged <- read_xlsx("../AUROC+AUPR/AUROC_Merged.xlsx")
AUPR_data_Merged <- read_xlsx("../AUROC+AUPR/AUPR_Merged.xlsx")
save(AUROC_data_Single, AUPR_data_Single, AUROC_data_Merged, AUPR_data_Merged,
     file = "RData/Figure3_errorbar.RData")

## 3. F1 score bar plot ----------------------

F1_barplot_xBlank_all <- F1_barplot_data_load("xBlank", "all")
save_F1_barplot <- list(F1_barplot_xBlank_all = F1_barplot_xBlank_all)
for (c in concentration) {
  for (s in species) {
    df_name <- sprintf("F1_barplot_%s_%s", s, c)
    df <- assign(df_name, F1_barplot_data_load(s, c))
    save_F1_barplot[[df_name]] <- df
  }
}
save(save_F1_barplot, file = "RData/Figure3_F1_barplot.RData")



# Figure 4 ------------------------------

## 1.Multi-classification bar chart ----------------------

F1_multi_PCA <- F1_multi_barplot_data_load("PCA+LDA")
F1_multi_RF <- F1_multi_barplot_data_load("RF")
save(F1_multi_PCA, F1_multi_RF, file = "RData/Figure4.RData")



# Figure 5 ------------------------------

## 1.Hierarchical classification bar chart ----------------------

data_PCA <- F1_Hierarchical_barplot_data_load("PCA+LDA")
data_RF <- F1_Hierarchical_barplot_data_load("RF")

F1_Hierarchical_data <- rbind(data_PCA, data_RF)
F1_Hierarchical_data$group <- paste(F1_Hierarchical_data$Model_type,
                                    F1_Hierarchical_data$data_type,
                                    sep = ", ")
F1_Hierarchical_data$group <- factor(F1_Hierarchical_data$group,
                                     levels = group_level)

save(F1_Hierarchical_data, file = "RData/Figure5.RData")



# Figure S1 ------------------------------

## 1.Comparison_histogram ----------------------

df <- read_xlsx("../Interaction characterization/Interaction characterization.xlsx")
save(df, file = "RData/FigureS1.RData")



# Figure S4 ------------------------------

## 1.Bubble plot ----------------------

bubble_Single <- bubble_plot_data_load("Single")
bubble_Merged <- bubble_plot_data_load("Merged")
save(bubble_Single, bubble_Merged, file = "RData/FigureS4.RData")



# Figure S6-S7 ------------------------------

## 1.Scatter diagram ----------------------

nine_LDA <- read.table("../LDA Scatter diagram/data/nine_LDA.txt", header = F)
N_of_image <- c("single", "merged")
save_scatter <- scatter_data_load("../LDA Scatter diagram/data/nine_%s_%s.csv",
                                  N_of_image)

## 2.Scatter diagram (hierarchical) ----------------------

order_LDA <- read.table("../LDA Scatter diagram(hierarchical)/data/order.txt", 
                        header = F)
order = c("order","Bacillales","Enterobacteriales")
save_scatter_order <- scatter_data_load("../LDA Scatter diagram(hierarchical)/data/order_%s_%s.csv",
                                        order)

LDA <- rbind(nine_LDA, order_LDA)
scatter <- c(save_scatter, save_scatter_order)
save(scatter, LDA, file = "RData/FigureS6-7.RData")

