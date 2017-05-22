
library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(stringr)
library(stringdist)
library(car)

data = read.csv("model_output2.csv")
m = melt(data, id=c("subj", "blicket", "resp", "hyp",
		 "hyp_pred", "prob", "hamming", "complexity", "verbal", "verbal_pred", 
		 	"alpha", "time","RT_mean", "RT_median" ))

m$unique <- as.numeric(1:nrow(m))


#m <- (m %>% group_by(subj, alpha) %>% filter(unique == min(unique)))

thresh <- 0.01
m_m <- mean(m$RT_mean)
# <- m %>%  group_by(subj) %>% mutate(pct=RT_mean/m_m) %>% 
     #filter(pct > thresh)



head(m)
length(m$subj)


m$time <- factor(m$time)

m <- mutate(m, log_alpha = log(alpha, 2.0))



m <-  m%>% group_by(subj, hyp, time) %>% mutate(cplx_verb= 1 + str_count(as.character(verbal),"and") +
				str_count(as.character(verbal),"or") )


m <-  m%>% group_by(subj, hyp, time) %>% mutate(cplx_resp=str_count(as.character(hyp),"C\\["))

z <- sum(m$prob)
m <- m %>% group_by(subj, hyp) %>% mutate(p2=prob/z)


z


p <- ggplot(data=m, aes(group=alpha)) +
  geom_bar(data=m, stat='count',  
    aes(x=cplx_resp),color="black", fill="black", size=2.0)+

    facet_wrap(~alpha)
p

p <- ggplot(data=m) +
 # geom_bar(data=m, stat='identity', aes(x=cplx_verb, y=p2), 
   # color="red", fill="red", width=0.5, alpha=0.5)  +

  geom_point(data=m, stat='identity',  
  	aes(x=cplx_resp, y=prob,fill=alpha, color=alpha, 
  		group=alpha, size=prob), alpha=0.25) +

  	stat_smooth(method="glm", 
  		aes(x=cplx_resp, y=prob, color=alpha, group=alpha),
  		se=FALSE, alpha=0.5, size=2.0)#
  #+
  	#facet_wrap(~alpha)
p 

p <- ggplot(data=m, aes(group=alpha)) +
  geom_point(data=m, stat='identity',  
  	aes(x=cplx_resp, y=prob, group=alpha), size=2.0)+
  	stat_smooth(method="lm",  aes(x=cplx_resp, y=prob, group=alpha),
  		se=FALSE, alpha=0.5, size=2.0) +
  	facet_wrap(~alpha)


p <- ggplot(data=m, aes(group=alpha)) +
  geom_bar(data=m, stat='identity',  
  	aes(x=cplx_resp, y=prob, group=alpha),color="black", fill="black", size=2.0)+

  	facet_wrap(~alpha)


  		#+ #+
     	#stat_smooth(method="lm", inherit.aes=FALSE, aes(x=cplx_resp, y=prob),color="black", 
     	#se=FALSE, linetype='dotted', size=2.0) #+


    #scale_colour_gradient2()
 # facet_wrap(~log_alpha


p + xlab("Hypothesis Complexity") + ylab("Probability Mass over Hypotheses") + 
      labs(title="Model Complexity by Alpha", strip="Alpha") +
       theme(plot.title=element_text(size=23),
        axis.text=element_text(size=20), 
    strip.text.x = element_text(size = 18),
    axis.text.x=element_text(size=18),
    axis.title.x=element_text(size=23),
    axis.text.y=element_text(size=18),

    axis.title.y=element_text(size=23),

    legend.title=element_text(size=20),
    legend.text=element_text(size=20),
     legend.key.size = unit(4, 'lines'))

ggsave("model_cplx_alpha.pdf", width=15, height=9)





