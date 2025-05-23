from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

model = SentenceTransformer("jhgan/ko-sroberta-multitask")


class CustomEmbeddingFunction(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = model.encode(
            texts,
            convert_to_tensor=False,
            normalize_embeddings=True,
        )
        return embeddings  # type: List[List[float]]
