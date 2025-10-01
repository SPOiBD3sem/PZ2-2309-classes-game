from abc import ABC, abstractmethod
from descriptors import BoundedStat
from mixins import CritMixin, LoggerMixin, SilenceMixin

class Human(ABC):
    """Базовый класс для всех персонажей"""
    
    # Дескрипторы для характеристик
    hp = BoundedStat(0, 1000)
    mp = BoundedStat(0, 500)
    strength = BoundedStat(1, 100)
    agility = BoundedStat(1, 100)
    intelligence = BoundedStat(1, 100)
    
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self.max_hp = 100
        self.max_mp = 50
        self.effects = []
    
    @property
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        """Получение урона с учетом эффектов"""
        actual_damage = damage
        # Проверяем щиты
        for effect in self.effects:
            if hasattr(effect, 'absorb_damage'):
                actual_damage = effect.absorb_damage(actual_damage)
                if actual_damage == 0:
                    print(f"Щит поглотил весь урон!")
                    break
        
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def add_effect(self, effect):
        """Добавление эффекта"""
        self.effects.append(effect)
        effect.apply_effect(self)
    
    def remove_effect(self, effect):
        """Удаление эффекта"""
        if effect in self.effects:
            self.effects.remove(effect)
    
    def update_effects(self):
        """Обновление всех эффектов в конце хода"""
        effects_to_remove = []
        for effect in self.effects[:]:
            if effect.update(self):
                effects_to_remove.append(effect)
        
        for effect in effects_to_remove:
            self.remove_effect(effect)
    
    def __str__(self):
        return f"{self.name} (Ур. {self.level}) - HP: {self.hp}/{self.max_hp}, MP: {self.mp}/{self.max_mp}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', level={self.level})"

class Character(Human, CritMixin, SilenceMixin, ABC):
    """Абстрактный класс персонажа"""
    
    def __init__(self, name, level=1):
        # Явно вызываем конструкторы всех родителей
        Human.__init__(self, name, level)
        CritMixin.__init__(self)
        SilenceMixin.__init__(self)
        
        self.skills = []
        self.cooldowns = {}
    
    @abstractmethod
    def basic_attack(self, target):
        pass
    
    @abstractmethod
    def use_skill(self, skill_index, target):
        pass
    
    def can_use_skill(self, skill):
        """Проверка возможности использования навыка"""
        if self.is_silenced:
            print(f"{self.name} немой и не может использовать навыки!")
            return False
        
        if self.mp < skill.mana_cost:
            print(f"Недостаточно маны для {skill.name}!")
            return False
        
        if skill.name in self.cooldowns and self.cooldowns[skill.name] > 0:
            print(f"Навык {skill.name} на перезарядке! Осталось: {self.cooldowns[skill.name]} ходов")
            return False
        
        return True
    
    def update_cooldowns(self):
        """Обновление перезарядки навыков"""
        for skill_name in list(self.cooldowns.keys()):
            self.cooldowns[skill_name] -= 1
            if self.cooldowns[skill_name] <= 0:
                del self.cooldowns[skill_name]