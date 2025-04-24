from pypokerengine.players import BasePokerPlayer
import random
import copy
from treys import Card, Evaluator, Deck


class HybridPlayer1(BasePokerPlayer):
    def __init__(self, num_simulations=1000, depth=2, use_mcts=True):
        self.num_simulations = num_simulations
        self.depth = depth
        self.use_mcts = use_mcts
        self.evaluator = Evaluator()

    def declare_action(self, valid_actions, hole_card, round_state):
        if self.use_mcts:
            return self.mcts_declare_action(valid_actions, hole_card, round_state)
        else:
            return self.minimax_declare_action(valid_actions, hole_card, round_state)

    # === MCTS STRATEGY ===
    def mcts_declare_action(self, valid_actions, hole_card, round_state):
        best_score = -float('inf')
        best_action = valid_actions[0]

        for action_info in valid_actions:
            if action_info["action"] == "fold":
                best_action = action_info
                break  # No need to simulate, just fold if possible
            total_score = 0
            for _ in range(self.num_simulations):
                sim_round_state = copy.deepcopy(round_state)
                sim_hole_card = list(hole_card)

                reward = self.simulate_game(sim_round_state, sim_hole_card, action_info)
                total_score += reward

            avg_score = total_score / self.num_simulations
            if avg_score > best_score:
                best_score = avg_score
                best_action = action_info

        return best_action["action"], best_action.get("amount", 0)

    def simulate_game(self, round_state, hole_card, chosen_action):
        sim_state = self.simulate_round(round_state, chosen_action)
        win_chance = self.simulate_win_rate(hole_card, sim_state.get("community_card", []), 30)
        return win_chance - self.calculate_action_cost(chosen_action, round_state)

    # === MINIMAX STRATEGY ===
    def minimax_declare_action(self, valid_actions, hole_card, round_state):
        best_score = -float('inf')
        best_action = valid_actions[0]

        for action_info in valid_actions:
            score = self.minimax(round_state, hole_card, action_info, self.depth, True)
            if score > best_score:
                best_score = score
                best_action = action_info

        return best_action["action"], best_action.get("amount", 0)

    def minimax(self, round_state, hole_card, action_info, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_state(round_state, hole_card, action_info)

        sim_round_state = self.simulate_round(round_state, action_info)
        actions = self.get_valid_actions(sim_round_state)
        if not actions:
            return self.evaluate_state(sim_round_state, hole_card, action_info)

        scores = []
        for next_action in actions:
            score = self.minimax(sim_round_state, hole_card, next_action, depth - 1, not maximizing_player)
            scores.append(score)

        return max(scores) if maximizing_player else min(scores)

    def evaluate_state(self, round_state, hole_card, action_info):
        community_cards = round_state.get("community_card", [])
        win_rate = self.simulate_win_rate(hole_card, community_cards, num_simulations=100)
        pot_odds = self.calculate_pot_odds(round_state)
        cost = self.calculate_action_cost(action_info, round_state)

        utility = win_rate - cost + pot_odds * 0.5
        return utility

    def simulate_win_rate(self, hole_card, community_card, num_simulations=100):
        win, tie = 0, 0
        try:
            deck = Deck()
            known_cards = [Card.new(c[1].lower() + c[0].lower()) for c in hole_card + community_card]
            for c in known_cards:
                if c in deck.cards:
                    deck.cards.remove(c)

            for _ in range(num_simulations):
                deck_copy = copy.deepcopy(deck)
                opponent_hand = deck_copy.draw(2)
                needed_community = 5 - len(community_card)
                remaining = deck_copy.draw(needed_community) if needed_community > 0 else []

                player_cards = [Card.new(c[1].lower() + c[0].lower()) for c in hole_card]
                community_cards = [Card.new(c[1].lower() + c[0].lower()) for c in community_card] + remaining

                player_score = self.evaluator.evaluate(community_cards, player_cards)
                opponent_score = self.evaluator.evaluate(community_cards, opponent_hand)

                if player_score < opponent_score:
                    win += 1
                elif player_score == opponent_score:
                    tie += 1

            return (win + 0.5 * tie) / num_simulations
        except:
            return 0.5  # fallback if evaluation fails

    def calculate_pot_odds(self, round_state):
        try:
            pot = round_state["pot"]["main"]["amount"]
            current = round_state["betting"]["current"]["amount"]
            return current / pot if pot else 0
        except:
            return 0

    def calculate_action_cost(self, action_info, round_state):
        if "amount" in action_info:
            return action_info["amount"]["amount"] / (round_state.get("pot", {}).get("main", {}).get("amount", 1) + 1)
        return 0

    def simulate_round(self, round_state, action_info):
        sim_state = copy.deepcopy(round_state)
        if "pot" in sim_state and "main" in sim_state["pot"]:
            sim_state["pot"]["main"]["amount"] += action_info.get("amount", {}).get("amount", 10)
        return sim_state

    def get_valid_actions(self, round_state):
        return round_state.get("valid_actions", [])

    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, round_state): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass


def setup_ai():
    return HybridPlayer1(num_simulations=300, depth=2, use_mcts=True)
