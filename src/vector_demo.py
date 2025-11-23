# Standalone demo: embedding → index → query
# This file demonstrates the complete vector search workflow
import os
import dotenv
import openai

# Load environment variables from .env file (searches in current and parent directories)
dotenv.load_dotenv(dotenv.find_dotenv())

class Settings:
     
    def __init__(self) -> None:
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.open_api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = "text-embedding-3-large"
    
    def getAllInitValues(self):
        if not self.pinecone_api_key or not self.open_api_key:
            print("Warning: API keys not found. Please check your .env file.")
        else:
            print(
                f"""
    App Settings values:
    1. PINECONE: {self.pinecone_api_key}
    2. OPEN_AI_KEY: {self.open_api_key}
    3. OPEN_AI_EMBEDDING_MODEL: {self.embedding_model}
    """
        )



# initialize settings object
settings = Settings()

def main():
    checkAllKeys()
    checkSampleDataModelAndcreateEmbedding()
    
    
    
    

def checkAllKeys():
    # check pinecone, open ai, embedding type and your dataset key from settings class 
    # check for pinecona and open ai keys here 
    settings.getAllInitValues()





def checkSampleDataModelAndcreateEmbedding():
    # 1. Define a list of sample sentences for embedding
    sentences = [
    "the hive of bees protect their queen",          #0
    "a beehive is an enclosed structure in which honet bees live",   #1
    "a condominium is a an enclosed structure in which people luve",    #2
    "the flying hive has bees in it"          #3
    ] 
    print(f"Embedding raw sample data: {sentences}") # Print the raw sample data

    # 2. Use the new v1 API for embeddings to create embedding from data
    res = openai.embeddings.create(input=sentences, model=settings.embedding_model)

    # 3. Extract the embedding vectors from the API response, visualizing this .. [[vector1],[vector2],[vector3],[vector4]]
    embeds = [r.embedding for r in res.data] 

    # 4. Print the full embedding results
    # print(f"Embedding sample result: {embeds}") 

    # 5. Print the number of embeddings generated
    print(f"Embedding length: {len(embeds)}") 




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
