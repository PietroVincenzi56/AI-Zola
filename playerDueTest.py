import math
import random


# Profondita di ricerca fissa. Puoi cambiarla senza toccare il resto del file.
SEARCH_DEPTH = 2

def evaluate_state(game, state, root_player): #vecchia versione

    """Valuta lo stato dal punto di vista di root_player."""
    winner = game.winner(state)
    if winner == root_player:
        return 50000000
    if winner == game.opponent(root_player):
        return -50000000
    if winner is not None:
        return 0

    opponent = game.opponent(root_player)
    player_powns = state.count(root_player) #numero di pedine del giocatore
    opp_powns = state.count(opponent)

    tot_player_moves = game._actions_for_player(state, root_player)
    tot_opp_moves = game._actions_for_player(state, opponent)


    player_mobility = len(tot_player_moves) #numero di mosse del giocatore
    opp_mobility = len(tot_opp_moves)


    player_captures = 0   
    opp_captures = 0
    for i in tot_player_moves:
        if (i[2]):
            player_captures += 1
    for i in tot_opp_moves:
        if (i[2]):
            opp_captures += 1


    # Calcoliamo la distanza accumulata (lower better), penalità per chi è ai bordi
    player_center_dist = 0
    opp_center_dist = 0    
    for r in range(state.size):
        for c in range(state.size):
            cell = state.board[r][c]
            if cell is None: continue
            
            # get_distance_level: 0 è il centro, valori alti sono i bordi
            dist = game.get_distance_level(r, c) #distanza dal centro
            pos_bonus = max(0, (state.size // 2) - dist)
            
            if cell == root_player:
                player_center_dist += pos_bonus
            else:
                opp_center_dist += pos_bonus

    center_score = 0.5 * (player_center_dist - opp_center_dist)


    if opp_powns <4 and player_powns >= 2 : #direi di lasciarla cosi
       return 34 *(player_powns - opp_powns) + (player_mobility - opp_mobility) + player_captures - 3*opp_captures + 0.5*center_score - 2*opp_mobility

    return 13 *(player_powns - opp_powns) + (player_mobility - opp_mobility) + 1.5*(player_captures-opp_captures) + center_score
   
    

def alphabeta(game, state, depth, alpha, beta, maximizing_player, root_player):
    legal_moves = game.actions(state)
    if depth == 0 or game.is_terminal(state) or not legal_moves:
        return evaluate_state(game, state, root_player), None

    best_moves = []

    if maximizing_player:
        value = -math.inf
        for move in legal_moves:
            child_state = game.result(state, move)
            child_value, _ = alphabeta(
                game,
                child_state,
                depth - 1,
                alpha,
                beta,
                False,
                root_player,
            )

            if child_value > value:
                value = child_value
                best_moves = [move]
            elif child_value == value:
                best_moves.append(move)

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, random.choice(best_moves) if best_moves else None

    value = math.inf
    for move in legal_moves:
        child_state = game.result(state, move)
        child_value, _ = alphabeta(
            game,
            child_state,
            depth - 1,
            alpha,
            beta,
            True,
            root_player,
        )

        if child_value < value:
            value = child_value
            best_moves = [move]
        elif child_value == value:
            best_moves.append(move)

        beta = min(beta, value)
        if alpha >= beta:
            break

    return value, random.choice(best_moves) if best_moves else None


def playerStrategy(game, state, timeout=3):
    """Strategia di esempio: alpha-beta con profondita fissa SEARCH_DEPTH."""
    legal_moves = game.actions(state)
    if not legal_moves:
        return None

    _, best_move = alphabeta(
        game,
        state,
        SEARCH_DEPTH,
        -math.inf,
        math.inf,
        True,
        state.to_move,
    )
    return best_move
