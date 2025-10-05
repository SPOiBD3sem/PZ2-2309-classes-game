import unittest
from characters import Warrior, Mage, Healer
from bosses import Boss
from skills import PowerStrike, Fireball, Heal
from effects import PoisonEffect, ShieldEffect
from items import HealthPotion, ManaPotion

class TestCharacters(unittest.TestCase):
    
    def setUp(self):
        self.warrior = Warrior("ТестВоин")
        self.mage = Mage("ТестМаг") 
        self.healer = Healer("ТестЛекарь")
        self.boss = Boss("ТестБосс", 1)
    
    def test_character_creation(self):
        self.assertEqual(self.warrior.name, "ТестВоин")
        self.assertTrue(self.warrior.is_alive)
    
    def test_basic_attack(self):
        start_hp = self.boss.hp
        self.warrior.basic_attack(self.boss)
        self.assertLess(self.boss.hp, start_hp)
    
    def test_take_damage(self):
        start_hp = self.warrior.hp
        self.warrior.take_damage(20)
        self.assertEqual(self.warrior.hp, start_hp - 20)

class TestSkills(unittest.TestCase):
    
    def setUp(self):
        self.warrior = Warrior("Воин")
        self.mage = Mage("Маг")
        self.boss = Boss("Босс", 1)
    
    def test_power_strike(self):
        skill = PowerStrike()
        start_hp = self.boss.hp
        skill.use(self.warrior, self.boss)
        self.assertLess(self.boss.hp, start_hp)
    
    def test_fireball(self):
        skill = Fireball()
        start_hp = self.boss.hp
        skill.use(self.mage, self.boss)
        self.assertLess(self.boss.hp, start_hp)
    
    def test_heal(self):
        skill = Heal()
        self.warrior.take_damage(30)
        damaged_hp = self.warrior.hp
        skill.use(self.mage, self.warrior)
        self.assertGreater(self.warrior.hp, damaged_hp)

class TestEffects(unittest.TestCase):
    
    def setUp(self):
        self.warrior = Warrior("Воин")
    
    def test_poison_effect(self):
        poison = PoisonEffect()
        start_hp = self.warrior.hp
        poison.on_turn_start(self.warrior)
        self.assertLess(self.warrior.hp, start_hp)
    
    def test_shield_effect(self):
        shield = ShieldEffect()
        damage = shield.absorb_damage(15)
        self.assertEqual(damage, 0)

class TestBoss(unittest.TestCase):
    
    def setUp(self):
        self.boss = Boss("Босс", 1)
        self.warrior = Warrior("Воин")
        self.party = [self.warrior]
    
    def test_boss_attack(self):
        start_hp = self.warrior.hp
        self.boss.basic_attack(self.warrior)
        self.assertLess(self.warrior.hp, start_hp)
    
    def test_boss_phases(self):
        self.boss.hp = self.boss.max_hp * 0.8  # Фаза 1
        self.boss.choose_action(self.party)
        
        self.boss.hp = self.boss.max_hp * 0.5  # Фаза 2  
        self.boss.choose_action(self.party)

if __name__ == '__main__':
    unittest.main()