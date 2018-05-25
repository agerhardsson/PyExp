# Clear workspace --------------------------------------------------------------
cat("\014")
rm(list=ls())
graphics.off()
# ------------------------------------------------------------------------------

# load useful libraries --------------------------------------------------------
# library(dplyr)
# library(gdata)
library(MixedPsy)
library(psyphy)


# set working directory --------------------------------------------------------

user <- ("/Users/ange3856/Box Sync/PhD/Courses/Applied Psychophysics using Python and R/experiment/linedistance/")

# import main data -------------------------------------------------------------
data_path <- paste(user, "data/", sep= "")
setwd(data_path)
getwd()

temp = list.files(pattern="*.txt$")

d_prel <- do.call(rbind, lapply(temp, read.delim, as.is=TRUE))

# d <- d_prel[d_prel$subject_id>40,]
d <- d_prel

save.image("linedistance.RData")

load("linedistance.RData")



d$response <- as.numeric(d$response)
d <- d[is.na(d$response)==FALSE,]
d$abs_distance <- d$distance-d$probedistance
d$probedistance <- as.factor(d$probedistance)
d$direction <- as.factor(d$direction)

par(mfrow=c(2, 2))
id <- unique(d$subject_id)
block <- unique(d$block)
for (i in id) {
  for (b in block) {
    plot(distance~trial, data = d[d$subject_id==i & d$block==b,], 
         main = paste0("subject id: ", i, ", Direction: ", b),
         ylim = c(0, 6), ylab=('Difference in distance'))
    lines(distance~trial, data = d[d$subject_id==i & d$block==b,])
    
    
  }
  
}

d$correct <- d$response
d$incorrect <- 1-d$response
d$r_distance <- round(d$abs_distance, 1)

tapply(d$abs_distance[d$reversal==1], d$block[d$reversal==1], mean)

################################################################################
# Psycometric functions --------------------------------------------------------
################################################################################

# Aggregate data ---------------------------------------------------------------

d2 <- data.frame(aggregate(d$correct, list(d$direction, d$probedistance, d$abs_distance), sum, na.rm=TRUE), 
                 aggregate(d$incorrect, list(d$direction, d$probedistance, d$abs_distance), sum, na.rm=TRUE)[4])
names(d2) <- c('direction', 'p_distance', 'distance', 'correct', 'incorrect')

d3 <- data.frame(aggregate(d$correct, list(d$direction, d$probedistance, d$r_distance), sum, na.rm=TRUE), 
                 aggregate(d$incorrect, list(d$direction, d$probedistance, d$r_distance), sum, na.rm=TRUE)[4])
names(d3) <- c('direction', 'p_distance', 'distance', 'correct', 'incorrect')

################################################################################
# Cumulative distribution ------------------------------------------------------
data <- d2
pcex <- pnorm(data$correct/data$incorrect - 1) + 0.2
pch <- 1:2
p <- with(data, correct/(correct + incorrect))

# using log transformed distance since variable is skewed. 
# mafc.probit(2) link function for 2AFC
prob1.glm <- glm(cbind(correct, incorrect) ~ log(distance), 
                 binomial(mafc.probit(2)), data = data)

# prob2.glm <- update(prob1.glm, . ~ . + I(log(distance)^2))
# prob3.glm <- update(prob2.glm, . ~ . + I(log(distance)^2) - log(distance))

prob2.glm <- update(prob1.glm, . ~ . + direction)
prob3.glm <- update(prob1.glm, . ~ . + direction:log(distance))
prob4.glm <- update(prob2.glm, . ~ . + p_distance)
prob5.glm <- update(prob3.glm, . ~ . + p_distance)
prob6.glm <- update(prob1.glm, . ~ . + log(distance)*direction*p_distance)

anova(prob1.glm, prob2.glm, prob3.glm, prob4.glm, prob5.glm, prob6.glm, test = 'Chisq')
AIC(prob1.glm, prob2.glm, prob3.glm, prob4.glm, prob5.glm, prob6.glm)

# anova(prob1.glm, prob2.glm, prob3.glm, test = 'Chisq')
# AIC(prob1.glm, prob2.glm, prob3.glm)
# proceding with model2
prob.model <- prob6.glm

summary(prob.model)


hist(log(d2$distance))
# predicted prob.model -------------------------------------------------------------

xx <- seq(0, 3, len = 100)
nd <- data.frame(distance = rep(xx, 4),
                direction = rep(c(levels(data$direction)), each = 100),
                p_distance = rep(c(levels(data$p_distance)), each = 100))

prob.model.pred <- predict(prob.model, newdata = nd, type = "response", se.fit = TRUE)


# plot -------------------------------------------------------------------------
par(mfrow=c(1, 1))
plot(p ~ distance, data, log = 'x',
     xlab = "Distance", ylab = "Proportion Correct",
     xlim=c(0.01, 10), ylim=c(0,1),
     type = 'n',  main= "Gaussian cdf")

abline(0.5, 0, lty = 2, lwd = 2, col = "grey")
abline(0.6, 0, lty = 3, lwd = 1, col = "grey")

lines(xx, prob.model.pred$fit[1:100], lwd = 2, lty = 1)
lines(xx, prob.model.pred$fit[101:200], lwd = 2, lty = 2)

points(p ~ distance, data = data, 
       pch = 20 + pch[unclass(direction)], bg = "white", cex = pcex)

legend(0.5, 0.4, legend = levels(d2$direction), pch = c(21, 22),
       pt.cex = 1.8, bty = "l", lty=c(1, 2, 3, 4, 5))
# ------------------------------------------------------------------------------

d2$hitrate <- d2$correct/(d2$correct+d2$incorrect)
d3 <- aggregate(d2$hitrate, list(d2$direction, d2$p_distance), mean)
names(d3) <- c("direction", "distance", "hitrate")

dp <- tapply(d3$hitrate, list(d3$direction, d3$distance), dprime.mAFC, 2)
d3 <- cbind(d3, dp=rbind(dp[1,1], dp[2,1], dp[1,2], dp[2,2]))


