install.packages("dplyr")
install.packages("ggplot2")
install.packages("forcats")
install.packages("shiny")
install.packages("hrbrthemes")
install.packages("viridis")
install.packages("gridExtra")
library(dplyr)
library(ggplot2)
library(forcats)
library(viridis)
library(hrbrthemes)
library(grid)
library(gridExtra)
covidData <- read.csv(file = 'covid_50.csv')
covidData2 <- read.csv(file = 'covid_50.csv')
as_tibble(covidData) -> covidDf
as_tibble(covidData2) -> covidDf2

covidDf

#plot 1
covidDf %>%
  ggplot(aes(x = log(Population), y = (Total.Cases/Population)*100, size = Population, color = Continent)) +
  geom_text(aes(angle = 30), label = covidDf$Country, check_overlap = TRUE) +
  scale_size(range = c(2, 50)) +
  ylab("Total % of Covid Cases") +
  xlab("Country's Population") +
  guides(size = "none") +
  coord_cartesian(xlim=c(14,22), ylim=c(-5,68), expand = FALSE) +
  theme_bw()

#plot2
#extract legend
g_legend<-function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

plot1 <- covidDf %>%
  ggplot(aes(x="", y= (Total.Recovered/Population)*100, fill=Size)) +
  geom_bar(stat="identity", width=1) +
  coord_polar("y", start=0) +
  ggtitle("Total % recovered based on country size") +
  theme_void() +
  theme(legend.position="bottom") +
  theme(plot.title = element_text(hjust = 0.5)) + 
  scale_fill_discrete(name = "Country Size") +
  scale_fill_manual(values=c("#CCCC00",
                             "#3399FF",
                             "#006666"))

mylegend<-g_legend(plot1)

plot2 <- covidDf %>%
  ggplot(aes(x="", y= (Total.Deaths/Population)*100, fill=Size)) +
  geom_bar(stat="identity", width=1) +
  coord_polar("y", start=0) +
  ggtitle("Total % death based on country size") +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_fill_manual(values=c("#CCCC00",
                             "#3399FF",
                             "#006666"))

p3 <- grid.arrange(arrangeGrob(plot1 + theme(legend.position="none"),
                               plot2 + theme(legend.position="none"),
                               nrow=1),
                   mylegend, nrow=2,heights=c(10, 1))

#plot3
covidDfContinents <-
  aggregate(covidDf$Total.Deaths/covidDf$Population, by=list(Continent=covidDf$Continent), FUN = sum)
covidDfContinents %>% 
  ggplot( aes(x= reorder(Continent, -x), y=x * 100, fill = Continent)) +
  geom_bar(stat="identity") +
  coord_flip() +
  ylab("Total % of deaths based on population") + 
  xlab("") +
  theme_bw() +
  theme(legend.position = "none")

#plot4

label_data <- covidDf2
number_of_bar <- nrow(label_data)
angle <-  90 - 360 * (label_data$id-0.5) /number_of_bar
label_data$hjust<-ifelse( angle < -90, 1, 0)
label_data$angle<-ifelse(angle < -90, angle+180, angle)

p <- ggplot(covidDf2, aes(x=as.factor(id), y=(Total.Test/Population) * 100, fill = Continent)) +       
  
  geom_bar(stat="identity", color = "gray50") + 
  
  ylim(-2400,2400) +
 
  theme_minimal() +
  labs(
    subtitle = paste(
      "\n\n\n\nTotal % of tests based on population",
      sep = "\n")) +
  theme(
    plot.subtitle = element_text(face = "bold" ,size = 25, hjust = 0.5, vjust = -15),
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid = element_blank(),
    plot.margin = unit(rep(-2,4), "cm"),

  ) +
  coord_polar(start = 0) +
 geom_text(data=label_data, aes(x=id, y=(Total.Test/Population) * 100 , label=Country, hjust=hjust), color="black", fontface="bold",alpha=0.6, size=4, angle= label_data$angle, inherit.aes = FALSE ) 
  
p


