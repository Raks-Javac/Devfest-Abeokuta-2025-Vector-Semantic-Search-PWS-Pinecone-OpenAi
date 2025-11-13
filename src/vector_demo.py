# Standalone demo: embedding → index → query
# This file demonstrates the complete vector search workflow
class Settings:
    # load keys from .env or os.env in init and pass to created class members 
    pass


def main():
    """
    Main function to demonstrate:
    1. Creating embeddings
    2. Building vector index
    3. Performing similarity search
    4. Test
    """
    pass

def checkAllKeys():
    # check pinecone, open ai, embedding type and your dataset key from settings class 
    # check for pinecona and open ai keys here 
    pass


def createEmbedding():
    # create with open ai "text-embedding-3-large" 
    pass

def checkSampleDataModelAndEmbeddingSize():
    # maybe a list of array of sentences here
    pass

def dotEmbeddingSimilarity():
    # dot product fomular between vector for similarity , 
    # converting sample data[array] to a vector which has been done in checkSampleDataModelAndEmbeddingSize 
    # then applying dot product on the sample data set
    pass

def visualizeEmbeddingSimilarity():
    # after applying dot product on sample data, visualize similarity with  with matplotlib and seaborn
    pass

def loadAndViewActualDataSet():
    # load actual dataset from hugging face or csv or sql db
    pass


def getVectorDbIndexesList():
    pass

def createVectorIndexForDataSet():
    # more like creatting db in pinecone if it doesnt exist  
    # then running migration into the pinecone db which is called indexing ,
    # load data into vector db with tqdm 
    pass

def semanticSearch():
    # pass a query into the vector db[pinecone],
    #  obviously first embeddibng it , then query
    # returns score based on top k[nearest vector in the vector space/place], with score and all[context to data]
    pass




if __name__ == "__main__":
    main()


print(main())
