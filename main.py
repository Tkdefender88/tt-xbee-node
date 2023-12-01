# Default template for Digi projects
import time
import xbee
from TemperatureController import TemperatureSensor
import machine
import state_machine
import events


class SensorDevice(object):
    def __init__(self):
        self.state = state_machine.ListenMode()
        self.light_pin = machine.Pin('D3', machine.Pin.OUT)
        self.light_pin.on()
        self.analog_in = machine.ADC('D0')
        self.pair_button = machine.Pin('D4', machine.Pin.IN, machine.Pin.PULL_UP)

    def on_event(self, event):
        self.state = self.state.on_event(event)


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


x = xbee.XBee()
sensor = SensorDevice()
pair_button = machine.Pin('D4', machine.Pin.IN, machine.Pin.PULL_UP)
count = 0
PAIRING_THRESHOLD = 200

while True:
    if sensor.state is state_machine.ListenMode:
        while pair_button.value() == 0:
            count += 1

        if count > PAIRING_THRESHOLD:
            sensor.on_event(events.PAIR)

        count = 0


    '''
    print('Going to sleep')

    # sleep the board
    sleep_ms = x.sleep_now(60000, False)

    print('slept for %u ms' % sleep_ms)

    if x.wake_reason() is xbee.RTC_WAKE:
        print('waking based on the clock')

    t = TemperatureSensor()
    print('temperature: ', t.read_temperature())

    # take reading
    val = analogPin.read()
    print('Taking reading of analog')
    print(val//100)
    '''

