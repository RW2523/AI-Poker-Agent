from pypokerengine.players import BasePokerPlayer
import random
import copy

class MinimaxPlayer(BasePokerPlayer):

    def __init__(self, depth=6):  # Default value for depth
        self.depth = depth

    def declare_action(self, valid_actions, hole_card, round_state):
        print("Round State:", round_state)  # Print round_state to inspect it
        print("Valid Actions:", valid_actions)  # Print valid_actions to check its structure
        
        best_action = None
        best_score = -float('inf')

        # Loop through the valid actions and evaluate them using the minimax algorithm
        for valid_action in valid_actions:
            print(f"Valid action being considered: {valid_action}")  # Inspect individual valid_action

            # Make sure valid_action is a dictionary before accessing it
            if isinstance(valid_action, dict):
                action = valid_action.get("action")  # Safely access 'action' from valid_action dictionary
                if action:
                    score = self.minimax(round_state, hole_card, action, self.depth, True)
                    if score > best_score:
                        best_score = score
                        best_action = action
            else:
                print("Unexpected valid_action format. Expected dictionary.")

        # Fallback to 'fold' if no best_action is found
        if best_action is None:
            best_action = "fold"
            print("No best action found, defaulting to 'fold'")

        return best_action  # Return the action with the best score

    def minimax(self, round_state, hole_card, valid_action, depth, maximizing_player):
        # Perform Minimax evaluation here
        print(f"Minimax evaluation: {valid_action} at depth {depth}")
        
        if depth == 0:
            return self.evaluate_state(round_state, hole_card, valid_action)
        
        # Simulate the next state
        sim_round_state = self.simulate_round(round_state, valid_action)
        score = None
        
        if maximizing_player:
            score = -float('inf')
            # Iterate over all valid actions and evaluate
            for valid_action in self.get_valid_actions(sim_round_state):
                score = max(score, self.minimax(sim_round_state, hole_card, valid_action["action"], depth - 1, False))
        else:
            score = float('inf')
            # Iterate over all valid actions and evaluate
            for valid_action in self.get_valid_actions(sim_round_state):
                score = min(score, self.minimax(sim_round_state, hole_card, valid_action["action"], depth - 1, True))
        
        return score

    def evaluate_state(self, round_state, hole_card, valid_action):
        # Evaluate the state based on your logic
        # For example, evaluate based on the player's hole cards, the community cards, and action taken
        return 0  # Placeholder: Replace with actual evaluation logic

    def simulate_round(self, round_state, valid_action):
        # Simulate the round with the selected action
        # Modify the round state based on the action taken
        sim_round_state = copy.deepcopy(round_state)
        # Apply action (simplified for now)
        # You can modify sim_round_state based on the action (e.g., adjusting pot, player stacks, etc.)
        sim_round_state["pot"]["main"]["amount"] += 10  # Example action simulation (raise amount)
        return sim_round_state

    def get_valid_actions(self, round_state):
        # Access the valid actions from the round state
        if "valid_actions" in round_state:
            return round_state["valid_actions"]
        else:
            print("Warning: 'valid_actions' not found in round_state")
            return []

    def evaluate_game_state(self, round_state, hole_card):
        """Evaluate the game state. Return a score representing the desirability of the state."""
        # Placeholder: simple evaluation, where 1 means win, -1 means loss, and 0 is neutral
        if self.is_winner(round_state):
            return 1  # Win
        elif self.is_loser(round_state):
            return -1  # Loss
        else:
            return 0  # Draw or neutral

    def is_game_over(self, round_state):
        """Returns whether the game has ended."""
        return round_state['street'] == 'showdown'

    def is_winner(self, round_state):
        """Returns whether the player is the winner."""
        return round_state.get('winner', None) == self.uuid

    def is_loser(self, round_state):
        """Returns whether the player is the loser."""
        return round_state.get('winner', None) != self.uuid

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return MinimaxPlayer(depth=6)