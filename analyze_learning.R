
library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(stringr)
library(stringdist)

#data = read.csv("learning_model_2_bs.csv")
data = read.csv("learning_model.csv")
m = melt(data, id=c("subj", "blicket", "alpha", "hyp", "cplx", "prob", "time", "part_resp"))

head(m)


m <- mutate(m, cplx_verb= 1 + str_count(as.character(part_resp),"and") +
				str_count(as.character(part_resp),"or"))


p <- ggplot(data=m, aes(group=alpha)) +
  geom_bar(data=m, stat='identity',  
  	aes(x=cplx, y=prob, group=alpha),color="black", fill="black", size=2.0)+

  	facet_wrap(~alpha)

p