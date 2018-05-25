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

# mafc.probit(2) link function for 2AFC
prob1.glm <- glm(cbind(correct, incorrect) ~ log(distance), 
                 binomial(mafc.logit(2)), data = data)

# prob2.glm <- update(prob1.glm, . ~ . + I(log(distance)^2))
# prob3.glm <- update(prob2.glm, . ~ . + I(log(distance)^2) - log(distance))

prob2.glm <- update(prob1.glm, . ~ . + direction)
prob3.glm <- update(prob1.glm, . ~ . + direction:log(distance))
prob4.glm <- update(prob2.glm, . ~ . + p_distance)
prob5.glm <- update(prob3.glm, . ~ . + p_distance)
prob6.glm <- update(prob4.glm, . ~ . + log(distance):direction:p_distance)

anova(prob1.glm, prob2.glm, prob3.glm, prob4.glm, prob5.glm, prob6.glm, test = 'Chisq')
AIC(prob1.glm, prob2.glm, prob3.glm, prob4.glm, prob5.glm, prob6.glm)

# anova(prob1.glm, prob2.glm, prob3.glm, test = 'Chisq')
# AIC(prob1.glm, prob2.glm, prob3.glm)
# proceding with model2
prob.model <- prob4.glm

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







# Analysis -------------------------------------------------------------------
par(mfrow=c(2, 2))
direction <- unique(levels(d$direction))
pdistance <- unique(d$probedistance)
for (dir in direction) {
  for (pd in pdistance) {
    data <- d2
    data <- data[data$direction == dir & data$p_distance == pd,]
    q50 <- rep(qnorm(0.5), nrow(data))
    pcex <- pnorm(data$correct/data$incorrect - 1) + 0.5
    p <- with(data, correct/(correct + incorrect))
    rp.mns <- with(d[d$direction==dir & d$probedistance == pd,], tapply(correct, distance, mean))
    
    cdf1.glm <- glm(cbind(correct, incorrect) ~ distance - 1,
                    binomial(probit), data = data)
    cdf2.glm <- update(cdf1.glm, . ~ . + I(distance^2))
    cdf3.glm <- update(cdf2.glm, . ~ . - distance)
    
    plot(p ~ distance, data = data,
         xlab = "Distance", ylab = "Proportion Correct",
         ylim = c(0, 1), xlim = c(0, 6), type = "n",
         main = paste("Distance:", dir))
    abline(0.5, 0, lty = 2, lwd = 2, col = "grey")
    cc <- seq(0, 6, len = 200)
    nq50 <- rep(qnorm(0.50), length(cc))
    nd <- data.frame(distance = cc)
    
    cdf1.pred <- predict(cdf1.glm, newdata = nd, type = "response", se.fit = TRUE)
    cdf2.pred <- predict(cdf2.glm, newdata = nd, type = "response", se.fit = TRUE)
    cdf3.pred <- predict(cdf3.glm, newdata = nd, type = "response", se.fit = TRUE)
    
    # polygon(c(cc, rev(cc)),with(cdf1.pred, c(fit + 2 * se.fit, rev(fit - 2 * se.fit))),
    #         col = "grey", border = "white" )
    polygon(c(cc, rev(cc)),with(cdf3.pred, c(fit + 2 * se.fit, rev(fit - 2 * se.fit))),
            col = "grey", border = "white" )
    
    lines(cc, cdf1.pred$fit, lty = 1, lwd = 1)
    
    lines(cc, cdf2.pred$fit, lty = 2, lwd = 1)
    
    lines(cc, cdf3.pred$fit, lty = 3, lwd = 1)
    
    points(p ~ distance, data = data,
           pch = 21, bg = "white", cex = pcex)
    
    cdf1.jndpse <- paste("cdf1.jndpse", dir, sep="")
    cdf3.jndpse <- paste("cdf3.jndpse", dir, sep="")
    # assign(cdf1.jndpse, PsychDelta(cdf1.glm))
    # assign(cdf3.jndpse, PsychDelta(cdf3.glm))
    
    rp.mns <- paste("rp.mns", dir, sep = "")
    assign(rp.mns, with(d[d$direction==dir,], tapply(correct, distance, mean)))
    
    # pse <- paste('pse_', ts, sep='')
    # assign(pse)
    
    coef(summary(cdf1.glm))
    coef(summary(cdf2.glm))
    coef(summary(cdf3.glm))
    model <- paste0("modeltest", dir, pd)
    assign(model, anova(cdf1.glm, cdf2.glm, cdf3.glm, test = 'Chisq'))
  }
  
}

# Stair case: logistic function ------------------------------------------------

par(mfrow=c(2, 2))
direction <- unique(levels(d$direction))
pdistance <- unique(d$probedistance)
for (dir in direction) {
  for (pd in pdistance) {
  
  data <- d
  data <- data[data$direction==dir & data$probedistance == pd,]
  # data <- data[data$distance>0,]
  pcex <- pnorm(data$correct/data$incorrect - 1) + 0.5
  
  rp.glm <- glm(response ~ log10(distance), binomial(mafc.logit(2)), data = data)
  rp.mns <- with(d[d$direction==dir & d$probedistance == pd,], tapply(response, distance, mean))
  
  plot(abs(as.numeric(names(rp.mns))), rp.mns, log = "x",
       xlab = "Distance", ylab = "Proportion Correct",
       xlim =c(1.5, 6), ylim=c(0,1),
       type = 'n', main = paste("Direction:", dir, "\n Probe distance: ", pd))
  cnt <- seq(1, 10, len = 200)
  abline(0.5, 0, lty = 2, lwd = 2, col = "grey")
  
  rp.pred <- predict(rp.glm, newdata = data.frame(distance = cnt), type = "response", se.fit = TRUE)
  
  polygon(c(cnt, rev(cnt)),with(rp.pred, c(fit + 2 * se.fit, rev(fit - 2 * se.fit))),
          col = "grey", border = "white" )

  lines(cnt, rp.pred$fit, lty = 1, lwd = 1)
  
  points(abs(as.numeric(names(rp.mns))), rp.mns,
         pch = 21, bg = "white", cex = pcex)
  
}
}


d4 <- cbind(tapply(d$correct, list(d$direction, d$probedistance)),
                 tapply(d$incorrect, list(d$direction, d$probedistance), sum))


# 
# dprime.ABX(d$correct, d$incorrect, )
