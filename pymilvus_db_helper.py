import json, time
from pymilvus import MilvusClient
import streamlit as st
import numpy as np

CLUSTER_ENDPOINT = st.secrets["DB_CLUSTER_ENDPOINT"] # Set your cluster endpoint
TOKEN = st.secrets["DB_TOKEN"] # Set your token
COLLECTION_NAME = st.secrets["DB_COLLECTION_NAME"]  # Set your collection name

# 1. Initialize a MilvusClient instance
# Replace uri and API key with your own
client = MilvusClient(
    uri=CLUSTER_ENDPOINT, # Cluster endpoint obtained from the console
    token=TOKEN # API key or a colon-separated cluster username and password
)

def create_collection(collection_name):
    # Create a collection
    client.create_collection(collection_name=collection_name,dimension=1536,auto_id=True) # Create
    
def describe_collection(collection_name):
    res = client.describe_collection(collection_name=collection_name)
    return res

def insert(data,collection_name):
    # Insert a single entity
    res = client.insert(
        collection_name=collection_name,
        data=data
    )
    return res

def empty_collection(collection_name):
    # Empty the collection
    client.delete(collection_name=collection_name, pks=0)

def search(vector,output_fields,filter,collection_name,limit=10):
    response = client.search(
    collection_name=collection_name,
    data=vector,
    filter=filter,
    output_fields=output_fields,
    limit=limit)
    titles,texts = [],[]
    for db_response_item in response[0]:
        titles.append(db_response_item["entity"]["title"])
        texts.append(db_response_item["entity"]["text"])

    return titles,texts

if __name__ == '__main__':
    create_collection(COLLECTION_NAME)
    """
    
    data={  "id": 0, 
            "title": "The Reported Mortality Rate of Coronavirus Is Not Important", 
            "text": "The Reported Mortality Rate of Coronavirus Is Not Important",
            "namespace" : "rm",
            "vector": np.random.rand(1536).tolist() }
    res = insert(data,COLLECTION_NAME)
    data={  "id": 1, 
            "title": "The Reported Mortality Rate of Coronavirus Is Not Important", 
            "text": "The Reported Mortality Rate of Coronavirus Is Not Important",
            "namespace" : "rm",
            "vector": np.random.rand(1536).tolist() }
    res = insert(data,COLLECTION_NAME)
    data={  "id": 2, 
            "title": "The Reported Mortality Rate of Coronavirus Is Not Important", 
            "text": "The Reported Mortality Rate of Coronavirus Is Not Important",
            "namespace" : "rm",
            "vector": np.andom.rand(1536).tolist() }
    res = insert(data,COLLECTION_NAME)
    data={  "id": 3, 
            "title": "The Reported Mortality Rate of Coronavirus Is Not Important", 
            "text": "The Reported Mortality Rate of Coronavirus Is Not Important",
            "namespace" : "rm2",
            "vector": np.random.rand(1536).tolist() }
    res = insert(data,COLLECTION_NAME)
    data={  "id": 4, 
            "title": "The Reported Mortality Rate of Coronavirus Is Not Important", 
            "text": "The Reported Mortality Rate of Coronavirus Is Not Important",
            "namespace" : "rm2",
            "vector": np.random.rand(1536).tolist() }
    res = insert(data,COLLECTION_NAME)
    """
    output_fields=["title","text","namespace"]
    namespace = ["dragon_ball.pdf","one_punch_man.pdf"]
    filter=f'namespace  in {namespace}'
    db_response = search([np.random.rand(1536).tolist()],output_fields,filter,COLLECTION_NAME)
    titles,texts = db_response[0],db_response[1]
    context = ".".join(texts)
    print(context)