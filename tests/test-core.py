import unittest
import sys
import os

# Добавляем корневую директорию в путь, чтобы видеть пакет atss
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atss.core import ATSS
from atss.dictionary import DictionaryChecker
from atss.strategies import StegoAnalyzer

class TestATSS(unittest.TestCase):
    
    def test_dictionary_checker_ru(self):
        """Проверка работы русского словаря и сегментации"""
        checker = DictionaryChecker(lang="ru")
        # Имитируем отсутствие файла, чтобы загрузился встроенный fallback-словарь
        checker.load_dictionary("non_existent_file.txt")
        
        # В fallback словаре есть "птичка" и "клетке"
        raw = "птичкавклетке"
        score, text = checker.calculate_score_and_segment(raw)
        
        # ДОБАВЛЕНО: .upper() для игнорирования регистра
        self.assertEqual(text.upper(), "ПТИЧКА В КЛЕТКЕ")
        self.assertGreater(score, 0.8)

    def test_dictionary_checker_en(self):
        """Проверка английского словаря"""
        checker = DictionaryChecker(lang="en")
        checker.load_dictionary("non_existent_file.txt") # Грузим fallback
        
        raw = "thebirdinthecage"
        score, text = checker.calculate_score_and_segment(raw)
        
        self.assertEqual(text, "THE BIRD IN THE CAGE")

    def test_strategies(self):
        """Проверка извлечения первых букв"""
        analyzer = StegoAnalyzer()
        text = "Alpha\nBravo\nCharlie"
        
        results = analyzer.analyze(text)
        self.assertIn("Первые буквы строк", results)
        self.assertEqual(results["Первые буквы строк"], "ABC")

    def test_full_analysis_ru(self):
        """Интеграционный тест: Русский текст"""
        # Текст: Первые буквы -> АГЕНТ
        text = "Акула плывет\nГром гремит\nЕнот бежит\nНочь темна\nТень упала"
        
        app = ATSS(text=text, lang="ru", threshold=0.1)
        
        found = False
        for method, data in app.ex_words.items():
            if "АГЕНТ" in data["text"]:
                found = True
                break
        self.assertTrue(found, "Не найдено слово АГЕНТ в русском тексте")

    def test_full_analysis_en_rot13(self):
        """Интеграционный тест: Английский + ROT13"""
        # Скрыто: DATA (ROT13 -> QNGN)
        # Q -> Queen
        # N -> Night
        # G -> Gold
        # N -> Now
        text = "Queen is here\nNight falls\nGold mine\nNow or never"
        
        app = ATSS(text=text, lang="en", threshold=0.1)
        
        found_rot13 = False
        for key, data in app.ex_words.items():
            # Мы ищем ключ, который содержит пометку ROT13 и правильный текст
            if "ROT13" in data["transformation"] and "DATA" in data["text"]:
                found_rot13 = True
        
        self.assertTrue(found_rot13, "Не обнаружено слово DATA через ROT13")

if __name__ == '__main__':
    unittest.main()