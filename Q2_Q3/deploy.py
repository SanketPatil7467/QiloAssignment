import numpy as np
import chainlit as cl
import faiss
import nltk
from sentence_transformers import SentenceTransformer
import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
from credentials import GOOGLE_API_KEY as key


def returnTop3RelevantChunks(question):
    nltk.download('punkt')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open('luke_skywalker_page.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    sentences = nltk.sent_tokenize(content)
    chunk_size = 5
    chunks = [sentences[i:i+chunk_size]
            for i in range(0, len(sentences), chunk_size)]

    index = faiss.read_index('luke_skywalker_index.faiss')
    question_embedding = model.encode([question]).reshape(1, -1)
    distances, indices = index.search(question_embedding, 3)

    top_chunks = []
    for idx in indices[0]:
        chunk_text = ' '.join(chunks[idx])
        top_chunks.append(chunk_text)
    return top_chunks

def feedToLLM(question,relevant_chunks):
    context = "\n".join(relevant_chunks)
    genai.configure(api_key=key)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(question+"Remember thi is Context: "+context+".Now answer the question")
    return response.text

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    relevant_chunks = returnTop3RelevantChunks(str(message.content))
    output = feedToLLM(str(message.content), relevant_chunks)
    msg.content = output
    await msg.update()



@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"A new chat session has started!\nAsk me anything about Luke Skywalker",
    ).send()
