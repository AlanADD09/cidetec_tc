
from typing import Dict, Any

from automata_tool.automata.nfa import NFA
from automata_tool.automata.dfa import DFA
from automata_tool.regex.parser import Parser
from automata_tool.builders.thompson import ThompsonBuilder
from automata_tool.builders.subset import SubsetConstruction
from .definitions import AutomatonDefinition, EPSILON_SYMBOL

class AutomatonFactory:
    """High-level factory to construct NFAs/DFAs from regex or quintuple definitions."""

    def from_regex(self, regex: str) -> Dict[str, Any]:
        """Build NFA and DFA from a regular expression string."""
        parser = Parser(regex)
        ast_root = parser.parse()

        thompson = ThompsonBuilder()
        nfa: NFA = thompson.build(ast_root)

        subset = SubsetConstruction()
        dfa: DFA = subset.build(nfa)

        nfa_def = self._definition_from_nfa(nfa)
        dfa_def = self._definition_from_dfa(dfa)

        return {
            "nfa": nfa,
            "dfa": dfa,
            "nfa_def": nfa_def,
            "dfa_def": dfa_def,
        }

    def from_definition(self, definition: AutomatonDefinition) -> Dict[str, Any]:
        """Build both NFA and DFA starting from a 5-tuple definition.

        - If definition.kind == 'NFA', we build an NFA and then convert to DFA.
        - If definition.kind == 'DFA', we build a DFA and then a trivial NFA.
        """
        kind = definition.kind.upper()
        if kind == "NFA":
            nfa = self._nfa_from_definition(definition)
            subset = SubsetConstruction()
            dfa = subset.build(nfa)
        elif kind == "DFA":
            dfa = self._dfa_from_definition(definition)
            nfa = self._nfa_from_dfa(dfa)
        else:
            raise ValueError("AutomatonDefinition.kind debe ser 'NFA' o 'DFA'")

        nfa_def = self._definition_from_nfa(nfa)
        dfa_def = self._definition_from_dfa(dfa)

        return {
            "nfa": nfa,
            "dfa": dfa,
            "nfa_def": nfa_def,
            "dfa_def": dfa_def,
        }

    # ---- helpers to go from definitions to objects ----

    def _nfa_from_definition(self, definition: AutomatonDefinition) -> NFA:
        transitions = {}
        for state, trans in definition.transition_function.items():
            for symbol, dests in trans.items():
                if symbol == EPSILON_SYMBOL:
                    real_symbol = None
                else:
                    real_symbol = symbol
                if not isinstance(dests, (list, tuple, set)):
                    dest_set = {dests}
                else:
                    dest_set = set(dests)
                transitions.setdefault(state, {})
                transitions[state].setdefault(real_symbol, set()).update(dest_set)

        return NFA(
            states=set(definition.states),
            alphabet=set(definition.alphabet),
            initial_state=definition.initial_state,
            final_states=set(definition.final_states),
            transitions=transitions,
        )

    def _dfa_from_definition(self, definition: AutomatonDefinition) -> DFA:
        transitions = {}
        for state, trans in definition.transition_function.items():
            for symbol, dest in trans.items():
                if symbol == EPSILON_SYMBOL:
                    raise ValueError("Un DFA no puede tener transiciones epsilon")
                if isinstance(dest, (list, tuple, set)):
                    if len(dest) != 1:
                        raise ValueError("Transición de DFA debe ir a un único estado")
                    dest_state = next(iter(dest))
                else:
                    dest_state = dest
                transitions.setdefault(state, {})
                transitions[state][symbol] = dest_state

        return DFA(
            states=set(definition.states),
            alphabet=set(definition.alphabet),
            initial_state=definition.initial_state,
            final_states=set(definition.final_states),
            transitions=transitions,
        )

    def _nfa_from_dfa(self, dfa: DFA) -> NFA:
        """Trivial conversion: DFA is already an NFA with no epsilons."""
        transitions = {}
        for state, inner in dfa.transitions.items():
            for symbol, dest in inner.items():
                transitions.setdefault(state, {})
                transitions[state].setdefault(symbol, set()).add(dest)
        return NFA(
            states=set(dfa.states),
            alphabet=set(dfa.alphabet),
            initial_state=dfa.initial_state,
            final_states=set(dfa.final_states),
            transitions=transitions,
        )

    # ---- helpers to go from objects to definitions ----

    def _definition_from_nfa(self, nfa: NFA) -> AutomatonDefinition:
        tf = {}
        for state, inner in nfa.transitions.items():
            tf.setdefault(state, {})
            for symbol, dests in inner.items():
                key = EPSILON_SYMBOL if symbol is None else symbol
                tf[state][key] = sorted(dests)
        return AutomatonDefinition(
            kind="NFA",
            states=set(nfa.states),
            alphabet=set(sym for sym in nfa.alphabet if sym is not None),
            initial_state=nfa.initial_state,
            final_states=set(nfa.final_states),
            transition_function=tf,
        )

    def _definition_from_dfa(self, dfa: DFA) -> AutomatonDefinition:
        tf = {}
        for state, inner in dfa.transitions.items():
            tf.setdefault(state, {})
            for symbol, dest in inner.items():
                tf[state][symbol] = dest
        return AutomatonDefinition(
            kind="DFA",
            states=set(dfa.states),
            alphabet=set(dfa.alphabet),
            initial_state=dfa.initial_state,
            final_states=set(dfa.final_states),
            transition_function=tf,
        )
