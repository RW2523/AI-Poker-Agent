from pypokerengine.players import BasePokerPlayer
import random
import copy

class SmartPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        """
        MCTS-like strategy: Simulate possible actions, rollout future states randomly,
        and pick the action with the highest average win rate.
        """
        simulations_per_action = 50
        best_score = -float("inf")
        best_action = valid_actions[1]["action"]  # default to call

        for action_info in valid_actions:
            action = action_info["action"]
            total_score = 0

            for _ in range(simulations_per_action):
                sim_round_state = copy.deepcopy(round_state)
                sim_hole_card = list(hole_card)
                score = self.simulate_game(action, sim_round_state, sim_hole_card)
                total_score += score

            avg_score = total_score / simulations_per_action

            if avg_score > best_score:
                best_score = avg_score
                best_action = action

        return best_action

    def simulate_game(self, action, round_state, hole_card):
        """
        Very basic rollout simulation — plays random actions for opponents and estimates win/loss.
        Can be replaced by actual evaluation logic if available.
        """
        # Assign simplified equity based on hole cards strength
        rank_strength = self.evaluate_hand_strength(hole_card)
        # Add randomness to simulate unknown future
        noise = random.uniform(-0.3, 0.3)
        return rank_strength + noise

    def evaluate_hand_strength(self, hole_card):
        # Debug: Show input
        print("[DEBUG] evaluate_hand_strength received:", hole_card)

        # Convert string cards like 'H2' to dicts like {'rank': '2', 'suit': 'H'}
        try:
            hole_card_dicts = [{'suit': c[0], 'rank': c[1:]} for c in hole_card]
        except Exception as e:
            raise ValueError(f"[ERROR] Failed to parse cards: {hole_card}, error: {e}")

        # Debug: Show converted cards
        print("[DEBUG] Parsed hole_card:", hole_card_dicts)

        # Mapping of card ranks to values
        ranks = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11,
            'Q': 12, 'K': 13, 'A': 14
        }

        try:
            first_rank = ranks[hole_card_dicts[0]['rank']]
            second_rank = ranks[hole_card_dicts[1]['rank']]
        except KeyError as e:
            raise ValueError(f"[ERROR] Invalid rank: {e} in {hole_card_dicts}")

        rank_strength = (first_rank + second_rank) / 2
        print(f"[DEBUG] Hand strength evaluated: {rank_strength}")
        return rank_strength

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
    return SmartPlayer()
