class Signal:
    def __init__(self):
        self.subscribers = []

    def connect(self, callback):
        self.subscribers.append(callback)

    def emit(self, *args, **kwargs):
        for fn in self.subscribers:
            fn(*args, **kwargs)

    def disconnectAll(self):
        self.subscribers.clear()