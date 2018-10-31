rm(list=ls())

getwd()

pictjap <- list.files("Pictogram/japanese/black")
pictchi <- list.files("Pictogram/chinese/black")
pictchi <- pictchi[-49]
length(pictchi)
image <- list.files("Payen2005IAPS", pattern = ".jpg")
list <- read.delim("Payen2005IAPS/Payen2005IAPS.txt")
nlists <- 10

for (i in seq(1,nlists)) {
  name <- paste("list", i, sep="_")
  df <- data.frame(list[sample(nrow(list)),], 
                   pictjap = rep(sample(pictjap), length.out = length(image)),
                   pictchi = sample(pictchi))
  print(paste0(i,"/", nlists, ' lists finished!'))
  assign(name, df)
  write.table(df, file = paste0("lists/",name, ".txt"), quote = FALSE, sep = '\t', row.names = FALSE)
  
}


