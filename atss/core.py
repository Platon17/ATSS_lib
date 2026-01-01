# atss/core.py
import os
import codecs
from .dictionary import DictionaryChecker
from .strategies import StegoAnalyzer

class Config:
    def __init__(self):
        self.defaults = {
            "ru": "russian_words.txt",
            "en": "english_words.txt"
        }

atss_conf = Config()

class ATSS:
    def __init__(self, input_file=None, text=None, wordlist=None, lang="ru", threshold=0.3):
        self.lang = lang
        
        # Выбор словаря
        if wordlist:
            wl_path = wordlist
        else:
            wl_path = atss_conf.defaults.get(lang, "russian_words.txt")
        
        self.checker = DictionaryChecker(dictionary_path=wl_path, lang=self.lang)
        self.analyzer = StegoAnalyzer()
        self.threshold = threshold
        
        self.raw_text = ""
        # ex_words будет словарем вида: { "Method Name": {data...} }
        self.ex_words = {} 

        if input_file:
            self._load_from_file(input_file)
        elif text:
            self.raw_text = text
        
        if self.raw_text:
            self._run_analysis()

    def _load_from_file(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.raw_text = f.read()
        else:
            print(f"[ATSS WARN] Файл '{path}' не найден.")

    def _run_analysis(self):
        # Получаем "сырые" кандидаты от стратегий
        candidates = self.analyzer.analyze(self.raw_text)
        
        # Список трансформаций: (Название, Функция)
        transforms = [
            ("Plain", lambda s: s),
            ("ROT13", lambda s: codecs.encode(s, 'rot_13'))
        ]

        for method, raw_string in candidates.items():
            for t_name, t_func in transforms:
                # Применяем трансформацию (Plain или ROT13)
                processed_string = t_func(raw_string)
                
                # Проверяем по словарю
                score, segmented = self.checker.calculate_score_and_segment(processed_string)
                
                # Формируем уникальный ключ метода, например: "Первые буквы [ROT13]"
                key_method = method if t_name == "Plain" else f"{method} [{t_name}]"

                if score > self.threshold:
                    self.ex_words[key_method] = {
                        "text": segmented,
                        "raw": processed_string,
                        "score": round(score, 4),
                        "transformation": t_name,
                        "original_method": method
                    }