import random
import tkinter
import customtkinter


# UI System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("750x650")
app.title("Game")


# UI elements
title = customtkinter.CTkLabel(app,text = "Select Algorithm:", font = ("Courier New",20))
title.pack()

intalgo = None
lenstr = None
intturn = None
showp1text = None
showp2text = None
showp1 = None
showp2 = None
showroottxt = None
showstring = None
retrybutton = None
playbutton = None
win = None
def setalgo(choice):
    global intalgo
    if choice is "MinMax":
        intalgo = 1
        # print(intalgo)
    else:
        intalgo = 0
        # print(intalgo)

def set_lenstr(value):
    global lenstr
    lenstr = value
    txtlength.configure(text = value)
    # print(lenstr)


algo = customtkinter.CTkComboBox(app,values=["MinMax","AlphaBeta"], command=setalgo)
algo.set("Select")
algo.pack()

txtlengthask = customtkinter.CTkLabel(app,text="Select length of the string:", font = ("Courier New",20))
txtlengthask.pack()

lengthOfString = customtkinter.CTkSlider(app, from_=15, to=25, command= set_lenstr,number_of_steps=10)
lengthOfString.pack()

txtlength = customtkinter.CTkLabel(app,text="", font = ("Courier New",20))
txtlength.pack()

txtlengthturn = customtkinter.CTkLabel(app,text="Choose Turn:", font = ("Courier New",20))
txtlengthturn.pack()

intturn_var = tkinter.IntVar(value=0)

def set_intturn():
    global intturn
    intturn = intturn_var.get()
    print(intturn)

turnbutton1 = customtkinter.CTkRadioButton(app, text="Player", command = set_intturn, variable= intturn_var, value= 1, font = ("Courier New",20))
turnbutton2 = customtkinter.CTkRadioButton(app, text="Computer", command = set_intturn,variable= intturn_var, value= 0, font = ("Courier New",20))
turnbutton1.pack()
turnbutton2.pack()


def retryactivate():
    global retrybutton
    retrybutton = customtkinter.CTkButton(app,text= "Retry", command = resetgame, font = ("Courier New",20))
    retrybutton.place(x=300,y=600)

playeroptions = None
playerchoice = tkinter.IntVar()

# lenstr = int(input("Length of the string of numbers: "))






def startgame():
    global lenstr
    global intturn
    global intalgo
    rand_list = []
    x = 0
    for x in range(int(lenstr)):
        rand_list.append(random.randint(1,4))

    #rand_str = ''.join(str(x) for x in rand_list)

    # intturn = int(input("Choose 1 for Your Turn, 0 for Computer's Turn: "))
    # intalgo= int(input("Choose 1 for MinMax, 0 for AlphaBeta"))


    class Node:
        def __init__(self, child_value):
            self.value = child_value
            self.children = []
            self.heuristic = 0
            self.evaluated = False

            
        def add_node(self,child):
            self.children.append(child)


        def add_heuristic(self):
            global intturn
            hv = 0
            # print(f"Calculating heuristic for {self.value}")
            if self.value["StateString"]:
                for values in self.value["StateString"] :
                    if values%2 == 0:
                        hv +=1

                    if values%3 == 0 or values%4 == 0:
                        hv +=1
                if intturn == 1:
                    dif = self.value["P2Score"] - self.value["P1Score"] 
                    hv+=dif*1.5
                else:
                    dif = self.value["P2Score"] - self.value["P1Score"] 
                    hv+=dif*1.5
                self.heuristic=hv
                # print(f"Assigned heuristic {hv} to {self.value}")
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
                # print(f"Terminal heuristic {self.heuristic} to {self.value}")
            
                
    global showp1text
    global showp2text
    global showp1
    global showp2
    global showroottxt
    global showstring        

    root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100, "Depth": 1})
    print(root.value)

    showp1text = customtkinter.CTkLabel(app,text="Player Score:", font = ("Courier New",20))
    showp1text.place(x = 80, y=400 )
    # showp1text.pack()

    showp1 = customtkinter.CTkLabel(app,text=root.value["P1Score"], font = ("OCR A Extended",25))
    showp1.place(x= 120,y=430)


    showp2text = customtkinter.CTkLabel(app,text="Computer Score:", font = ("Courier New",20))
    showp2text.place(x = 450, y=400 )

    showp2 = customtkinter.CTkLabel(app,text=root.value["P2Score"], font = ("OCR A Extended",25))
    showp2.place(x= 520,y=430)


    if showroottxt is None:
        showroottxt = customtkinter.CTkLabel(app,text="Randomly generated string:", font = ("Courier New",20))
        showroottxt.pack()
    else:
        showroottxt.configure(text="Randomly generated string:", font = ("Courier New",20))

    


    if showstring is None:
        showstring = customtkinter.CTkLabel(app,text=root.value["StateString"], font = ("OCR A Extended",25))
        showstring.pack()
    else:
        showstring.configure(text=root.value["StateString"], font = ("OCR A Extended",25))


    def calculate_score(curr_node,chosen_value):
        global intturn
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
    global max_depth

    max_depth =4

    def generate_list(curr_node):
        global turn
        global max_depth

        if curr_node is None:
            return
        
        curr_list = curr_node.value["StateString"]

        if(len(curr_list) == 0):
            return
        
        if (curr_node.value["Depth"] > max_depth ):
            return
        
        avail_options = set(curr_node.value["StateString"])

        if not avail_options:
            return
        for i in (avail_options):
                

            child = calculate_score(curr_node,i)
            # print(child.value)


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
            if not node.children:
                node.add_heuristic()
                return
            for w in node.children:
                if not w.children:
                    w.add_heuristic()
                else:
                    for x in w.children:
                        if not x.children:
                            x.add_heuristic()
                        else:
                            maxh = -float('inf')
                            for y in x.children:
                                if y.heuristic>maxh:
                                    maxh = y.heuristic
                            x.heuristic = maxh
                    # print("maximizing",x.value , x.heuristic)
                    maxh2 = float('inf')
                    for x in w.children:
                        if x.heuristic<maxh2:
                            maxh2 = x.heuristic
                    w.heuristic = maxh2
                # print("minimizing",w.value , w.heuristic)
            maxh3 = -float('inf')
            for w in node.children:
                if w.heuristic>maxh3:
                    maxh3 = w.heuristic
            node.heuristic = maxh3
            # print("maximizing",node.value , node.heuristic)
        else: 
            if not node.children:
                node.add_heuristic()
                return
            for w in node.children:
                if not w.children:
                    w.add_heuristic()
                else:
                    for x in w.children:
                        maxh = float('inf')
                        for y in x.children:
                            if not x.children:
                                x.add_heuristic()
                            else:
                                if y.heuristic < maxh:
                                    maxh = y.heuristic
                        x.heuristic = maxh
                        # print("minimizing",x.value, x.heuristic)
                    maxh2 = -float('inf')
                    for x in w.children:
                        if x.heuristic > maxh2:
                            maxh2 = x.heuristic
                    w.heuristic = maxh2
                    # print("maximizing",w.value, w.heuristic)
            maxh3 = float('inf')
            for w in node.children:
                if w.heuristic < maxh3:
                    maxh3 = w.heuristic
            node.heuristic = maxh3
            # print("minimizing",node.value , node.heuristic)
                            

    def minmax(node,root):
        print("Executing Minmax")
        add_heuristic_to_leaves(node) # step 2
        propagate(node,root)  

    


    def computer_move(node):
        global win
        if win is not None:
            win.destroy()
        # print(f"Current state: {node.value}")
        # print(f"Children: {[(child.value,node.heuristic) for child in node.children]}")
        if (node.value["StateString"] == []):
            if node.value["P1Score"] > node.value["P2Score"]:
                win=customtkinter.CTkLabel(app, text = "Player Wins!", font = ("Courier New",20))
                win.place(x=290,y=550)
                print("Player Wins!")
            elif node.value["P1Score"] < node.value["P2Score"]:
                win=customtkinter.CTkLabel(app, text = "Computer Wins!", font = ("Courier New",20))
                win.place(x=290,y=550)
                print("Computer Wins!")
                
            else:
                win=customtkinter.CTkLabel(app, text = "Draw!", font = ("Courier New",20))
                win.place(x=300,y=550)
                print("Draw!")
            return None

        if node.children == None:
            return None


        bestmove = None
        bestheur = -float("inf")
        for x in node.children:
            if x.heuristic>bestheur:
                bestheur = x.heuristic
                bestmove = x

        # for options in node.children:
        #      if options.heuristic==bestheur:
        #         print(options.value)
        showp1.configure(text=bestmove.value["P1Score"])
        showp2.configure(text=bestmove.value["P2Score"])
        showstring.configure(text = bestmove.value["StateString"])
        print(bestmove.value)
        return bestmove
    
    

    def setoption(value):
        global playerchoice
        playerchoice.set(int(value))
            
    def player_move(node):
        global playerchoice
        global playeroptions
        global win
        if win is not None:
            win.destroy()
        if (node.value["StateString"] == []):
            playeroptions.set("") 
            # if win:
            #     win.destroy() 
            if node.value["P1Score"] > node.value["P2Score"]:
                win=customtkinter.CTkLabel(app, text = "Player Wins!", font = ("Courier New",20))
                win.place(x=290,y=550)
                print("Player Wins!")
            elif node.value["P1Score"] < node.value["P2Score"]:
                win=customtkinter.CTkLabel(app, text = "Computer Wins!", font = ("Courier New",20))
                win.place(x=290,y=550)
                print("Computer Wins!")
                
            else:
                win=customtkinter.CTkLabel(app, text = "Draw!", font = ("Courier New",20))
                win.place(x=300,y=550)
                print("Draw!")
            
            return None

        if node.children == None:
            return None
        # print("Choose a number")
        # playerchoice = int(input())
        

        if playeroptions is None: 
            playeroptions = customtkinter.CTkComboBox(app,values=[str(v) for v in set(node.value["StateString"])],command=setoption)
            playeroptions.set("Select")
            playeroptions.pack()
        else:
            playeroptions.configure(values=[str(v) for v in set(node.value["StateString"])])
            playeroptions.set("Select")
        app.wait_variable(playerchoice)

        

        choice = playerchoice.get()

        temp_list = node.value["StateString"].copy()
        temp_list.remove(choice)
        chosen_node = None
        for x in node.children:
            if (temp_list == x.value["StateString"]):

                print(x.value)
                showp1.configure(text=x.value["P1Score"])
                showp2.configure(text=x.value["P2Score"])
                showstring.configure(text = x.value["StateString"])
                return x

    def generate_further(node,root):
        global max_depth
        global intturn
        max_depth +=4
        generate_list(node)
        minmax(node,root)
        return node

    actual_root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100, "Depth": 1})
    if intalgo == 1:
        if intturn == 1 :
            while root is not None or root.value["StateString"] != [] or root.children !=[] or x.children !=[]:

            # x = player_move(root)
            # if (x == None or x.value["StateString"] == []):
            #     break
            # y = computer_move(x)
            # if (y == None or y.value["StateString"] == []):
            #     break
            # z = player_move(y)
            # a = generate_further(z,actual_root)
            # if (a == None or a.value["StateString"] == []):
            #     break
            # w = computer_move(a)
            # if (w == None or w.value["StateString"] == []):
            #     break
            # root = w



                x = player_move(root)
                if x is None:
                    break
                elif not x.children:
                    a = generate_further(x,actual_root)
                    x = a
                    root = a
                    continue
                root = computer_move(x)
                if root is None:
                    break
                elif not root.children:
                    a = generate_further(root,actual_root)
                    root = a


        else:
            while root is not None or root.value["StateString"] != [] or root.children !=[] or x.children !=[]:
        #     x = computer_move(root)
        #     # if (x == None or x.value["StateString"] == []):
        #     #     break
        #     y = player_move(x)
        #     if (y == None or y.value["StateString"] == []):
        #         break
            
        #     a = generate_further(y,actual_root)
        #     if (a == None or a.value["StateString"] == []):
        #         break
        #     z = computer_move(a)
        #     w = player_move(z)
        #     root = w

        
                x = computer_move(root)

                if x is None:
                    break
                elif not x.children:
                    a = generate_further(x,actual_root)
                    x = a
                    root = a
                    continue

                root = player_move(x)
                if root is None:
                    break
                elif not root.children:
                    a = generate_further(root,actual_root)
                    root = a

    else:
        # n = 0
        # def go_to_depth(node,d):
        #     global n
        #     if node is not None and node.children and node.value["Depth"]< d:
        #         return go_to_depth(node.children[n],d)       
        #     else:
        #         if node.evaluated == True:
        #             n+=1
        #             go_to_depth(node.children[n],d)
        #         else:
        #             node.add_heuristic()
        #             node.evaluated = True
        #             return node
    
        # generate_list(actual_root)

        # def propagate_up(node):
        #     global alpha
        #     global beta
        #     allchildren_evaluated = True
        #     parent_node = go_to_depth(node,node.value["Depth"]-1)
        #     for children in parent_node.children:
        #         allchildren_evaluated = allchildren_evaluated and children.evaluated
        #     if allchildren_evaluated is True:
        #         if len(parent_node.value["StateString"])%2 == len(actual_root.value["StateString"])%2: #Maximizer
        #             max_heur = -float("inf")
        #             for children in parent_node.children:
        #                 if children.heuristic > max_heur:
        #                     max_heur = children.heuristic
        #                     print(max_heur)
        #             parent_node.heuristic = max_heur
        #             parent_node.evaluated = True
        #             print(parent_node.heuristic)
        #         else:
        #             min_heur = float("inf")
        #             for children in parent_node.children:
        #                 if children.heuristic < min_heur:
        #                     min_heur = children.heuristic
        #                     print(min_heur)
        #             parent_node.heuristic = min_heur
        #             parent_node.evaluated = True
        #             print(parent_node.heuristic)


        #     else:
        #         if len(parent_node.value["StateString"])%2 == len(actual_root.value["StateString"])%2: #Beta Level
        #             max_heur = -float("inf")
        #             for children in parent_node.children:
        #                 if children.evaluated == True:
        #                     if children.heuristic > max_heur:
        #                         max_heur = children.heuristic
        #                         print(max_heur)
        #             if max_heur != -float("inf"):
        #                 alpha = max_heur
        #                 print(alpha)
        #                 if beta is not None:
        #                     if alpha>=beta:
        #                         parent_node.add_heuristic(alpha)
        #                         alpha = None
        #                     else:
        #                         go_to_depth(parent_node,parent_node.value["Depth"])

        #         else: #Alpha level
        #             min_heur = float("inf")
        #             for children in parent_node.children:
        #                 if children.evaluated == True:
        #                     if children.heuristic < min_heur:
        #                         min_heur = children.heuristic
        #                         print(min_heur)
        #             if min_heur != float("inf"):
        #                 beta = min_heur
        #                 print(beta)
        #                 if alpha is not None:
        #                     if beta <= alpha:
        #                         parent_node.add_heuristic(beta)
        #                         beta= None
        #                     else:
        #                         go_to_depth(parent_node,parent_node.value["Depth"])



        def alphabeta(node, alpha, beta):
            print("Executing Alpha Beta")
            if not node.children:
                node.add_heuristic()
                node.evaluated = True
                return node.heuristic

            if len(node.value["StateString"])%2 == len(actual_root.value["StateString"])%2:
                max_heu = -float("inf")
                for child in node.children:
                    heu = alphabeta(child, alpha, beta)
                    max_heu = max(max_heu, heu)
                    alpha = max(alpha, heu)
                    if beta <= alpha:
                        break
                node.heuristic = max_heu
                node.evaluated = True
                return max_heu
            else:
                min_heu = float("inf")
                for child in node.children:
                    heu = alphabeta(child, alpha, beta)
                    min_heu = min(min_heu, heu)
                    beta = min(beta, heu)
                    if beta <= alpha:
                        break
                node.heuristic = min_heu
                node.evaluated = True
                return min_heu

    def generate_further2(node,root):
        global max_depth
        max_depth +=4
        generate_list(node)
        alphabeta(node, -float("inf"), float("inf"))
        return node

    actual_root = Node({"P1Score": 100, "StateString": rand_list, "P2Score": 100, "Depth": 1})
    if intturn == 1 :
        while root is not None or root.value["StateString"] != [] or root.children !=[] or x.children !=[]:
                x = player_move(root)
                if x is None:
                    break
                elif not x.children:
                    a = generate_further2(x,actual_root)
                    x = a
                    root = a
                    continue
                root = computer_move(x)
                if root is None:
                    break
                elif not root.children:
                    a = generate_further2(root,actual_root)
                    root = a


    else:
            while root is not None or root.value["StateString"] != [] or root.children !=[] or x.children !=[]:
                x = computer_move(root)

                if x is None:
                    break
                elif not x.children:
                    a = generate_further2(x,actual_root)
                    x = a
                    root = a
                    continue

                root = player_move(x)
                if root is None:
                    break
                elif not root.children:
                    a = generate_further2(root,actual_root)
                    root = a
    retryactivate()


def selection():
    global playbutton
    if  playbutton is None:
        playbutton = customtkinter.CTkButton(app,text = "Play", command = startgame, font = ("Courier New",20))
        playbutton.pack()
    else:
        
        playbutton.configure(text = "Play", command = startgame, font = ("Courier New",20))
selection()
def resetgame():
    global showp1text
    global showp2text
    global showp1
    global showp2
    global showroottxt
    global showstring
    global retrybutton 
    global playeroptions
    global win
    showp1text.configure(text = "")
    showp2text.configure(text = "")
    showp1.configure(text = "")
    showp2.configure(text = "")
    showroottxt.configure(text = "")
    showstring.configure(text = "")

    if retrybutton:
        retrybutton.destroy()
        retrybutton = None
    if playeroptions:
        playeroptions.destroy()
        playeroptions = None
    if win:
        win.destroy() 
        win = None

    selection()



# Run App
app.mainloop()