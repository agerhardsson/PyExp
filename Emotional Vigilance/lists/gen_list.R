
rm(list=ls())

setwd("/Users/ange3856/Box Sync/PyExp/Emotional Vigilance/lists")

user <-  '/Users/ange3856/Box Sync/'
iaps <-  paste0(user, 'SleepBoxDocuments/Documents/IAPS/IAPS 2008 1-20 2')
files_path <-  paste0(iaps, '/IAPS 1-20 Images')
emw_path <- paste0('/Users/ange3856/Box Sync/SleepBoxDocuments/',
                   'Programs/PsychoPy/Emotional N-back_12pictures/')

list_iaps <- read.delim(paste0(iaps,'/IAPS Tech Report/AllSubjects_1-20.txt'), 
                    skip = 5)
head(list_iaps)
names(list_iaps) <- c('desc', 'iaps_num', names(list_iaps)[3:length(list_iaps)])

# files <- data.frame(iaps_jpg = list.files(files_path))
# files$iaps_num <- gsub("\\..*", "", files$iaps_jpg)

emw_files <- list.files(paste0(emw_path,'/images'))
emw_files <- emw_files[-c(grep("image*", emw_files), grep('fix*', emw_files))]
emw_lists <- paste0(paste0(emw_path, 'lists/'),
                    list.files(paste0(emw_path, 'lists'), pattern = '*_block'))

emw_lists <- do.call(rbind, lapply(emw_lists, read.delim, as.is=TRUE))

ewm_pictures <- emw_lists[!duplicated(emw_lists$picture), c('picture', 'valence')]

ewm_pictures$iaps_jpg <- gsub(".*_", "", ewm_pictures$picture)
ewm_pictures$iaps_num <- gsub("\\..*", "", ewm_pictures$iaps_jpg)
ewm_pictures$picture <- NULL
ewm_pictures <- ewm_pictures[,c(3,2,1)]
rownames(ewm_pictures) <- 1:nrow(ewm_pictures)

list_m <- merge(ewm_pictures, list_iaps, by.x = 'iaps_num')
head(list_m)

write.table(list_m, 'iaps_list.txt', quote = FALSE, sep = '\t', row.names = FALSE)

# version_lists

negative <- list_m[list_m$valence=='negative',
                   c('iaps_num', 'iaps_jpg', 'valence')]
positive <- list_m[list_m$valence=='positive',
                   c('iaps_num', 'iaps_jpg', 'valence')]
neutral <- list_m[list_m$valence=='neutral',
                  c('iaps_num', 'iaps_jpg', 'valence')]
# side <- c('left', 'right')
side <- c(-1, 1)
soa <- rep(c(0.0, 0.50, 0.100, 0.200, 0.300, 0.500), each = 10)


for (i in 1:6) {
  list_name <- paste0('list_', i)

  neu_list <- c(sample(neutral$iaps_jpg))
    # ------------------------------------------------------------------------.
    pass <- FALSE
    while (pass == FALSE) {
      neg_list <- data.frame(emo_jpg = c(sample(negative$iaps_jpg, 24),
                                         sample(negative$iaps_jpg, 24)),
                             emo_side = sample(side, 48, replace = TRUE),
                             neu_jpg = neu_list,
                             valence = 'negative',
                             probe_side = sample(side, 48, replace = TRUE)
                             )

      pass <- all(c(sum(neg_list$emo_side) == 0,
                        sum(neg_list$probe_side) == 0,
                        sum(neg_list$congruent) == 0))

    }
    print('Negative list base created')
    # ------------------------------------------------------------------------.
    pass <- FALSE
    while (pass == FALSE) {
        neg_list$soa <- sample(soa, size = 48)
        pass <-  all((table(neg_list$soa)[1:5] > 8
             & table(neg_list$soa)[1:5] < 11))
    }
    print("SOA's created")
    # ------------------------------------------------------------------------.

    # ------------------------------------------------------------------------.
    pass <- FALSE
    while (pass == FALSE) {
      pos_list <- data.frame(emo_jpg = c(sample(positive$iaps_jpg, 24),
                                         sample(positive$iaps_jpg, 24)),
                             emo_side = sample(side, 48, replace = TRUE),
                             neu_jpg = neu_list,
                             valence = 'positive',
                             probe_side = sample(side, 48, replace = TRUE)
      )

      pass <- all(c(sum(pos_list$emo_side) == 0,
                    sum(pos_list$probe_side) == 0,
                    sum(pos_list$congruent) == 0))

    }
    print('Positive list base created')
    # ------------------------------------------------------------------------.
    pass <- FALSE
    while (pass == FALSE) {
      pos_list$soa <- sample(soa, size = 48)
      pass <-  all((table(pos_list$soa)[1:5] > 8
                    & table(pos_list$soa)[1:5] < 11))
    }
    print("SOA's created")
    # ------------------------------------------------------------------------.

      if ((i %% 2) == 0) {
        df <- rbind(neg_list, pos_list)
      }
      else {
        df <- rbind(pos_list, neg_list)
      }
      if (i > 4) {
        df <- df[sample(nrow(df)),]
      }
  
  df$congruence <- df$emo_side*df$probe_side 
  df$trial <- 1:nrow(df)
  

  assign(list_name, df)
  print(paste('Done exporting:', list_name))
  write.table(df, paste0(list_name, ".txt"),
              quote = FALSE, row.names = FALSE, sep = '\t')
}

