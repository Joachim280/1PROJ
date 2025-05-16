from coordinates import Coordinates

def calculate_move(x, y, directions, max_steps, board):
    """Calcule les mouvements avec obstacles"""
    moves = []
    for dx, dy in directions:
        for step in range(1, max_steps + 1):
            new_x = x + dx * step
            new_y = y + dy * step
            coord = Coordinates(new_x, new_y)
            
            if not board.is_valid(new_x, new_y):
                break
                
            if board.is_occupied(coord):
                break
                
            moves.append(coord)
    return moves

def is_enemy_line(coord, player):
    """Vérifie si la coordonnée est sur la ligne adverse"""
    return (player.color == "white" and coord.y == 7) or (player.color == "black" and coord.y == 0)