from copy import deepcopy


class Scheduler(object):
    def __init__(self, Queue, name):
        self.name = name
        self.Queue = Queue

    def schedule(self):
        pass
