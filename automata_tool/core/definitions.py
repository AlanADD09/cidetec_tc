
from dataclasses import dataclass
from typing import Set, Dict, Any

EPSILON_SYMBOL = "ε"

@dataclass
class AutomatonDefinition:
    """Simple container for an automaton 5-tuple definition."""

    kind: str  # "NFA" or "DFA"
    states: Set[str]
    alphabet: Set[str]
    initial_state: str
    final_states: Set[str]
    transition_function: Dict[str, Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "states": sorted(self.states),
            "alphabet": sorted(self.alphabet),
            "initial_state": self.initial_state,
            "final_states": sorted(self.final_states),
            "transition_function": self.transition_function,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AutomatonDefinition":
        kind = data.get("kind", "").upper()
        if kind not in {"NFA", "DFA"}:
            raise ValueError("AutomatonDefinition.kind debe ser 'NFA' o 'DFA'")
        states = set(data.get("states", []))
        alphabet = set(data.get("alphabet", []))
        initial_state = data.get("initial_state")
        final_states = set(data.get("final_states", []))
        transition_function = data.get("transition_function", {})
        return AutomatonDefinition(
            kind=kind,
            states=states,
            alphabet=alphabet,
            initial_state=initial_state,
            final_states=final_states,
            transition_function=transition_function,
        )
