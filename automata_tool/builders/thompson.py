
from dataclasses import dataclass
from typing import Dict, Set, Optional as OptType

from automata_tool.regex.ast import (
    RegexNode,
    Literal,
    Concat,
    Union,
    Star,
    Plus,
    Optional as OptNode,
)
from automata_tool.automata.nfa import NFA

Symbol = OptType[str]  # None for epsilon

@dataclass
class NFAFragment:
    start: str
    end: str
    transitions: Dict[str, Dict[Symbol, Set[str]]]

class ThompsonBuilder:
    """Builds an NFA from a Regex AST using Thompson's construction."""

    def __init__(self) -> None:
        self._state_counter = 0
        self.alphabet: Set[str] = set()

    def _new_state(self) -> str:
        s = f"q{self._state_counter}"
        self._state_counter += 1
        return s

    def _merge(self, a: Dict[str, Dict[Symbol, Set[str]]],
               b: Dict[str, Dict[Symbol, Set[str]]]) -> Dict[str, Dict[Symbol, Set[str]]]:
        result: Dict[str, Dict[Symbol, Set[str]]] = {
            k: {sym: set(vs) for sym, vs in inner.items()} for k, inner in a.items()
        }
        for state, inner in b.items():
            if state not in result:
                result[state] = {sym: set(vs) for sym, vs in inner.items()}
            else:
                for sym, vs in inner.items():
                    result[state].setdefault(sym, set()).update(vs)
        return result

    def _build(self, node: RegexNode) -> NFAFragment:
        if isinstance(node, Literal):
            start = self._new_state()
            end = self._new_state()
            transitions: Dict[str, Dict[Symbol, Set[str]]] = {start: {node.symbol: {end}}}
            self.alphabet.add(node.symbol)
            return NFAFragment(start, end, transitions)

        if isinstance(node, Concat):
            left_frag = self._build(node.left)
            right_frag = self._build(node.right)
            transitions = self._merge(left_frag.transitions, right_frag.transitions)
            transitions.setdefault(left_frag.end, {}).setdefault(NFA.EPSILON, set()).add(right_frag.start)
            return NFAFragment(left_frag.start, right_frag.end, transitions)

        if isinstance(node, Union):
            left_frag = self._build(node.left)
            right_frag = self._build(node.right)
            start = self._new_state()
            end = self._new_state()
            transitions = self._merge(left_frag.transitions, right_frag.transitions)
            transitions.setdefault(start, {}).setdefault(NFA.EPSILON, set()).update({left_frag.start, right_frag.start})
            transitions.setdefault(left_frag.end, {}).setdefault(NFA.EPSILON, set()).add(end)
            transitions.setdefault(right_frag.end, {}).setdefault(NFA.EPSILON, set()).add(end)
            return NFAFragment(start, end, transitions)

        if isinstance(node, Star):
            frag = self._build(node.child)
            start = self._new_state()
            end = self._new_state()
            transitions = self._merge(frag.transitions, {})
            transitions.setdefault(start, {}).setdefault(NFA.EPSILON, set()).update({frag.start, end})
            transitions.setdefault(frag.end, {}).setdefault(NFA.EPSILON, set()).update({frag.start, end})
            return NFAFragment(start, end, transitions)

        if isinstance(node, Plus):
            # One or more: R+ behaves like R followed by R*
            frag = self._build(node.child)
            start = self._new_state()
            end = self._new_state()
            transitions = self._merge(frag.transitions, {})
            # from new start to fragment start
            transitions.setdefault(start, {}).setdefault(NFA.EPSILON, set()).add(frag.start)
            # loop from frag.end to frag.start
            transitions.setdefault(frag.end, {}).setdefault(NFA.EPSILON, set()).add(frag.start)
            # and to new end
            transitions.setdefault(frag.end, {}).setdefault(NFA.EPSILON, set()).add(end)
            return NFAFragment(start, end, transitions)

        if isinstance(node, OptNode):
            # Optional: R? = (ε | R)
            frag = self._build(node.child)
            start = self._new_state()
            end = self._new_state()
            transitions = self._merge(frag.transitions, {})
            # from new start to either skip R or go into R
            transitions.setdefault(start, {}).setdefault(NFA.EPSILON, set()).update({frag.start, end})
            # from frag.end we can go to end
            transitions.setdefault(frag.end, {}).setdefault(NFA.EPSILON, set()).add(end)
            return NFAFragment(start, end, transitions)

        raise TypeError(f"Tipo de nodo de regex no soportado: {type(node)}")

    def build(self, root: RegexNode) -> NFA:
        frag = self._build(root)
        # Collect all states from transitions plus start/end
        states: Set[str] = set()
        for s, inner in frag.transitions.items():
            states.add(s)
            for _, dests in inner.items():
                states.update(dests)
        states.update({frag.start, frag.end})

        # Ensure every state appears in transitions dict
        for s in states:
            frag.transitions.setdefault(s, {})

        alphabet = set(self.alphabet)
        if None in alphabet:
            alphabet.remove(None)
        return NFA(states=states,
                   alphabet=alphabet,
                   initial_state=frag.start,
                   final_states={frag.end},
                   transitions=frag.transitions)
