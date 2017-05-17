
library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(stringr)
library(stringdist)

data = read.csv("model_output3.csv")
m = melt(data, id=c("subj", "blicket", "resp", "hyp",
		 "hyp_pred", "prob", "hamming", "complexity", "verbal", "verbal_pred"))

#head(m)

#m <- mutate(m, verb_char = as.character(verbal))

m <-  m%>% group_by(subj, hyp) %>% mutate(cplx_verb= 1 + str_count(as.character(verbal),"and") +
				str_count(as.character(verbal),"or") )


m <-  m%>% group_by(subj, hyp) %>% mutate(cplx_resp= str_count(as.character(hyp),"C\\["))

m2 <- cbind(m$cplx_verb, as.character(m$verbal))



#p <- ggplot(data=m) +
  #geom_histogram(data=m,bins=3, aes(x=cplx_verb), color="black", fill="black")
p <- ggplot(data=m) +
  geom_bar(data=m, stat='identity', aes(x=cplx_verb, y=prob), 
    color="black", fill="black") 


p <- p + xlab("Verbal Complexity") + ylab("Count") + 
      labs(title="Histogram of Boolean Complexity (Verbal)") +
       theme(plot.title=element_text(size=26),
        axis.text=element_text(size=28), 
    strip.text.x = element_text(size = 26),
    axis.text.x=element_text(size=24),
    axis.title.x=element_text(size=24),
    axis.text.y=element_text(size=24),

    axis.title.y=element_text(size=24),

    legend.title=element_text(size=24),
    legend.text=element_text(size=24),
     legend.key.size = unit(4, 'lines'))

ggsave("verbal_cplx.pdf", width=10, height=6)


p <- ggplot(data=m) +
  geom_bar(data=m, stat='identity', aes(x=cplx_resp, y=prob), color="black", fill="black")

p <- p + xlab("Predicted Cplx from Responses") + ylab("Count") + 

  labs(title="Histogram of Predicted Complexity (Responses)") +
       theme(plot.title=element_text(size=26),
        axis.text=element_text(size=28), 
    strip.text.x = element_text(size = 26),
    axis.text.x=element_text(size=24),
    axis.title.x=element_text(size=24),
    axis.text.y=element_text(size=24),

    axis.title.y=element_text(size=24),

    legend.title=element_text(size=24),
    legend.text=element_text(size=24),
     legend.key.size = unit(4, 'lines'))



ggsave("response_cplx.pdf", width=10, height=6)

p <- ggplot(data=m, aes(x=cplx_resp, y=cplx_verb)) +
stat_summary(fun.data = "mean_cl_boot", geom = "point")

  #geom_jitter(data=m, stat='identity', height=0.1, width=0.1, alpha=0.1,
  			#	aes(x=cplx_resp, y=cplx_verb, size=prob, color=factor(subj)))

p
m <- m %>% group_by(subj, hyp) %>% mutate(hd_verb_resp=stringdist(verbal_pred,
				 resp, method="hamming"))


p <- ggplot(data=m) +
  geom_bar(data=m, stat='identity', aes(x=hd_verb_resp, y=prob), color="black", fill="black")

p <- p + xlab("Hamming Distance") + ylab("Count") + 

  labs(title="Histogram of Hamming Distance b/w Survey and Responses") +
       theme(plot.title=element_text(size=23),
        axis.text=element_text(size=25), 
    strip.text.x = element_text(size = 26),
    axis.text.x=element_text(size=24),
    axis.title.x=element_text(size=24),
    axis.text.y=element_text(size=24),

    axis.title.y=element_text(size=24),

    legend.title=element_text(size=24),
    legend.text=element_text(size=24),
     legend.key.size = unit(4, 'lines'))

ggsave("hamming_resp_verb.pdf", width=14, height=8)



m <- m %>% group_by(subj, hyp) %>% mutate(hd_verb_pred=stringdist(verbal_pred,
				 hyp_pred, method="hamming"))


p <- ggplot(data=m) +
  geom_bar(data=m, stat='identity', aes(x=hd_verb_pred, y=prob), color="black", fill="black")


p <- p + xlab("Hamming Distance") + ylab("Count") + 

  labs(title="Histogram of Hamming Distance b/w Survey and Predicted Hypothesis") +
       theme(plot.title=element_text(size=23),
        axis.text=element_text(size=25), 
    strip.text.x = element_text(size = 26),
    axis.text.x=element_text(size=24),
    axis.title.x=element_text(size=24),
    axis.text.y=element_text(size=24),

    axis.title.y=element_text(size=24),

    legend.title=element_text(size=24),
    legend.text=element_text(size=24),
     legend.key.size = unit(4, 'lines'))

ggsave("hamming_verb_pred.pdf", width=14, height=8)




if (FALSE ) {
m$subj <- factor(m$subj)
m <- m %>%  group_by(subj, hyp) %>% mutate(cmp_p=((1+complexity)/2)*prob  + runif(1,0,1)/100000)


p3 <- ggplot(data=m, aes(group=complexity, fill=subj)) +
  geom_bar(data=m,stat='identity', aes(x=complexity, y=prob, fill=subj, group=subj))
p3



#m <- mutate(m, cplx_p=complexity*prob)


m <- m %>% group_by(subj, hyp) %>% mutate(comp_resp=(length(grep("C\\[", hyp))))




m <- m %>% group_by(subj) %>% mutate(exp_cmp = sum(cmp_p))


m <- m %>% group_by(subj) %>% filter(cmp_p==max(cmp_p))


m$exp_cmp


p <- ggplot(data=m) +
  geom_histogram(data=m, aes(x=exp_cmp))



p
#m <- m %>% group_by(subj, hyp) %>% mutate(prob_jit= prob+ runif(1,0,1)/10000)

#m <- m %>% group_by(subj) %>% filter(prob_jit >= max(prob_jit)) 

m <- m %>% mutate(comp_verb=1+(length(grep("and", verbal))+length(grep("or", verbal))))


m$comp_verb

m$comp_resp

p2 <- ggplot(data=m) +
  geom_point(data=m,stat='identity', aes(x=comp_verb, y=comp_resp))

p2


p4 <- ggplot(data=m) +
  geom_histogram(data=m, aes(x=comp_verb))

p4
}

