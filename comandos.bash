python3 -m automata_tool.cli.main from-regex "a(b|c)*" \
  --string "abcb" \
  --string "ac" \
  --string "abb" \
  --output-dir diagrams

python3 -m automata_tool.cli.main from-definition mi_automata.json \
  --string "101" \
  --string "000" \
  --output-dir diagrams

#!/usr/bin/env bash
set -e

# Opcional: ajusta esta ruta si es necesario
# cd ~/cidetec/tc/automata_tool_project

#######################################
# 1. Concatenación simple
#######################################
echo "### 1. Concatenación simple: regex = ab"
python3 -m automata_tool.cli.main from-regex "ab" \
  --string "ab" \
  --string "a" \
  --string "b" \
  --string "abc" \
  --output-dir diagrams/concat


#######################################
# 2. Unión (|)
#######################################
echo
echo "### 2.1 Unión simple: regex = a|b"
python3 -m automata_tool.cli.main from-regex "a|b" \
  --string "a" \
  --string "b" \
  --string "ab" \
  --string "" \
  --output-dir diagrams/union1

echo
echo "### 2.2 Unión con cadenas compuestas: regex = (ab|cd)"
python3 -m automata_tool.cli.main from-regex "(ab|cd)" \
  --string "ab" \
  --string "cd" \
  --string "abc" \
  --string "ad" \
  --output-dir diagrams/union2


#######################################
# 3. Cerradura de Kleene (*)
#######################################
echo
echo "### 3.1 Kleene simple: regex = a*"
python3 -m automata_tool.cli.main from-regex "a*" \
  --string "" \
  --string "a" \
  --string "aaaa" \
  --string "b" \
  --output-dir diagrams/star1

echo
echo "### 3.2 Kleene sobre bloque: regex = (ab)*"
python3 -m automata_tool.cli.main from-regex "(ab)*" \
  --string "" \
  --string "ab" \
  --string "abab" \
  --string "aba" \
  --output-dir diagrams/star2


#######################################
# 4. Cerradura positiva (+)
#######################################
echo
echo "### 4.1 Positiva simple: regex = a+"
python3 -m automata_tool.cli.main from-regex "a+" \
  --string "" \
  --string "a" \
  --string "aa" \
  --string "b" \
  --output-dir diagrams/plus1

echo
echo "### 4.2 Positiva sobre bloque: regex = (ab)+"
python3 -m automata_tool.cli.main from-regex "(ab)+" \
  --string "ab" \
  --string "abab" \
  --string "" \
  --string "aba" \
  --output-dir diagrams/plus2


#######################################
# 5. Opción (?)
#######################################
echo
echo "### 5.1 Opción simple: regex = ab?c"
python3 -m automata_tool.cli.main from-regex "ab?c" \
  --string "ac" \
  --string "abc" \
  --string "abbc" \
  --string "ab" \
  --output-dir diagrams/opt1

echo
echo "### 5.2 Opción con unión: regex = (a|b)?c"
python3 -m automata_tool.cli.main from-regex "(a|b)?c" \
  --string "c" \
  --string "ac" \
  --string "bc" \
  --string "abc" \
  --output-dir diagrams/opt2


#######################################
# 6. Combinación: unión + Kleene
#######################################
echo
echo "### 6. Combinación: regex = a(b|c)*"
python3 -m automata_tool.cli.main from-regex "a(b|c)*" \
  --string "a" \
  --string "ab" \
  --string "ac" \
  --string "abcb" \
  --string "ba" \
  --string "" \
  --output-dir diagrams/comb1


#######################################
# 7. Combinación: concatenación + +
#######################################
echo
echo "### 7. Combinación: regex = (ab)+c"
python3 -m automata_tool.cli.main from-regex "(ab)+c" \
  --string "abc" \
  --string "ababc" \
  --string "c" \
  --string "ab" \
  --output-dir diagrams/comb2


#######################################
# 8. Con dígitos en el alfabeto
#######################################
echo
echo "### 8.1 Dígitos con unión y Kleene: regex = 1(2|3)*4"
python3 -m automata_tool.cli.main from-regex "1(2|3)*4" \
  --string "14" \
  --string "124" \
  --string "134" \
  --string "1324" \
  --string "1235" \
  --string "4" \
  --output-dir diagrams/digits1

echo
echo "### 8.2 Letras + dígitos: regex = (a1)+b"
python3 -m automata_tool.cli.main from-regex "(a1)+b" \
  --string "a1b" \
  --string "a1a1b" \
  --string "ab" \
  --string "a1" \
  --output-dir diagrams/digits2


#######################################
# 9. Combinación más grande
#######################################
echo
echo "### 9. Combinación compleja: regex = (ab|cd)*e"
python3 -m automata_tool.cli.main from-regex "(ab|cd)*e" \
  --string "e" \
  --string "abe" \
  --string "cde" \
  --string "abcdabe" \
  --string "abce" \
  --output-dir diagrams/comb3

echo
echo "### Pruebas de regex completadas."
