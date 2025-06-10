from utils.embedding_util import CustomEmbeddingFunction
from settings import CHROMA_HOST, CHROMA_PORT, CHROMA_COLLECTION_NAME
import chromadb

collection_name = "jhgan_ko-sroberta-multitask_250503"


def search_similar(query_sentence):
    collection = load_collection()
    result = collection.query(
        query_texts=[query_sentence],
        n_results=5,
        include=[
            "metadatas",
            "documents",
            "distances",
        ],
    )

    return postprocess(result)


def load_collection():
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    collection = chroma_client.get_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=CustomEmbeddingFunction(),
    )

    return collection


def preprocess():
    return 0


def postprocess(result):

    ids = result.get("ids")[0]
    metadatas = result.get("metadatas")[0]
    documents = result.get("documents")[0]
    distances = result.get("distances")[0]

    # for id_, document, distance in zip(ids, documents, distances):
    #     print(f"ID: {id_}, Document: {document}, Similarity: {1 - distance}")
    threshold = 0.40

    rows = [
        {
            "pred_id": id_,
            "pred_post_id": meta["post_id"],
            "pred_board_id": meta["board_id"],
            "pred_document": doc,
            "cosine_distance": dist,
            # "similarity": round(1 - dist, 6),
            # cosine은 1-dist가 맞는데 euclidean은 애매함
        }
        for id_, meta, doc, dist in zip(ids, metadatas, documents, distances)
        if dist <= threshold
    ]

    return rows
