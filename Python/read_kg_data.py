import pandas as pd

def read_all_kg_data(path) : # Read all KG data from the json files
    kg_data = pd.read_json(path, lines=True) # Lines true is to avoid the ValueError: Trailing data
    return kg_data

def split_kg_data(kg_data, length) : # Split the KG data by either the length of the data or ratio
    if length < 1 :
        data = kg_data.sample(frac=length)
        return data
    else : 
        data = kg_data.sample(frac = 1) # Shuffle the data
        data = kg_data[:length]
        return data

def split_kg_data_by_difficulty(kg_data, difficulty) : # Split the KG data by the difficulty
    if difficulty == "env_length" : 
        easy_data = kg_data[kg_data["observation"].str.len() < 50] # Easy data
        medium_data = kg_data[(50 <= kg_data["observation"].str.len()) & (kg_data["observation"].str.len() < 100)] # Medium data
        hard_data = kg_data[100 <= kg_data["observation"].str.len()] # Hard data
        easy_data = easy_data.reset_index(drop=True)
        medium_data = medium_data.reset_index(drop=True)
        hard_data = hard_data.reset_index(drop=True)
        return easy_data, medium_data, hard_data
    elif difficulty == "graph_updates" : 
        easy_data = kg_data[kg_data["target_commands"].apply(len) < 3]
        medium_data = kg_data[(3 <= kg_data["target_commands"].apply(len)) & (kg_data["target_commands"].apply(len) < 7)]
        hard_data = kg_data[7 <= kg_data["target_commands"].apply(len)]
        return easy_data, medium_data, hard_data
    elif difficulty == "all" :
        easy_data = kg_data[(kg_data["observation"].str.len() < 50) & (kg_data["target_commands"].apply(len) < 3)]
        medium_data = kg_data[(50 <= kg_data["observation"].str.len()) & (kg_data["observation"].str.len() < 100) & (3 <= kg_data["target_commands"].apply(len)) & (kg_data["target_commands"].apply(len) < 7)]
        hard_data = kg_data[100 <= kg_data["observation"].str.len() & (7 <= kg_data["target_commands"].apply(len))]
        return easy_data, medium_data, hard_data   

# if __name__ == "__main__" : 
#     kg_data = read_all_kg_data("Data/KG/valid_dataset.json") # Read all KG data
#     print("The number of data points:")
#     print(len(kg_data))
#     easy_data, medium_data, hard_data = split_kg_data_by_difficulty(kg_data, "all") # Split the KG data by the difficulty
#     print("The number of easy data points With Respect to Environment Length:")
#     print(len(easy_data))
#     print("The number of medium data points With Respect to Environment Length::")
#     print(len(medium_data))
#     print("The number of hard data points With Respect to Environment Length::")
#     print(len(hard_data))