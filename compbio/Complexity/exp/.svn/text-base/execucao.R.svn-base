

# Arquivos de entrada
arquivo_entrada <- "./alizadeh-2000-v1_database.txt"
classif_entrada <- "./alizadeh-classes.txt"
no_classes <- 2

# Arquivos de saida para o shrunken e dda
shrunken_classif <- "./shrunken_classif.txt"
shrunken_erro <- "./shrunken_erro.txt"
shrunken_list_genes <- "./shrunken_list_genes.txt"
shrunken_confusion <- "./shrunken_confusion.txt"

dda_classif <- "./dda_classif.txt"
dda_erro <- "./dda_erro.txt"
dda_confusion <- "./dda_confusion.txt"

# Transformação dos dados para o algoritmo
data <- read.table(arquivo_entrada,header=TRUE)
classif <- read.table(classif_entrada)
data <- as.matrix(data)
classif <- as.matrix(classif)
classif <- as.vector(classif)
# Shrunken
shrunken_resultado <- shrunken(data,classif,120)
shrunken_classif_R <- shrunken_resultado$classy
shrunken_erro_R <- shrunken_resultado$erro
shrunken_list_genes_R <- shrunken_resultado$list_genes

# DDA
dda_resultado <- dd_analysis(data,classif)
dda_classif_R <- dda_resultado$resultados
dda_erro_R <- dda_resultado$erro

# Matriz Confusão
shrunken_confusion_R <- confusion_matrix(classif,shrunken_classif_R,no_classes)
shrunken_percent <- shrunken_confusion_R$percent

dda_confusion_R <- confusion_matrix(classif,dda_classif_R,no_classes)
dda_percent <- dda_confusion_R$percent

#Escrevendo os dados
write.table(shrunken_classif_R,file=shrunken_classif)
write.table(shrunken_erro_R,file=shrunken_erro)
write.table(nrow(shrunken_list_genes_R),file=shrunken_list_genes)
write.table(shrunken_percent,file=shrunken_confusion)

write.table(dda_classif_R,file=dda_classif)
write.table(dda_erro_R,file=dda_erro)
write.table(dda_percent,file=dda_confusion)
