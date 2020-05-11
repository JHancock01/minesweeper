import unittest

# from minesweeper.minesweeper import Minesweeper, Sentence
from minesweeper import Minesweeper, Sentence, MinesweeperAI


class MinsweeperTestCases(unittest.TestCase):

    def setUp(self):
        self.ai = MinesweeperAI(8,8)
        #  initialize a class with only one bomb and not at random, so that I can trace what's happening
        ms = Minesweeper(8, 8, 8)
        ms.mines.add((1,7))
        ms.board[1][7] = True




        # setje = [(0, 1), (0, 2), (1, 7)]
        # sentence = Sentence(setje, 1)
        # known_mines = sentence.known_mines()
        # print(known_mines)

    # def test_moves_made(self):
    #
    #     self.assertTrue(True, True)

    def test_moves_made(self):
        tuple_example = (1, 4)
        self.ai.add_knowledge(tuple_example, 0)
        print(self.ai.moves_made)
        self.assertTrue(tuple_example in self.ai.moves_made)

    def test_mark_safe(self):
        tuple_example = (1, 6)
        self.ai.add_knowledge(tuple_example, 0)
        self.ai.print_knowledge()
        self.assertTrue(tuple_example in self.ai.safes)

    # def test_mark_mine(self):
    #     tuple_example = (1, 7)
    #     self.ai.add_knowledge(tuple_example, 1)
    #     self.ai.print_knowledge()
    #     self.assertTrue(tuple_example in self.ai.mines)

    def test_makes_safe_move(self):
        self.ai.mines = ((7, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                         (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3),
                         (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
                         (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 0))
        self.ai.safes = ((0, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7))
        self.assertIn(self.ai.make_safe_move(), [(0,0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)])

    def test_random_move(self):
        self.ai.mines = ((7, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                         (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3),
                         (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7))
        self.ai.moves_made = ((0, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7))
        self.assertIn(self.ai.make_random_move(), [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 0)])

    # given {a,b,c} = X in knowledge en {c} = X then add {a,b} = 0 to knowledge
    def test_add_knowledge_1(self):

        # given  sentence_1 in knowledge
        sentence1 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 1)
        self.ai.knowledge.append(sentence1)

        # if I resolve sentence_2
        sentence2 = Sentence({(6, 4)}, 1)
        self.ai.resolve(sentence2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(6, 3), (7, 4), (6, 2), (7, 2)}, 0)

        self.assertIn(sentence_3, self.ai.knowledge)

    # given a set {a,b,c,d} = X and a subset {a,b} = Y add set {c,d} = X - Y
    def test_add_knowledge_2(self):
        # given  sentence_1 in knowledge
        sentence1 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.knowledge.append(sentence1)

        # resolve sentence_2
        sentence2 = Sentence({(6, 4), (6, 3)}, 1)
        self.ai.resolve(sentence2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(7, 4), (6, 2), (7, 2)}, 1)
        print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)

    def test_add_knowledge_5(self):
        # given  sentence_1 in knowledge
        sentence = Sentence({(6, 4), (6, 3), (7, 4)}, 0)
        self.ai.knowledge.append(sentence)
        self.ai.originate_one_element_sentences(sentence)

        # then sentence_3 should be in knowledge
        sentence_0 = Sentence({(6, 4)}, 0)  # program makes sentence (4,6)=0 , ????
        sentence_1 = Sentence({(6, 3)}, 0)
        sentence_2 = Sentence({(7, 4)}, 0)

        self.assertIn(sentence_0, self.ai.knowledge)
        self.assertIn(sentence_1, self.ai.knowledge)
        self.assertIn(sentence_2, self.ai.knowledge)

    # given a set {a,b} = X and a superset {a,b,c,d} = Y add set {c,d} = Y - X
    def test_add_knowledge_3(self):
        # given  sentence_1 in knowledge
        sentence1 = Sentence({(6, 4), (6, 3)}, 1)
        self.ai.knowledge.append(sentence1)

        # if I resolve sentence_2
        sentence2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.resolve(sentence2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(7, 4), (6, 2), (7, 2)}, 1)
        print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)

    def test_add_knowledge_4(self):
        # given  sentence_1 in knowledge
        sentence1 = Sentence({(6, 4)}, 0)
        self.ai.knowledge.append(sentence1)

        sentence2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        self.ai.resolve(sentence2)

        # then sentence_3 should be in knowledge
        sentence_3 = Sentence({(6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        print(self.ai.knowledge)
        self.assertIn(sentence_3, self.ai.knowledge)

    # given a sentence {a, b, c}= 0 add {a}=0, {b}=0 and {c}=0 to knowledge

    def test_new_functions_in_sentence(self):
        # given  sentence_1 in knowledge
        sentence_1 = Sentence({(6, 4)}, 0)
        sentence_2 = Sentence({(6, 4), (6, 3), (7, 4), (6, 2), (7, 2)}, 2)
        sentence_3 = Sentence(set(), 0)

        self.assertEqual(len(sentence_1), 1)
        self.assertEqual(len(sentence_2), 5)
        self.assertTrue(sentence_1.is_literal)
        self.assertTrue(sentence_3.is_empty_set)

    def test_known_mines(self):
        sentence_1 = Sentence({(6, 4), (6, 3)}, 2)
        sentence_2 = Sentence({(6, 4), (6, 3)}, 0)

        self.assertEqual(sentence_1.known_mines, {(6, 4), (6, 3)})
        self.assertEqual(sentence_2.known_mines, set())

    def test_known_safes(self):
        sentence_1 = Sentence({(6, 4)}, 1)
        sentence_2 = Sentence({(6, 3)}, 0)
        sentence_3 = Sentence({(6, 4), (6, 3)}, 2)
        sentence_4 = Sentence({(6, 4), (6, 3)}, 0)

        if len(sentence_1.cells) == sentence_1.count:
            print("het is hetzelfde")

        self.assertEqual(sentence_1.known_safes, set())
        self.assertEqual(sentence_2.known_safes, {(6, 3)})
        self.assertEqual(sentence_3.known_safes, set())
        self.assertEqual(sentence_4.known_safes, {(6, 4), (6, 3)})


if __name__ == '__main__':
    unittest.main()
