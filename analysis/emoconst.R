# Clear workspace --------------------------------------------------------------
cat("\014")
rm(list=ls())
graphics.off()

# ------------------------------------------------------------------------------

# load useful libraries --------------------------------------------------------
# library(dplyr)
# library(gdata)
# library(MixedPsy)
# library(psyphy)


# set working directory --------------------------------------------------------

user <- ("/Users/ange3856/Box Sync/PhD/Courses/Applied Psychophysics using Python and R/experiment/emotion constancy/")

# # import main data -------------------------------------------------------------
# data_path <- paste(user, "pics/", sep= "")
# setwd(data_path)
# getwd()
# 
# filename_l = list.files(pattern="*.jpg$")
# 
# dL <- data.frame(filename_l)
# dL$female_l <- ifelse(grepl("F", dL$filename_l), 1, 0)
# dL$angry_l <- ifelse(grepl("AN", dL$filename_l), 1, 0)
# dL$intensity_l <- ifelse(grepl("40", dL$filename_l), 40, 0)
# dL$intensity_l <- ifelse(grepl("60", dL$filename_l), 60, dL$intensity_l)
# dL$intensity_l <- ifelse(grepl("80", dL$filename_l), 80, dL$intensity_l)
# dL$intensity_l <- ifelse(grepl("100", dL$filename_l), 100, dL$intensity_l)
# dL$size_l <- ifelse(grepl("-1", dL$filename_l), 4, 5)
# dL$size_l <- ifelse(grepl("-2", dL$filename_l), 3, dL$size_l)
# dL$size_l <- ifelse(grepl("-3", dL$filename_l), 2, dL$size_l)
# dL$size_l <- ifelse(grepl("-4", dL$filename_l), 1, dL$size_l)
# dL$size_l <- ifelse(grepl("-5", dL$filename_l), 0, dL$size_l)
# 
# dR <- dL
# names(dR) <- gsub("_l", "_r", names(dR))
# 
# dL <- dL[dL$intensity_l> 0,]
# dR <- dR[dR$intensity_r> 0,]
# 
# man_l <- dL[dL$female_l == 0 & dL$angry == 1,]
# fan_l <- dL[dL$female_l == 1 & dL$angry == 1,]
# mha_l <- dL[dL$female_l == 0 & dL$angry == 0,]
# fha_l <- dL[dL$female_l == 1 & dL$angry == 0,]
# man_r <- dR[dR$female_r == 0 & dR$angry == 1,]
# fan_r <- dR[dR$female_r == 1 & dR$angry == 1,]
# mha_r <- dR[dR$female_r == 0 & dR$angry == 0,]
# fha_r <- dR[dR$female_r == 1 & dR$angry == 0,]
# 
# 
# 
# rand.fem <- function(x, y) {
#   repeat {
#       x$rand <- sample(seq(1, nrow(x)), replace = FALSE)
#       x <- x[order(x$rand),]
#       intensity_diff <- fan_l$intensity_l-x$intensity_r
#       check <- ifelse(abs(intensity_diff) > 40 & abs(intensity_diff) < 80, 1, 0)
#   if (sum(check) > 2)
#     Recall(x, y)
#   else return(cbind(y, x, intensity_diff))
#   }
# }
# 
# mha <- rand.fem(mha_r, mha_l)
# man <- rand.fem(man_r, man_l)
# fha <- rand.fem(fha_r, fha_l)
# fan <- rand.fem(fan_r, fan_l)
# 
# save.image("randomlist.RData")
load("randomlist.RData")

code.set <- function(data) {
  size_diff <- data$size_l - data$size_r
  intensity_target <- ifelse(data$intensity_diff>0, -1, 0)
  intensity_target <- ifelse(data$intensity_diff<0, 1, intensity_target)
  size_target <- ifelse(size_diff>0, -1, 0)
  size_target <- ifelse(size_diff<0, 1, size_target)
  return(cbind(data, size_diff, intensity_target, size_target))
}

man <- code.set(man)
