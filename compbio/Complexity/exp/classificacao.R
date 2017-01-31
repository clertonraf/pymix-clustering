################################
#
# Carregando as Bibliotecas...
library(sma) # Para o DDA
library(pamr) # Para o shrunken centroids 
#
################################



################################
#
# Diagonal Discriminant Analysis
#
################################
# Parametros:
# - dados: Matriz de expressao de entrada no formato original (genes x condicoes)
# - classif: vetor contendo a classificacao das colunas (tem q ser numerico)
#
# Retorno:
# - $resultados: mostra um vetor com o resultado de todas as classificacoes para todas as colunas
# - $erro: mostra a taxa de erro do DDA

dd_analysis <- function(dados,classif){

	resultados <- c()
	error <- 0

	treino <- t(dados)
	treinoCL <- classif

	for(i in 1:nrow(treino)){

		treino_SUB <- treino[-i,]
		teste_SUB <- t(as.matrix(treino[i,]))
		treinoCL_SUB <- treinoCL[-i]

		resultado_DDA <- stat.diag.da(treino_SUB,treinoCL_SUB,teste_SUB,pool=1)
		print(resultado_DDA$pred)
		resultados <- c(resultados,resultado_DDA$pred[1])
		
		if(treinoCL[i] != resultado_DDA$pred[1]) error=error+1

	}

	list(resultados=resultados,erro=(error*100)/length(treinoCL))

}

# Teste

dados <- matrix(c(4,13,24,33,
			3,12,25,31,
			3,11,23,32,
			5,11,24,31,
			2,14,22,31,
			1,14,23,32,
			2,13,23,33,
			3,12,25,34,
			9,20,29,38,
			8,19,28,39,
			7,18,27,39,
			8,20,27,39,
			8,21,28,37,
			7,18,27,38,
			6,19,29,38,
			3,13,23,33),
			nrow=4,ncol=16,byrow=FALSE)
dados
classif <- c(1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2)
classif

resultado <- dd_analysis(dados,classif)
resultado$resultados
resultado$erro


###########################################################################################################



################################
#
# SHUNKREN CENTROIDS
#
################################
# Parametros:
# - dados: Matriz de expressao de entrada no formato original (genes x condicoes)
# - classif: vetor contendo a classificacao das colunas (tem q ser numerico)
# - seed: parametro do shrunken, geralmente usa 120
#
# Retorno:
# $classy: retorna um vetor com todas as classificacoes
# $erro: o erro associado a classificacao

shrunken <- function(dados, classif, seed){

	set.seed(seed)

	x <- dados
	y <- classif

	mydata <- list(x=x,y=factor(y), geneid=as.character(1:nrow(x)), 
               genenames=paste("g", as.character(1:nrow(x)), sep=""))
	index <- c(1:length(y))

	result <- pamr.train(mydata)
	min_index <- which.min(result$errors)
	classy <- result$yhat[,min_index]
	threshold_ <- result$threshold[min_index]

	list_genes <- pamr.listgenes(result,mydata,threshold=threshold_)

	erros <- 0
	for(i in 1:length(classy)){
		if(classy[i]!=classif[i]) erros <- erros + 1
	}

	list(result=result,classy=classy,list_genes=list_genes,erro=(erros*100/(length(classy))))
 

} # END SHRUNKEN

## Exemplo de Utilizacao

dados <- matrix(c(4,13,24,33,
			3,12,25,31,
			3,11,23,32,
			5,11,24,31,
			2,14,22,31,
			1,14,23,32,
			2,13,23,33,
			3,12,25,34,
			9,20,29,38,
			8,19,28,39,
			7,18,27,39,
			8,20,27,39,
			8,21,28,37,
			7,18,27,38,
			6,19,29,38,
			4,12,24,33),
			nrow=4,ncol=16,byrow=FALSE)
dados
classif <- c(1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2)
classif

resultado <- shrunken(dados,classif,120)
resultado$result
resultado$classy
resultado$erro

##########################################################################################################



################################
#
# MATRIZ DE CONFUSAO
#
################################
# Ele da a taxa de erro para diversos metodos, entre eles o qlda e o lda
# Parametros:
# - classif: vetor contendo a classificacao original das colunas (tem q ser numerico)
# - new: vetor contendo a classificacao nova a partir do knn ou shrunken ou qlda ou lda (numerico)
# - no_classes: o numero de classes, para facilitar a construcao do metodo
#
# Retorno:
# - $confusion: a matriz de confusao
# - $percent: retorna a matriz de confusao no formato percentual. cada coluna soma 100%

confusion_matrix <- function(classif,new,no_classes){

	confusion <- matrix(rep(0,(no_classes*no_classes)),nrow=no_classes,ncol=no_classes,byrow=TRUE)

	# Criando a matriz de confusao
	for(i in 1:(length(classif))){
		actual <- classif[i]
		predicted <- new[i]
		confusion[predicted,actual] = confusion[predicted,actual] + 1
	}

	percent <- confusion

	# Transformando em porcentagem
	for(i in 1:(nrow(percent))){
		for(j in 1:(ncol(percent))){
			percent[i,j] = (percent[i,j] * 100) / (colSums(confusion)[j])
		}
	}

	list(confusion=confusion,percent=percent)

}

# Teste:

classif <- c(1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5)
new     <- c(2,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5)

confusion_matrix(classif,new,5)


##################################################################################################################








