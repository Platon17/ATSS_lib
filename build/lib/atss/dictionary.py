# atss/dictionary.py
import os

class DictionaryChecker:
    def __init__(self, dictionary_path=None, lang="ru"):
        self.words = set()
        self.lang = lang
        # Если путь не передан, пытаемся загрузить дефолт для языка
        self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        """Загружает словарь. Если файла нет, создает базовый набор в зависимости от языка."""
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip().lower()
                        if len(word) > 1: 
                            self.words.add(word)
                return
            except Exception as e:
                print(f"[ATSS ERROR] Ошибка чтения словаря: {e}")

        # --- FALLBACK (Встроенные словари) ---
        if self.lang == "en":
            self.words = {
                "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
                "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
                "this", "but", "his", "by", "from", "bird", "cage", "fly", "sky",
                "freedom", "eagle", "fate", "garden", "secret", "code", "hidden",
                "message", "steganography", "agent", "spy", "system", "data",
                "tree", "water", "river", "moon", "sun", "stars", "night", "day",
                "help", "sos", "save", "me", "danger", "look", "first", "last"
            }
        else:
            # Дефолтный русский
            self.words = {
                "птичка", "клетке", "птичку", "воле", "саду", "орёл", "судьбе",
                "в", "на", "с", "по", "из", 
                "лит", "хабаровск", "стеганография",
                "лицей", "храм", "науки", "добра", "интеллект",
                "технологий", "будущего", "светлые", "умы",
                "базы", "данных", "код", "охрана", "вирусов",
                "системы", "каждый", "бит", "сокрытие", "тайны",
                "единый", "глубоко", "алгоритмы", "научились",
                "агент", "шпион",
                "лес", "шумел", "ивы", "вода", "трава",
                "ворона", "будет", "три", "пруду",
                "золотистые", "привет"
            }

    def calculate_score_and_segment(self, text):
        """
        Жадный алгоритм поиска слов.
        Возвращает: (score, readable_text)
        """
        if not text:
            return 0.0, ""

        clean_text = text.lower()
        n = len(clean_text)
        if n == 0:
            return 0.0, ""

        recognized_chars = 0
        result_segments = []
        i = 0
        
        while i < n:
            found_word = None
            # Ограничиваем длину слова для поиска (оптимизация)
            max_len = min(25, n - i)
            
            for length in range(max_len, 1, -1):
                sub = clean_text[i : i + length]
                if sub in self.words:
                    found_word = sub
                    break
            
            if found_word:
                result_segments.append(found_word.upper()) 
                recognized_chars += len(found_word)
                i += len(found_word)
            else:
                result_segments.append(clean_text[i])
                i += 1

        score = recognized_chars / n
        readable_text = " ".join(result_segments)
        return score, readable_text