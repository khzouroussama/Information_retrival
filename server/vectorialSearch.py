# back end 
import re 
import nltk
import numpy as np
import string
import math
from pickle import dump ,load
from nltk.probability import FreqDist 
from server.utils import create_invertedFile ,list_repetition , extract_information ,calculate_frequency ,saveToFile

######## vectorial search 
# preparation (creat the matrix)
def preparationVectorialSearch(repetitionDict,invertedFile,numberDocuments):
    
    matrixDoxumentTerm = np.zeros( ( numberDocuments,len(repetitionDict.keys()) ) )
    wordIndexInRepetition = 0
    
    for word,documentCollection in repetitionDict.items():
        for documentNumber in documentCollection: 

            matrixDoxumentTerm[documentNumber-1][wordIndexInRepetition] = invertedFile[ (word, documentNumber ) ]

        wordIndexInRepetition = wordIndexInRepetition + 1

    # for j in matrixDoxumentTerm.:
    
    return matrixDoxumentTerm
#search
def vectorialModelSearh(Query , matrixDoxumentTerm , similarityMeasure ,listWords ):
    
    with open ('data/common_words') as common_word:
        listLines = common_word.readlines()
    stopWordsList=[]
    for l in listLines:
        stopWordsList.append(l.split("\n")[0].lower())

       
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    queryAllWords = tokenizer.tokenize(Query)
    queryWords = list(sorted(token.lower() for token in queryAllWords if token not in stopWordsList))
    
    ####### query victor
    queryVictor = {}
    for index in range(len(queryWords)):
        word = queryWords[index]
        if word in listWords:
            if listWords.index(word) not in queryVictor.keys():
                 queryVictor[listWords.index(word)] = 0 
            queryVictor[listWords.index(word)] = queryVictor[listWords.index(word)] + 1
  
    ####### calculate sem
    documentList = {}
    if similarityMeasure == "Inner product" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
 
            for key in queryVictor.keys() :
                sommex_y = sommex_y + queryVictor[key] * matrixDoxumentTerm[documentNumber][key]
                
            if sommex_y != 0 :
                somme = sommex_y
                documentList[documentNumber+1] = somme
            
    elif similarityMeasure == "Sørensen–Dice coefficient":
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            
            for key in queryVictor.keys():
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x + sommey_y > 0 and sommex_y != 0 :
                somme = 2 * sommex_y/(sommex_x + sommey_y)
                documentList[documentNumber+1]= somme
    elif similarityMeasure == "Cosine similarity" : 
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for key in queryVictor.keys(): 
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x * sommey_y > 0 and  sommex_y != 0 :
                somme = sommex_y/math.sqrt(sommex_x * sommey_y)
                documentList[documentNumber+1]= somme

    elif similarityMeasure == "Jaccard index" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for key in queryVictor.keys():
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x + sommey_y - sommex_y > 0 and sommex_y != 0 :
                somme = sommex_y/(sommex_x + sommey_y - sommex_y)
                documentList[documentNumber+1]= somme
    
    
    documentListResult = list(documentList.items())
    documentListResult = sorted(documentListResult)
    return documentListResult



#evaluation module victorial 
#calculer recall

def calculeRecall():

    return
#calculate Precision
def calculatePrecision():
    
    return
    
###################################
###################################
#### applying the fonctions########
###################################
###################################
if __name__ == '__main__':
    documentList = extract_information()
    wordFrequenctList = calculate_frequency(documentList)

    
    invertedFile = create_invertedFile(wordFrequenctList)
    # saveInvertedFile("data/invertedFile.pkl",invertedFile)
    
    
    repetitionDict = list_repetition(wordFrequenctList)
    # invertedFile_weights =createInvertedFileWeights(wordFrequenctList,repetitionDict)
    # saveInvertedFileWeights("data/invertedFileWeights.pkl",invertedFile_weights)
    matrixDoxumentTerm = preparationVectorialSearch(repetitionDict,invertedFile,len(documentList) )
    
    query = 'Dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information. Hashing or indexing methods are usually applied to English spelling or natural language problems.'
    
    similarityMeasure =  "Sørensen–Dice coefficient"#type de similariy 4
    listWords = list(repetitionDict.keys())
    
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(documentListResult)
    
    
    similarityMeasure =  "Cosine similarity"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(documentListResult)
    
    similarityMeasure =  "Jaccard index"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(documentListResult)

    similarityMeasure =  "Inner product"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(documentListResult)