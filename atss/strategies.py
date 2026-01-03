# atss/strategies.py
import re

class StegoAnalyzer:
    def __init__(self):
        self.strategies = [
            # --- Базовые стратегии ---
            ("Первые буквы строк", self.get_first_letters),
            ("Последние буквы строк", self.get_last_letters),
            ("Первые буквы предложений", self.get_first_letters_sentences_strict),
            
            # --- НОВЫЕ СТРАТЕГИИ (Фокус на начало и конец текста) ---
            ("Первые буквы (Начало - 50 строк)", self.get_first_letters_head),
            ("Первые буквы (Конец - 50 строк)", self.get_first_letters_tail),
            
            # --- Дополнительные ---
            ("Вторые буквы строк", self.get_second_letters_clean),
            ("Первые буквы ВТОРОГО слова", self.get_first_letters_second_word),
            ("Края строк (1-я + Последняя)", self.get_first_and_last_combined),
        ]

    def prepare_lines(self, text):
        if not text:
            return []
        # Удаляем пустые строки, так как они сбивают акростих
        return [line.strip() for line in text.split('\n') if line.strip()]

    def analyze(self, text):
        lines = self.prepare_lines(text)
        results = {}
        if not text:
            return results

        for name, strategy_func in self.strategies:
            try:
                # Некоторые функции работают с полным текстом, некоторые со списком строк
                if strategy_func == self.get_first_letters_sentences_strict:
                    candidate = strategy_func(text)
                else:
                    candidate = strategy_func(lines)
                
                # Чистим от всего, кроме букв
                candidate_clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', candidate)
                
                # Если кандидат слишком короткий, отбрасываем
                if len(candidate_clean) > 2:
                    results[name] = candidate_clean
            except Exception:
                continue
        return results

    # --- Методы извлечения ---

    def get_first_letters_head(self, lines):
        """Берет только первые 50 непустых строк"""
        limit = 50
        subset = lines[:limit]
        return self.get_first_letters(subset)

    def get_first_letters_tail(self, lines):
        """Берет только последние 50 непустых строк"""
        limit = 50
        # Если строк меньше лимита, берем все
        if len(lines) < limit:
            return self.get_first_letters(lines)
        subset = lines[-limit:]
        return self.get_first_letters(subset)

    def get_first_letters_sentences_strict(self, text):
        one_line = text.replace('\n', ' ')
        # Разбиваем по знакам конца предложения
        sentences = re.split(r'(?<=[.!?])\s+', one_line)
        res = []
        for s in sentences:
            match = re.search(r'[а-яА-Яa-zA-Z]', s.strip())
            if match: res.append(match.group(0))
        return "".join(res)

    def get_first_letters(self, lines):
        return "".join([line[0] for line in lines if len(line) > 0])

    def get_last_letters(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if clean: res.append(clean[-1])
        return "".join(res)

    def get_first_and_last_combined(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2: res.append(clean[0] + clean[-1])
            elif len(clean) == 1: res.append(clean[0])
        return "".join(res)

    def get_second_letters_clean(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2: res.append(clean[1])
        return "".join(res)

    def get_first_letters_second_word(self, lines):
        res = []
        for line in lines:
            words = line.split()
            if len(words) >= 2:
                word = re.sub(r'[^а-яА-Яa-zA-Z]', '', words[1])
                if word: res.append(word[0])
        return "".join(res)