class Board:
    """Represents a board for Noughts and Crosses."""

    combos = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    def __init__(self, p1s="X", p2s="O"):
        """
        Creates a 3x3 board.
        """
        self.board = [
                       [" ", " ", " "],
                       [" ", " ", " "],
                       [" ", " ", " "]
                       ]
        self._current_turn = 1

        self.PLAYER_1_SYMBOL = p1s
        self.PLAYER_2_SYMBOL = p2s

    def __setitem__(self, coords, value):
        self.board[coords[0]][coords[1]] = value

    def __getitem__(self, coords):
        return self.board[coords[0]][coords[1]]

    def __eq__(self, other):
        return (isinstance(other, Board)
                and self.board == other.board
                and self._current_turn == other._current_turn)

    def get_turn(self):
        """
        Returns the current turn on the board.
        :return: int
        """
        return self._current_turn

    def move(self, coords, player=1):
        """
        Makes a move in the spot specified by coords.
        Player 1 == "X", player 2 == "O"
        :param coords: tuple(int, int)
        :param player: Any[1, 2]
        :return: None
        """
        if player == 1:
            symbol = self.PLAYER_1_SYMBOL
        elif player == 2:
            symbol = self.PLAYER_2_SYMBOL
        else:
            raise ValueError("'player' value must be one of [1, 2]")

        self[coords] = symbol
        self._current_turn += 1
        return self

    def undo(self, coords):
        """
        Deletes a move.
        :param coords: tuple(int, int)
        :return: None
        """
        self[coords] = " "
        self._current_turn -= 1

    def game_over(self, player=1):
        """
        Checks if the game is over.

        Returns True if the specified player won, or False if the game is not over.
        :return: bool
        """
        if player == 1:
            symbol = self.PLAYER_1_SYMBOL
        elif player == 2:
            symbol = self.PLAYER_2_SYMBOL
        else:
            raise ValueError("'player' value must be one of [1, 2]")

        for combo in self.combos:
            if list(map(lambda x: self[x], combo)) == [symbol] * 3:
                return True
        return False

    def free_cells(self):
        """
        Returns the list of coordinates for cells that are not occupied.
        :return: list
        """
        return [(row, col) for col in range(3) for row in range(3) if self[(row, col)] == " "]

    def __str__(self):
        """
        Formats a board and returns a string with it.
        :return:
        """
        res = f"""     |- - -|
     |{self[(0, 0)]} {self[(0, 1)]} {self[(0, 2)]}|
     |{self[(1, 0)]} {self[(1, 1)]} {self[(1, 2)]}|
     |{self[(2, 0)]} {self[(2, 1)]} {self[(2, 2)]}|
     |- - -|"""
        return res
