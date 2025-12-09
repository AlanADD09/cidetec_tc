
from typing import Dict, Set
from .base import Automaton

class DFA(Automaton):
    """Deterministic finite automaton."""

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str],
                 transitions: Dict[str, Dict[str, str]]) -> None:
        super().__init__(states, alphabet, initial_state, final_states)
        self.transitions = transitions  # state -> symbol -> state

    def transition(self, state: str, symbol: str):
        return self.transitions.get(state, {}).get(symbol)

    def accepts(self, input_str: str) -> bool:
        current = self.initial_state
        for ch in input_str:
            if ch not in self.alphabet:
                return False
            current = self.transition(current, ch)
            if current is None:
                return False
        return current in self.final_states
