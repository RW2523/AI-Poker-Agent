from pypokerengine.players import BasePokerPlayer
import random as rand

class StrategicPokerPlayer(BasePokerPlayer):

    def evaluate_hand(self, hole_card, round_state):
        # Convert string cards like 'D3' into dicts like {'suit': 'D', 'rank': '3'}
        parsed_cards = [{"suit": card[0], "rank": card[1:]} for card in hole_card]
        
        print("Parsed Hole Cards:", parsed_cards)

        ranks = [card["rank"] for card in parsed_cards]
        suits = [card["suit"] for card in parsed_cards]

        # Check for pairs
        if ranks[0] == ranks[1]:
            return "pair"

        # Check for suited cards
        if suits[0] == suits[1]:
            return "suited"

        return "off-suit"
        
    def declare_action(self, valid_actions, hole_card, round_state):
        from pprint import pprint

        print("\n=== DEBUG INFO ===")
        print("Hole Cards:", hole_card)
        print("Valid Actions:", valid_actions)
        print("Round State:")
        pprint(round_state)

        ranks = [card[1] for card in hole_card]
        suits = [card[0] for card in hole_card]
        high_cards = ['A', 'K', 'Q', 'J']
        has_high_card = any(rank in high_cards for rank in ranks)
        is_suited = suits[0] == suits[1]

        # If the player has a high card or suited cards, consider raising
        if has_high_card or is_suited:
            for action in valid_actions:
                if action["action"] == "raise":
                    min_raise = action.get("amount", {}).get("min")
                    if min_raise is not None:
                        return {"action": "raise", "amount": min_raise}

        # If the only valid actions are fold, call, or raise, determine which one to take
        for action in valid_actions:
            if action["action"] == "check":
                # Only check if the pot has not been raised and it is the right moment to do so
                if round_state["pot"]["main"]["amount"] == 30:  # Example check for no raise yet
                    return {"action": "check"}

        for action in valid_actions:
            if action["action"] == "call":
                # Calculate the call amount based on the current pot size and stack
                call_amount = round_state["pot"]["main"]["amount"] - round_state["seats"][round_state["big_blind_pos"]]["stack"]
                if call_amount > 0:
                    return {"action": "call", "amount": call_amount}
                else:
                    # If no amount to call, just check
                    return {"action": "check"}

        return {"action": "fold"}  # Default action if no valid action is found

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
    return StrategicPokerPlayer()