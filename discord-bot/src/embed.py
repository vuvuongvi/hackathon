#import


import os

import sys
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)

def load_data():
    from pathlib import Path
    from llama_index import download_loader

    DocxReader = download_loader("DocxReader")
    loader = DocxReader()
    documents = loader.load_data(file=Path(path))

    return documents

def embedding(documents):
    index = VectorStoreIndex.from_documents(documents)
    index.set_index_id("vector_index")
    index.storage_context.persist("./storage")
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    # load index
    index = load_index_from_storage(storage_context, index_id="vector_index")

    return index

def agent_qa(path='../data/qa_dataset.docx')
    import os
    import sys
    
    documents = load_data(path)
    index = embedding(documents)
    query_engine = index.as_query_engine(response_mode="tree_summarize")

    return query_engine