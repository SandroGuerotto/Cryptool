class Dataholder:
    def __init__(self):
        self.source = ""
        self.destination = ""
        self.key = None
        print("data")

    def set_source(self, source):
        self.source = source

    def set_destination(self, destination):
        self.destination = destination

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination