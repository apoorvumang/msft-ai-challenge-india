import re

#Initialize Global variables 
GloveEmbeddings = {}
max_query_words = 12
max_passage_words = 50
emb_dim = 50
#The following method takes Glove Embedding file and stores all words and their embeddings in a dictionary
def loadEmbeddings(embeddingfile):
    global GloveEmbeddings,emb_dim

    fe = open(embeddingfile,"r")
    for line in fe:
        tokens= line.strip().split()
        word = tokens[0]
        vec = tokens[1:]
        vec = " ".join(vec)
        GloveEmbeddings[word]=vec
    #Add Zerovec, this will be useful to pad zeros, it is better to experiment with padding any non-zero constant values also.
    GloveEmbeddings["zerovec"] = "0.0 "*emb_dim
    fe.close()


def TextDataToCTF(inputfile,outputfile,isEvaluation):
    global GloveEmbeddings,emb_dim,max_query_words,max_passage_words

    f = open(inputfile,"r")  # Format of the file : query_id \t query \t passage \t label \t passage_id
    fw = open(outputfile,"w")
    n = 0
    for line in f:
        if n%10000 == 0:
            print str(n) + " lines done"
        n += 1
        if n == 10001:
            exit(0)
        tokens = line.strip().lower().split("\t")
        query_id,query,passage,label = tokens[0],tokens[1],tokens[2],tokens[3]

        #****Query Processing****
        words = re.split('\W+', query)
        words = [x for x in words if x] # to remove empty words 
        word_count = len(words)
        print word_count
        remaining = max_query_words - word_count  
        # if(remaining>0):
        #     words += ["zerovec"]*remaining # Pad zero vecs if the word count is less than max_query_words
        words = words[:max_query_words] # trim extra words
        #create Query Feature vector 
        query_feature_vector = ""
        for word in words:
            if(word in GloveEmbeddings):
                query_feature_vector += GloveEmbeddings[word]+" "
            # else:
            #     query_feature_vector += GloveEmbeddings["zerovec"]+" "  #Add zerovec for OOV terms
        query_feature_vector = query_feature_vector.strip() 

        #***** Passage Processing **********
        words = re.split('\W+', passage)
        words = [x for x in words if x] # to remove empty words 
        word_count = len(words)
        remaining = max_passage_words - word_count  
        if(remaining>0):
            words += ["zerovec"]*remaining # Pad zero vecs if the word count is less than max_passage_words
        words = words[:max_passage_words] # trim extra words
        #create Passage Feature vector 
        passage_feature_vector = ""
        foundWords = 0
        for word in words:
            if(word in GloveEmbeddings):
                foundWords += 1
                passage_feature_vector += GloveEmbeddings[word]+" "
            # else:
            #     passage_feature_vector += GloveEmbeddings["zerovec"]+" "  #Add zerovec for OOV terms
        print foundWords
        passage_feature_vector = passage_feature_vector.strip() 

        #convert label
        label_str = " 1 0 " if label=="0" else " 0 1 " 

        if(not isEvaluation):
            fw.write("|qfeatures "+query_feature_vector+" |labels "+label_str+"\n")
        else:
            fw.write("|qfeatures "+query_feature_vector+" |pfeatures "+passage_feature_vector+"|qid "+str(query_id)+"\n")
        exit(0)


if __name__ == "__main__":

    trainFileName = "../../data/train.tsv"
    validationFileName = "../../data/valid.tsv"
    EvaluationFileName = "../../data/eval1_unlabelled.tsv"

    embeddingFileName = "../../data/glove.6B.50d.txt"

    loadEmbeddings(embeddingFileName)    

    # Convert Query,Passage Text Data to CNTK Text Format(CTF) using 50-Dimension Glove word embeddings 
    TextDataToCTF(trainFileName,"/scratche/home/apoorv/TrainData.ctf",False)
    print("Train Data conversion is done")
    TextDataToCTF(validationFileName,"/scratche/home/apoorv/ValidationData.ctf",False)
    print("Validation Data conversion is done")
    TextDataToCTF(EvaluationFileName,"/scratche/home/apoorv/EvaluationData.ctf",True)
    print("Evaluation Data conversion is done")





