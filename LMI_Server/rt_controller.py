from collections import namedtuple
from typing import Union

import serial

StepConfig = namedtuple('StepConfig', ['steps', 'micro', 'offset'])


class RTController:
    def __init__(self, port, steps: dict, xoffset, yoffset, xspace, yspace):
        self.port = serial.Serial(port, 115200)
        self.steps = steps
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.xspace = xspace
        self.yspace = yspace

    def send(self, text: str):
        text = text.strip()
        #print('->' + text)
        text += '\n'
        self.port.write(text.encode())
        resp = ''
        while True:
            recv = self.port.readline().decode()
            #print('<-' + recv.strip())
            if recv.startswith('ok'):
                return resp
            else:
                resp += recv

    def move_position(self, x=None, y=None, z=None, r=None):
        cmd = 'G0'
        for axis in 'xyzr':
            if locals()[axis] is not None:
                pos = (locals()[axis] + self.steps[axis].offset) * self.steps[axis].steps * self.steps[axis].micro
                cmd += ' {}{}'.format(axis.upper(), pos)
        self.send(cmd)
        self.send('M400')

    def move_spot(self, x, y, height=0, *args, **kwargs):
        self.move_position(self.xoffset + x * self.xspace if x is not None else None,
                           self.yoffset + y * self.yspace + height if y is not None else None,
                           *args, **kwargs)

    def pickup_container(self, x, y):
        self.move_position(z=0)
        self.move_spot(x,y,-20)
        self.move_position(z=190)
        self.move_spot(x,y,10)
        self.move_position(z=0)

    def place_container(self, x, y):
        self.move_position(z=0)
        self.move_spot(x,y,10)
        self.move_position(z=180)
        self.move_spot(x,y,-20)
        self.move_position(z=0)

    def home(self,
             x: Union[bool, int, float]=False, y: Union[bool, int, float]=False,
             z: Union[bool, int, float]=False, r: Union[bool, int, float]=False):
        cmd = 'G28'
        for axis in 'xyzr':
            value = locals()[axis]
            if value:
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    value = ''
                cmd += ' {}{}'.format(axis.upper(), value)
        self.send(cmd)


if __name__ == '__main__':
    steps = {'x': StepConfig(140 / 360 * 1.8 / 960 * 1000, 16, 0),
             'y': StepConfig(140 / 360 * 1.8 * 1.1879194630872485, 16, 0),
             'z': StepConfig(8 / 360 * 1.8 * 626.9592476489028, 4, 0),
             'r': StepConfig(1000 / 360, 4, 53)}
    nucleo = RTController('COM12', steps, 2.3, 137, 137, 140)
    nucleo.home(z=True)
    nucleo.home(x=True, y=True)
    nucleo.pickup_container(0, 0)
