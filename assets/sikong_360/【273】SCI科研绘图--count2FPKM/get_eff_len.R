##' download or load local gtf file and get the longest transcript of each gene
##'
##' @title get_eff_len
##' @param file url or local file path of gff3 file
##' @param feature CDS or exon
##' @param gene_id the feature name of gene id in gtf
##' @param transcript_id the feature name of transcript id in gtf
##' @export
##' @author XuZhougeng
get_eff_len <- function(file=NULL, 
                        feature = "exon",
                        gene_id = 'gene_id',
                        transcript_id = "transcript_id",...){
  # check if file parameter is provided
  if ( is.null(file)){
    stop(" no file path or url provided")
  }
  
  file_split <- unlist(strsplit(file,'/'))
  file_name <- file.path(Sys.getenv('R_USER'),
                         file_split[length(file_split)])
  
  # check file is url or local path
  if (grepl(pattern = '(ftp|http|https)', file)){
    file_name <- file_name
    if ( ! file.exists(file_name)){
      print(paste0("file will save in ", file_name))
      download.file(url = file, 
                    destfile = ,file_name,
                    method = "internal")
    }
  } else{
    if ( ! file.exists(file)){
      stop("file is not exists")
    }
    file_name <- file
  }
  
  # get the file type from the file name
  # and build connection  with different read function
  file_type <- sub('.*?\\.(.*?)$','\\1',file_name)
  if (file_type == 'gtf'){
    gtf_in <- file(file_name, open='rt')
  } else if(file_type == 'gz'){
    file_name_tmp <- gsub(sprintf("[.]%s$",'gz'),"",file_name)
    if ( ! file.exists(file_name_tmp)) 
      R.utils::gunzip(file_name, remove = FALSE)
    gtf_in <- file(file_name_tmp, open='rt')
  } else{
    err_message <- paste0("unsupport file type: ", file_name)
    stop(err_message)
  }
  
  gtf_lines <- readLines(gtf_in, warn=FALSE)
  close(gtf_in)
  
  # save the effitve length of gene
  feature_pattern <- paste0("\\t",feature,"\\t")
  mt_rows <- sum(grepl(feature_pattern, gtf_lines))
  # check the feature
  if ( mt_rows <= 1){
    features <- do.call(rbind, strsplit(gtf_in, '\\t'))[,3]
    print("feature is unfoundable, the top 5 feature is:")
    print(as.data.frame(table(feature))[1:5,])
    stop(paste0("set your feature and run again"))
  }
  
  mt <- matrix(nrow = mt_rows, ncol= 1)
  factor_names <- vector(mode = "character",length = mt_rows)
  # save the gene id of the previous line 
  # iteration 
  line_num <- 1
  for (line in gtf_lines){
    if ( grepl(pattern = "^#", x = line)) next
    records <- unlist(strsplit(x = line, '\\t'))
    if ( grepl(feature, records[3]) ){
      gene_pattern <- paste0(".*?", gene_id, " \"(.*?)\";.*")
      gene_id_ <- sub(gene_pattern,"\\1",records[9])
      tx_pattern <- paste0(".*?", transcript_id, " \"(.*?)\";.*")
      tx_id_ <- sub(tx_pattern, "\\1",records[9])
      gene_start <- records[4]
      gene_end <- records[5]
      # add 1 for gtf coordinate is 1-based
      gene_len <- abs(as.numeric(gene_end) - as.numeric(gene_start) + 1)
      mt[line_num,] <- gene_len
      factor_names[line_num] <- paste0(gene_id_,"_",tx_id_)
      line_num <- line_num + 1
    }
  }
  by_transcript <- as.factor(factor_names)
  tx_length <- sapply(split(mt[,1], by_transcript), sum, na.rm=TRUE)
  by_gene <- as.factor(do.call(rbind, 
                               strsplit(names(tx_length), '_'))[,1])
  gene_length <- sapply(split(tx_length, by_gene), max)
  return(gene_length)
}
