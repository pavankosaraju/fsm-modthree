class FSM:
    """
    A generic Finite State Machine (FSM) class.

    This class implements a generic finite automaton defined by a 5-tuple (Q, Sigma, q0, F, delta),
    where:
    Q: A finite set of states.
    Sigma: A finite input alphabet.
    q0: The initial state.
    F: The set of accepting/final states.
    delta: The transition function (Q x Sigma -> Q).
    """

    def __init__(self, states, alphabet, initial_state, final_states, transition_function):
        """
        Initializes the FSM.

        Args:
            states (set): A set of all possible states (e.g., {'S0', 'S1', 'S2'}).
            alphabet (set): A set of all possible input symbols (e.g., {'0', '1'}).
            initial_state (str): The starting state of the FSM. Must be in 'states'.
            final_states (set): A set of states considered as accepting/final states. Must be a subset of 'states'.
            transition_function (dict): A dictionary representing the transition function.
                                        Keys are (current_state, input_symbol) tuples, values are next_states.
                                        Example: {('S0', '0'): 'S0', ('S0', '1'): 'S1'}
        """
        # arg validations
        if not isinstance(states, set) or not all(isinstance(s, str) for s in states):
            raise ValueError("States must be a set of strings.")
        if not isinstance(alphabet, set) or not all(isinstance(a, str) for a in alphabet):
            raise ValueError("Alphabet must be a set of strings.")
        if initial_state not in states:
            raise ValueError("Initial state must be in the set of states.")
        if not isinstance(final_states, set) or not final_states.issubset(states):
            raise ValueError("Final states must be a subset of the set of states.")
        if not isinstance(transition_function, dict):
            raise ValueError("Transition function must be a dictionary.")

        # assign class vars
        self.states = states
        self.alphabet = alphabet
        self.current_state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function

        for (state, symbol), next_state in self.transition_function.items():
            if state not in self.states:
                raise ValueError(f"Transition function contains invalid current state: {state}")
            if symbol not in self.alphabet:
                raise ValueError(f"Transition function contains invalid input symbol: {symbol}")
            if next_state not in self.states:
                raise ValueError(f"Transition function contains invalid next state: {next_state}")
            

    def transition(self, input_symbol):
        """
        Transitions the FSM to the next state based on the current state and input symbol.

        Args:
            input_symbol (str): The input symbol to process.

        Raises:
            ValueError: If the input symbol is not in the FSM's alphabet or no transition is defined.
        """
        if input_symbol not in self.alphabet:
            raise ValueError(f"Invalid input symbol: {input_symbol}. Must be one of {self.alphabet}")

        try:
            self.current_state = self.transition_function[(self.current_state, input_symbol)]
        except KeyError:
            raise ValueError(f"No transition defined for state {self.current_state} with input {input_symbol}")

    def run(self, input_string):
        """
        Runs the FSM on a given input string.

        Args:
            input_string (str): The sequence of input symbols to process.

        Returns:
            The final state after processing the entire input string.
        """
        self.current_state = self.initial_state  # Reset to initial state for each run
        for symbol in input_string:
            self.transition(symbol)
        return self.current_state if self.current_state in self.final_states else None

    def reset(self):
        """Resets the FSM to its initial state."""
        self.current_state = self.initial_state