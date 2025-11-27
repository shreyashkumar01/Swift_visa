# 5. BUILD PROMPT

def build_prompt(user_query, documents):
    context = "\n\n".join([
        f"Chunk {i+1}:\n{doc.page_content}"
        for i, doc in enumerate(documents)
    ])

    return f"""
Use the following context to answer the user's question.
If information is not found in the context, say clearly: "The answer is not available in the documents."

----------------
CONTEXT:
{context}
----------------

USER QUESTION:
{user_query}

Final Answer:
"""