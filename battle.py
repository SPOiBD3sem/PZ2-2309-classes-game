import random
import json
from mixins import LoggerMixin

class TurnOrder:
    """Итератор для определения порядка ходов"""
    
    def __init__(self, participants):
        self.participants = participants
        self.current_turn = 0
        self.order = self.calculate_order()
    
    def calculate_order(self):
        """Расчет порядка ходов на основе ловкости"""
        return sorted(self.participants, key=lambda x: x.agility, reverse=True)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_turn >= len(self.order):
            self.current_turn = 0
            self.order = self.calculate_order()
            raise StopIteration
        
        participant = self.order[self.current_turn]
        self.current_turn += 1
        return participant

class Battle(LoggerMixin):
    """Класс управления боем"""
    
    def __init__(self, party, boss):
        super().__init__()
        self.party = party
        self.boss = boss
        self.round = 0
        self.is_active = True
    
    def save_state(self, filename):
        """Сохранение состояния боя в JSON"""
        # Добавляем расширение .json если его нет
        if not filename.endswith('.json'):
            filename += '.json'
        
        state = {
            "round": self.round,
            "boss_hp": self.boss.hp,
            "boss_mp": self.boss.mp,
            "party": [
                {
                    "name": char.name,
                    "class": char.__class__.__name__,
                    "hp": char.hp,
                    "mp": char.mp,
                    "max_hp": char.max_hp,
                    "max_mp": char.max_mp
                }
                for char in self.party
            ]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            self.add_log(f"✓ Игра сохранена в файл: {filename}")
            return True
        except Exception as e:
            self.add_log(f"✗ Ошибка при сохранении: {e}")
            return False
    
    def load_state(self, filename):
        """Загрузка состояния боя из JSON"""
        try:
            # Добавляем расширение .json если его нет
            if not filename.endswith('.json'):
                filename += '.json'
                
            with open(filename, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.round = state["round"]
            self.boss.hp = state["boss_hp"]
            self.boss.mp = state["boss_mp"]
            
            for char_data, char in zip(state["party"], self.party):
                char.hp = char_data["hp"]
                char.mp = char_data["mp"]
            
            self.add_log(f"✓ Состояние боя загружено из {filename}")
            return True
        except FileNotFoundError:
            self.add_log("✗ Файл сохранения не найден!")
            return False
        except Exception as e:
            self.add_log(f"✗ Ошибка при загрузке: {e}")
            return False
    
    def start_battle(self):
        """Запуск боя"""
        self.add_log("=== НАЧАЛО БОЯ ===")
        self.add_log(f"Босс: {self.boss}")
        self.add_log("Группа:")
        for char in self.party:
            self.add_log(f"  - {char}")
        
        turn_order = TurnOrder(self.party + [self.boss])
        
        while self.is_active:
            self.round += 1
            self.add_log(f"\n=== РАУНД {self.round} ===")
            
            for participant in turn_order:
                if not participant.is_alive:
                    continue
                
                self.process_turn(participant)
                
                # Проверка условий окончания боя
                if not self.boss.is_alive:
                    self.add_log("=== ПОБЕДА! Босс повержен! ===")
                    self.is_active = False
                    break
                
                if all(not char.is_alive for char in self.party):
                    self.add_log("=== ПОРАЖЕНИЕ! Вся группа пала! ===")
                    self.is_active = False
                    break
            
            # Обновление эффектов в конце раунда
            self.update_all_effects()
    
    def update_all_effects(self):
        """Обновление всех эффектов в конце раунда"""
        for participant in self.party + [self.boss]:
            if participant.is_alive:
                # Обновляем эффекты
                effects_to_remove = []
                for effect in participant.effects[:]:
                    if effect.update(participant):
                        effects_to_remove.append(effect)
                
                for effect in effects_to_remove:
                    participant.remove_effect(effect)
                
                # Обновляем перезарядки
                if hasattr(participant, 'update_cooldowns'):
                    participant.update_cooldowns()
    
    def process_turn(self, participant):
        """Обработка хода участника"""
        self.add_log(f"\nХод {participant.name}:")
        
        # Обработка эффектов в начале хода
        self.process_start_of_turn_effects(participant)
        
        if not participant.is_alive:
            return
        
        if hasattr(participant, 'choose_action') and participant.__class__.__name__ == 'Boss':
            # Ход босса
            participant.choose_action(self.party)
        else:
            # Ход игрока
            self.player_turn(participant)
    
    def process_start_of_turn_effects(self, participant):
        """Обработка эффектов в начале хода"""
        for effect in participant.effects[:]:
            if hasattr(effect, 'on_turn_start'):
                effect.on_turn_start(participant)
    
    def choose_target(self, prompt, allow_self=False, allow_party=True, allow_boss=True):
        """Выбор цели с дополнительными параметрами"""
        print(f"\n{prompt}")
        targets = []
        
        if allow_boss and self.boss.is_alive:
            targets.append(self.boss)
        
        if allow_party:
            for char in self.party:
                if char.is_alive:
                    targets.append(char)
        
        # Если можно выбрать себя и текущий персонаж жив, добавляем опцию "на себя"
        current_player = None
        if allow_self:
            # Находим текущего игрока (того, чей сейчас ход)
            for char in self.party:
                if char.is_alive and char.hp > 0:
                    current_player = char
                    break
        
        for i, target in enumerate(targets):
            target_type = "Босс" if target == self.boss else "Союзник"
            print(f"{i + 1}. {target.name} ({target_type}) - HP: {target.hp}/{target.max_hp}")
        
        # Добавляем опцию "на себя" если разрешено
        if allow_self and current_player and current_player.is_alive:
            print(f"{len(targets) + 1}. На себя - {current_player.name} (HP: {current_player.hp}/{current_player.max_hp})")
        
        try:
            target_choice = int(input("Выберите цель: ")) - 1
            
            # Если выбрана опция "на себя"
            if allow_self and current_player and target_choice == len(targets):
                return current_player
            
            if 0 <= target_choice < len(targets):
                return targets[target_choice]
            else:
                print("Неверный выбор цели!")
                return None
        except ValueError:
            print("Пожалуйста, введите число!")
            return None

    def player_turn(self, player):
        """Ход игрока"""
        print(f"\n--- Ход {player.name} ---")
        print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}")
        
        if player.effects:
            print("Эффекты:", ", ".join(str(effect) for effect in player.effects))
        
        print("\nДоступные действия:")
        print("1. Базовая атака")
        print("2. Использовать навык")
        print("3. Использовать предмет")
        print("4. Пропустить ход")
        print("5. Сохранить игру")
        
        while True:
            try:
                choice = int(input("Выберите действие: "))
                
                if choice == 1:
                    target = self.choose_target("Выберите цель для атаки:", allow_self=False, allow_party=False, allow_boss=True)
                    if target:
                        success = player.basic_attack(target)
                        if success:
                            print("✓ Атака успешна!")
                        break
                    else:
                        break
                
                elif choice == 2:
                    self.use_skill(player)
                    break
                
                elif choice == 3:
                    self.use_item(player)
                    break
                
                elif choice == 4:
                    print(f"{player.name} пропускает ход.")
                    break
                
                elif choice == 5:
                    filename = input("Введите имя файла для сохранения: ").strip()
                    if filename:
                        self.save_state(filename)
                    else:
                        print("Имя файла не может быть пустым!")
                    # Продолжаем ход после сохранения
                    continue
                
                else:
                    print("Неверный выбор!")
            
            except ValueError:
                print("Пожалуйста, введите число!")
    
    def use_skill(self, player):
        """Использование навыка игроком"""
        print("\nДоступные навыки:")
        for i, skill in enumerate(player.skills):
            cooldown = player.cooldowns.get(skill.name, 0)
            print(f"{i + 1}. {skill} {'(КД: ' + str(cooldown) + ')' if cooldown > 0 else ''}")
        
        try:
            skill_choice = int(input("Выберите навык: ")) - 1
            if skill_choice < 0 or skill_choice >= len(player.skills):
                print("Неверный индекс навыка!")
                return False
            
            skill = player.skills[skill_choice]
            
            # Определяем параметры выбора цели в зависимости от типа навыка
            from skills import HealSkill, EffectSkill
            from effects import ShieldEffect
            
            is_healing_or_shield = (isinstance(skill, HealSkill) or 
                                  (isinstance(skill, EffectSkill) and skill.effect_class == ShieldEffect))
            
            if is_healing_or_shield:
                # Лечебные и защитные навыки можно применять на себя и союзников
                target = self.choose_target("Выберите цель:", allow_self=True, allow_party=True, allow_boss=False)
            else:
                # Атакующие навыки только на врагов
                target = self.choose_target("Выберите цель:", allow_self=False, allow_party=False, allow_boss=True)
            
            if target:
                # Дополнительная проверка для защитных навыков
                if (isinstance(skill, EffectSkill) and skill.effect_class == ShieldEffect and target == self.boss):
                    print("Нельзя наложить щит на босса!")
                    return False
                
                success = player.use_skill(skill_choice, target)
                if success:
                    print("✓ Навык использован успешно!")
                return success
            
            return False
        
        except ValueError:
            print("Пожалуйста, введите число!")
            return False
    
    def use_item(self, player):
        """Использование предмета игроком"""
        from items import HealthPotion, ManaPotion, Inventory
        inventory = Inventory()
        inventory.add_item(HealthPotion())
        inventory.add_item(ManaPotion())
        
        print("\nИнвентарь:")
        print(inventory)
        
        try:
            item_choice = int(input("Выберите предмет: "))
            # Предметы можно использовать на себя и союзников
            target = self.choose_target("Выберите цель:", allow_self=True, allow_party=True, allow_boss=False)
            if target:
                success = inventory.use_item(item_choice, target)
                if success:
                    print("✓ Предмет использован успешно!")
                return success
            return False
        
        except ValueError:
            print("Пожалуйста, введите число!")
            return False
        except IndexError:
            print("Неверный выбор предмета!")
            return False