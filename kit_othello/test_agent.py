import unittest

import advsearch.othello.board as board
import advsearch.othello.gamestate as gamestate
import advsearch.timer as timer

import advsearch.your_agent.agent as agent  # change your_agent by the name of your agent module


class TestAgent(unittest.TestCase):
    def test_initial_state(self):
        """
        If your test fails here, your agent is returning
        an invalid move for the initial state
        :return:
        """
        b = board.Board()
        g = gamestate.GameState(b, 'B')
        t = timer.FunctionTimer(agent.make_move, (g,) )  # must pass a tuple (even if it's 1-element)
        try:
            move = t.run(5)
            self.assertIn(move, [(2, 3), (4, 5), (5, 4), (3, 2)])
        except TimeoutError:
            self.fail("timeout")

    def test_no_valid_moves_white(self):
        """
        If this test fails, your agent is returning a move
        for a state where there is no move
        :return:
        """
        # triple-quoted string must be 'glued' to the left because indentation becomes part of the string
        b = board.from_string(
"""WWWWWWWW
WWWWWBBW
WWWWBWBW
WBWBWBBW
WBWWBWBW
WBBWBWBW
WBBBWBWW
WWWWWWW."""
        )
        g = gamestate.GameState(b, 'W')
        t = timer.FunctionTimer(agent.make_move, (g,) )  # must pass a tuple (even if it's 1-element)
        try:
            move = t.run(5)
            self.assertEqual(move, (-1, -1))
        except TimeoutError:
            self.fail("timeout")


if __name__ == '__main__':
    unittest.main()
