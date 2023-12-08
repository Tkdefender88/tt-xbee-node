import events


class State(object):
    def __init__(self):
        print('handling state: ', str(self))

    def on_event(self, event):
        pass

    def configure_xbee(self, xbee):
        pass


class PairingMode(State):
    def on_event(self, event):
        if event == events.LISTEN:
            # save the frequency and information received during pairing to memory.
            return ListenMode()

        return self

    def configure_xbee(self, xbee):
        xbee.atcmd('CH', 0x1A)  # set the channel
        xbee.atcmd('NI', 1234)  # set the network ID
        xbee.atcmd('KY', 0x12345678ABBCCDDE)


class ListenMode(State):
    def on_event(self, event):
        if event == events.PAIR:
            return PairingMode()
        return self

    def configure_xbee(self, xbee):
        pass


class TestMode(State):
    def on_event(self, event):
        return ListenMode()

    def configure_xbee(self, xbee):
        pass