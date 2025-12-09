
from abc import ABC, abstractmethod
from typing import Set

class Automaton(ABC):
    """Abstract base class for finite automata."""

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str]) -> None:
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states

    @abstractmethod
    def accepts(self, input_str: str) -> bool:
        """Return True if the automaton accepts the input string."""
        raise NotImplementedError
