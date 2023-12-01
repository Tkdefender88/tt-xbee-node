import events


class State(object):
    def __init__(self):
        print('handling state: ', str(self))

    def on_event(self, event):
        pass


class PairingMode(State):
    def on_event(self, event):
        if event == events.LISTEN:
            # save the frequency and information received during pairing to memory.
            return ListenMode()

        return self


class ListenMode(State):
    def on_event(self, event):
        if event == events.PAIR:
            return PairingMode()
        return self


class TestMode(State):
    def on_event(self, event):
        return ListenMode()
