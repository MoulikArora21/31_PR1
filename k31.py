import random
lenstr = int(input("Length of the string of numbers: "))


rand_list = []
x = 0
for x in range(lenstr):
    rand_list.append(random.randint(1,4))

#rand_str = ''.join(str(x) for x in rand_list)

intturn = int(input("Choose 1 for P1, 0 for P2: "))

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
            
        

root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100, "Depth": 1})
print(root.value)


def calculate_score(curr_node,chosen_value):
    x = curr_node.value.copy()
    y = curr_node.value["StateString"].copy()

    child = Node({"P1Score": x["P1Score"], "StateString":y, "P2Score": x["P2Score"], "Depth":x["Depth"]})
    child.value["Depth"]+=1


    if intturn == 1:  
        if (len(curr_node.value["StateString"])%2 == len(root.value["StateString"])%2):
            turn = True
        else:
            turn = False
    else:
        if (len(curr_node.value["StateString"])%2 == len(root.value["StateString"])%2):
            turn = False
        else:
            turn = True



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
    return child


depth = 1

def generate_list(curr_node):
    global turn
    global depth

    
    curr_list = curr_node.value["StateString"]

    if(len(curr_list) == 0):
        return
    

    
    avail_options = set(curr_node.value["StateString"])
    for i in (avail_options):
            

        child = calculate_score(curr_node,i)
        print(child.value)
        if (child.value["Depth"]> 3):
            return

        generate_list(child)
    return

generate_list(root) 


def minmax(root):
    for w in root.children:
        for x in w.children:
            for y in x.children:
                y.add_heuristic()
                print(y.value , y.heuristic)

    for w in root.children:
        for x in w.children:
            for y in x.children:
                maxh = 0
                if y.heuristic>maxh:
                    maxh = y.heuristic
            x.heuristic = maxh
            print(x.value, x.heuristic)

minmax(root)