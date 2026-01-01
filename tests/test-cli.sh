#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ">>> Генерация тестовых данных..."
python3 tests/generate_data.py

echo -e "\n>>> 1. Тест одиночного файла (Русский)..."
# Запускаем CLI, ищем "ПРИВЕТ" в выводе
OUTPUT=$(python3 -m atss.cli -in tests/data/ru_simple.txt --lang ru)
if echo "$OUTPUT" | grep -q "ПРИВЕТ"; then
    echo -e "${GREEN}[PASS] Русский текст обработан верно.${NC}"
else
    echo -e "${RED}[FAIL] Ошибка обработки русского текста.${NC}"
    echo "$OUTPUT"
    exit 1
fi

echo -e "\n>>> 2. Тест JSON вывода и Английского языка..."
# Ищем "CODE" в JSON
JSON_OUT=$(python3 -m atss.cli -in tests/data/en_last.txt --lang en --json)
if echo "$JSON_OUT" | grep -q "CODE"; then
    echo -e "${GREEN}[PASS] JSON и Английский язык работают.${NC}"
else
    echo -e "${RED}[FAIL] Ошибка в JSON/English.${NC}"
    echo "$JSON_OUT"
    exit 1
fi

echo -e "\n>>> 3. Тест директории (-d) и ROT13..."
# Запускаем на папку. Должен найти "HELP" (расшифровка ROT13 в файле en_rot13.txt)
DIR_OUT=$(python3 -m atss.cli -d tests/data --lang en)
if echo "$DIR_OUT" | grep -q "HELP"; then
    echo -e "${GREEN}[PASS] Пакетная обработка и ROT13 работают.${NC}"
else
    echo -e "${RED}[FAIL] Ошибка в режиме директории или ROT13.${NC}"
    echo "$DIR_OUT"
    exit 1
fi

echo -e "\n${GREEN}=== ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО ===${NC}"