# alpha_beta_Reversi_game
This program will simulate an agent playing Reversi (https://en.wikipedia.org/wiki/Reversi). The agent with which my program will compete will be an agent playing randomly (i.e. in each situation, it should choose 1 move from available moves, assigning the same probability to each of them).

alpha_beta.py: strong evaluation function used where the search depth is too great, without sorting possible moves by heuristic function value  
alpha_beta_without_sort.py: strong evaluation function used in each max_alpha_beta call, with sorting possible moves using heuristic function  
basic_aplha_beta.py: simple evaluation function  

To compile:``python basic_alpha_beta.py``, ``python alpha_beta.py`` or ``python alpha_beta_without_sort.py``
