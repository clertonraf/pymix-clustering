###############################################################################
# Format matrix
#	
# Date : August 24, 2009
# Last update: August 24, 2009
#
# Author: Clerton Ribeiro de Araujo Filho
# E-mail: craf@cin.ufpe.br
#
# Formata a matriz para o uso do SVM: Converte a matriz de genes vs. amostras,
# para uma matriz composta por [amostras:classes] vs. genes. A nova matriz tem
# apenas valores numéricos, com exceção da ultima coluna que é composta pela
# classe; além dos valores das amostras e dos genes serem representados como 
# nome das linhas e colunas, respectivamente.
#
# Input: caminho do arquivo com as base
# Output: matriz [amostras:classes] vs. genes
#
# Using Google's R Style Guide:
# http://google-styleguide.googlecode.com/svn/trunk/google-r-style.html
#
###############################################################################

library(sma)

FormatMatrix <- function(matrix.path) {

  matrix <- read.table(matrix.path, sep = "\t", quote = "", header = T, row.names = NULL)
  #matrix <- read.table(matrix.path, sep = "\t", quote = "", header = T, row.names = NULL)
  genes <- matrix[, 1]
  matrix <- matrix[, -1]

  classes <- matrix[1, ]
  row.names(classes) <- "class"
  matrix <- matrix[-1, ]

  samples <- colnames(matrix)

  matrix.t <- t(matrix)
  colnames(matrix.t) <- genes[2:length(genes)]

  matrix.t <- cbind(matrix.t, t(classes) )

  list(matrix = matrix.t)

}
