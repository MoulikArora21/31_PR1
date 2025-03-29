import random
lenstr = int(input("Length of the string of numbers: "))


rand_list = []
x = 0
for x in range(lenstr):
    rand_list.append(random.randint(1,4))

#rand_str = ''.join(str(x) for x in rand_list)

intturn = int(input("Choose 1 for Your Turn, 0 for Computer's Turn: "))

class Node:
    def __init__(self, child_value):
        self.value = child_value
        self.children = []
        self.heuristic = 0

        
    def add_node(self,child):
        self.children.append(child)


    def add_heuristic(self):
        hv = 0
        if (self.value["StateString"] != []):
            for values in self.value["StateString"] :
                if values%2 == 0:
                    hv +=1

                if values%3 == 0 or values%4 == 0:
                    hv +=1
            if intturn == 1:
                dif = self.value["P2Score"] - self.value["P1Score"] 
                hv+=dif
            else:
                dif = self.value["P2Score"] - self.value["P1Score"] 
                hv+=dif
            self.heuristic=hv
        else:
            if((self.value["P1Score"] - self.value["P2Score"]) < 0):
                if intturn == 1:
                    self.heuristic = -1
                else:
                    self.heuristic = 1
            elif(self.value["P1Score"] - self.value["P2Score"] == 0):
                self.heuristic = 0
            else:
                if intturn ==1:
                    self.heuristic = 1
                else:
                    self.heuristic = -1
        
            
        

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
    # print(f"From: {curr_node.value}")
    # print(f"Chosen Value: {chosen_value}, Turn: {'P1' if turn else 'P2'}")
    # print(f"Current Node: {curr_node.value}, Generated Child Node: {child.value}")



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


max_depth =4

def generate_list(curr_node):
    global turn
    global max_depth

    
    curr_list = curr_node.value["StateString"]

    if(len(curr_list) == 0):
        return
    

    
    avail_options = set(curr_node.value["StateString"])
    for i in (avail_options):
            

        child = calculate_score(curr_node,i)
        # print(child.value)
        if (child.value["Depth"] > max_depth ):
            return

        generate_list(child)
        # print(f"Current Node: {curr_node.value}, Generated Child Node: {child.value}")

    return

generate_list(root) 


def add_heuristic_to_leaves(root):
    for w in root.children:
        for x in w.children:
            for y in x.children:
                y.add_heuristic()
                # print(y.value , y.heuristic)


def propagate(node,root):
    if (len(node.value["StateString"])%2 == len(root.value["StateString"])%2):
        for w in node.children:
            for x in w.children:
                maxh = -float('inf')
                for y in x.children:
                    if y.heuristic>maxh:
                        maxh = y.heuristic
                x.heuristic = maxh
                #print(x.value , x.heuristic)
            maxh2 = float('inf')
            for x in w.children:
                if x.heuristic<maxh2:
                    maxh2 = x.heuristic
            w.heuristic = maxh2
            #print(w.value , w.heuristic)
        maxh3 = -float('inf')
        for w in node.children:
            if w.heuristic>maxh3:
                maxh3 = w.heuristic
        node.heuristic = maxh3
        # print(root.value , root.heuristic)
    else:
        for w in node.children:
            for x in w.children:
                maxh = float('inf')
                for y in x.children:
                    if y.heuristic<maxh:
                        maxh = y.heuristic
                x.heuristic = maxh
                #print(x.value , x.heuristic)
            maxh2 = -float('inf')
            for x in w.children:
                if x.heuristic>maxh2:
                    maxh2 = x.heuristic
            w.heuristic = maxh2
            #print(w.value , w.heuristic)
        maxh3 = float('inf')
        for w in node.children:
            if w.heuristic<maxh3:
                maxh3 = w.heuristic
        node.heuristic = maxh3
                        

def minmax(node,root):
    add_heuristic_to_leaves(node) # step 2
    propagate(node,root)  

minmax(root,root)


def computer_move(node):
    # if (node.value["StateString"] == []):
    #     return None

    # if node.children == None:
    #     return None

    bestmove = None
    bestheur = -float("inf")
    for x in node.children:
        if x.heuristic>bestheur:
            bestheur = x.heuristic
            bestmove = x

    for options in node.children:
         if options.heuristic==bestheur:
            print(options.value, options.heuristic)
    return bestmove
    
        
def player_move(node):
    # if (node.value["StateString"] == []):
    #     return None

    # if node.children == None:
    #     return None
    print("Choose a number")
    choice = int(input())
    temp_list = node.value["StateString"].copy()
    temp_list.remove(choice)
    chosen_node = None
    for x in node.children:
        if (temp_list == x.value["StateString"]):
            print(x.value)
            return x

def generate_further(node,root):
    global max_depth
    max_depth +=4
    generate_list(node)
    print(node.value, node.children[0])
    minmax(node,root)
    return node

actual_root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100, "Depth": 1})
if intturn == 1:
    while root.value["StateString"] != [] or root!= None:
        x = player_move(root)
        if (x == None or x.value["StateString"] == []):
            break
        y = computer_move(x)
        if (y == None or y.value["StateString"] == []):
            break
        z = player_move(y)
        a = generate_further(z,actual_root)
        w = computer_move(a)
        if (w == None or w.value["StateString"] == []):
            break
        root = w

else:
    while root.value["StateString"] != [] and root!= None:
        x = computer_move(root)
        # if (x == None or x.value["StateString"] == []):
        #     break
        y = player_move(x)
        # if (y == None or y.value["StateString"] == []):
        #     break
        z = computer_move(y)
        a = generate_further(z,actual_root)
        w = player_move(a)
        root = w

