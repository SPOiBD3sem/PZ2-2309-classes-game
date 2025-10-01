class BoundedStat:
    """Дескриптор для валидации характеристик"""

    def __init__(self, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name, 0)

    def __set__(self, obj, value):
        value = max(self.min_value, min(value, self.max_value))
        setattr(obj, self.name, value)