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
        self.path_to_belief = "core/src/main/resources/config/edu/tufts/hrilab/belief"
        self.client = OpenAI()
    
    @JOverride
    def ReturnInput(self, belief_path = None) : 
        if belief_path is None:
            belief_path = self.path_to_belief
        belief_name = easygui.enterbox("Enter the name of the belief file to update")
        if re.match(r'.*\.pl', belief_name) is None : # If the file does not have a .pl extension, add it
            belief_name = belief_name + ".pl" 
        
        if re.match(r'.*\.pl', self.path_to_belief) is None or (belief_name not in self.path_to_belief): # If the path is already determined
            self.path_to_belief = belief_path + "/" + belief_name

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
                            args = [args.strip() for args in args] # remove whitespace

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
            model = "ft:gpt-4o-mini-2024-07-18:link-lab::AZvFKi2Y",
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
            pattern = r"\[(.*?)\]"
            match = re.search(pattern, message)
            message = match.group(0)
            message = ast.literal_eval(message)
            print("Message: " + str(message))
        except : 
            print("Can't parse message: " + message)
        
        if message == [] : 
            return message
        else : 
            for i in range(len(message)) : # For each message in the list, add or delete the belief
                print(message[i])
                list_term = [s.strip() for s in message[i].split(",")]
                print(list_term)
                if len(list_term) < 2 : 
                    list_term = message # If the message is a single belief, add it to the list, this is due to an error on LLM side
                if list_term[0] ==  "add" :  # If the first term is add
                    if list_term[1:] not in belief :
                        belief.append(list_term[1:]) # Add the belief to the list
                elif list_term[0] == "delete" : # If the first term is delete
                    try : 
                        belief.remove(list_term[1:])
                    except ValueError : 
                        print("belief:" + str(belief[2]))
                        print("Can't remove belief as it does not exist: " + str(list_term[1:]))

        belief_str_box = str(belief)
        choice = easygui.choicebox("Do you want to update the belief system with the following beliefs: " + belief_str_box, choices = ["Yes", "No"])
        if choice == "Yes" :
            with open(belief_path, "w+") as file : 
                for belief_single in belief : 
                    if (belief_single[-1] + "(" + ",".join(belief_single[:-1]) + ")\n") not in file : 
                        file.write(belief_single[-1] + "(" + ",".join(belief_single[:-1]) + ").\n")
            
            easygui.msgbox("Belief updated")
        else : 
            easygui.msgbox("Belief Revereted, You Can Always Try a new Prompt!")
        return str(belief)
    

if __name__ == "__main__" :
    wrapper = TRADEWrapper()
    beliefupdater = LLMBeliefUpdater()
    TRADE.registerAllServices(beliefupdater, "")
    time.sleep(1)
    #print(TRADE.getAvailableServices())
    try_again = True
    while try_again : # This is used for calling the TRADE Service directly, if you want to just register it, comment this area out and keep the program running.
        wrapper.call_trade("UpdateBelief",)
        choice = easygui.choicebox("Continue the Execution?", choices = ["Yes", "No"])
        if choice == "No" : 
            try_again = False