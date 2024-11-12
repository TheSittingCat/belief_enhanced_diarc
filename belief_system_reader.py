import re
from collections import defaultdict

def parse_pl_file(file_path):
    data = defaultdict(list)

    pattern = re.compile('(\w+)\(([^)]+)\)\.')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = re.sub(r'%.*', '', line).strip() # to remove comments and whitespace
                if line:
                    match = pattern.match(line)
                    if match:
                        predicate = match.group(1)
                        args = match.group(2).split(',') # needed to split args by comma
                        args = tuple(arg.strip() for arg in args)
                        data[predicate].append(args)
        
        return data
    except FileNotFoundError:
        print("file not found")
    except IOError:
        print("an error occured reading this file")

file_path = "agents.pl"
parsed_data = parse_pl_file(file_path)

print(parsed_data)
# each list corresponds to a set of relationships under the lists index (i.e "name"), and contains relations between two objects
# from here, we could potentially create a knowledge graph, or put into a database
# print(parsed_data["name"])
# print(parsed_data["admin"])
