# Clear workspace --------------------------------------------------------------
cat("\014")
rm(list=ls())
graphics.off()

library(readxl)

import_export <- function(file) {
  sheets <- excel_sheets(file)
  for (i in seq(1:length(sheets))) {
    data <- read_excel(file, sheet = sheets[i])
    write.table(data, sheets[i], quote = FALSE, sep = '\t', row.names = FALSE)
  }
  
}

import_export("main_list.xlsx")

