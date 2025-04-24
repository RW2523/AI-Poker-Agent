from pypokerengine.players import BasePokerPlayer
import random
import copy

class MCTSPlayer(BasePokerPlayer):
    def __init__(self, num_simulations=10000):
        self.num_simulations = num_simulations

    def declare_action(self, valid_actions, hole_card, round_state):
        best_score = -float('inf')
        best_action = valid_actions[0]["action"]  # default to fold

        for action_info in valid_actions:
            total_score = 0
            for _ in range(self.num_simulations):
                sim_round_state = copy.deepcopy(round_state)
                sim_hole_card = list(hole_card)

                reward = self.simulate_game(sim_round_state, sim_hole_card, action_info["action"])
                total_score += reward

            avg_score = total_score / self.num_simulations

            if avg_score > best_score:
                best_score = avg_score
                best_action = action_info["action"]

        return best_action

    def simulate_game(self, round_state, hole_card, chosen_action):
        # This is a simplified simulation that just returns a random score.
        # In a full MCTS implementation, you'd simulate the rest of the game.
        return random.uniform(-1, 1)  # placeholder for win/loss outcome

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
    return MCTSPlayer(num_simulations=10000)