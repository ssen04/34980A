import pyvisa as visa
import time


class _34980A:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.v34980A = self.rm.open_resource('TCPIP0::172.30.29.14::inst0::INSTR')

    def set_range(self, val=100.0):
        self.v34980A.write(':SENSe:VOLTage:DC:RANGe %G' % (val))

    def set_four_wire(self):
        """Sets the sourcemeter to remote mode, thereby enabling 4-wire measurements"""
        self.v34980A.write('SENSE:REMOTE ON')

    # Triggers the internal DMM to scan one channel (channel 4 in slot 3), and then transfers the reading to reading memory and the instrument's output buffer.
    # MEAS:VOLT:DC? (@3004)
    def get_voltage(self):
        # Configure the range, resolution and channel for voltage measurement
        self.v34980A.write(':CONFigure:SCALar:VOLTage:DC %G,%G,(%s)' % (100.0, 6.5, '@1001'))
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:VOLTage:DC? (%s)' % ('@1001'))  # channel 1 in slot 1
        dcVoltage = temp_values[0]
        return dcVoltage

    def get_current(self):
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:CURRent:DC?')
        # temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:CURRent:DC? (%s)' % ('@1001'))
        dcCurrent = temp_values[0]
        return dcCurrent

    def get_resistance(self):
        # Configure the range, resolution and channel for resistance measurement
        self.v34980A.write(':CONFigure:SCALar:RESistance %G,%G,(%s)' % (100.0, 6.5, '@1001'))
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:RESistance? (%s)' % ('@1001'))
        resistance = temp_values[0]
        print("From instrument")
        print("Resistance value : ", resistance)
        return resistance

    def close(self):
        self.v34980A.close()
        self.rm.close()


inst = _34980A()
inst.set_range()
inst.set_four_wire()
voltage = inst.get_voltage()
print("Voltage : ", voltage)
print("=====================================")
current = inst.get_current()
print("Current : ", current)
print("=====================================")
inst.get_resistance()
inst.close()
