import itertools
import random
from typing import Tuple


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        # true if board cell is true
        print(cell)
        (i, j) = cell
        print("hhieeer")
        print(i)
        print(j)

        return self.board[i][j]
        #TypeError: cannot unpack non-iterable method object


    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):  # cell[0] gives me the y coordinate of the cell, if cell[0] = 4 then I check 3, 4, 5
            for j in range(cell[1] - 1, cell[1] + 2):  # cell[1] gives me the x coordinate of the cell, if cell[1] = 4 then I check 3, 4, 5
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]: # it's a mine
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __len__(self):
        return len(self.cells)

    def is_literal(self):
        return len(self.cells) == 1

    def is_empty_set(self):
        return self.cells == set()

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return self.cells
        else:
            return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if abc = 2 and a = 0 the ab =2
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def print_knowledge(self):
        for i in range(len(self.knowledge)):
            print(self.knowledge[i])

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # {a, b, c},  2
        # {a, b}, 1 {c} 1

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

        # self.update_knowledge(cell, -1)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def neighbors(self, cell):  # copied from nearby_mines
        neighbors = []
        for i in range(cell[0] - 1, cell[0] + 2):   # cell[0] is the y coord. of the cell, if cell[0] = 4 then I check 3, 4, 5
            for j in range(cell[1] - 1, cell[1] + 2):  # cell[1] gives me the x coordinate of the cell, if cell[1] = 4 then I check 3, 4, 5

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < 8 and 0 <= j < 8:
                    neighbors.append((i,j))
        return neighbors

    def resolve(self, sentence):
        # update new knowledge
        if sentence.count == 0:
            for cell in sentence.cells:
                self.mark_safe(cell)

        else:
            # generate new knowledge
            for knowledge in self.knowledge:
                if sentence.cells.issubset(knowledge.cells):    # sentence.cells {a,b}, 2 knowledge.cells{a,b,c,d}, 4
                    new_sentence = Sentence(knowledge.cells - sentence.cells, knowledge.count - sentence.count)
                    self.knowledge.append(new_sentence)
                elif sentence.cells.issuperset(knowledge.cells): # sentences.cells {a,b,c,d} knowledge {c,d}
                    new_sentence = Sentence(sentence.cells - knowledge.cells, sentence.count - knowledge.count)
                    self.knowledge.append(new_sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        ## if count is 4 you may write {a,b,c,d,e,f,g,h} = 4

        This function should:
            1) mark the cell as a move that has been made (done)
            2) mark the cell as safe (done)
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count` (done)
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as moved
        self.moves_made.add(cell)

        # add the cell as safe
        self.mark_safe(cell) # plus update knowledge

        # look for neighbors
        tuples_list_of_neighbors = self.neighbors(cell)

        # create a sentence with all neighbors
        new_sentence = Sentence(tuples_list_of_neighbors, count)

        # resolve sentence
        self.resolve(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        temporary_board = []

        for height in range(8):
            for width in range(8):
                move = (height, width)
                if move not in self.mines and move in self.safes:
                    # print(move)
                    temporary_board.append(move)
        print(temporary_board)

        if temporary_board:
            random_index = random.choice(range(len(temporary_board)))
            return temporary_board[random_index]
        # else:
        #     return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            random_height = random.randint(0, 7)
            random_width = random.randint(0, 7)
            move = (random_height, random_width)
            print(move)
            if move not in self.moves_made and not move in self.mines:
                return move
