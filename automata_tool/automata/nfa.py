
from typing import Dict, Set, Optional
from .base import Automaton

Symbol = Optional[str]  # None will represent epsilon

class NFA(Automaton):
    """Non-deterministic finite automaton with epsilon transitions."""

    EPSILON: Symbol = None

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str],
                 transitions: Dict[str, Dict[Symbol, Set[str]]]) -> None:
        super().__init__(states, alphabet, initial_state, final_states)
        self.transitions = transitions  # state -> symbol/epsilon -> set(states)

    def add_transition(self, from_state: str, symbol: Symbol, to_state: str) -> None:
        self.transitions.setdefault(from_state, {})
        self.transitions[from_state].setdefault(symbol, set()).add(to_state)

    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """Compute epsilon-closure of the given set of states."""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for nxt in self.transitions.get(state, {}).get(self.EPSILON, set()):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def move(self, states: Set[str], symbol: str) -> Set[str]:
        """Set of states reachable from any state in `states` via `symbol` (no epsilons)."""
        result: Set[str] = set()
        for state in states:
            result |= self.transitions.get(state, {}).get(symbol, set())
        return result

    def accepts(self, input_str: str) -> bool:
        """Simulate NFA on the given input string."""
        current_states = self.epsilon_closure({self.initial_state})
        for ch in input_str:
            if ch not in self.alphabet:
                return False
            current_states = self.epsilon_closure(self.move(current_states, ch))
            if not current_states:
                return False
        return any(s in self.final_states for s in current_states)
