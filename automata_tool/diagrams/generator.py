from typing import Optional
import os

from automata_tool.automata.nfa import NFA
from automata_tool.automata.dfa import DFA


def automaton_to_dot(automaton, name: str = "Automaton") -> str:
    """Return a Graphviz DOT representation of an NFA or DFA."""
    lines = [
        "digraph {",
        "  rankdir=LR;",
        "  node [shape=circle];",
        '  "__start__" [shape=point];',
    ]

    # Final states as doublecircle
    for state in automaton.states:
        shape = "doublecircle" if state in automaton.final_states else "circle"
        lines.append(f'  "{state}" [shape={shape}];')

    # Edge from pseudo start to real start
    lines.append(f'  "__start__" -> "{automaton.initial_state}";')

    # Transitions
    if isinstance(automaton, NFA):
        for state, inner in automaton.transitions.items():
            for symbol, dests in inner.items():
                label = symbol if symbol is not None else "ε"
                for dest in dests:
                    lines.append(f'  "{state}" -> "{dest}" [label="{label}"];')
    elif isinstance(automaton, DFA):
        for state, inner in automaton.transitions.items():
            for symbol, dest in inner.items():
                lines.append(f'  "{state}" -> "{dest}" [label="{symbol}"];')
    else:
        raise TypeError("Solo se pueden dibujar NFAs o DFAs.")

    lines.append("}")
    return "\n".join(lines)


def save_automaton_diagram(automaton, filepath_base: str, name: Optional[str] = None) -> str:
    """Save DOT (and optionally PNG if graphviz is available) for the automaton.

    Returns the path of the DOT file.
    """
    if name is None:
        name = "Automaton"
    dot = automaton_to_dot(automaton, name=name)

    dot_path = filepath_base + ".dot"
    os.makedirs(os.path.dirname(dot_path) or ".", exist_ok=True)
    with open(dot_path, "w", encoding="utf-8") as f:
        f.write(dot)

    # Try to render PNG using graphviz (optional)
    try:
        import graphviz  # type: ignore
        src = graphviz.Source(dot)
        # cleanup=True removes intermediate .gv file if created
        src.render(filepath_base, format="png", cleanup=True)
    except Exception:
        # If graphviz is not installed, silently ignore; the .dot file is still usable.
        pass

    return dot_path
