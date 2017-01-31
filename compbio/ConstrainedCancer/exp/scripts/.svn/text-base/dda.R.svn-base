library(foreign)
library(class)
library(sma)

source("/media/Clerton_DATA/mestrado/sbrn/scripts/format_matrix.R")
source("/media/Clerton_DATA/mestrado/sbrn/scripts/input_output.R")

data.path.input <- "/media/Clerton_DATA/mestrado/sbrn/splitted/chen-2002_database.txt"
data.name <- "chen-2002_database"
data.dir.output <- "/media/Clerton_DATA/mestrado/sbrn/splitted/"
data.extension <- ".txt"
logTransform <- FALSE

dd_analysis <- function(dados,classif){

	resultados <- c()
	error <- 0

	treino <- dados
	treinoCL <- classif

	for(i in 1:nrow(treino)){

		treino_SUB <- treino[-i,]
		teste_SUB <- treino[i,]
		treinoCL_SUB <- treinoCL[-i]

		resultado_DDA <- stat.diag.da(treino_SUB,treinoCL_SUB,teste_SUB,pool=1)
		#print(resultado_DDA$pred)
		resultados <- c(resultados,resultado_DDA$pred[1])
		
		if(treinoCL[i] != resultado_DDA$pred[1]) error=error+1

	}

	list(resultados=resultados,accuracy=(error*100)/length(treinoCL),error)

}

print("reading data frame")
data <- read.table(data.path.input, sep = "\t", quote = "", header = T, row.names = NULL)
classif <- data[,ncol(data)]
matrix <- data[,-ncol(data)]

cat("Executando DDA")
dda_resultado <- dd_analysis(as.data.frame(matrix),as.vector(classif))
#dda_erro_R <- dda_resultado$error
