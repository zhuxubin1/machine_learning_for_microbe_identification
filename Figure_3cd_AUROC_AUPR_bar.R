library(ggplot2)
library(ggpubr)
library(patchwork)
library(readxl)
library(ggnewscale)
library(dplyr)

my_color <- c("#FE8600","#FEB705","#219EBC","#034C75")
my_backgroud <- c("#EFE4B0", "#FFFFFF")
x_label <- c("BLI","ECL","ECO",
             "EFA","LMO","SAU",
             "SCE","SEN","SMA") 

plot_fun <- function(df, start, title, y_lim) {
  df <- df %>% filter(target != "xBlank")
  # 计算置信区间 ci
  N <- 30
  end <- start + N - 1 
  df$avgValue <- rowMeans(df[, start:end])
  
  df$sd <- apply(df[, start:end], 1, sd)
  df$se <- df$sd / sqrt(N)
  conf.interval = 0.95
  ciMult <- qt(conf.interval/2 + .5, 29)
  df$ci <- df$se * ciMult
  
  df$concentration <- factor(df$concentration, 
                             levels = c("10^4","10^5","10^6","all"))
  
  # 用于画背后的柱状图
  bar_data <- data.frame(x = seq(2.5, 37.5, by = 4), y = rep(1, 9),
                         color = c(rep(c("A", "B"), 4), "A"))
  
  ggplot(df, aes(x=1:nrow(df), y=avgValue)) +
    # 背后的柱状图
    geom_bar(data = bar_data, aes(x = x, y = 1, fill = color),
             stat = "identity", width = 4, 
             show.legend = FALSE, alpha=0.3) +
    
    scale_fill_manual(values = my_backgroud) +
    
    new_scale_color() + 
    geom_point(size=2.5, aes(col = concentration)) +
    scale_color_manual(values = my_color, 
                       labels = expression(10^4, 10^5, 10^6, "all")) +

    geom_errorbar(aes(ymin=ifelse(avgValue-ci<0,0,avgValue-ci), 
                      ymax=ifelse(avgValue+ci>1,1,avgValue+ci),
                      col = concentration),
                  width=0.4,size=1.2,position = position_dodge(0.9)) +
    scale_color_manual(values = my_color,
                       labels = expression(10^4, 10^5, 10^6, "all")) +
    
    # 自定义 y 轴标签
    # scale_y_continuous(breaks = seq(0, 1, by = 0.1), limits = c(0,1)) +
    scale_y_continuous(breaks = seq(y_lim, 1, by = 0.2), limits = c(y_lim,1),
                       expand = c(0,0)) +
    
    # 自定义 x 轴标签
    scale_x_continuous(breaks = seq(2.5, 37.5, by = 4), labels = x_label) + 
    
    geom_hline(yintercept = 1, linetype="dashed") +   # y=1 虚线
    xlab("")+ylab("Area Under Curve") + 
    ggtitle(title) +
    theme_pubr() + 
    labs(color = "Concentration(CFU/mL)") +
    
    theme(axis.text.x = element_text(size = 15, vjust = 1), # 旋转x轴文字
          plot.title = element_text(hjust = 0.5),
          axis.title.x = element_text(face="bold"),
          axis.title.y = element_text(face="bold"),
          legend.position = 'none')
}

AUROC_data <- read_xlsx("AUROC+AUPR/AUROC_Single.xlsx")
p_ROC <- plot_fun(AUROC_data, start=5, title="AUROC", 0)    # AUROC值从第5列开始
AUPR_data <- read_xlsx("AUROC+AUPR/AUPR_Single.xlsx")
p_PR <- plot_fun(AUPR_data, start=5, title="AUPR", 0)

# 保存图片
ggsave("AUROC+AUPR/AUROC_Single.png", plot=p_ROC, device="png",
       units = 'in', width = 8, height = 5, dpi=600)
ggsave("AUROC+AUPR/AUPR_Single.png", plot=p_PR, device="png",
       units = 'in', width = 8, height = 5, dpi=600)
