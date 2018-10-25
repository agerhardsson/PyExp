rm(list=ls())

n_trials <- 550
n_mw <- 16 # ≈ 3%
n_tot <- n_trials + n_mw
# prob_go <- 0.95/8
n_nogo <- 28 # ≈ 5 %
prob_mw <- n_mw/n_tot

go_list <- c(1, 2, 4, 5, 6, 7, 8, 9)
nogo <- 3
mw <- 0
lists <- 10

# Sample loop (It takes a while to run...)
  for (i in seq(1,lists)) {
  list_name <- paste('list', i, sep = "_")
  success <- FALSE
    while (!success) {
      list <- c()
      while (length(list) < n_tot + 1) {
      # Generat a list of n items 1-9, without 3 and 0
        x <- sample(go_list, 8)
        block <- round(n_tot/n_mw)
        
        # Generate random positions for 0s and 3s
        # first MW not before trial 15, and first 3 not before trial 3
        # (start_mw <- sample(12:20, 1))
        (start_nogo <- sample(3:5, 1))
        
        # nogo size, wheighted
        nogo_size <- sample(c(1,2), 1, prob = c(1/4, 3/4))
        
        while (length(x)<block+1) {
          x <- c(x, sample(go_list, 8))
        }
        x <- x[1:block] # 
        
        # genereate position list

          (mw_pos <- sort(sample(x = seq(12, block), size = 1)))
          (nogo_pos <- sort(sample(x = seq(start_nogo, block), size = nogo_size)))
          

        x[mw_pos] <- 0
        x[nogo_pos] <- 3
        
        list <- c(list,x)
      }
      list <- list[1:n_tot]
      
      mw_new_pos <- which(list %in% list[list==0])
      nogo_new_pos <- which(list %in% list[list==3])
      
      to_close <- NULL
      check <- NULL
      for (p in nogo_new_pos){
        for (r in seq(-5,2)) {
          check <-  c(check, mw_new_pos + r)
          
          to_close <- c(to_close, any(p %in% check))
        }
        for (b in c(seq(-3,-1), seq(1,3))) {
          check <- c(check, nogo_new_pos+b)
          to_close2 <- any(p %in% check)
        }
      }
      to_close <- any(to_close==TRUE)
      
      # repeat script until there is 28 3s and 10 0s in the list
      if (length(list[list==3]) == n_nogo 
          & length(list[list==0]) == n_mw
          & to_close == FALSE) 
        success <- TRUE
    }
    print(paste0(i,"/", lists, ' lists finished!'))
    assign(list_name, list)
  }

list_df <- data.frame(cbind(list_1, list_2, list_3, list_4, list_5, 
      list_6, list_7, list_8, list_9, list_10))
probe_df <- data.frame(which(list_df==0, arr.ind = TRUE))
nogo_df <- data.frame(which(list_df==3, arr.ind = TRUE))

probe_sd <- round(tapply(probe_df$row, probe_df$col, sd), 2)
nogo_sd <- round(tapply(nogo_df$row, nogo_df$col, sd), 2)

pdf(file = "NoGo and Probe positions.pdf", height = 8, width = 11, paper = "a4r")
plot(nogo_df$row~nogo_df$col,
     type = 'n',
     xaxt = 'n',
     xlab = "Lists", 
     ylab = "Position"
     )
abline(h = seq(0,566, by = 35), col = "grey")
points(nogo_df$col-0.05, nogo_df$row, col = "grey20", pch = 16)
points(probe_df$col+0.05, probe_df$row, col = "tomato", pch = 16)
axis(side = 1, labels = 1:10, at = 1:10) 
text(x = 0.5, y = 580, 
     labels = 'SD:', xpd = TRUE, pos = 3, font = 2, offset = 1.2, cex = 0.8)
text(x = 0.95:9.95, y = 580, 
     labels = nogo_sd, xpd = TRUE, pos = 3, offset = 1.2, cex = 0.8)
text(x = 0.5, y = 580, 
     labels = 'SD:', xpd = TRUE, pos = 3, font = 2, col = "tomato", cex = 0.8)
text(x = 1.05:10.05, y = 580, 
     labels = probe_sd, xpd = TRUE, pos = 3, col = "tomato", cex = 0.8)
mtext(side = 3, "NoGo", line = 2.5, cex = 1.2, font = 4, at = 4)
mtext(side = 3, "and", line = 2.5, cex = 1.2, font = 2, at = 5)
mtext(side = 3, "Probe", line = 2.5, cex = 1.2, font = 4, col = "tomato", at = 6)
mtext(side = 3, "positions", line = 2.5, cex = 1.2, font = 2, at = 7)
dev.off()

# save.image("lists.RData")
# load("lists.RData")

# write lists to files
write.table(list_1, 'list_1.txt', row.names = FALSE, col.names = FALSE)
write.table(list_2, 'list_2.txt', row.names = FALSE, col.names = FALSE)
write.table(list_3, 'list_3.txt', row.names = FALSE, col.names = FALSE)
write.table(list_4, 'list_4.txt', row.names = FALSE, col.names = FALSE)
write.table(list_5, 'list_5.txt', row.names = FALSE, col.names = FALSE)
write.table(list_6, 'list_6.txt', row.names = FALSE, col.names = FALSE)
write.table(list_7, 'list_7.txt', row.names = FALSE, col.names = FALSE)
write.table(list_8, 'list_8.txt', row.names = FALSE, col.names = FALSE)
write.table(list_9, 'list_9.txt', row.names = FALSE, col.names = FALSE)
write.table(list_10, 'list_10.txt', row.names = FALSE, col.names = FALSE)

write.csv2(list_df, file = "check_list.csv")

# write.csv2(cbind(list_1, list_2), 
#            file = "check_list2.csv")
