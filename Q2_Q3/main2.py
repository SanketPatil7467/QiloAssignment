import faiss
import nltk
from sentence_transformers import SentenceTransformer

# Download required NLTK data
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
chunks = [sentences[i:i+chunk_size] for i in range(0, len(sentences), chunk_size)]

# Initialize the Faiss index
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatIP(dimension)

# Process each chunk and store it in the Faiss index
for chunk in chunks:
    chunk_text = ' '.join(chunk)
    embedding = model.encode(chunk_text)
    index.add(embedding.reshape(1, -1))

# Save the Faiss index
faiss.write_index(index, 'luke_skywalker_index.faiss')
print("Faiss index saved to 'luke_skywalker_index.faiss'")