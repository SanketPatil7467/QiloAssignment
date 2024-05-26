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
chunks = [sentences[i:i+chunk_size]
          for i in range(0, len(sentences), chunk_size)]

# Load the Faiss index
index = faiss.read_index('luke_skywalker_index.faiss')

# Sample question
question = "What are Luke Skywalker's abilities and powers?"
# question = "Name movies in which Luke Skywalker's is present?"
# question = "who is Luke Skywalker?"



# Encode the question
question_embedding = model.encode([question]).reshape(1, -1)

# Perform similarity search
distances, indices = index.search(question_embedding, 3)

# Get the top 3 relevant chunks
top_chunks = []
for idx in indices[0]:
    chunk_text = ' '.join(chunks[idx])
    top_chunks.append(chunk_text)

# Print the top 3 relevant chunks
print("Top 3 relevant chunks for the question:")
for chunk in top_chunks:
    print(chunk)
    print()
