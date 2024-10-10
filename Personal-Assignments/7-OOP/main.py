class User:

    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear

    def get_name(self):
        return self.name.upper()

    def age(self, current_year):
        age = current_year - self.birthyear
        return age


user = User("John", 1999)
age = user.age(2023)
print(age)
print(user.get_name())