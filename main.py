from characters import Warrior, Mage, Healer
from bosses import Boss
from battle import Battle
import random
import os
import json

def create_party():
    """Создание новой группы"""
    party = []
    
    print("\nДоступные классы:")
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
        
        party.append(character)
        print(f"Создан {character.__class__.__name__}: {character}")
    
    return party

def list_save_files():
    """Показать список файлов сохранения в текущей директории"""
    save_files = []
    current_dir = os.getcwd()
    print(f"\nТекущая директория: {current_dir}")
    
    for file in os.listdir(current_dir):
        if file.endswith(".json"):
            # Покажем размер файла и дату изменения
            file_path = os.path.join(current_dir, file)
            file_size = os.path.getsize(file_path)
            save_files.append((file, file_size))
    
    return save_files

def load_save_file(filename):
    """Загрузка сохранения из файла"""
    try:
        # Добавляем расширение .json если его нет
        if not filename.endswith('.json'):
            filename += '.json'
            
        with open(filename, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        print(f"\nЗагружаем сохранение: {filename}")
        
        # Воссоздаем группу на основе сохраненных данных
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
                print(f"Неизвестный класс: {class_name}")
                continue
            
            character.hp = char_data["hp"]
            character.mp = char_data["mp"]
            party.append(character)
        
        # Создаем босса
        boss = Boss("Древний Великан", 10)
        boss.hp = state["boss_hp"]
        boss.mp = state["boss_mp"]
        
        # Создаем битву
        battle = Battle(party, boss)
        battle.round = state["round"]
        
        print("✓ Игра успешно загружена!")
        print(f"Раунд: {state['round']}")
        print(f"Босс: HP {state['boss_hp']}/{boss.max_hp}")
        for char_data in state["party"]:
            char_class = char_data["class"]
            print(f"{char_data['name']} ({char_class}): HP {char_data['hp']}/{char_data.get('max_hp', 100)}")
        
        return battle
    
    except FileNotFoundError:
        print(f"✗ Файл {filename} не найден!")
        print("Проверьте правильность имени файла.")
        return None
    except json.JSONDecodeError:
        print(f"✗ Ошибка чтения файла {filename}!")
        print("Файл поврежден или имеет неверный формат.")
        return None
    except Exception as e:
        print(f"✗ Ошибка при загрузке: {e}")
        return None

def main_menu():
    """Главное меню игры"""
    print("\n" + "="*50)
    print("=== ПАТИ ПРОТИВ БОССА ===")
    print("1. Новая игра")
    print("2. Загрузить игру")
    print("3. Выход")
    print("="*50)
    
    while True:
        try:
            choice = input("Выберите действие (1-3): ").strip()
            
            if choice == "1":
                return new_game()
            elif choice == "2":
                return load_game_menu()
            elif choice == "3":
                print("До свидания!")
                exit()
            else:
                print("Неверный выбор! Введите 1, 2 или 3.")
        
        except KeyboardInterrupt:
            print("\nВыход из игры...")
            exit()

def new_game():
    """Запуск новой игры"""
    print("\n" + "="*50)
    print("=== НОВАЯ ИГРА ===")
    
    # Настройка случайного генератора
    seed = input("Введите seed для случайного генератора (или нажмите Enter для случайного): ").strip()
    if seed:
        random.seed(seed)
        print(f"Используется seed: {seed}")
    
    # Создание группы
    party = create_party()
    
    # Создание босса
    boss_level = 10
    boss = Boss("Древний Великан", boss_level)
    
    print(f"\nВаш противник: {boss}")
    input("Нажмите Enter чтобы начать бой...")
    
    # Запуск боя
    battle = Battle(party, boss)
    return battle

def load_game_menu():
    """Меню загрузки игры"""
    print("\n" + "="*50)
    print("=== ЗАГРУЗКА ИГРЫ ===")
    
    save_files = list_save_files()
    
    if not save_files:
        print("Файлы сохранения не найдены в текущей директории!")
        print("Сначала создайте новую игру и сохраните ее.")
        input("Нажмите Enter чтобы вернуться в главное меню...")
        return main_menu()
    
    print(f"\nНайдено сохранений: {len(save_files)}")
    print("\nДоступные сохранения:")
    print("-" * 40)
    
    for i, (filename, file_size) in enumerate(save_files, 1):
        print(f"{i}. {filename} ({file_size} байт)")
    
    print(f"{len(save_files) + 1}. Назад в главное меню")
    print("-" * 40)
    
    while True:
        try:
            choice = input(f"Выберите сохранение (1-{len(save_files) + 1}): ").strip()
            
            if choice == str(len(save_files) + 1):
                return main_menu()
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(save_files):
                filename, _ = save_files[choice_num - 1]
                battle = load_save_file(filename)
                if battle:
                    input("Нажмите Enter чтобы продолжить бой...")
                    return battle
                else:
                    print("Попробуйте выбрать другое сохранение.")
            else:
                print(f"Неверный выбор! Введите число от 1 до {len(save_files) + 1}.")
        
        except ValueError:
            print("Пожалуйста, введите число!")
        except KeyboardInterrupt:
            print("\nВозврат в главное меню...")
            return main_menu()

def main():
    """Основная функция игры"""
    try:
        while True:
            battle = main_menu()
            
            if battle:
                battle.start_battle()
            
            # После окончания боя предлагаем сыграть еще раз
            print("\n" + "="*50)
            print("Бой завершен!")
            print("1. Новая игра")
            print("2. Выход")
            
            while True:
                try:
                    choice = input("Выберите действие (1-2): ").strip()
                    
                    if choice == "1":
                        break
                    elif choice == "2":
                        print("До свидания!")
                        return
                    else:
                        print("Неверный выбор! Введите 1 или 2.")
                
                except KeyboardInterrupt:
                    print("\nВыход из игры...")
                    return
    
    except KeyboardInterrupt:
        print("\nВыход из игры...")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Игра будет закрыта.")

if __name__ == "__main__":
    main()