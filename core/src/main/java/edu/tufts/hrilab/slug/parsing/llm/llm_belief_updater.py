from pyTRADE.core.wrapper import TRADEWrapper
from ai.thinkingrobots.trade import TRADE
from jpype import JImplements, JOverride, JClass
from edu.tufts.hrilab.slug.parsing.llm import LLMBeliefUpdater
from openai import OpenAI
import easygui
import re
import ast
import time

@JImplements(LLMBeliefUpdater)
class LLMBeliefUpdater : 
    def __init__(self):
        self.path_to_belief = "core/src/main/resources/config/edu/tufts/hrilab/belief/llm"
        self.client = OpenAI()
    
    @JOverride
    def ReturnInput(self, belief_path = None) : 
        if belief_path is None:
            belief_path = self.path_to_belief
        belief_name = easygui.enterbox("Enter the name of the belief file to update")
        self.path_to_belief = belief_path + "/" + belief_name + ".pl"

        prompt = easygui.enterbox("Enter the prompt to update the belief file")

        return prompt
    
    @JOverride
    def ReadBelief(self, belief_path = None) : 
        belief_list_formatted = []
        if belief_path is None:
            belief_path = self.path_to_belief
        try :
            with open(belief_path, 'r') as file:
                while line := file.readline():
                    try : 
                        match = re.match(r'(\w+)\(([^)]+)\)', line)
                        if match : 
                            name = match.group(1) # name of the belief
                            args = match.group(2).split(",") # arguments of the belief

                            belief_list_formatted.append(args + [name]) # add the belief to the list
                    except ValueError : 
                        print("Can't parse belief: " + line)
                        return None
        except FileNotFoundError : 
            print("File not found: " + belief_path)
            return None
        return belief_list_formatted
    
    @JOverride 
    def UpdateBelief(self, belief_path = None, belief = None) :
        prompt = self.ReturnInput()

        if belief_path is None:
            belief_path = self.path_to_belief
        if belief is None:
            belief = self.ReadBelief(belief_path)

        prefix = "Given the following environment description and the current belief state, generate the commands that the agent can add to its belief system in the format of a list of beliefs. Here is an example of the format: ['add , cookbook , inventory, in' , delete , cookbook , table , on'] where the first term specifies the add or delete actions, the second and third terms are the nodes, and the final node is the connection between them. Note that it is possible to have a single node in the action or the target belief list can be empty if no new action can be taken that is not in the belief system.  Environment Description: "
        postfix = "Current Belief State: " + str(belief)

        prompt = prefix + prompt + postfix

        completion = self.client.chat.completions.create(
            model = "ft:gpt-4o-mini-2024-07-18:personal::AZxpeOEh",
            messages = [
                {
                    "role" : "user",
                    "content" : prompt
                }
            ],
            temperature = 0,
        )
        message = completion.choices[0].message.content

        try : 
            message = ast.literal_eval(message)
        except : 
            print("Can't parse message: " + message)
        
        if message == [] : 
            return message
        else : 
            for i in range(len(message)) : # For each message in the list, add or delete the belief
                print(message[i])
                list_term = [s.strip() for s in message[i].split(",")]
                print(list_term)
                if list_term[0] ==  "add" :  # If the first term is add
                    belief.append(list_term[1:]) # Add the belief to the list
                elif list_term[0] == "delete" : # If the first term is delete
                    try : 
                        belief.remove(message[i][1:])
                    except ValueError : 
                        print("Can't remove belief as it does not exist: " + message[i][1:])
        
        with open(belief_path, "w+") as file : 
            for belief_single in belief : 
                if (belief_single[-1] + "(" + ",".join(belief_single[:-1]) + ")\n") not in file : 
                    file.write(belief_single[-1] + "(" + ",".join(belief_single[:-1]) + ")\n")
        
        print("Belief updated")
        print(belief)
        return belief
    

if __name__ == "__main__" :
    wrapper = TRADEWrapper()
    beliefupdater = LLMBeliefUpdater()
    TRADE.registerAllServices(beliefupdater, "")
    time.sleep(1)
    print(TRADE.getAvailableServices())
    wrapper.call_trade("UpdateBelief",)
    #beliefupdater.UpdateBelief()