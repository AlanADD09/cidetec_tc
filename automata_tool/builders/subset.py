
from typing import Dict, Set, FrozenSet, List
from automata_tool.automata.nfa import NFA
from automata_tool.automata.dfa import DFA

class SubsetConstruction:
    """Convert an NFA to an equivalent DFA (subset construction)."""

    def build(self, nfa: NFA) -> DFA:
        # Initial DFA state is epsilon-closure of NFA initial state
        start_closure = nfa.epsilon_closure({nfa.initial_state})
        state_map: Dict[FrozenSet[str], str] = {}
        dfa_states: Set[str] = set()
        dfa_transitions: Dict[str, Dict[str, str]] = {}
        queue: List[FrozenSet[str]] = []

        def get_name(state_set: FrozenSet[str]) -> str:
            if state_set not in state_map:
                name = f"D{len(state_map)}"
                state_map[state_set] = name
            return state_map[state_set]

        start_set = frozenset(start_closure)
        start_name = get_name(start_set)
        queue.append(start_set)
        dfa_states.add(start_name)

        dfa_final_states: Set[str] = set()

        alphabet = {sym for sym in nfa.alphabet if sym is not None}

        while queue:
            current_set = queue.pop(0)
            current_name = state_map[current_set]
            dfa_transitions.setdefault(current_name, {})

            # Mark as final if any NFA state in the set is final
            if any(s in nfa.final_states for s in current_set):
                dfa_final_states.add(current_name)

            for symbol in alphabet:
                move_set = nfa.move(current_set, symbol)
                if not move_set:
                    continue
                closure = nfa.epsilon_closure(move_set)
                closure_fs = frozenset(closure)
                next_name = get_name(closure_fs)
                dfa_transitions[current_name][symbol] = next_name
                if next_name not in dfa_states:
                    dfa_states.add(next_name)
                    queue.append(closure_fs)

        return DFA(states=dfa_states,
                   alphabet=alphabet,
                   initial_state=start_name,
                   final_states=dfa_final_states,
                   transitions=dfa_transitions)
