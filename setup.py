``` bash
pip install .
```
#CODE
``` python
from atss import ATSS, atss_conf

# Глобальная настройка (опционально)
atss_conf.wl = "my_words.txt"

# Создаем анализатор (вместо 'in' используем 'input_file')
a = ATSS(input_file="letter.txt")

# Смотрим результат
print(a.ex_words)
```
#CLI
``` bash
atss -in "letter.txt" -wl "russian_words.txt"
```