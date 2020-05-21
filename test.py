import unittest

# from minesweeper.minesweeper import Minesweeper, Sentence
from minesweeper import Minesweeper, Sentence, MinesweeperAI


class MinsweeperTestCases(unittest.TestCase):

    def setUp(self):
        self.ai = MinesweeperAI(8, 8)
        #  initialize a class with only one bomb and not at random, so that I can trace what's happening
        ms = Minesweeper(8, 8, 8)
        ms.mines.add((1, 7))
        ms.board[1][7] = True

        # setje = [(0, 1), (0, 2), (1, 7)]
        # sentence = Sentence(setje, 1)
        # known_mines = sentence.known_mines()
        # print(known_mines)

    def test_moves_made(self):
        tuple_example = (1, 4)
        self.ai.add_knowledge(tuple_example, 0) # dit werkt niet goed

        print(self.ai.moves_made)

        self.assertTrue(tuple_example in self.ai.moves_made)

    def test_mark_safe(self):
        tuple_example = (1, 6)
        self.ai.add_knowledge(tuple_example, 0)
        self.ai.print_knowledge()
        self.assertTrue(tuple_example in self.ai.safes)

    def test_mark_mine(self):
        sentence_1 = Sentence({(6, 4), (6, 3)}, 1)
        sentence_2 = Sentence({(6, 4)}, 1)
        sentence_3 = Sentence({(6, 3)}, 0)

        self.ai.knowledge.append(sentence_1)
        self.ai.resolve(sentence_2)
        self.ai.print_knowledge()

        self.assertTrue(sentence_3 in self.ai.knowledge)
        self.assertTrue((6, 4) in self.ai.mines)

    def test_makes_safe_move(self):
        self.ai.mines = {(7, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                         (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3),
                         (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
                         (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 0)}
        self.ai.safes = {(0, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)}
        self.assertIn(self.ai.make_safe_move(), {(0, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)})

    def test_random_move(self):
        self.ai.mines = {(7, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                         (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3),
                         (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)}
        self.ai.moves_made = {(0, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)}
        self.assertIn(self.ai.make_random_move(),
                      [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 0)])

    # given {a,b,c} = X in knowledge en {c} = X then add {a,b} = 0 to knowledge
    def test_add_knowledge_1(self):
        # this works because of sentence.mark_mine().
        # sentence_1 and sentence_3 are the same sentence where
        # (6,4) has been removed and count decreased
        # Sweet!

        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 1)
        self.ai.knowledge.append(sentence_1)

        # if I resolve sentence_2
        sentence_2 = Sentence({(6, 4)}, 1)
        self.ai.resolve(sentence_2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(6, 3), (7, 4), (6, 2), (7, 2)}, 0)

        self.assertIn(sentence_3, self.ai.knowledge)

    # given {a,b,c,d} = X and {a,b} = Y add set {c,d} = X - Y
    def test_add_knowledge_2(self):
        # the resolved sentence (_2) is a subset of sentence in knowledge (_1)
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.knowledge.append(sentence_1)

        # resolve sentence_2
        sentence_2 = Sentence({(6, 4), (6, 3)}, 1)
        self.ai.resolve(sentence_2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(7, 4), (6, 2), (7, 2)}, 1)
        print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)

    # given a set {a,b} = X and {a,b,c,d} = Y add set {c,d} = Y - X
    def test_add_knowledge_3(self):
        # the resolved sentence (_2) is a superset of sentence in knowledge (_1)

        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4), (6, 3)}, 1)
        self.ai.knowledge.append(sentence_1)

        # if I resolve sentence_2
        sentence_2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)

        self.ai.knowledge.append(sentence_2)
        self.ai.resolve(sentence_2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(7, 4), (6, 2), (7, 2)}, 1)
        self.assertIn(sentence_3, self.ai.knowledge)

    # applies same logica as test_add_knowledge_4 but with safe
    def test_add_knowledge_4(self):
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4)}, 0)
        self.ai.knowledge.append(sentence_1)

        # if I resolve sentence_2
        sentence_2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.resolve(sentence_2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)

    # given a sentence {a, b, c}= 0 add {a}=0, {b}=0 and {c}=0 to knowledge
    def test_add_knowledge_5(self):
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4), (6, 3), (7, 4)}, 0)

        # sentence_0
        sentence_2 = Sentence({(6, 4), (5, 4), (5, 3)}, 2)  # program makes sentence (4,6)=0 , ????
        self.ai.knowledge.append(sentence_2)

        # self.ai.knowledge.append(sentence)
        self.ai.resolve(sentence_1)

        # then ai.safes is filled with these tuples
        self.assertIn((6, 4), self.ai.safes)
        self.assertIn((6, 3), self.ai.safes)
        self.assertIn((7, 4), self.ai.safes)

        sentence_3 = Sentence({(5, 4), (5, 3)}, 2)

        # then while resolving sentence_1,  mark_safe will remove (6,4) from sentence_2
        self.assertIn(sentence_3,self.ai.knowledge)

    def test_new_functions_in_sentence(self):
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4)}, 0)
        sentence_2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        sentence_3 = Sentence(set(), 0)

        # self.assertEqual(len(sentence_1), 1)
        # self.assertEqual(len(sentence_2), 5)
        self.assertTrue(sentence_1.is_literal)
        self.assertTrue(sentence_3.is_empty_set)

    # def test_is_literal(self):
    #     # pass niet
    #     sentence_3 = Sentence({(6, 3)}, 0)
    #     sentence_2 = Sentence({(6, 3), (6, 4)}, 0)
    #     self.assertTrue(sentence_3.is_literal)
    #     self.assertFalse(sentence_2.is_literal)

    def test_known_mines(self):
        sentence_1 = Sentence({(6, 4), (6, 3)}, 2)
        sentence_2 = Sentence({(5, 4)}, 1)

        self.ai.resolve(sentence_1)
        self.ai.resolve(sentence_2)

        self.assertEqual(self.ai.mines, {(5, 4), (6, 4), (6, 3)})

    def test_known_safes(self):
        sentence_1 = Sentence({(6, 4), (6, 3)}, 1)
        sentence_2 = Sentence({(6, 4)}, 1)

        self.ai.resolve(sentence_1)
        print(self.ai.knowledge)
        print(self.ai.safes)
        # self.assertEqual(len(self.ai.safes), 0)
        self.assertEqual(self.ai.safes, set())

        self.ai.resolve(sentence_2)
        print(self.ai.safes)
        # self.assertIn((6, 3), self.ai.safes)

        #
        # self.assertEqual(sentence_1.known_safes, set())
        # self.assertEqual(sentence_2.known_safes, {(6, 3)})
        # self.assertEqual(sentence_3.known_safes, set())
        # self.assertEqual(sentence_4.known_safes, {(6, 4), (6, 3)})

    def test_whats_happening(self):
        self.ai.knowledge = [Sentence({(5, 1), (6, 1), (6, 3), (6, 2), (4, 2), (4, 1)}, 1),
                             Sentence({(3, 3), (5, 3)}, 0),
                             Sentence({(5, 4), (5, 5), (5, 6)}, 0),
                             Sentence({(3, 2), (5, 4), (3, 3), (5, 2), (4, 2), (5, 3)}, 1),
                             Sentence({(5, 4), (3, 2), (5, 2), (4, 2)}, 1),
                             Sentence({(2, 6), (4, 6), (4, 5), (4, 4), (3, 6), (2, 5), (3, 4), (2, 4)}, 0)]
        self.safes = {(5, 4), (3, 5), (2, 6), (3, 3), (5, 5), (4, 6), (4, 5), (5, 6), (4, 4), (4, 3), (3, 6), (3, 4), (2, 5), (5, 2), (2, 4), (5, 3)}


    def test_add_knowledge_88(self):
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4), (5, 0)}, 1)
        sentence_2 = Sentence({(6, 4)}, 0)
        # self.ai.knowledge.append(sentence_1)
        self.ai.knowledge.append(sentence_2)

        # if I resolve sentence_2
        # sentence_2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.resolve(sentence_1)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(5, 0)}, 1)
        # print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)
        self.assertIn((5, 0), self.ai.mines)




# possible cells:
# []
# No known safe moves, AI making random move.
# {(4, 6)}
# New sentence is in add knowledge:
# {(4, 7), (5, 5), (4, 5), (5, 6), (5, 7), (3, 6), (3, 7), (3, 5)} = 0
# possible cells:
# [(3, 5), (3, 6), (3, 7), (4, 5), (4, 7), (5, 5), (5, 6), (5, 7)]
# safe move
# (3, 5)
# AI making safe move.
# {(4, 6), (3, 5)}
# New sentence is in add knowledge:
# {(2, 6), (4, 6), (4, 5), (4, 4), (3, 6), (2, 5), (3, 4), (2, 4)} = 1
# new knowledge inferred:
# {(2, 6), (4, 6), (4, 5), (4, 4), (3, 6), (2, 5), (3, 4), (2, 4)} = 1


if __name__ == '__main__':
    unittest.main()
