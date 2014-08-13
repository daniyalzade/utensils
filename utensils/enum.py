from utensils.listutils import OrderedSet

class Enum(OrderedSet):
    def __getattr__(self, name):
        if name in self:
            return name
        return None

def create_enum(**enums):
    return type('Enum', (), enums)
