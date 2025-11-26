# Standalone demo: embedding → index → query
# This file demonstrates the complete vector search workflow
import os
import dotenv
import openai
from numpy import dot, array
from numpy.linalg import norm
import seaborn as snb
import matplotlib.pyplot as plt
from IPython.display import display
from pandas import DataFrame
from datasets import load_dataset
from pinecone import Pinecone, ServerlessSpec
import time
from tqdm import tqdm


# Load environment variables from .env file (searches in current and parent directories)
dotenv.load_dotenv(dotenv.find_dotenv())


class Settings:

    def __init__(self) -> None:
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.open_api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = "text-embedding-3-large"
        self.embeds = None
        self.index_name = "embedding-search"

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
    dotEmbeddingSimilarity()
    visualizeEmbeddingSimilarity()
    # createVectorIndexForDataSet()
    # loadAndViewActualDataSet()
    # getVectorDbIndexesList()
    # getVectorDbIndexesInformation()
    # semanticSearch("what is a beehive?")


def checkAllKeys():
    # check pinecone, open ai, embedding type and your dataset key from settings class
    # check for pinecona and open ai keys here
    settings.getAllInitValues()


def checkSampleDataModelAndcreateEmbedding():
    # 1. Define a list of sample sentences for embedding
    sentences = [
        "The constant sound of the dripping tap kept me awake all night",  # 0
        "We need to call a plumber to fix the leaky faucet in the kitchen",  # 1
        "She is looking for a reliable budget car to get to work",  # 2
        "It can be difficult to find an affordable vehicle in this market",  # 3
    ]
    print(f"Embedding raw sample data: {sentences}")  # Print the raw sample data

    # 2. Use the new v1 API for embeddings to create embedding from data
    res = openai.embeddings.create(input=sentences, model=settings.embedding_model)

    # 3. Extract the embedding vectors from the API response, visualizing this .. [[vector1],[vector2],[vector3],[vector4]]
    embeds = [r.embedding for r in res.data]
    settings.embeds = embeds
    # 4. Print the full embedding results
    # print(f"Embedding sample result: {embeds}")

    # 5. Print the number of embeddings generated (result should be 4)
    print(f"Embedding length: {len(embeds)}")

    # 6. loop through each vector to get the length of each vector
    # The result should be [3072, 3072, 3072, 3072] because the text emedding model we are using is text-embedding-3-large
    embed_ints = []
    for r in embeds:
        embed_ints.append(len(r))
    print(f"Embedding length: {embed_ints}")


def dotEmbeddingSimilarity():
    # working with the first two items in the list  for sample
    a = settings.embeds[0]
    b = settings.embeds[1]

    # Dot product
    dot_product = dot(a, b)

    # Cosine similarity
    cos_sim = dot(a, b) / (norm(a) * norm(b))

    print("Dot product:", dot_product)
    print("Cosine similarity:", cos_sim)

    print(f"Embeds Size {len(settings.embeds)}")

    # working with the whole list
    embeds_arr = array(settings.embeds)
    embeds_arr.shape  # this should return this as a turple of the x and y axis size of the matrix
    print(f"Shape of the embeds array {embeds_arr.shape}")

    # getting the size
    dot_prod = dot(embeds_arr, embeds_arr.T)
    dot_prod.shape
    print(f"Shape after dot product of embedding and its transpose {dot_prod.shape}")
    return dot_prod


def visualizeEmbeddingSimilarity():
    a = settings.embeds[0]
    b = settings.embeds[1]
    dot_prod = dot(a, b)
    plt.figure(figsize=(8, 6))
    snb.heatmap(dot_prod, cmap="viridis", annot=True)
    plt.title("Embedding Similarity Heatmap")
    plt.ylabel("Sentence Index")
    plt.show()
    sentences = settings.embeds

    sim_matrix = np.array(dotEmbeddingSimilarity())
    np.fill_diagonal(sim_matrix, -np.inf)  # Exclude self-similarity
    most_similar_idx = np.argmax(sim_matrix, axis=1)
    most_similar_val = np.max(sim_matrix, axis=1)

    summary_df = pd.DataFrame(
        {
            "Sentence": sentences,
            "Most Similar To (Index)": most_similar_idx,
            "Most Similar To (Sentence)": [sentences[i] for i in most_similar_idx],
            "Similarity Value": most_similar_val,
        }
    )

    display(summary_df)
    # after applying dot product on sample data, visualize similarity with  with matplotlib and seaborn


def loadAndViewActualDataSet():
    # load actual dataset from hugging face or csv or sql db
    squad_dataset = load_dataset("squad_v2", split="train")
    # print(f"Squad Dataset from huggingface {squad_dataset}")
    # print(f"Squad Dataset from huggingface, first item:  {squad_dataset[0]}")
    contexts = list(set(squad_dataset["context"]))
    # context here is extracted from each model, and converted to a set to avoid duplicates
    print(f"Number of unique contexts: {len(contexts)}")
    print(f"First context: {contexts[0]}")
    return squad_dataset


def getVectorDbIndexesList():
    # the index_name is also more like db name
    # but this is referring to the index name on the pinecone db
    pc = Pinecone(api_key=settings.pinecone_api_key)
    print(pc.list_indexes())
    return pc.list_indexes()


def getVectorDbIndexesInformation():
    index = pc.Index(index_name)
    batch_size = 100

    for i in tqdm(range(0, len(contexts), batch_size)):
        i_end = min(i + batch_size, len(contexts))

        context_batch = contexts[i:i_end]
        id_batch = [str(x) for x in range(i, i_end)]

        res = openai.embeddings.create(input=context_batch, model=model)
        embeds = [r.embedding for r in res.data]

        metadata = [{"context": x} for x in context_batch]

        to_upsert = zip(id_batch, embeds, metadata)
        index.upsert(vectors=list(to_upsert))

    return index.describe_index_stats()


def createVectorIndexForDataSet(index_name):
    if index_name is None:
        index_name = settings.index_name
    if index_name not in getVectorDbIndexesList():
        create_index_response = pc.create_index(
            name=index_name,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    print(f"Index created: {create_index_response}, PC: {pc}")
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)


def runDbMigrateDateSetToVectorDB():
    getVectorDbIndexesInformation()
    batch_size = 100

    for i in tqdm(range(0, len(contexts), batch_size)):
        i_end = min(i + batch_size, len(contexts))

        context_batch = contexts[i:i_end]
        id_batch = [str(x) for x in range(i, i_end)]

        res = openai.embeddings.create(input=context_batch, model=model)
        embeds = [r.embedding for r in res.data]

        metadata = [{"context": x} for x in context_batch]

        to_upsert = zip(id_batch, embeds, metadata)
        index.upsert(vectors=list(to_upsert))

    return index.describe_index_stats()


def search_vector_db(query):
    res = openai.embeddings.create(input=[query], model=model)
    query_embedding = res.data[0].embedding
    res = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    formatted_list = []
    for match in res.matches:
        context = match["metadata"]["context"]
        score = match.score
        formatted_list.append(f"[{round(score, 3)}]: {context}")
    return formatted_list


def semanticSearch(query: str):
    # pass a query into the vector db[pinecone],
    #  obviously first embeddibng it , then query
    # returns score based on top k[nearest vector in the vector space/place], with score and all[context to data]
    res = search_vector_db(query)
    print(f"Query Formatted Result: {res}")
    return res


if __name__ == "__main__":
    main()
