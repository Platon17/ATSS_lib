# atss/cli.py
import argparse
import os
import sys
import json
from .core import ATSS, atss_conf 

def run_refactor(input_path, output_path):
    """
    Reads the input file, removes specific punctuation/symbols from the start 
    of each line, and writes to the output file.
    """
    if not os.path.exists(input_path):
        print(f"[ATSS] Ошибка: Файл '{input_path}' не найден.", file=sys.stderr)
        return

    chars_to_strip = ".:-,?!—; \t"

    try:
        with open(input_path, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()

        cleaned_lines = []
        count = 0
        for line in lines:
            # lstrip removes any combination of the characters in 'chars_to_strip'
            # from the beginning of the string until it hits a character not in the set.
            original_content = line.rstrip('\n')
            if not original_content:
                cleaned_lines.append(line) # Keep empty lines as is
                continue
                
            new_content = original_content.lstrip(chars_to_strip)
            
            # Re-attach the newline character if it existed
            if line.endswith('\n'):
                cleaned_lines.append(new_content + '\n')
            else:
                cleaned_lines.append(new_content)
            
            if len(new_content) != len(original_content):
                count += 1

        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(cleaned_lines)
            
        print(f"[ATSS] Refactor complete.")
        print(f"       Processed lines: {len(lines)}")
        print(f"       Modified lines:  {count}")
        print(f"       Saved to:        {output_path}")

    except Exception as e:
        print(f"[ATSS] Ошибка при рефакторинге '{input_path}': {e}", file=sys.stderr)

def process_file(filepath, args):
    if not os.path.exists(filepath):
        print(f"[ATSS] Файл '{filepath}' не найден.", file=sys.stderr)
        return None

    try:
        app = ATSS(
            input_file=filepath, 
            wordlist=args.wordlist, 
            lang=args.lang,
            min_length=args.min_length
        )
        return app
    except Exception as e:
        print(f"[ATSS] Ошибка при обработке '{filepath}': {e}", file=sys.stderr)
        return None

def print_text_report(filepath, app):
    print(f"\n=== Файл: {filepath} ===")
    
    if not app or not app.ex_words:
        print("  -> Скрытых сообщений не обнаружено.")
    else:
        sorted_items = sorted(app.ex_words.items(), key=lambda x: x[1]['score'], reverse=True)
        print(f"  {'МЕТОД / ТРАНСФОРМАЦИЯ':<40} | {'SCORE':<6} | {'ТЕКСТ'}")
        print("  " + "-" * 88)
        
        for method_key, data in sorted_items:
            text = data['text']
            score = data['score']
            display_text = (text[:40] + '...') if len(text) > 40 else text
            print(f"  {method_key:<40} | {score:<6} | {display_text}")
    print("-" * 90)

def main():
    parser = argparse.ArgumentParser(description="ATSS: AcroText Steganography Solver")
    
    # --- Mutually Exclusive Group (Main Modes) ---
    group = parser.add_mutually_exclusive_group(required=True)
    
    #файл
    group.add_argument("-in", "--input", dest="input_file",
                        help="Путь к одному входному файлу (.txt) для анализа")
    
    #директория
    group.add_argument("-d", "--directory", dest="directory",
                        help="Путь к директории с файлами для пакетного анализа")
    
    #regactor
    group.add_argument("--refactor", dest="refactor_file",
                        help="Путь к файлу для очистки пунктуации в начале строк")

    #options
    parser.add_argument("-o", "--output", dest="output_file", default=None,
                        help="Путь к выходному файлу (обязателен для --refactor)")

    parser.add_argument("-wl", "--wordlist", dest="wordlist", default=None,
                        help="Путь к файлу словаря")
    parser.add_argument("--lang", dest="lang", default="ru", choices=["ru", "en"],
                        help="Язык анализа: 'ru' или 'en' (default: ru)")
    
    parser.add_argument("-ml", "--min-length", dest="min_length", type=int, default=5,
                        help="Минимальная длина слова для валидации (default: 5)")

    parser.add_argument("--json", dest="json_output", action="store_true",
                        help="Вывести результат анализа в формате JSON")
    
    args = parser.parse_args()

    #refacroring
    if args.refactor_file:
        if not args.output_file:
            print("[ATSS] Ошибка: Для режима --refactor необходимо указать выходной файл через флаг -o", file=sys.stderr)
            sys.exit(1)
        
        run_refactor(args.refactor_file, args.output_file)
        sys.exit(0)

    #analysis
    files_to_process = []
    if args.input_file:
        files_to_process.append(args.input_file)
    elif args.directory:
        if not os.path.isdir(args.directory):
            print(f"[ATSS] Ошибка: Директория '{args.directory}' не найдена.")
            sys.exit(1)
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                if file.endswith(".txt"):
                    files_to_process.append(os.path.join(root, file))
        
        if not files_to_process:
            print(f"[ATSS] В директории '{args.directory}' не найдено .txt файлов.")
            sys.exit(0)

    json_results = []
    if not args.json_output:
        print(f"--- ATSS Start | Lang: {args.lang} | MinLen: {args.min_length} | Files: {len(files_to_process)} ---")

    for filepath in files_to_process:
        app = process_file(filepath, args)
        if not app:
            continue

        if args.json_output:
            file_result = {
                "file": filepath,
                "language": args.lang,
                "min_length": args.min_length,
                "found_messages": app.ex_words
            }
            json_results.append(file_result)
        else:
            print_text_report(filepath, app)

    if args.json_output:
        if args.input_file:
            print(json.dumps(json_results[0] if json_results else {}, ensure_ascii=False, indent=4))
        else:
            print(json.dumps(json_results, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()