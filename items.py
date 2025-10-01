class Item:
    """Базовый класс предмета"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def use(self, target):
        pass
    
    def __str__(self):
        return f"{self.name}: {self.description}"

class HealthPotion(Item):
    """Зелье здоровья"""
    
    def __init__(self):
        super().__init__("Зелье здоровья", "Восстанавливает 50 HP")
    
    def use(self, target):
        old_hp = target.hp
        target.hp = min(target.max_hp, target.hp + 50)
        heal_amount = target.hp - old_hp
        print(f"{target.name} использует {self.name} и восстанавливает {heal_amount} HP!")
        return True

class ManaPotion(Item):
    """Зелье маны"""
    
    def __init__(self):
        super().__init__("Зелье маны", "Восстанавливает 30 MP")
    
    def use(self, target):
        old_mp = target.mp
        target.mp = min(target.max_mp, target.mp + 30)
        restore_amount = target.mp - old_mp
        print(f"{target.name} использует {self.name} и восстанавливает {restore_amount} MP!")
        return True

class Inventory:
    """Инвентарь персонажа"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def use_item(self, item_index, target):
        if item_index < 0 or item_index >= len(self.items):
            print("Неверный индекс предмета!")
            return False
        
        item = self.items[item_index]
        if item.use(target):
            self.remove_item(item)
            return True
        return False
    
    def __str__(self):
        if not self.items:
            return "Инвентарь пуст"
        return "\n".join([f"{i}: {item}" for i, item in enumerate(self.items)])