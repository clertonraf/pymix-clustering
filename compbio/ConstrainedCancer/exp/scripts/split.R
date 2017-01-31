source("/media/Clerton_DATA/mestrado/sbrn/scripts/format_matrix.R")
source("/media/Clerton_DATA/mestrado/sbrn/scripts/input_output.R")

data.path.input <- "/media/Clerton_DATA/mestrado/sbrn/original/chen-2002_database.txt"
data.name <- "chen-2002_database"
data.dir.output <- "/media/Clerton_DATA/mestrado/sbrn/splitted/"
data.extension <- ".txt"
logTransform <- FALSE

WriteData <- function(matrix, path, data.name, i, data.extension, data.type) {
	path.0 <- paste(path,data.name,sep = "/")	#makes path/data.name
	path.1 <- paste(path.0,data.type,sep = "_") 	#makes path/data.name_data.type
	path.2 <- paste(path.1,i,sep="_")		#makes path/data.name_data.type_i
	path.3 <- paste(path.2,data.extension)		#makes path/data.name_data.type_i.data.extension
	WriteMatrix(matrix, path.3)
}

print("reading data frame")
data <- as.data.frame(FormatMatrix(data.path.input)$matrix)
data.size <- length(data[1,])
numfolds <- length(data$class)
class.vector <- data$class
data <- data[,-data.size]
data <- as.matrix(data)

if (logTransform == TRUE){
	print("log transforming...")
	#log transform
	for(data_column in 1:length(data[1,])){
		for(data_row in 1:length(data[,1])){
			data[data_row,data_column] = log(as.real(data[data_row,data_column]))
		}
	}
}

print("class normalizing...")
class <- seq(numfolds,1)
classes <- unique(class.vector)
classes <- as.factor(levels(classes))
for(i in 1:length(class.vector)){
	for(index in 1:length(classes)) {
		if (class.vector[i] == classes[index]){
			class[i] <- index
		}
	}
}

data <- cbind(data,class)
data <- as.data.frame(data)

path <- paste(data.dir.output,data.name,data.extension,sep="")
WriteMatrix(data,path)

print("scrambling folds...")
index.list <- seq(1,length(data[,1]))
scramble.list <- sample(index.list,replace=FALSE)
data.scr <- data[scramble.list,]

n <- as.numeric(numfolds)
nelements <- floor(length(class.vector)/n)
nbiggerfolds <- length(class.vector) - (nelements*n)

i <- 0
foldindex <- c()

while(i < (length(class.vector))) {
	if(i < ((nelements+1)*nbiggerfolds)) {
		i <- i+nelements+1
	} else {
		i <- i+1
	}
	foldindex <- c(foldindex,i)
}

i <- 0
test <- data[i:foldindex[i+1],]
train <- data[-(i:foldindex[i+1]),]
i <- i+1

dir.data <- paste(data.dir.output,data.name,sep="")
dir.create(dir.data)
print(dir.data)

path <- paste(dir.data,i,sep="/")
dir.create(path)
print(path)

WriteData(test, path, data.name, i, data.extension, "test")
WriteData(train, path, data.name, i, data.extension, "train")

while(i < (length(foldindex))) {

	test <- data[(foldindex[i]+1):foldindex[i+1],]
	train <- data[-((foldindex[i]+1):foldindex[i+1]),]
	i <- i+1

	path <- paste(dir.data,i,sep="/")
	print(path)
	dir.create(path)

	WriteData(test, path, data.name, i, data.extension, "test")
	WriteData(train, path, data.name, i, data.extension, "train")

}
