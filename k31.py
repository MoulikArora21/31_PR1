import random
lenstr = int(input("Length of the string of numbers: "))


rand_list = []
x = 0
for x in range(lenstr):
    rand_list.append(random.randint(1,4))

#rand_str = ''.join(str(x) for x in rand_list)

intturn = int(input("Choose 1 for P1, 0 for P2: "))
if intturn == 0:
    turn = False
else:
    turn = True

class Node:
    def __init__(self, child_value):
        self.value = child_value
        self.children = []
        self.heuristic = 0
        
    def add_node(self,child):
        self.children.append(child)


    def add_heuristic(self):
        hv = 0
        for values in self.value["StateString"] :
            if values%2 == 0:
                hv +=1

            if values%3 == 0 or values%4 == 0:
                hv +=1
        self.heuristic=hv
            
        

root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100})
print(root.value)


def calculate_score(curr_node,chosen_value,turn):
    x = curr_node.value.copy()
    y = curr_node.value["StateString"].copy()
    child = Node({"P1Score": x["P1Score"], "StateString":y, "P2Score": x["P2Score"]})

    if turn == True:
        if chosen_value%2 == 0:
            child.value["P1Score"] -= 2*chosen_value
        else:
            child.value["P2Score"] += chosen_value

    else:
        if chosen_value%2 == 0:
            child.value["P2Score"] -= 2*chosen_value
        else:
            child.value["P1Score"] += chosen_value

    y.remove(chosen_value)
    child.value["StateString"] = y

    curr_node.add_node(child)
    child.add_heuristic()
    return child



def generate_list(curr_node):
    global turn
    curr_list = curr_node.value["StateString"]

    if(len(curr_list) == 0):
        return
    

    
    avail_options = set(curr_node.value["StateString"])
    for i in (avail_options):

        if len(root.value["StateString"]) == len(curr_node.value["StateString"]):
            turn = turn
        else:
            turn = not turn

        child = calculate_score(curr_node,i,turn)
        print(child.value)
        print(child.heuristic)
        generate_list(child)
            

    return

generate_list(root) 