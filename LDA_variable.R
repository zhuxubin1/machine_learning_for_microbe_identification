# Script name: LDA_variable.R
# Purpose: Used to generate the RData file that holds the parameters of the LDA scatter plot.
# Author: Zhu Xubin
# Date Created: 2024-02-18


LDA_color <- c('#1F77B4', '#D62728', '#2CA02C',
               '#9467BD', '#8C564B', '#E377C2',
               '#7F7F7F', '#BCBD22', '#17BECF', '#FF7F0E')
order_color <- c('#1F77B4', '#D62728', '#2CA02C','#9467BD', '#b2b2b2')
Bacillales_color <- c('#165682', '#5492bf', '#8ed2ff', '#b2b2b2')
Enterobacteriales_color <- c('#ba2223', '#d46f50', '#ebac8c', '#ffe6d5', '#b2b2b2')

order_label <- c("Bacillales", "Enterobacteriales",
                 "Lactobacillales", "Saccharomycetales", "Control")
Bacillales_label <- c("BLI", "LMO", "SAU", "Control")
Enterobacteriales_label <- c("ECL", "ECO", "SEN", "SMA", "Control")

save(LDA_color, order_color, Bacillales_color,
     Enterobacteriales_color, order_label,
     Bacillales_label, Enterobacteriales_label,
     file = "RData/FigureS6-7_variable.RData")
