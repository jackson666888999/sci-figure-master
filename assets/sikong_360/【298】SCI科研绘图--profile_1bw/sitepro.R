#! /usr/bin/env Rscript

source("./corelib.R")

# ----- parameters -----
outputName <- "multiSitepro_example.pdf"
bigWigFile <- c("8cell.K4me3.bw")
bedFiles <- c("mm9_HCP_tss.bed","mm9_ICP_tss.bed","mm9_LCP_tss.bed")
labels <- c("HCP","ICP","LCP")
siteType <- "TSS"
resolution <- 10
span <- 2000
coreNumber <- detectCores() - 1
normalization_constant <- 1
colors <- c("darkorange","navy","darkgreen")


# ----- capture signal -----
average_signal <- c()
for(i in 1:length(bedFiles)){
  
  # load bed file
  bed <- read.table(bedFiles[i])
  isNormalChrosome <- !grepl("_",bed$V1)
  bed <- bed[isNormalChrosome,]
  
  # sampling, remove these part for final figure
  set.seed(6666)
  idx <- sample(1:nrow(bed),size=5000)
  bed <- bed[idx,]
  
  # caputre signal
  average_signal <- rbind(average_signal,signal_caputer_around_sites(bigWigFile,bed,resolution=resolution,span=span,cores=as.integer(coreNumber)))
}
average_signal <- average_signal / normalization_constant


# ----- plot -----

minimum <- min(average_signal) - (max(average_signal) - min(average_signal)) * 0.1
maximum <- max(average_signal) + (max(average_signal) - min(average_signal)) * 0.1 * length(bedFiles)

datapoints <- span / resolution

pdf(outputName,width = 7, height = 7)
plot(1:(datapoints*2+1),average_signal[1,],type="l",col=colors[1],
     xaxt="n",xlab="",ylab="Normalized signal",ylim=c(minimum,maximum))
for(i in 2:length(bedFiles)){
  lines(1:(datapoints*2+1),average_signal[i,],col=colors[i])
}
legend("topleft",col=colors,legend=labels,lty=1)
axis(side=1,at=c(0,datapoints,datapoints*2)+1,labels=c(paste(-1*span/1000,"kb"),siteType,paste(span/1000,"kb")))
dev.off()
