import re
import cPickle as pickle

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
        vecFloat = []
        vec = tokens[1:]
        for token in vec:
            vecFloat.append(float(token))
        GloveEmbeddings[word]=vecFloat
    #Add Zerovec, this will be useful to pad zeros, it is better to experiment with padding any non-zero constant values also.
    zerovec = []
    for i in range(0, emb_dim):
        zerovec.append(0.0)
    GloveEmbeddings["zerovec"] = zerovec
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
        remaining = max_query_words - word_count  
        if(remaining>0):
            words += ["zerovec"]*remaining # Pad zero vecs if the word count is less than max_query_words
        words = words[:max_query_words] # trim extra words
        #create Query Feature vector 
        query_feature_vector = []
        for word in words:
            if(word in GloveEmbeddings):
                query_feature_vector.append(GloveEmbeddings[word])
            else:
                query_feature_vector.append(GloveEmbeddings["zerovec"])  #Add zerovec for OOV terms

        #***** Passage Processing **********
        words = re.split('\W+', passage)
        words = [x for x in words if x] # to remove empty words 
        word_count = len(words)
        remaining = max_passage_words - word_count  
        if(remaining>0):
            words += ["zerovec"]*remaining # Pad zero vecs if the word count is less than max_passage_words
        words = words[:max_passage_words] # trim extra words
        #create Passage Feature vector 
        passage_feature_vector = []
        for word in words:
            if(word in GloveEmbeddings):
                passage_feature_vector.append(GloveEmbeddings[word])
            else:
                passage_feature_vector.append(GloveEmbeddings["zerovec"])  #Add zerovec for OOV terms

        #convert label
        label_str = " 1 0 " if label=="0" else " 0 1 " 

        with open('../../data/.txt', 'w') as file:
            file.write(pickle.dumps(passage_feature_vector)) # use `pickle.loads` to do the reverse
        # if(not isEvaluation):
        #     fw.write("|qfeatures "+query_feature_vector+" |pfeatures "+passage_feature_vector+" |labels "+label_str+"\n")
        # else:
        #     fw.write("|qfeatures "+query_feature_vector+" |pfeatures "+passage_feature_vector+"|qid "+str(query_id)+"\n")
        exit(0)



if __name__ == "__main__":

    trainFileName = "../../data/train.tsv"
    validationFileName = "../../data/valid.tsv"
    EvaluationFileName = "../../data/eval1_unlabelled.tsv"

    embeddingFileName = "../../data/glove.6B.50d.txt"

    loadEmbeddings(embeddingFileName)    

    # Convert Query,Passage Text Data to CNTK Text Format(CTF) using 50-Dimension Glove word embeddings 
    TextDataToCTF(trainFileName,"../../data/TrainData.ctf",False)
    print("Train Data conversion is done")
    TextDataToCTF(validationFileName,"../../data/ValidationData.ctf",False)
    print("Validation Data conversion is done")
    TextDataToCTF(EvaluationFileName,"../../data/EvaluationData.ctf",True)
    print("Evaluation Data conversion is done")





