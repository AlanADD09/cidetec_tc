
from .factory import AutomatonFactory
from .definitions import AutomatonDefinition

def is_string_accepted_by_regex(regex: str, s: str) -> bool:
    factory = AutomatonFactory()
    result = factory.from_regex(regex)
    dfa = result["dfa"]
    return dfa.accepts(s)

def is_string_accepted_by_definition(definition: AutomatonDefinition, s: str) -> bool:
    factory = AutomatonFactory()
    result = factory.from_definition(definition)
    dfa = result["dfa"]
    return dfa.accepts(s)
