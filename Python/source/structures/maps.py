class Maps_active:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Maps_active, cls).__new__(cls)
            cls._instance.value = False
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.value

    @classmethod
    def set_instance(cls, value):
        if value not in [True, False]:
            raise ValueError("Maps_active can only be True or False")
        if cls._instance is None:
            cls._instance = cls(value)
        else:
            cls._instance.value = value

# # Usage
# Maps_active.set_instance(True)
# print(Maps_active.get_instance())  # Output: True

# Maps_active.set_instance(False)
# print(Maps_active.get_instance())  # Output: False