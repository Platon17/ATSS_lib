# atss/cli.py
import argparse
import os
import sys
from .core import ATSS, atss_conf

def main():
    parser = argparse.ArgumentParser(description="ATSS: AcroText Steganography Solver")
    
    parser.add_argument("-in", "--input", dest="input_file", required=True,
                        help="Путь к входному файлу (.txt)")
    parser.add_argument("-wl", "--wordlist", dest="wordlist", default=None,
                        help="Путь к файлу словаря")
    parser.add_argument("--lang", dest="lang", default="ru",
                        help="Язык (влияет только на дефолтные настройки)")
    
    args = parser.parse_args()

    # Настройка
    atss_conf.lang = args.lang
    wl_path = args.wordlist if args.wordlist else atss_conf.wl

    if not os.path.exists(args.input_file):
        print(f"[ATSS] Ошибка: Файл '{args.input_file}' не найден.")
        sys.exit(1)

    # Запуск анализатора
    app = ATSS(input_file=args.input_file, wordlist=wl_path)

    print(f"\n--- Результаты ATSS для: {args.input_file} ---")
    
    if not app.ex_words:
        print("Скрытых сообщений не обнаружено (или словарь не подходит).")
    else:
        print(f"{'МЕТОД':<35} | {'ТЕКСТ'}")
        print("-" * 80)
        for method, text in app.ex_words.items():
            display_text = (text[:60] + '...') if len(text) > 60 else text
            print(f"{method:<35} | {display_text}")
    print("-" * 80)

if __name__ == "__main__":
    main()