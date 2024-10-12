import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import chromadb

# Load the environment variables from the .env file
load_dotenv()

api_key = os.getenv('W_KEY')
base_url = os.getenv('W_URL')
api_version = os.getenv('W_API_VERSION')

client = AzureOpenAI(
    api_version=api_version,
    api_key=api_key,
    base_url=base_url
)

# Create a persistent client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
transcriptions_collection = chroma_client.get_or_create_collection("transcriptions")

def store_in_vectordb(filename: str, text: str):
    transcriptions_collection.add(
        documents=[text],
        metadatas=[{"filename": filename}],
        ids=[filename]
    )

    print(f"Stored transcription for {filename} in the vector database.")

def get_transcription():
    data_dir = 'data'
    transcriptions = {}

    for filename in os.listdir(data_dir):
        if filename.endswith(('.mp3', '.wav', '.m4a', '.mp4')):
            file_path = os.path.join(data_dir, filename)
            print(file_path)
            with open(file_path, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper",
                    file=audio_file,
                    response_format="text"
                )
            transcriptions[filename] = transcription
            # Store the transcription in the vector database
            store_in_vectordb(filename, transcription)

    return transcriptions




# Example usage
if __name__ == "__main__":
    results = get_transcription()
    
