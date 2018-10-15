rm(list=ls())

n_trials <- 550
n_mw <- 10
n_tot <- n_trials + n_mw
# prob_go <- 0.95/8
n_nogo <- 28 # ≈ 5 %
prob_mw <- n_mw/(n_trials + n_mw)

go_list <- c(1, 2, 4, 5, 6, 7, 8, 9)
nogo <- 3
mw <- 0

# Sample loop (It takes a while to run...)
  for (i in seq(1,10)) {
  list_name <- paste('list', i, sep = "_")
  success <- FALSE
    while (!success) {
      list <- c()
      while (length(list) < n_tot + 1) {
      # Generat a list of n items 1-9, without 3 and 0
        x <- sample(go_list, 8)
        block <- n_tot/10
        
        # Generate random positions for 0s and 3s
        # first MW not before trial 15, and first 3 not before trial 3
        (start_mw <- sample(12:20, 1))
        (start_nogo <- sample(3:5, 1))
        
        # nogo size, proper 2.8 times per 55 block it is weighted in favor to 3
        nogo_size <- sample(c(2,3), 1, prob = c(0.4, 0.6))
        
        while (length(x)<block+1) {
          x <- c(x, sample(go_list, 8))
        }
        x <- x[1:block] # 
        
        # genereate position list

          (mw_pos <- sort(sample(x = seq(start_mw, block), size = 1)))
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
        for (r in seq(-3,3)) {
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
    assign(list_name, list)
  }

# save.image("lists.RData")

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

write.csv2(cbind(list_1, list_2, list_3, list_4, list_5, 
                 list_6, list_7, list_8, list_9, list_10), 
           file = "check_list.csv")
