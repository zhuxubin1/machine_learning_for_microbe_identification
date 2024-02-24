# Script name: Universal variable.R
# Purpose: Used to load common variables into DRata files.
# Author: Zhu Xubin
# Date Created: 2024-02-18


species <- c("B.licheniformis", "E.cloacae", "E.coli",
             "E.faecalis", "L.monocytogenes", "S.aureus",
             "S.cerevisiae", "S.enterica", "S.marcescens")
abbr <- c("BLI", "ECL", "ECO",
          "EFA", "LMO", "SAU",
          "SCE", "SEN", "SMA") 
concentration <- c("10^4", "10^5", "10^6", "all")
group_level <- c("PCA+LDA, Merged", "PCA+LDA, Hierarchical",
                 "RF, Merged", "RF, Hierarchical")
color_scale <- c("#44045a", "#413e85", "#30688d",
                 "#1f928b", "#35b777", "#91d542",
                 "#f8e620", "#FF8000", "#FE2E2E")

save(species, abbr, concentration, group_level, color_scale,
     file = "RData/Universal_variable.RData")
