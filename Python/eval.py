from openai import OpenAI
import read_kg_data
from tqdm import tqdm

def load_client() : 
    client = OpenAI() # Load the OpenAI client
    return client

def get_answer(client, prompt) : 
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature = 0,
    )
    message = completion.choices[0].message.content
    return message # return the GPT response to the question

def exact_match_accuracy(preds, targets) : 
    correct = 0
    for i in range(len(preds)) : 
        if preds[i] == targets[i] : 
            correct += 1
    return correct / len(preds)

def jaccard_index(preds, targets) : # Jaccard index is the intersection over the union of the predicted and target sets
    jaccard = 0
    for i in range(len(preds)) : 
        pred_set = set(preds[i])
        target_set = set(targets[i])
        if len(pred_set.union(target_set)) == 0 : 
            jaccard += 1
        else :
            jaccard += len(pred_set.intersection(target_set)) / len(pred_set.union(target_set))
    return jaccard / len(preds)

def partial_match_accuracy(preds, targets) : # Partial match accuracy is the percentage of the target that is in the prediction
    correct = 0
    for i in range(len(preds)) : 
        pred_set = set(preds[i])
        target_set = set(targets[i])
        if len(target_set) != 0 :
            correct += len(pred_set.intersection(target_set)) / len(target_set) # The percentage of the target that is in the prediction, if all of the target is in the prediction, this will be 1 and equal to exact match accuracy
        else : 
            if len(pred_set) == 0 : 
                correct += 1 # If the target is empty and the prediction is empty, then the prediction is correct
    return correct / len(preds)

def create_prompt(question) : 
    instruction_prompt = "Given the following environment description and the current belief state, generate the commands that the agent can add to its belief system in the format of a list of beliefs. Here is an example of the format: ['add , cookbook , inventory, in' , delete , cookbook , table , on'] where the first term specifies the add or delete actions, the second and third terms are the nodes, and the final node is the connection between them. Note that it is possible to have a single node in the action or the target belief list can be empty if no new action can be taken that is not in the belief system. " 
    return_instruction = "Return the list of actions that the agent can take in the format of a list of actions and NOTHING ELSE."
    environment_description = question["observation"]
    belief_state = question["previous_triplets"]
    prompt = f"{instruction_prompt} Environment Description: {environment_description} Belief State: {belief_state} {return_instruction}"
    return prompt

def parse_abstract_tree(x) : 
    import ast # Import the abstract syntax tree module
    try : 
        return ast.literal_eval(x) #
    except :
        return []

if __name__ == "__main__" : 
    client = load_client()
    questions = read_kg_data.read_all_kg_data("Data/KG/valid_dataset.json")
    questions_easy, questions_medium, questions_hard = read_kg_data.split_kg_data_by_difficulty(questions, "all")
    questions_easy = questions_easy.iloc[:200] # Test on the 200 easiest questions
    questions_medium = questions_medium.iloc[:200] # Test on the 200 medium questions
    questions_hard = questions_hard.iloc[:200] # Test on the 200 hardest questions
    prompts_easy = questions_easy.apply(create_prompt, axis=1)
    prompts_medium = questions_medium.apply(create_prompt, axis=1)
    prompts_hard = questions_hard.apply(create_prompt, axis=1)
    answers = [get_answer(client, prompt) for prompt in tqdm(prompts_easy)] 
    targets = list(questions_easy["target_commands"]) # Convert the target commands to a list
    print("The easy exact match accuracy is:")
    preds = [parse_abstract_tree(answer) for answer in tqdm(answers)] # Convert the predicted commands to a list
    print(exact_match_accuracy(preds, targets))
    print("The easy partial match accuracy is:")
    print(partial_match_accuracy(preds, targets))
    print("The easy Jaccard index is:")
    print(jaccard_index(preds, targets))

    answers = [get_answer(client, prompt) for prompt in tqdm(prompts_medium)]
    targets = list(questions_medium["target_commands"])
    print("The medium exact match accuracy is:")
    preds = [parse_abstract_tree(answer) for answer in tqdm(answers)]
    print(exact_match_accuracy(preds, targets))
    print("The medium partial match accuracy is:")
    print(partial_match_accuracy(preds, targets))
    print("The medium Jaccard index is:")
    print(jaccard_index(preds, targets))

    answers = [get_answer(client, prompt) for prompt in tqdm(prompts_hard)]
    targets = list(questions_hard["target_commands"])
    print("The hard exact match accuracy is:")
    preds = [parse_abstract_tree(answer) for answer in tqdm(answers)]
    print(exact_match_accuracy(preds, targets))
    print("The hard partial match accuracy is:")
    print(partial_match_accuracy(preds, targets))
    print("The hard Jaccard index is:")
    print(jaccard_index(preds, targets))