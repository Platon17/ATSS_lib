import os

def create_data():
    os.makedirs("tests/data", exist_ok=True)

    # 1. Русский: Первые буквы -> ПРИВЕТ
    ru_text = """
Поля покрыты белым снегом
Река замерзла уж давно
Иней на ветках серебрится
Ветер гудит в печной трубе
Ель зеленеет у ворот
Тишина стоит кругом
"""
    with open("tests/data/ru_simple.txt", "w", encoding="utf-8") as f:
        f.write(ru_text.strip())

    # 2. Английский: Последние буквы -> CODE
    # Music -> c, Hero -> o, Road -> d, Love -> e
    en_text = """
I love magic
Be my hero
On the road
Full of love
"""
    with open("tests/data/en_last.txt", "w", encoding="utf-8") as f:
        f.write(en_text.strip())

    # 3. Английский ROT13: Первые буквы
    # Скрытое слово: HELP
    # ROT13("HELP") = "URYC"
    # U -> Under
    # R -> Run
    # Y -> Yellow
    # C -> Call
    en_rot13_text = """
Under the bridge
Run away fast
Yellow birds fly
Call me now
"""
    with open("tests/data/en_rot13.txt", "w", encoding="utf-8") as f:
        f.write(en_rot13_text.strip())

    print("[+] Тестовые данные сгенерированы в tests/data/")

if __name__ == "__main__":
    create_data()