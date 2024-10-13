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

def store_in_vectordb(filename: str, transcription_data: dict):
    documents = []
    metadatas = []
    ids = []
    
    for segment in transcription_data.segments:
        document = segment.text
        metadata = {
            "filename": filename,
            "start_time": segment.start,
            "end_time": segment.end,
            "segment_id": segment.id
        }
        id = f"{filename}_segment_{segment.id}"

        documents.append(document)
        metadatas.append(metadata)
        ids.append(id)

    transcriptions_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Stored transcription segments for {filename} in the vector database.")

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
                    response_format="verbose_json",
                    timestamp_granularities=['segment']
                )
            transcriptions[filename] = transcription
            # Store the transcription in the vector database
            store_in_vectordb(filename, transcription)

    return transcriptions

def search_transcriptions(query: str, n_results: int = 5):
    results = transcriptions_collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    formatted_results = []
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        formatted_results.append({
            "text": doc,
            "filename": metadata['filename'],
            "start_time": metadata['start_time'],
            "end_time": metadata['end_time']
        })
    
    return formatted_results

if __name__ == "__main__":
    # results = get_transcription()
    a = search_transcriptions('how to see existing user')
    print(a)
    
