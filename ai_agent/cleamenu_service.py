import requests
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex

from llama_index.core.vector_stores import MetadataFilters, MetadataFilter
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from llama_index.llms.openai import OpenAI

import os
import json

from ai_agent.utils.ai_utils import Utils

utils = Utils()
PINECONE_API_KEY = utils.get_pinecone_api_key()
OPENAI_API_KEY = utils.get_openai_api_key()
load_dotenv()


# LLM Initialization
openai_api_key = os.getenv("OPENAI_API_KEY")
cleamenu_data_service_url = os.getenv("CLEAMENU_DATA_SERVICE_URL")
llm = OpenAI(model="gpt-4o")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


utils = Utils()
INDEX_NAME = "mongo-from-code"

index = pinecone.Index(INDEX_NAME)


def update_price_api(storeId: str, itemId: str, new_price: float):
    url = f"{cleamenu_data_service_url}/{storeId}/items/{itemId}"
    # Create your header as required
    payload = {"price" : new_price}
    headers = {"content-type": "application/json"}

    try:
        response = requests.put(url, data=json.dumps(payload), headers=headers)

        if response.status_code >= 200 | response.status_code < 300:
            response = response.json()
            return response
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None




def vector_query(store_id: str, query: str):
    """Perform a vector search over an index.
    query (str): the string query to be embedded.
    """
    vector_store = PineconeVectorStore(
        pinecone_index=index
    )
    # Instantiate VectorStoreIndex object from your vector_store object
    vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)


    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="_id", value=store_id),
        ],
    )
    query_engine = vector_index.as_query_engine(filters=filters, include_metadata=True, include_values=False)
    chat_engine = vector_index.as_chat_engine(llm=llm, filters=filters, include_metadata=True)


    #response = chat_engine.chat(query)
    response = query_engine.query(query)
    print(response)
    print(response.metadata)
    return response.metadata




def update_price_of_existed_food(store_id: str, food_id: str, food_price: float):
    update_price_api(store_id, food_id, food_price)
    return f"Started changing the food {food_id} to {food_price}"
