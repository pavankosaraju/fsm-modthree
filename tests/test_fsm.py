import unittest
import sys
sys.path.append('./src')
from src.fsm import FSM

class TestFSM(unittest.TestCase):
    def setUp(self):
        # Define a simple FSM for testing the generic class
        self.states = {'A', 'B'}
        self.alphabet = {'x', 'y'}
        self.initial_state = 'A'
        self.final_states = {'B'}
        self.transition_function = {
            ('A', 'x'): 'A',
            ('A', 'y'): 'B',
            ('B', 'x'): 'B',
            ('B', 'y'): 'A',
        }
        self.fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transition_function)

    def test_initialization(self):
        self.assertEqual(self.fsm.current_state, 'A')
        self.assertEqual(self.fsm.states, {'A', 'B'})
        self.assertEqual(self.fsm.alphabet, {'x', 'y'})
        self.assertEqual(self.fsm.initial_state, 'A')
        self.assertEqual(self.fsm.final_states, {'B'})
        self.assertEqual(self.fsm.transition_function, self.transition_function)

    def test_invalid_initialization(self):
        with self.assertRaisesRegex(ValueError, "States must be a set of strings."):
            FSM(['A', 'B'], self.alphabet, self.initial_state, self.final_states, self.transition_function)
        with self.assertRaisesRegex(ValueError, "Alphabet must be a set of strings."):
            FSM(self.states, ['x', 'y'], self.initial_state, self.final_states, self.transition_function)
        with self.assertRaisesRegex(ValueError, "Initial state must be in the set of states."):
            FSM(self.states, self.alphabet, 'C', self.final_states, self.transition_function)
        with self.assertRaisesRegex(ValueError, "Final states must be a subset of the set of states."):
            FSM(self.states, self.alphabet, self.initial_state, {'C'}, self.transition_function)
        with self.assertRaisesRegex(ValueError, "Transition function must be a dictionary."):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, [])
        
        # Test invalid state/symbol in transition function
        invalid_transition_func = {('A', 'x'): 'A', ('Z', 'y'): 'B'}
        with self.assertRaisesRegex(ValueError, "Transition function contains invalid current state: Z"):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, invalid_transition_func)

        invalid_transition_func = {('A', 'x'): 'A', ('A', 'z'): 'B'}
        with self.assertRaisesRegex(ValueError, "Transition function contains invalid input symbol: z"):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, invalid_transition_func)

        invalid_transition_func = {('A', 'x'): 'A', ('A', 'y'): 'Z'}
        with self.assertRaisesRegex(ValueError, "Transition function contains invalid next state: Z"):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, invalid_transition_func)


    def test_transition(self):
        self.fsm.transition('x')
        self.assertEqual(self.fsm.current_state, 'A')
        self.fsm.transition('y')
        self.assertEqual(self.fsm.current_state, 'B')
        self.fsm.transition('x')
        self.assertEqual(self.fsm.current_state, 'B')
        self.fsm.transition('y')
        self.assertEqual(self.fsm.current_state, 'A')

    def test_invalid_transition_symbol(self):
        with self.assertRaisesRegex(ValueError, "Invalid input symbol: z. Must be one of "):
            self.fsm.transition('z')

    def test_run(self):
        # Path: A -> x -> A -> y -> B -> x -> B -> y -> A -> y -> B
        self.fsm.reset()
        final_state = self.fsm.run("xyxyy")
        self.assertEqual(final_state, 'B')

        self.fsm.reset()
        final_state = self.fsm.run("xyxy")
        self.assertEqual(final_state, None)

    def test_reset(self):
        self.fsm.transition('y')
        self.assertEqual(self.fsm.current_state, 'B')
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state, 'A')

if __name__ == '__main__':
    unittest.main()