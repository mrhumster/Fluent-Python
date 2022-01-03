class HauntedBuss:
    def __init__(self, passangers=None):
        if passangers is None:
            self.passangers = []
        else:
            self.passangers = list(passangers)
            # Если тут сделать просто self.passangers = passangers,
            # эти объекты будут синонимами.

    def pick(self, name):
        self.passangers.append(name)

    def drop(self, name):
        self.passangers.remove(name)