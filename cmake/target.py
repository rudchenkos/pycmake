class Target:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.sources = []

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def addSource(self, src):
        self.sources.append(src)
