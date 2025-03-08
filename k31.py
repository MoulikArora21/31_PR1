import random
lenstr = int(input("Length of the string of numbers:"))


rand_list = []
x = 0
for x in range(lenstr):
    rand_list.append(random.randint(1,4))

rand_str = ''.join(str(x) for x in rand_list)

#child_value = [int, string, int]
class Node:
    def __init__(self, child_value):
        self.value = child_value
        self.children = []

    def add_node(self,child):
        self.children.append(child)

root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100})
print(root.value)


def calculate_score(curr_node,chosen_value):
    x = curr_node.value.copy()
    y = curr_node.value["StateString"].copy()
    child = Node({"P1Score": x["P1Score"], "StateString":y, "P2Score": x["P2Score"]})

    # if turn == True:
    if chosen_value%2 == 0:
        child.value["P1Score"] -= 2*chosen_value
    else:
        child.value["P2Score"] += chosen_value

    # else:
    #     if chosen_value%2 == 0:
    #         child.value["P2Score"] -= 2*chosen_value
    #     else:
    #         child.value["P1Score"] += chosen_value

    y.remove(chosen_value)
    child.value["StateString"] = y

    curr_node.add_node(child)
    return child



#turn = True

def generate_list(curr_node):
    #global turn
    if(curr_node == None):
        return

    curr_list = curr_node.value["StateString"]

    if(len(curr_list) == 0):
        return
    
    avail_options = set(curr_node.value["StateString"])
    for i in range(len(avail_options)):
        for option in list(avail_options):
            child = calculate_score(curr_node,option)
            generate_list(child)
            print(child.value)
        #turn = not turn
    return

generate_list(root)

print(root.children[0].value["StateString"])
    