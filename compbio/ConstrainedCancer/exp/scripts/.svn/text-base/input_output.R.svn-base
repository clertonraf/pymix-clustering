library(sma)

ReadMatrix <- function(matrix.path) {
	matrix <- read.table(matrix.path, sep = "\t", quote = "", header = T, row.names = NULL)
	list(matrix = matrix)
}

WriteMatrix <- function(matrix, path) {
    temp <- format(matrix, trim=TRUE, nsmall=4, justify=c("left"))
    write.table(temp, path, row.names=TRUE, sep=" \t", qmethod=c("double"),quote=FALSE)
}
