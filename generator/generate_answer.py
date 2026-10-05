import os

from langchain_groq import ChatGroq
from dotenv import load_dotenv


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()


# --------------------------------
# LLM
# --------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# --------------------------------
# Generate answer
# --------------------------------

def generate_answer(question, documents):

    # Build context
    context_parts = []

    for i, document in enumerate(
        documents,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {i}

Title:
{document["title"]}

URL:
{document["source"]}

Content:
{document["text"]}
"""
        )

    context = "\n".join(
        context_parts
    )

    # --------------------------------
    # Prompt
    # --------------------------------

    prompt = f"""
You are a technical documentation assistant.

Answer the user's question using ONLY the
provided documentation context.

If the answer cannot be found in the context,
say:

"I could not find this information in the
provided documentation."

Do not make up information.

Give a clear and concise technical answer.

User Question:
{question}

Documentation Context:
{context}

Answer:
"""

    # --------------------------------
    # Generate response
    # --------------------------------

    response = llm.invoke(prompt)

    return response.content