# Default template for Digi projects
import time
import xbee
from TemperatureController import TemperatureSensor
import machine
import state_machine
import events

PAIRING_BUTTON = 'D0'
STATUS_LIGHT = 'P0'
ANALOG_IN = 'D1'


class SensorDevice(object):
    def __init__(self):
        self.xbee = xbee.XBee()
        self.xbee.atcmd('EE', 1)  # enable encryption
        self.xbee.atcmd('D0', 1)
        self.xbee.atcmd('P0', 4)
        self.state = state_machine.ListenMode()
        self.light_pin = machine.Pin(STATUS_LIGHT, machine.Pin.OUT)
        self.light_pin.on()
        self.analog_in = machine.ADC(ANALOG_IN)
        self.pair_button = machine.Pin(PAIRING_BUTTON, machine.Pin.IN, machine.Pin.PULL_UP)
        self.temperature_sensor = TemperatureSensor()

    def configure_xbee(self):
        self.state.configure_xbee(self.xbee)

    def on_event(self, event):
        # set the new state based on the received event
        self.state = self.state.on_event(event)

        # configure the device for the new state
        self.configure_xbee()

    def read_adc(self) -> int:
        val = self.analog_in.read()
        print('Taking reading of analog')
        print(val // 100)
        return val

    def sleep(self):
        print('Going to sleep')

        # sleep the board
        sleep_ms = self.xbee.sleep_now(60000, False)

    def read_temperature(self) -> int:
        return self.temperature_sensor.read_temperature()


def find_nodes():
    nodes = list(xbee.discover())
    if not nodes:
        raise Exception("Discovery did not find any nodes")
    for node in nodes:
        print('\nRadio found:')
        for key, value in node.items():
            print('\t {:<12} : {}'.format(key, value))

        destination_address = node['sender_eui64']
        destination_node_id = node['node_id']

        payload_data = 'Toggle Door'

        try:
            print('\nSending {} to {}'.format(payload_data, destination_node_id))
            xbee.transmit(destination_address, payload_data)
        except Exception as err:
            print(err)


sensor = SensorDevice()
count = 0
PAIRING_THRESHOLD = 3000

while True:
    if type(sensor.state) is state_machine.ListenMode:
        while sensor.pair_button.value() == 0:
            print('counting')
            count += 1

            if count > PAIRING_THRESHOLD:
                print('pairing mode')
                sensor.on_event(events.PAIR)
                count = 0
                break

        count = 0

    if type(sensor.state) is state_machine.PairingMode:
        sensor.light_pin.toggle()

    time.sleep(1)
