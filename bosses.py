from core import Character
from mixins import LoggerMixin

class BossStrategy:
    """Базовый класс стратегии босса"""
    
    def __init__(self, boss):
        self.boss = boss
    
    def choose_action(self, targets):
        pass

class AggressiveStrategy(BossStrategy):
    """Агрессивная стратегия - атакует самого слабого"""
    
    def choose_action(self, targets):
        # Ищем цель с наименьшим HP
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return ("attack", None)
        weakest = min(alive_targets, key=lambda x: x.hp)
        return ("attack", weakest)

class AOEStrategy(BossStrategy):
    """Стратегия массовой атаки"""
    
    def choose_action(self, targets):
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return ("attack", None)
            
        if len(alive_targets) >= 2:
            return ("aoe", alive_targets)
        else:
            weakest = min(alive_targets, key=lambda x: x.hp)
            return ("attack", weakest)

class DebuffStrategy(BossStrategy):
    """Стратегия наложения дебаффов"""
    
    def choose_action(self, targets):
        from effects import PoisonEffect
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return ("attack", None)
            
        # Ищем цель без эффектов яда
        for target in alive_targets:
            if not any(isinstance(effect, PoisonEffect) for effect in target.effects):
                return ("poison", target)
        # Если все отравлены, атакуем
        weakest = min(alive_targets, key=lambda x: x.hp)
        return ("attack", weakest)

class Boss(Character, LoggerMixin):
    """Класс босса с фазами"""
    
    def __init__(self, name, level=10):
        Character.__init__(self, name, level)
        LoggerMixin.__init__(self)
        
        self._hp = 300 + level * 50
        self._mp = 200 + level * 20
        self._strength = 30 + level * 3
        self._agility = 20 + level * 2
        self._intelligence = 25 + level * 2
        self.max_hp = self._hp
        self.max_mp = self._mp
        
        # Стратегии босса
        self.strategies = {
            "phase1": AggressiveStrategy(self),    # HP > 70%
            "phase2": AOEStrategy(self),           # HP 30%-70%
            "phase3": DebuffStrategy(self)         # HP < 30%
        }
        self.current_strategy = self.strategies["phase1"]
    
    def basic_attack(self, target):
        if not target or not target.is_alive:
            return False
            
        damage = 20 + self.strength * 0.4
        damage = self.calculate_crit(damage, crit_chance=0.2)
        actual_damage = target.take_damage(int(damage))
        self.add_log(f"{self.name} атакует {target.name} и наносит {actual_damage} урона!")
        return True
    
    def use_skill(self, skill_index, target):
        # Босс использует автоматический выбор действия
        return self.choose_action(target)
    
    def choose_action(self, targets):
        """Автоматический выбор действия на основе стратегии"""
        # Определяем текущую фазу
        hp_percent = self.hp / self.max_hp
        if hp_percent > 0.7:
            self.current_strategy = self.strategies["phase1"]
        elif hp_percent > 0.3:
            self.current_strategy = self.strategies["phase2"]
        else:
            self.current_strategy = self.strategies["phase3"]
        
        action_type, target = self.current_strategy.choose_action(targets)
        
        if action_type == "attack" and target:
            self.basic_attack(target)
        elif action_type == "aoe" and target:
            self.aoe_attack(target)
        elif action_type == "poison" and target:
            self.poison_attack(target)
        
        return True
    
    def aoe_attack(self, targets):
        """Массовая атака"""
        if self.mp < 40:
            if targets:
                self.basic_attack(targets[0])
            return
        
        self.mp -= 40
        damage = 15 + self.intelligence * 0.3
        
        for target in targets:
            if target.is_alive:
                actual_damage = target.take_damage(int(damage))
                self.add_log(f"{self.name} использует массовую атаку на {target.name} и наносит {actual_damage} урона!")
    
    def poison_attack(self, target):
        """Атака ядом"""
        if self.mp < 25:
            self.basic_attack(target)
            return
        
        self.mp -= 25
        from effects import PoisonEffect
        poison = PoisonEffect(damage_per_turn=12, duration=3)
        target.add_effect(poison)
        self.add_log(f"{self.name} отравляет {target.name}!")