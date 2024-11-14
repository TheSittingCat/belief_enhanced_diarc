import json
import pandas as pd

def load_data(dataset_file):
    with open(dataset_file, 'r') as file:
        data = [json.loads(line) for line in file]

    df = pd.DataFrame(data)
    return df

def data_stats(df):
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("\nMissing Values:\n", df.isnull().sum())

    all_target_commands = [command for sublist in df['target_commands'] for command in sublist]
    unique_commands = list(set(all_target_commands))
    print("\nNum of unique target_commands:\n", len(unique_commands))
    return


test_df = load_data('test_dataset.json')
train_df = load_data('train_dataset.json')
valid_dataset = load_data('valid_dataset.json')

data_stats(test_df)
data_stats(train_df)
data_stats(valid_dataset)

# --------
# to parse thru the datasets to represent as a belief system
# --------
# iterate through every key in the dictionary
# for the previous tuples, you would represent them as relationships, where the 3rd part of the triplet 
# is the relationship name, and the other two parameters are a part of it
# ex) ["cookbook", "counter", "on"] --> on(cookbook, counter)
# target commands could be multiple singular relationships, i.e target_commands(pick_up)
# Not sure how we would convert the observation, worst case we just add it to a list of observation
# as a singular part in the pl file:
# ex) "You are carrying nothing." --> observation(You are carrying nothing.)

