## Setup
``` bash
pip install .
```

## Use (python script)
``` python
from atss import ATSS, atss_conf

# Глобальная настройка (опционально)
atss_conf.wl = "my_words.txt"

# Создаем анализатор (вместо 'in' используем 'input_file')
a = ATSS(input_file="letter.txt")

# Смотрим результат
print(a.ex_words)
```

## Use (CLI)
``` bash
atss -in "letter.txt" -wl "russian_words.txt"
```

Russian 1.5M wordlist -> https://github.com/danakt/russian-words
