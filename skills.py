from abc import ABC, abstractmethod

class Skill(ABC):
    """Абстрактный базовый класс для навыков"""
    
    def __init__(self, name, mana_cost, cooldown):
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown = cooldown
    
    @abstractmethod
    def use(self, caster, target):
        pass
    
    def __str__(self):
        return f"{self.name} (Мана: {self.mana_cost}, КД: {self.cooldown})"

class DamageSkill(Skill):
    """Навык нанесения урона"""
    
    def __init__(self, name, mana_cost, cooldown, base_damage, damage_type="physical"):
        super().__init__(name, mana_cost, cooldown)
        self.base_damage = base_damage
        self.damage_type = damage_type
    
    def use(self, caster, target):
        if caster.mp < self.mana_cost:
            return False
        
        caster.mp -= self.mana_cost
        
        # Расчет урона в зависимости от типа
        if self.damage_type == "physical":
            damage = self.base_damage + caster.strength * 1.5
        else:  # magical
            damage = self.base_damage + caster.intelligence * 1.7
        
        # Критический удар
        damage = caster.calculate_crit(damage)
        
        actual_damage = target.take_damage(int(damage))
        print(f"{caster.name} использует {self.name} на {target.name} и наносит {actual_damage} урона!")
        
        caster.cooldowns[self.name] = self.cooldown
        return True

class HealSkill(Skill):
    """Навык лечения"""
    
    def __init__(self, name, mana_cost, cooldown, base_heal):
        super().__init__(name, mana_cost, cooldown)
        self.base_heal = base_heal
    
    def use(self, caster, target):
        if caster.mp < self.mana_cost:
            return False
        
        caster.mp -= self.mana_cost
        
        heal_amount = self.base_heal + caster.intelligence * 1.2
        old_hp = target.hp
        target.hp = min(target.max_hp, target.hp + int(heal_amount))
        actual_heal = target.hp - old_hp
        
        print(f"{caster.name} использует {self.name} на {target.name} и восстанавливает {actual_heal} HP!")
        
        caster.cooldowns[self.name] = self.cooldown
        return True

class EffectSkill(Skill):
    """Навык наложения эффекта"""
    
    def __init__(self, name, mana_cost, cooldown, effect_class, **effect_kwargs):
        super().__init__(name, mana_cost, cooldown)
        self.effect_class = effect_class
        self.effect_kwargs = effect_kwargs
    
    def use(self, caster, target):
        if caster.mp < self.mana_cost:
            return False
        
        caster.mp -= self.mana_cost
        
        # Создаем новый экземпляр эффекта
        new_effect = self.effect_class(**self.effect_kwargs)
        new_effect.apply_effect(target)
        
        print(f"{caster.name} использует {self.name} на {target.name}!")
        
        caster.cooldowns[self.name] = self.cooldown
        return True

# Конкретные навыки
class PowerStrike(DamageSkill):
    def __init__(self):
        super().__init__("Мощный удар", 15, 2, 25)

class Fireball(DamageSkill):
    def __init__(self):
        super().__init__("Огненный шар", 30, 3, 40, "magical")

class Heal(HealSkill):
    def __init__(self):
        super().__init__("Лечение", 10, 2, 40)

class PoisonDart(EffectSkill):
    def __init__(self):
        from effects import PoisonEffect
        super().__init__("Отравленный дротик", 12, 3, PoisonEffect, damage_per_turn=20, duration=3)

class Shield(EffectSkill):
    def __init__(self):
        from effects import ShieldEffect
        super().__init__("Щит", 18, 4, ShieldEffect, shield_amount=25, duration=2)
