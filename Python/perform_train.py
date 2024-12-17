import eval
import read_kg_data
import time
from openai import OpenAI

def upload_data(data) : 
    client = eval.load_client()
    filename = client.files.create(
        file = open(data, 'rb'),
        purpose="fine-tune"
    )
    return client, filename

def start_training(client, filename) : 
    client.fine_tuning.jobs.create(
        training_file=filename,
        model="gpt-4o-mini-2024-07-18",
        hyperparameters={
        "n_epochs" : 3,
        "batch_size" : 64,
        }
    )

if __name__ == "__main__" :
    client = OpenAI()
    #client, filename = upload_data("Data/KG/training_data_belief_updates.json")
    #time.sleep(80) # Wait for the file to upload and be processed
    start_training(client, "file-FpaZkSDjFEFaTV49jJnTy4") # The filename is the id of the file, potentially replace it with the filename variable
    print("The training has started, wait for the email to see the results")