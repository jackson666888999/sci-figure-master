devtools::install_github("ddsjoberg/ggsurvfit")

library(tidyverse)
library(ggsurvfit)
library(gghighlight)
install.packages("tidycmprsk")
library(tidycmprsk)

p <- survfit2(Surv(time, status) ~ sex, data = df_lung) %>% 
  ggsurvfit(size = 1)+
  add_censor_mark()+
  add_confidence_interval() +
  add_risktable(theme=theme_test()+
                  theme(axis.title = element_blank(),
                        axis.text.x = element_blank(),
                        axis.ticks.x=element_blank(),
                        axis.text.y = element_text(color="black",size=10)),
                combine_groups=F)+
  add_quantile(color ="grey80",size=0.8,linetype =5)

p +
  theme(legend.position = "bottom",
        legend.title = element_blank()) +
  labs(
    y = "Probability of survival",
    x = "Months since treatment",
    title = "Kaplan-Meier Estimate of Survival by Sex")+
  scale_y_continuous(label = scales::percent, expand = c(0.01, 0)) +
  scale_x_continuous(breaks = 0:5*6, expand = c(0.02, 0))


survfit2(Surv(time, status) ~ sex, data = df_lung) %>% 
  ggsurvfit(size = 1) +
  add_censor_mark(shape = 4) +
  add_quantile(linetype = 3, size = 1) +
  add_confidence_interval() +
  facet_grid(~strata)

survfit2(Surv(time, status) ~ ph.ecog, data = df_lung) %>% 
  ggsurvfit(size = 1) +
  ggplot2::labs(color = "Gender") +
  gghighlight::gghighlight(strata == "Asymptomatic", calculate_per_facet = TRUE)

cuminc(Surv(ttdeath, death_cr) ~ trt, trial) %>%
  ggcuminc(outcome = "death from cancer", size = 1) +
  add_confidence_interval() +
  add_quantile(y_value = 0.20, size = 1) +
  add_risktable() +
  labs(x = "Months Since Treatment") +
  theme(legend.position = "bottom") +
  scale_y_continuous(label = scales::percent, expand = c(0.02, 0)) +
  scale_x_continuous(breaks = 0:4 * 6, expand = c(0.02, 0))

