from ghmm import *
from os import *
import io


def getSequences(fasta_dir):
    """O metodo getSequences retorna um vetor de sequencias, em que cada indice do
    vetor corresponde a um arquivo *.fasta do diretorio dado.
    """
    fasta_sequences = []
    for fasta in listdir(fasta_dir):
        
        fasta_filename = fasta_dir+fasta
        
        if(fasta_filename.find("fasta") != -1) :
            print fasta_filename

            fasta_file = io.open(fasta_filename,"r")
            head = fasta_file.readline().rstrip()

            line = fasta_file.readline()
            sequence = []
    
            while len(line) != 0:
                sequence.append(line.rstrip())
                line = fasta_file.readline()
            s = "".join(sequence)
            fasta_sequences.append(s)
    
    return fasta_sequences


def getElementsFreq(sequence):
    """O metodo getElementsFreq retorna, respectivamente, um vetor contendo as 
    frequencias de elementos das ilhas de CpGs, e um vetor contendo as frequencias
    de elementos nao-ilha de CpGs, dada uma sequencia. 
    """

    cpgs = []
    not_cpgs = []
    
    num_A = sequence.count("A")
    num_C = sequence.count("C")
    num_G = sequence.count("G")
    num_T = sequence.count("T")
    num_Upper = num_A+num_C+num_G+num_T

    num_a = sequence.count("a")
    num_c = sequence.count("c")
    num_g = sequence.count("g")
    num_t = sequence.count("t")
    num_Lower = num_a+num_c+num_g+num_t

    freq_A = float (num_A) /num_Upper
    cpgs.append(freq_A)
    freq_C = float (num_C) /num_Upper
    cpgs.append(freq_C)
    freq_G = float (num_G) /num_Upper
    cpgs.append(freq_G)
    freq_T = float (num_T) /num_Upper
    cpgs.append(freq_T)

    freq_a = float (num_a) /num_Lower
    not_cpgs.append(freq_a)
    freq_c = float (num_c) /num_Lower
    not_cpgs.append(freq_c)
    freq_g = float (num_g) /num_Lower
    not_cpgs.append(freq_g)
    freq_t = float (num_t) /num_Lower
    not_cpgs.append(freq_t)
    
    return cpgs, not_cpgs

"""
O metodo getStatesFreq retorna um vetor contendo as todas as possiveis 
frequencias de transicao entre estados repesentados por letras maiusculas e 
minusculas. [lower->lower, lower->UPPER, UPPER->lower, UPPER->UPPER]
"""

def getStatesFreq(sequence):

    freq = []
    
    count_lower_lower = 0
    count_upper_upper = 0
    count_lower_upper = 0
    count_upper_lower = 0
    
    for index in range(len(sequence)-1):
        if(sequence[index].islower()):
            if(sequence[index+1].islower()):
                count_lower_lower += 1
            else:
                count_lower_upper += 1
        else:
            if(sequence[index+1].isupper()):
                count_upper_upper += 1
            else:
                count_upper_lower += 1
                
    freq_lower_lower = float (count_lower_lower) /(count_lower_lower + count_lower_upper)
    freq_lower_upper = float (count_lower_upper) /(count_lower_lower + count_lower_upper)
    freq_upper_lower = float (count_upper_lower) /(count_upper_upper + count_upper_lower)
    freq_upper_upper = float (count_upper_upper) /(count_upper_upper + count_upper_lower)
    
    freq.append(freq_lower_lower)
    freq.append(freq_lower_upper)
    freq.append(freq_upper_lower)
    freq.append(freq_upper_upper)

    
    return freq

"""
Cria o modelo de uma HMM com 4 estados, probabilidade inicial de transicao
[0.99,0.01] e distribuicao discreta, dada um sequencia
"""
def createHMM(sequence):

    # Frequencia dos elementos
    cpgs, not_cpgs = getElementsFreq(sequence)
    
    # Frequencia de mudanca dos estados
    statesFreq = getStatesFreq(sequence)
    
    # Alfabeto que representa os estados. 
    # No caso, quatro: [lower->lower, lower->UPPER, UPPER->lower, UPPER->UPPER]
    sigma = IntegerRange(1, 5) 
    
    # Matriz com as probabilidades de transicao de estados
    A = [[statesFreq[0],statesFreq[1]],[statesFreq[2],statesFreq[3]]]
    
    # Matriz com as probabilidades de ser ilha ou nao-ilha em cada elemento da sequencia 
    B = [not_cpgs, cpgs]
    
    # Emissoes iniciais para o HMM comecar em ilha ou nao ilha
    pi = [float(0.99),float(0.01)]
    
    return HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)

"""
Retorna duas SequenceSet, respectivamente, de treino e de teste, dado as
listas com as sequencias para treino e para teste.
"""
def createSequenceSet(sequences):
    sequences_cp = []
    for index in range(len(sequences)):
        sequences_cp.append(sequences[index])
        sequences_cp[index] = sequences_cp[index].upper()

    alphabet = Alphabet(['A','C','G','T','N'])
 
    train_set = SequenceSet(alphabet,sequences_cp[0:len(sequences)-1])
    
    test_set = SequenceSet(alphabet,[sequences_cp[len(sequences)-1]])
    
    return train_set, test_set

"""
Retorna um float contendo o erro do algoritmo de viterbi dado uma sequencia de
teste
"""
def errorRate(viterbi,test):
        
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    
    tamanho = len(viterbi[0])-1
   
    for j in range(len(viterbi[0])-1):
        viterbi_char = viterbi[0][j]
        test_char = test[j]
        if viterbi_char == 1:
            if test_char.islower():
                false_positives += 1
            else:
                true_positives += 1
        else:
            if test_char.isupper():
                false_negatives += 1
            else:
                true_negatives += 1
    
        
    return float(false_negatives + false_positives)/float(false_positives + true_positives + false_negatives + true_negatives)

# Diretorio que contem os arquivos *.fasta
fasta_dir = "../cpgs/"

# As sequencias contidas nos arquivos *.fasta
sequences = getSequences(fasta_dir)

# As sequencias separadas em treino e teste, no objeto SequenceSet
train_set, test_set = createSequenceSet(sequences)

# itera dentre as sequencias, sendo a ultima reservada para teste.
for index in range(len(sequences)-1):
    
    # Cria uma HMM com uma sequencia dada
    m = createHMM(sequences[index])
    print "HMM inicial\n",m

    # Executa o algortimo de viterbi para um HMM e um conjunto de treino
    viterbi = m.viterbi(test_set)

    # Calculo do erro de execucao do Viterbi
    error = errorRate(viterbi,sequences[len(sequences)-1])
    print "Erro viterbi:",error,"\n"

    # Re-treinamento com o algoritmo de baumWelch
    m.baumWelch(train_set)
    print "HMM Baum-Welch \n",m

    # O novo calculo do viterbi, com o re-treinamento do Baum-Welch
    viterbi_welch = m.viterbi(test_set)

    # O novo calculo do erro de execucao do Viterbi, com o re-treinamento do Baum-Welch
    error = errorRate(viterbi,sequences[len(sequences)-1])
    print "Novo erro viterbi:",error,"\n"
