import read_kg_data
import eval
from tqdm import tqdm
import json
import pandas as pd

def prepare_training_data(path) : 
    data = read_kg_data.read_all_kg_data(path) # Read all KG data
    easy_data, medium_data, hard_data = read_kg_data.split_kg_data_by_difficulty(data, "graph_updates") # Split the KG data by the difficulty
    easy_data = easy_data.iloc[:600] # Test on the 200 easiest questions
    medium_data = medium_data.iloc[:300] # Test on the 200 medium questions
    hard_data = hard_data.iloc[:100] # Test on the 200 hardest questions
    return easy_data, medium_data, hard_data

def get_targets(data) : 
    return list(data["target_commands"]) # Convert the target commands to a lists

def data_to_json(data, name = "train_data.json") : 
    questions = list(data.apply(eval.create_prompt, axis=1)) # Create the prompts
    targets = get_targets(data) # Get the targets
    with open(name, 'w') as f:
        for i in tqdm(range((len(questions)))) : 
            message = {"messages" : [{"role" : "user", "content" : questions[i]}, {"role" : "assistant", "content" : str(targets[i])}]}
            json.dump(message, f)
            f.write("\n")
    print("The data has been saved to a jsonl file")

if __name__ == "__main__" :
    easy_data, medium_data, hard_data = prepare_training_data("Data/KG/train_dataset.json") # Prepare the training data
    combined_data = pd.concat([easy_data, medium_data, hard_data], ignore_index=True) # Combine the data
    data_to_json(combined_data, "Data/KG/training_data_belief_updates.json") # Save the data to a jsonl file