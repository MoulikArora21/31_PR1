import random

# --- Input Section ---
lenstr = int(input("Length of the string of numbers: "))
rand_list = [random.randint(1, 4) for _ in range(lenstr)]
intturn = int(input("Choose 1 for Your Turn, 0 for Computer's Turn: "))

# Determine which side the computer plays.
# If intturn == 1 then the player goes first (as P1) and the computer is P2.
# If intturn == 0 then the computer goes first (as P1).
computer_is_player1 = (intturn == 0)

# --- GameNode Class ---
class GameNode:
    def _init_(self, child_value):
        self.value = child_value  # A dictionary holding scores, state list, depth, and turn flag.
        self.children = []
        self.heuristic = 0

    def add_node(self, child):
        self.children.append(child)

    def add_heuristic(self):
        hv = 0
        # If there are still moves available, compute a heuristic based on the remaining numbers and score differences.
        if self.value["StateString"]:
            for val in self.value["StateString"]:
                if val % 2 == 0:
                    hv += 1
                if val % 3 == 0 or val % 4 == 0:
                    hv += 1
            # Adjust by the score difference. (Heuristic = P2Score - P1Score)
            hv += self.value["P2Score"] - self.value["P1Score"]
            self.heuristic = hv
        else:
            # Terminal state evaluation.
            if (self.value["P1Score"] - self.value["P2Score"]) < 0:
                self.heuristic = -1 if intturn == 1 else 1
            elif (self.value["P1Score"] - self.value["P2Score"]) == 0:
                self.heuristic = 0
            else:
                self.heuristic = 1 if intturn == 1 else -1

# --- Initialization ---
# Set up the initial game state with an explicit turn flag.
# "isPlayerTurn" is True if it’s P1's turn, False if it’s P2's turn.
initial_turn = True if intturn == 1 else False
root = GameNode({"P1Score": 100,"StateString": rand_list.copy(),"P2Score": 100,"Depth": 1,"isPlayerTurn": initial_turn})
print("Initial State:", root.value)

# Global variable for depth cutoff.
max_depth = 4

# --- Tree Generation and Move Application ---
def calculate_score(curr_node, chosen_value):
    # Copy the current state's dictionary and update it for the new child.
    new_state = curr_node.value.copy()
    new_state["StateString"] = curr_node.value["StateString"].copy()
    new_state["Depth"] = curr_node.value["Depth"] + 1
    # Flip the turn: the mover just moved, so now it’s the other side’s turn.
    new_state["isPlayerTurn"] = not curr_node.value["isPlayerTurn"]

    # Apply move effects based on whose turn it was in curr_node.
    if curr_node.value["isPlayerTurn"]:
        # P1's move.
        if chosen_value % 2 == 0:
            new_state["P1Score"] -= 2 * chosen_value
        else:
            new_state["P2Score"] += chosen_value
    else:
        # P2's move.
        if chosen_value % 2 == 0:
            new_state["P2Score"] -= 2 * chosen_value
        else:
            new_state["P1Score"] += chosen_value

    # Remove the chosen number from the list.
    new_state["StateString"].remove(chosen_value)
    child = GameNode(new_state)
    curr_node.add_node(child)
    return child

def generate_list(curr_node):
    """Recursively generate moves until the branch hits max_depth or no moves remain."""
    if not curr_node.value["StateString"]:
        return
    avail_options = set(curr_node.value["StateString"])
    for option in avail_options:
        child = calculate_score(curr_node, option)
        # Stop expanding this branch if the depth limit is reached.
        if child.value["Depth"] >= max_depth:
            continue
        generate_list(child)
    return

# --- Minimax Propagation ---
def minimax(node):
    # If this is a leaf node, compute and return its heuristic.
    if not node.children:
        node.add_heuristic()
        return node.heuristic
    # Recursively compute minimax values for children.
    child_values = [minimax(child) for child in node.children]
    # Decide whether to maximize or minimize based on whose turn is at this node.
    if node.value["isPlayerTurn"]:
        # When it’s P1's turn, choose the minimum value.
        node.heuristic = min(child_values)
    else:
        # When it’s P2's turn, choose the maximum value.
        node.heuristic = max(child_values)
    return node.heuristic

# --- Move Selection Functions ---
def computer_move(node):
    # Compute minimax values from the current node.
    minimax(node)
    best_move = None
    if node.children:
        if computer_is_player1:
            # Computer (P1) wants to minimize (since heuristic = P2Score - P1Score).
            best_value = float('inf')
            for child in node.children:
                if child.heuristic < best_value:
                    best_value = child.heuristic
                    best_move = child
        else:
            # Computer (P2) wants to maximize.
            best_value = -float('inf')
            for child in node.children:
                if child.heuristic > best_value:
                    best_value = child.heuristic
                    best_move = child
    print("Computer evaluating moves:")
    for child in node.children:
        print(child.value, "-> Heuristic:", child.heuristic)
    return best_move

def player_move(node):
    print("Available numbers:", node.value["StateString"])
    try:
        choice = int(input("Choose a number: "))
    except ValueError:
        print("Invalid input. Try again.")
        return None
    if choice not in node.value["StateString"]:
        print("Choice not available. Try again.")
        return None
    new_state = node.value["StateString"].copy()
    new_state.remove(choice)
    for child in node.children:
        if child.value["StateString"] == new_state:
            print("Player move:", child.value)
            return child
    print("No valid move found for that choice.")
    return None

def generate_further(node, root):
    global max_depth
    max_depth += 4  # Increase depth limit
    generate_list(node)
    minimax(root)
    return node

# --- Initial Tree Generation ---
generate_list(root)
minimax(root)

# Make a separate copy of the initial state for further expansion if needed.
actual_root = GameNode({
    "P1Score": 100,
    "StateString": rand_list.copy(),
    "P2Score": 100,
    "Depth": 1,
    "isPlayerTurn": initial_turn
})

# --- Game Loop ---
if intturn == 1:
    # Player goes first.
    while root is not None and root.value["StateString"]:
        x = player_move(root)
        if x is None or not x.value["StateString"]:
            break
        y = computer_move(x)
        if y is None or not y.value["StateString"]:
            break
        z = player_move(y)
        if z is None:
            break
        a = generate_further(z, actual_root)
        w = computer_move(a)
        if w is None or not w.value["StateString"]:
            break
        root = w
else:
    # Computer goes first.
    while root is not None and root.value["StateString"]:
        x = computer_move(root)
        if x is None or not x.value["StateString"]:
            break
        y = player_move(x)
        if y is None or not y.value["StateString"]:
            break
        z = computer_move(y)
        if z is None or not z.value["StateString"]:
            break
        a = generate_further(z, actual_root)
        w = player_move(a)
        if w is None:
            break
        root = w

print("Game over. Final state:", root.value if root else "No moves left.")