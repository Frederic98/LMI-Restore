#!/usr/bin/env python3


class BitSetting:
    def __new__(cls, name, fields):
        """
        :param name: Name of the BitSetting instance
        :param fields: [abc, len]
        """
        map = {}
        length = 0
        bitindex = 0
        for field in fields:
            if isinstance(field, (list, tuple)):
                name = field[0]
                try:
                    len = field[1]
                except IndexError:
                    len = 8 - bitindex
            else:
                name = field
                len = 8 - bitindex

            if name is not None:
                map[name] = (length, bitindex, len)
            bitindex += len
            if bitindex == 8:
                bitindex = 0
                length += 1
            elif bitindex > 8:
                raise ValueError('Field {} overlaps byte boundary'.format(name))

        values = [0] * length
        return type(name, (ConfiguredBitSetting,), {'fields': map,
                                                    'length': length,
                                                    'values': values})


class ConfiguredBitSetting:
    fields = {}
    length = 0
    values = []

    def __init__(self, values, readonly=False):
        if isinstance(values, (list, tuple, bytes)):
            self.values = list(values)
            if len(values) < self.length:
                n_missing = self.length - len(self.values)
                self.values.extend([0]*n_missing)
            elif len(self.values) > self.length:
                self.values = self.values[:self.length]
        else:
            raise ValueError('"values" has to be a list of ints or a bytes object')
        self.readonly = readonly
        self.changed = [False] * len(values)

    def __setitem__(self, key, value):
        if self.readonly:
            raise PermissionError('This {} instance is readonly'.format(self.__class__.__name__))
        if isinstance(value, bytes):
            value = ord(value)
        if not isinstance(value, int):
            raise ValueError('"value" has to be an int or byte')

        if isinstance(key, int):
            self.values[key] = value
            self.changed[key] = True
        else:
            vbyte, vbit, vlen = self.fields[key]
            mask = ((1 << vlen) - 1) << vbit
            self.values[vbyte] &= ~mask
            self.values[vbyte] |= (value << vbit) & mask
            self.changed[vbyte] = True

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.values[item]
        else:
            vbyte, vbit, vlen = self.fields[item]
            byte = self.values[vbyte]
            return (byte >> vbit) & ((1 << vlen) - 1)

    def reset_change(self):
        for i in range(len(self.changed)):
            self.changed[i] = False


if __name__ == '__main__':
    bs = BitSetting('ScannerSettings',
                    [('mode', 2), ('light', 2), ('laser', 2), ('buzzer', 1), ('led', 1),
                     None,
                     (None, 6), ('decode_state', 1), None,
                     ('printsettingcode', 1), ('settingcode', 1), None,
                     'stabilize_time',
                     'scan_interval',
                     'scan_time',
                     ('sleep_enable', 1), 'sleep_time_h'
                     'sleep_time_l',
                     None,
                     'buzzer_freq',
                     'buzzer_duration',
                     'buzzer_level',
                     (None, 4), ('data_format', 2), ('data_port', 2),
                     (None, 5), ('buzzer_scan', 1), None,
                     *[None]*28,
                     (None, 3), ('baud_h', 5),
                     'baud_l'])
    bi = bs([1, 2, 3, 4])
    print(bi)
