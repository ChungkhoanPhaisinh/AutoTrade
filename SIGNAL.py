class Signal:
    def __init__(self):
        self.subscribers = []

    def Connect(self, callback):
        self.subscribers.append(callback)

    def Emit(self, *args, **kwargs):
        for fn in self.subscribers:
            fn(*args, **kwargs)

    def DisconnectAll(self):
        self.subscribers.clear()