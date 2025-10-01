from abc import ABC, abstractmethod

class Effect(ABC):
    """Абстрактный базовый класс для эффектов"""
    
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.remaining_duration = duration
    
    @abstractmethod
    def apply_effect(self, target):
        pass
    
    @abstractmethod
    def remove_effect(self, target):
        pass
    
    def update(self, target):
        """Обновление эффекта в конце хода"""
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.remove_effect(target)
            return True
        return False
    
    def __str__(self):
        return f"{self.name} ({self.remaining_duration} ходов)"

class PoisonEffect(Effect):
    """Эффект яда - урон каждый ход"""
    
    def __init__(self, damage_per_turn=5, duration=3):
        super().__init__("Яд", duration)
        self.damage_per_turn = damage_per_turn
    
    def apply_effect(self, target):
        # Добавляем эффект к цели
        target.effects.append(self)
        print(f"{target.name} отравлен! Будет получать {self.damage_per_turn} урона каждый ход в течение {self.duration} ходов.")
    
    def remove_effect(self, target):
        # Удаляем эффект из цели
        if self in target.effects:
            target.effects.remove(self)
        print(f"Яд на {target.name} рассеялся.")
    
    def on_turn_start(self, target):
        """Вызывается в начале хода цели"""
        if target.is_alive:
            actual_damage = target.take_damage(self.damage_per_turn)
            print(f"{target.name} получает {actual_damage} урона от яда!")
        return True

class ShieldEffect(Effect):
    """Эффект щита - поглощает урон"""
    
    def __init__(self, shield_amount=20, duration=2):
        super().__init__("Щит", duration)
        self.shield_amount = shield_amount
        self.current_shield = shield_amount
    
    def apply_effect(self, target):
        target.effects.append(self)
        print(f"{target.name} получает щит на {self.shield_amount} урона!")
    
    def remove_effect(self, target):
        if self in target.effects:
            target.effects.remove(self)
        print(f"Щит на {target.name} исчез.")
    
    def absorb_damage(self, damage):
        """Поглощает урон, возвращает оставшийся урон"""
        if self.current_shield >= damage:
            self.current_shield -= damage
            absorbed = damage
            remaining = 0
        else:
            absorbed = self.current_shield
            remaining = damage - self.current_shield
            self.current_shield = 0
        
        if absorbed > 0:
            print(f"Щит поглотил {absorbed} урона!")
        return remaining

class RegenerationEffect(Effect):
    """Эффект регенерации - восстанавливает HP каждый ход"""
    
    def __init__(self, heal_per_turn=10, duration=3):
        super().__init__("Регенерация", duration)
        self.heal_per_turn = heal_per_turn
    
    def apply_effect(self, target):
        target.effects.append(self)
        print(f"{target.name} получает регенерацию! Будет восстанавливать {self.heal_per_turn} HP каждый ход.")
    
    def remove_effect(self, target):
        if self in target.effects:
            target.effects.remove(self)
        print(f"Регенерация на {target.name} закончилась.")
    
    def on_turn_start(self, target):
        """Вызывается в начале хода цели"""
        if target.is_alive:
            old_hp = target.hp
            target.hp = min(target.max_hp, target.hp + self.heal_per_turn)
            heal_amount = target.hp - old_hp
            if heal_amount > 0:
                print(f"{target.name} восстанавливает {heal_amount} HP от регенерации")
        return True