# atss/core.py
import os
from .dictionary import DictionaryChecker
from .strategies import StegoAnalyzer

class Config:
    def __init__(self):
        self.lang = "ru"
        self.wl = "russian_words.txt" # Дефолтное имя словаря

atss_conf = Config()

class ATSS:
    def __init__(self, input_file=None, text=None, wordlist=None, threshold=0.3):
        """
        :param input_file: путь к файлу (аналог CLI '-in')
        :param text: прямой текст для анализа
        :param wordlist: путь к словарю
        :param threshold: порог уверенности (0.0 - 1.0)
        """
        wl_path = wordlist if wordlist else atss_conf.wl
        self.checker = DictionaryChecker(wl_path)
        self.analyzer = StegoAnalyzer()
        self.threshold = threshold
        
        self.raw_text = ""
        self.results = {}  # Полные результаты
        self.ex_words = {} # Только найденные (score > threshold)

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
        candidates = self.analyzer.analyze(self.raw_text)
        
        for method, raw_string in candidates.items():
            score, segmented = self.checker.calculate_score_and_segment(raw_string)
            
            self.results[method] = {
                "score": score,
                "text": segmented,
                "raw": raw_string
            }

            if score > self.threshold:
                self.ex_words[method] = segmented