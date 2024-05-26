# AIzaSyD9z6OKvCkOcmRep1Mnx2PgaJMv1AiIhHo
import numpy as np
import openai
import faiss
import nltk
from sentence_transformers import SentenceTransformer
import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


nltk.download('punkt')

# Load the pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Open the text file and read the content
with open('luke_skywalker_page.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Tokenize the content into sentences
sentences = nltk.sent_tokenize(content)

# Define the chunk size (number of sentences per chunk)
chunk_size = 5

# Create chunks of sentences
chunks = [sentences[i:i+chunk_size]
          for i in range(0, len(sentences), chunk_size)]

# Load the Faiss index
index = faiss.read_index('luke_skywalker_index.faiss')

# Sample question
question = "What are Luke Skywalker's abilities and powers?"

# Encode the question
question_embedding = model.encode([question]).reshape(1, -1)

# Perform similarity search
distances, indices = index.search(question_embedding, 3)

# Get the top 3 relevant chunks
top_chunks = []

for idx in indices[0]:
    chunk_text = ' '.join(chunks[idx])
    top_chunks.append(chunk_text)

context = "\n".join(top_chunks)

GOOGLE_API_KEY = "AIzaSyD9z6OKvCkOcmRep1Mnx2PgaJMv1AiIhHo"
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(question+"Context: "+context)
# to_markdown(response.text)
print(response.text)