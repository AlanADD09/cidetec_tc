
# automata_tool

Proyecto en Python para:

- Aceptar como entrada una **expresión regular** o la **quíntupla** de un autómata finito (NFA/DFA).
- Generar como salida:
  - Un **NFA** equivalente.
  - Un **DFA** equivalente.
- Verificar si una **cadena de entrada** es aceptada o no.
- Inferir la **quíntupla** de ambos autómatas.
- Generar el **diagrama** de ambos autómatas en formato Graphviz DOT (y PNG si tienes `graphviz` instalado).

## Instalación rápida

```bash
cd automata_project
python -m pip install graphviz  # opcional, solo si quieres PNG directamente
```

> **Nota:** Para las imágenes PNG necesitas:
> - El paquete de Python `graphviz`.
> - El binario de Graphviz instalado en el sistema (`dot`, etc.).
> Si no lo tienes, el proyecto generará siempre los archivos `.dot`, que puedes renderizar con:
> ```bash
> dot -Tpng nfa_from_regex.dot -o nfa_from_regex.png
> ```

## Uso básico (desde expresión regular)

Desde la carpeta raíz del proyecto:

```bash
python -m automata_tool.cli.main from-regex "a(b|c)*" --string "abcb" --output-dir diagrams
```

- Imprime en pantalla la quíntupla del NFA y el DFA.
- Genera archivos:
  - `diagrams/nfa_from_regex.dot`
  - `diagrams/dfa_from_regex.dot`
  - y si tienes Graphviz, también `*.png`.

El alfabeto permitido para la expresión regular es:
- Caracteres `a`–`z`, `A`–`Z`, `0`–`9` como literales.
- Operadores:
  - `|` unión
  - concatenación implícita
  - `*` cerradura de Kleene
  - `+` cerradura positiva
  - `?` opcional
  - paréntesis `(` y `)`.

## Uso con quíntupla en JSON

Crea un archivo `mi_automata.json` como:

```json
{
  "kind": "DFA",
  "states": ["q0", "q1"],
  "alphabet": ["0", "1"],
  "initial_state": "q0",
  "final_states": ["q1"],
  "transition_function": {
    "q0": { "0": "q0", "1": "q1" },
    "q1": { "0": "q1", "1": "q1" }
  }
}
```

Para NFA, las transiciones pueden ser listas, y las epsilon-transiciones usan la clave `"ε"`:

```json
{
  "kind": "NFA",
  "states": ["q0", "q1"],
  "alphabet": ["a"],
  "initial_state": "q0",
  "final_states": ["q1"],
  "transition_function": {
    "q0": { "ε": ["q1"], "a": ["q1"] }
  }
}
```

Ejecuta:

```bash
python -m automata_tool.cli.main from-definition mi_automata.json --string "101" --output-dir diagrams
```

## API en Python

```python
from automata_tool.core import AutomatonFactory, is_string_accepted_by_regex

factory = AutomatonFactory()
result = factory.from_regex("a(b|c)*")

nfa = result["nfa"]
dfa = result["dfa"]
nfa_def = result["nfa_def"]
dfa_def = result["dfa_def"]

print(dfa.accepts("abcb"))  # True/False

# Validar de forma directa:
print(is_string_accepted_by_regex("a(b|c)*", "abcb"))
```

El diseño está pensado para que puedas extender:

- Nuevos operadores de regex (por ejemplo, rangos).
- Minimización de DFAs.
- Serialización más avanzada.
