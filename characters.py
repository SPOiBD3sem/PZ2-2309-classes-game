from core import Character
from skills import PowerStrike, Fireball, Heal, PoisonDart, Shield

class Warrior(Character):
    """Класс воина"""
    
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._hp = 150 + level * 20
        self._mp = 30 + level * 5
        self._strength = 20 + level * 2
        self._agility = 15 + level * 1
        self._intelligence = 8 + level * 0.5
        self.max_hp = self._hp
        self.max_mp = self._mp
        
        # Навыки воина
        self.skills = [PowerStrike()]
    
    def basic_attack(self, target):
        damage = 10 + self.strength * 0.3
        damage = self.calculate_crit(damage, crit_chance=0.15)
        actual_damage = target.take_damage(int(damage))
        print(f"{self.name} атакует {target.name} и наносит {actual_damage} урона!")
        return True
    
    def use_skill(self, skill_index, target):
        if skill_index < 0 or skill_index >= len(self.skills):
            print("Неверный индекс навыка!")
            return False
        
        skill = self.skills[skill_index]
        if not self.can_use_skill(skill):
            return False
        
        return skill.use(self, target)

class Mage(Character):
    """Класс мага"""
    
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._hp = 80 + level * 10
        self._mp = 80 + level * 15
        self._strength = 8 + level * 0.5
        self._agility = 12 + level * 1
        self._intelligence = 25 + level * 3
        self.max_hp = self._hp
        self.max_mp = self._mp
        
        # Навыки мага
        self.skills = [Fireball(), Shield()]
    
    def basic_attack(self, target):
        damage = 8 + self.intelligence * 0.2
        actual_damage = target.take_damage(int(damage))
        print(f"{self.name} атакует {target.name} магией и наносит {actual_damage} урона!")
        return True
    
    def use_skill(self, skill_index, target):
        if skill_index < 0 or skill_index >= len(self.skills):
            print("Неверный индекс навыка!")
            return False
        
        skill = self.skills[skill_index]
        if not self.can_use_skill(skill):
            return False
        
        return skill.use(self, target)

class Healer(Character):
    """Класс лекаря"""
    
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._hp = 100 + level * 12
        self._mp = 70 + level * 12
        self._strength = 10 + level * 1
        self._agility = 14 + level * 1.5
        self._intelligence = 18 + level * 2
        self.max_hp = self._hp
        self.max_mp = self._mp
        
        # Навыки лекаря
        self.skills = [Heal(), PoisonDart()]
    
    def basic_attack(self, target):
        damage = 7 + self.strength * 0.2
        actual_damage = target.take_damage(int(damage))
        print(f"{self.name} атакует {target.name} и наносит {actual_damage} урона!")
        return True
    
    def use_skill(self, skill_index, target):
        if skill_index < 0 or skill_index >= len(self.skills):
            print("Неверный индекс навыка!")
            return False
        
        skill = self.skills[skill_index]
        if not self.can_use_skill(skill):
            return False
        
        return skill.use(self, target)