
import argparse
import json
import os
from typing import Any

from automata_tool.core import (
    AutomatonFactory,
    AutomatonDefinition,
    EPSILON_SYMBOL,
    is_string_accepted_by_regex,
    is_string_accepted_by_definition,
)
from automata_tool.diagrams import save_automaton_diagram

def _load_definition_from_json(path: str) -> AutomatonDefinition:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return AutomatonDefinition.from_dict(data)

def cmd_from_regex(args: argparse.Namespace) -> None:
    factory = AutomatonFactory()
    result = factory.from_regex(args.regex)
    nfa = result["nfa"]
    dfa = result["dfa"]
    nfa_def = result["nfa_def"]
    dfa_def = result["dfa_def"]

    print("=== NFA generado desde la expresión regular ===")
    print(json.dumps(nfa_def.to_dict(), indent=2, ensure_ascii=False))
    print("\n=== DFA equivalente ===")
    print(json.dumps(dfa_def.to_dict(), indent=2, ensure_ascii=False))

    outdir = args.output_dir or "."
    os.makedirs(outdir, exist_ok=True)
    base_nfa = os.path.join(outdir, "nfa_from_regex")
    base_dfa = os.path.join(outdir, "dfa_from_regex")

    nfa_dot = save_automaton_diagram(nfa, base_nfa, name="NFA")
    dfa_dot = save_automaton_diagram(dfa, base_dfa, name="DFA")

    print(f"\nArchivos de diagrama generados:")
    print(f"  NFA: {nfa_dot}")
    print(f"  DFA: {dfa_dot}")

    if args.string:
        results = []
        for s in args.string:
            accepted = dfa.accepts(s)
            estado = "ACEPTADA" if accepted else "RECHAZADA"
            results.append((s, estado))

        print("\nResultados (cadena, estado):")
        print(results)

def cmd_from_definition(args: argparse.Namespace) -> None:
    definition = _load_definition_from_json(args.file)
    factory = AutomatonFactory()
    result = factory.from_definition(definition)
    nfa = result["nfa"]
    dfa = result["dfa"]
    nfa_def = result["nfa_def"]
    dfa_def = result["dfa_def"]

    print("=== NFA (a partir de definición) ===")
    print(json.dumps(nfa_def.to_dict(), indent=2, ensure_ascii=False))
    print("\n=== DFA equivalente ===")
    print(json.dumps(dfa_def.to_dict(), indent=2, ensure_ascii=False))

    outdir = args.output_dir or "."
    os.makedirs(outdir, exist_ok=True)
    base_nfa = os.path.join(outdir, "nfa_from_definition")
    base_dfa = os.path.join(outdir, "dfa_from_definition")

    nfa_dot = save_automaton_diagram(nfa, base_nfa, name="NFA")
    dfa_dot = save_automaton_diagram(dfa, base_dfa, name="DFA")

    print(f"\nArchivos de diagrama generados:")
    print(f"  NFA: {nfa_dot} ")
    print(f"  DFA: {dfa_dot} ")

    if args.string:
        results = []
        for s in args.string:
            accepted = dfa.accepts(s)
            estado = "ACEPTADA" if accepted else "RECHAZADA"
            results.append((s, estado))

        print("\nResultados (cadena, estado):")
        print(results)

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automata_tool",
        description="Construye autómatas finitos (NFA/DFA) desde expresiones regulares o quíntuplas.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # from-regex
    p_regex = subparsers.add_parser(
        "from-regex",
        help="Construir NFA y DFA a partir de una expresión regular.",
    )
    p_regex.add_argument("regex", help="Expresión regular de entrada.")
    p_regex.add_argument(
        "--string",
        action="append",
        help="Cadena(s) a validar contra el DFA generado (puedes repetir esta opción).",
        default=[],
    )
    p_regex.add_argument(
        "--output-dir",
        help="Directorio donde guardar los diagramas (.dot y opcionalmente .png).",
        default=".",
    )
    p_regex.set_defaults(func=cmd_from_regex)

    # from-definition
    p_def = subparsers.add_parser(
        "from-definition",
        help="Construir NFA y DFA a partir de una definición de autómata en JSON.",
    )
    p_def.add_argument(
        "file",
        help="Ruta al archivo JSON con la definición del autómata (quíntupla).",
    )
    p_def.add_argument(
        "--string",
        action="append",
        help="Cadena(s) a validar contra el DFA equivalente (puedes repetir esta opción).",
        default=[],
    )
    p_def.add_argument(
        "--output-dir",
        help="Directorio donde guardar los diagramas (.dot y opcionalmente .png).",
        default=".",
    )
    p_def.set_defaults(func=cmd_from_definition)

    return parser

def main(argv: Any = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
