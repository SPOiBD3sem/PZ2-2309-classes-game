from characters import Warrior, Mage, Healer
from bosses import Boss
from battle import Battle
import random
import os
import json


def select_difficulty():
    """Выбор уровня сложности"""
    print("\nВыберите уровень сложности:")
    print("1. Легкий - босс слабее, персонажи сильнее")
    print("2. Средний - стандартный баланс")
    print("3. Сложный - босс сильнее, персонажи слабее")
    print("4. Хардкор - босс очень сильный, ограниченные ресурсы")
    print("Выбор уровня сложности влияет на максимальное количество здоровья босса, а также на силу атаки и некоторые другие незначительные характеристики босса и персонажей")
    while True:
        try:
            choice = int(input("Выберите сложность (1-4): "))
            if 1 <= choice <= 4:
                difficulties = {
                    1: "easy",
                    2: "normal",
                    3: "hard",
                    4: "hardcore"
                }
                return difficulties[choice]
            else:
                print("Неверный выбор! Введите число от 1 до 4.")
        except ValueError:
            print("Пожалуйста, введите число!")


def create_party(difficulty):
    """Создание группы с учетом сложности"""
    party = []

    # Модификаторы сложности для персонажей
    difficulty_modifiers = {
        "easy": {"hp_multiplier": 1.3, "mp_multiplier": 1.2, "stats_multiplier": 1.1},
        "normal": {"hp_multiplier": 1.0, "mp_multiplier": 1.0, "stats_multiplier": 1.0},
        "hard": {"hp_multiplier": 0.8, "mp_multiplier": 0.9, "stats_multiplier": 0.9},
        "hardcore": {"hp_multiplier": 0.7, "mp_multiplier": 0.8, "stats_multiplier": 0.8}
    }

    mod = difficulty_modifiers[difficulty]

    print(f"\nСложность: {difficulty.upper()}")
    print("Доступные классы:")
    print("1. Воин - высокая защита и физический урон")
    print("2. Маг - магический урон и защитные навыки")
    print("3. Лекарь - лечение и поддержка")

    party_size = 0
    while party_size < 3 or party_size > 4:
        try:
            party_size = int(input("Выберите размер группы (3-4): "))
        except ValueError:
            print("Пожалуйста, введите число!")

    for i in range(party_size):
        print(f"\nСоздание персонажа {i + 1}:")
        name = input("Введите имя персонажа: ")

        while True:
            try:
                class_choice = int(input("Выберите класс (1-3): "))
                if class_choice == 1:
                    character = Warrior(name)
                    break
                elif class_choice == 2:
                    character = Mage(name)
                    break
                elif class_choice == 3:
                    character = Healer(name)
                    break
                else:
                    print("Неверный выбор класса!")
            except ValueError:
                print("Пожалуйста, введите число!")

        # Применяем модификаторы сложности
        character.max_hp = int(character.max_hp * mod["hp_multiplier"])
        character.hp = character.max_hp
        character.max_mp = int(character.max_mp * mod["mp_multiplier"])
        character.mp = character.max_mp
        character.strength = int(character.strength * mod["stats_multiplier"])
        character.agility = int(character.agility * mod["stats_multiplier"])
        character.intelligence = int(character.intelligence * mod["stats_multiplier"])

        party.append(character)
        print(f"Создан {character.__class__.__name__}: {character}")

    return party


def create_boss(difficulty, level=10):
    """Создание босса с учетом сложности"""
    # Модификаторы сложности для босса
    difficulty_modifiers = {
        "easy": {"hp_multiplier": 0.7, "stats_multiplier": 0.8, "damage_multiplier": 0.8},
        "normal": {"hp_multiplier": 1.0, "stats_multiplier": 1.0, "damage_multiplier": 1.0},
        "hard": {"hp_multiplier": 1.3, "stats_multiplier": 1.2, "damage_multiplier": 1.2},
        "hardcore": {"hp_multiplier": 1.6, "stats_multiplier": 1.4, "damage_multiplier": 1.5}
    }

    mod = difficulty_modifiers[difficulty]
    boss = Boss("Древний Великан", level)

    # Применяем модификаторы
    boss.max_hp = int(boss.max_hp * mod["hp_multiplier"])
    boss.hp = boss.max_hp
    boss.max_mp = int(boss.max_mp * mod["stats_multiplier"])
    boss.mp = boss.max_mp
    boss.strength = int(boss.strength * mod["stats_multiplier"])
    boss.agility = int(boss.agility * mod["stats_multiplier"])
    boss.intelligence = int(boss.intelligence * mod["stats_multiplier"])
    boss.damage_multiplier = mod["damage_multiplier"]

    return boss


def list_save_files():
    """Список файлов сохранения"""
    return [f for f in os.listdir(".") if f.endswith(".json")]


def load_save_file(filename):
    """Загрузка сохранения"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'

        with open(filename, 'r', encoding='utf-8') as f:
            state = json.load(f)

        print(f"\nЗагружаем: {filename}")

        # Воссоздаем группу
        party = []
        for char_data in state["party"]:
            name = char_data["name"]
            class_name = char_data["class"]

            if class_name == "Warrior":
                character = Warrior(name)
            elif class_name == "Mage":
                character = Mage(name)
            elif class_name == "Healer":
                character = Healer(name)
            else:
                continue

            character.hp = char_data["hp"]
            character.mp = char_data["mp"]
            party.append(character)

        # Создаем босса
        boss = Boss("Древний Великан", 10)
        boss.hp = state["boss_hp"]
        boss.mp = state["boss_mp"]

        battle = Battle(party, boss)
        battle.round = state["round"]

        print("✓ Игра загружена!")
        return battle

    except Exception as e:
        print(f"✗ Ошибка загрузки: {e}")
        return None


def main_menu():
    """Главное меню"""
    print("\n" + "=" * 50)
    print("=== ПАТИ ПРОТИВ БОССА ===")
    print("1. Новая игра")
    print("2. Загрузить игру")
    print("3. Выход")

    while True:
        try:
            choice = input("Выберите действие (1-3): ").strip()
            if choice == "1":
                return new_game()
            elif choice == "2":
                return load_game_menu()
            elif choice == "3":
                exit()
            else:
                print("Неверный выбор!")
        except KeyboardInterrupt:
            exit()


def new_game():
    """Новая игра"""
    print("\n=== НОВАЯ ИГРА ===")

    # Выбор сложности
    difficulty = select_difficulty()

    # Seed
    seed = input("Введите seed (или Enter для случайного): ").strip()
    if seed:
        random.seed(seed)
        print(f"Seed: {seed}")

    # Создание группы и босса
    party = create_party(difficulty)
    boss = create_boss(difficulty)

    print(f"\nБосс ({difficulty.upper()}): {boss}")
    input("Нажмите Enter чтобы начать...")

    return Battle(party, boss)


def load_game_menu():
    """Меню загрузки"""
    print("\n=== ЗАГРУЗКА ИГРЫ ===")

    save_files = list_save_files()
    if not save_files:
        print("Нет сохранений!")
        return main_menu()

    print("\nСохранения:")
    for i, filename in enumerate(save_files, 1):
        print(f"{i}. {filename}")
    print(f"{len(save_files) + 1}. Назад")

    try:
        choice = int(input("Выберите сохранение: "))
        if choice == len(save_files) + 1:
            return main_menu()
        elif 1 <= choice <= len(save_files):
            battle = load_save_file(save_files[choice - 1])
            if battle:
                input("Нажмите Enter чтобы продолжить...")
                return battle
    except (ValueError, IndexError):
        print("Неверный выбор!")

    return main_menu()


def main():
    """Основная функция"""
    try:
        while True:
            battle = main_menu()
            if battle:
                battle.start_battle()

            # После боя
            print("\n1. Новая игра")
            print("2. Выход")
            choice = input("Выберите действие (1-2): ").strip()
            if choice != "1":
                break

    except KeyboardInterrupt:
        print("\nВыход...")


if __name__ == "__main__":
    main()