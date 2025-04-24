from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from mcts_player import MCTSPlayer
from minimax_player import MinimaxPlayer
from hybrid_player import HybridPlayer
from hyb import HybridPlayer1

def simulate_games(num_games=100):
    hybrid1_wins = 0
    hybrid2_wins = 0

    for _ in range(num_games):
        config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)
        config.register_player(name="Hybrid_Agent1", algorithm=HybridPlayer1())
        config.register_player(name="Hybrid_Agent2", algorithm=HybridPlayer())
        
        game_result = start_poker(config, verbose=0)

        # Check which player has more stack at the end
        stacks = {p['name']: p['stack'] for p in game_result['players']}
        if stacks["Hybrid_Agent1"] > stacks["Hybrid_Agent2"]:
            hybrid1_wins += 1
        elif stacks["Hybrid_Agent2"] > stacks["Hybrid_Agent1"]:
            hybrid2_wins += 1
        # Tie not counted toward any win

    print(f"Out of {num_games} games:")
    print(f"Hybrid_Agent1 won {hybrid1_wins} times.")
    print(f"Hybrid_Agent2 won {hybrid2_wins} times.")
    print(f"Ties: {num_games - hybrid1_wins - hybrid2_wins}")

if __name__ == "__main__":
    simulate_games()
