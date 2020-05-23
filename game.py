from board import Board
from binary_search_tree.linkedbst import LinkedBST
from binary_search_tree.bstnode import BSTNode
from binary_search_tree.linkedstack import LinkedStack
import random
import time
from copy import deepcopy


class Game:
    """Represents a game of Noughts and Crosses (or Tic-Tac-Toe, duh...)"""

    def __init__(self):
        """
        Initializes the game with a board.
        """
        self.board = Board()

    def get_turn(self):
        """
        Returns which player currently is to move.
        Player 1 == "X", player 2 == "O"
        :return: Any[1, 2]
        """
        return 1 if self.board.get_turn() % 2 == 1 else 2

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
                if coords in self.board.free_cells():
                    self.board.move(coords, player=1)
                    return coords
            print("Invalid coordinates.\n")

    def ai_move(self, algorithm=1):
        """
        Algorithm for executing AI's move.
        Minimax algorithm will be implemented for the AI,
        but for now it moves randomly.

        Returns a tuple of the coordinates of the move.
        :param algorithm: Any[1, 2]
        :return: tuple(int, int)
        """
        if algorithm == 1:
            coords = self.minimax()
        else:
            coords = self.minimax2()

        self.board.move(coords, player=2)

    def minimax(self):
        """
        Runs the minimax algorithm for a current board state.

        This method builds a tree of some of the later game states
        and then runs the algorithm for the tree.

        Returns the coordinates for a move.
        :return: tuple(int, int)
        """

        def build_states(cur_state):
            """
            Builds a tree of states starting from the current game state.
            Always chooses 2 random move options. (god knows why it's stupid)
            This method pre-fills the terminal states with scores of 1, -1, and 0.
            :param cur_state: Game
            :return: LinkedBST
            """
            states = LinkedBST()
            st = LinkedStack()
            states.root = BSTNode([deepcopy(cur_state.board), None, None])
            st.push(states.root)
    
            while not st.isEmpty():
                curr = st.pop()
                curr_board = curr.data[0]
                print(curr_board)
                p1w = curr_board.game_over(player=1)
                p2w = curr_board.game_over(player=2)
    
                if p1w:
                    curr.data[1] = 1
                    continue
                elif p2w:
                    curr.data[1] = -1
                    continue
    
                cells = curr.data[0].free_cells()
                if not cells:
                    # No one won and no cells left - it's a tie.
                    curr.data[1] = 0
                    print("tie")
                    continue
    
                available = random.sample(cells, k=min(len(cells), 2))
                for cell in available:
                    new_board = deepcopy(curr.data[0].move(cell, player=1 if curr.data[0].get_turn() % 2 == 1 else 2))
                    curr.data[0].undo(cell)
                    if curr.left is None:
                        curr.left = BSTNode([new_board, None, cell])
                        st.add(curr.left)
                    elif curr.right is None:
                        curr.right = BSTNode([new_board, None, cell])
                        st.add(curr.right)
                    else:
                        break
    
            return states

        def score(state, player=1):
            """
            Recursively scores a particular state.

            Player 1 is maximizing, player 2 is minimizing.
            :param state: BSTNode
            :param player: Any[1, 2]
            :return: None
            """
            if state.data[1] is not None:
                return state.data[1]

            children = []

            if state.left is not None:
                children.append(score(state.left, player=player % 2 + 1))
            if state.right is not None:
                children.append(score(state.right, player=player % 2 + 1))

            state.data[1] = max(children) if player == 1 else min(children)
            return state.data[1]

        minimax_tree = build_states(self)
        rt = minimax_tree.root
        scores = []

        if rt.left is not None:
            scores.append((rt.left.data[2], score(rt.left, player=1)))
        if rt.right is not None:
            scores.append((rt.right.data[2], score(rt.right, player=1)))

        print(scores)
        return min(scores, key=lambda x: x[1])[0]

    def minimax2(self):

        def score(state, player=1):
            p1w = state.game_over(player=1)
            p2w = state.game_over(player=2)
            cells = state.free_cells()

            if True:
                pass

            return 1

        scores = score(self.board)
        return 1, 1

    def play(self, algorithm=1):
        """
        Executes the game algorithm.
        Player moves, then AI moves, until spaces run out or someone wins.

        !!! WARNING !!!
        'algorithm' parameters IS IMPORTANT.
        algorithm = 1 is Lab Task 3.
        algorithm = 2 is Lab Task 4.
        For now only Lab Task 3 is properly implemented.
        :param algorithm: Any[1, 2]
        :return:
        """
        # Play the game until someone wins or board space ends.
        current_player = self.get_turn()
        while not (self.board.game_over(player=current_player % 2 + 1) or self.board.free_cells() == []):
            if current_player == 1:
                self.player_move()
            else:
                time.sleep(0.2)
                print("AI is making a move...")
                time.sleep(0.5)
                self.ai_move(algorithm=algorithm)
            current_player = self.get_turn()
            print(f"\n{self}\n")

        # This point means the game is finished.
        p1win = self.board.game_over(player=1)
        p2win = self.board.game_over(player=2)
        no_cells = self.board.free_cells() == []
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
        return str(self.board)


if __name__ == '__main__':
    game = Game()
    game.play()
