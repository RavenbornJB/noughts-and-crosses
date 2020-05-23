from board import Board
import random
import time


class Game:
    """Represents a game of Noughts and Crosses (or Tic-Tac-Toe, duh...)"""

    def __init__(self):
        """
        Initializes the game with a board.
        """
        self._board = Board()

    def get_turn(self):
        """
        Returns which player currently is to move.
        Player 1 == "X", player 2 == "O"
        :return: Any[1, 2]
        """
        return 1 if self._board.get_turn() % 2 == 1 else 2

    def player_move(self):
        """
        Algorithm for executing player's move.

        Returns a tuple of the coordinates of the move.
        :return: tuple(int, int)
        """
        while True:
            coords = (input("Enter row (0, 1, or 2) : "),
                      input("Enter column (0, 1, or 2) : "))
            if coords[0] in ["0", "1", "2"] and coords[1] in ["0", "1", "2"]:
                coords = tuple(map(int, coords))
                if coords in self._board.free_cells():
                    self._board.move(coords, player=1)
                    return coords
            print("Invalid coordinates.\n")

    def ai_move(self):
        """
        Algorithm for executing AI's move.
        Minimax algorithm will be implemented for the AI,
        but for now it moves randomly.

        Returns a tuple of the coordinates of the move.
        :return: tuple(int, int)
        """
        # This is where minimax has to be implemented.
        available = self._board.free_cells()
        coords = random.choice(available)
        #
        self._board.move(coords, player=2)

    def play(self):
        """
        Executes the game algorithm.
        Player moves, then AI moves, until spaces run out or someone wins.
        :return:
        """
        # Play the game until someone wins or board space ends.
        current_player = self.get_turn()
        while not (self._board.game_over(player=current_player % 2 + 1) or self._board.free_cells() == []):
            if current_player == 1:
                self.player_move()
            else:
                time.sleep(0.2)
                print("AI is making a move...")
                time.sleep(0.5)
                self.ai_move()
            current_player = self.get_turn()
            print(f"\n{self}\n")

        # This point means the game is finished.
        p1win = self._board.game_over(player=1)
        p2win = self._board.game_over(player=2)
        no_cells = self._board.free_cells() == []
        if p1win:
            print("Player 1 won!")
        elif p2win:
            print("Player 2 won!")
        elif no_cells:
            print("Tie!")
        else:
            raise RuntimeError("The game ended in an unexpected way.")

        print(f"\nEnd board state:\n{self}\n")

    def __str__(self):
        """
        Returns a formatted string of the board.
        :return: str
        """
        return str(self._board)


if __name__ == '__main__':
    game = Game()
    game.play()
