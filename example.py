# from pypokerengine.api.game import setup_config, start_poker
# from Player1 import Player1
# from raise_player import RaisedPlayer


# #TODO:config the config as our wish
# config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)



# config.register_player(name="Player1", algorithm=Player1())
# config.register_player(name="Player2", algorithm=Player2())


# game_result = start_poker(config, verbose=1)
from pypokerengine.api.game import setup_config, start_poker
from raise_player import RaisedPlayer
from randomplayer import RandomPlayer
from mcts_player import MCTSPlayer
from minimax_player import MinimaxPlayer
from hybrid_player import HybridPlayer
from hyb import HybridPlayer1
from gem import MCTSPlayer
from nor import StrategicPokerPlayer

def simulate_games(num_games=10):
    hybrid1_wins = 0
    hybrid2_wins = 0

    for _ in range(num_games):
        config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)
        # config.register_player(name="Player1", algorithm=HybridPlayer1())
        # config.register_player(name="Player2", algorithm=RandomPlayer())
        config.register_player(name="Player1", algorithm=RandomPlayer())
        config.register_player(name="Player2", algorithm=StrategicPokerPlayer())
        
        game_result = start_poker(config, verbose=0)

        # Check which player has more stack at the end
        stacks = {p['name']: p['stack'] for p in game_result['players']}
        if stacks["Player1"] > stacks["Player2"]:
            hybrid1_wins += 1
        elif stacks["Player2"] > stacks["Player1"]:
            hybrid2_wins += 1
        # Tie not counted toward any win

    print(f"Out of {num_games} games:")
    print(f"Player1 won {hybrid1_wins} times.")
    print(f"Player2 won {hybrid2_wins} times.")
    print(f"Ties: {num_games - hybrid1_wins - hybrid2_wins}")

if __name__ == "__main__":
    simulate_games()
