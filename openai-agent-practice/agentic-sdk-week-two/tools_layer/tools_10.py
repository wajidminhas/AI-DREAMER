


from openai import OpenAI
from agents import tool
from configuration_layer.db_config import get_db_connection
from configuration_layer.config import groq_client
import os

# Client specifically for embedding calls
# openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def query_pgvector(query_text: str, top_k: int = 2) -> str:
    """Generates embeddings and queries PostgreSQL using cosine distance (<=>)."""
    # 1. Transform text query into dense vector space
    embedding_response = groq_client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_embedding = embedding_response.data[0].embedding

    # 2. Query DB via vector math operator
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Using 1 - (embedding <=> query) to expose similarity scores
            sql = """
                SELECT id, content, 1 - (embedding <=> %s::vector) AS similarity
                FROM documentation_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """
            cur.execute(sql, (query_embedding, query_embedding, top_k))
            rows = cur.fetchall()
            
            if not rows:
                return "The vector database search returned no matching results."
                
            formatted_chunks = []
            for row in rows:
                formatted_chunks.append(
                    f"[Chunk {row['id']} | Similarity: {row['similarity']:.2f}]\n{row['content']}"
                )
            return "\n\n".join(formatted_chunks)
    except Exception as e:
        return f"Tool execution failed on internal database scan: {str(e)}"
    finally:
        conn.close()

@tool
def semantic_knowledge_retrieval(search_query: str) -> str:
    """
    Queries the central PostgreSQL database using vector embeddings to retrieve 
    contextual architectural limits, endpoint layouts, or infrastructure details.

    Args:
        search_query: An optimized semantic keyword phrase or sentence formulated by the agent.
    """
    print(f"\n[Tool Execution] Agent executed vector search with query: '{search_query}'")
    return query_pgvector(query_text=search_query)