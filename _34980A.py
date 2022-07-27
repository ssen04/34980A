import datetime
import pandas as pd
import pyvisa as visa
import matplotlib.pyplot as plt

class _34980A:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.v34980A = self.rm.open_resource('TCPIP0::172.30.30.31::inst0::INSTR')

    def set_range(self, val=100.0):
        self.v34980A.write(':SENSe:VOLTage:DC:RANGe %G' % (val))

    def set_four_wire(self):
        # Sets the system to remote mode, thereby enabling 4-wire measurements
        self.v34980A.write('SENSE:REMOTE ON')

    def set_channel_delay(self, time=0.002):
        self.v34980A.write(':ROUTe:CHANnel:DELay %G,(%s)' % (time, '@1001'))

    # Triggers the internal DMM to scan one channel (channel 4 in slot 3), and then transfers the reading to reading memory and the instrument's output buffer.
    # MEAS:VOLT:DC? (@3004)
    def get_voltage(self, range=100.0, res=6.5, npl_cycles=10.0, offset=1, channel='@1001'):
        # Configure the range, resolution and channel for voltage measurement
        self.v34980A.write(':CONFigure:SCALar:VOLTage:DC %G,%G,(%s)' % (range, res, channel))
        # Configure number of NPL cycles
        self.v34980A.write(':SENSe:VOLTage:DC:NPLCycles %G,(%s)' % (npl_cycles, channel))
        # Sets offset compensation
        self.v34980A.write(':SENSe:VOLTage:OCOMpensated %d,(%s)' % (offset, channel))

        # Take a voltage measurement
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:VOLTage:DC? (%s)' % (channel))  # channel 1 in slot 1
        dcVoltage = temp_values[0]
        return dcVoltage

    def get_current(self, range=100.0, res=6.5, npl_cycles=10.0, offset=1, channel='@1001'):
        # Configure the range, resolution and channel for voltage measurement
        self.v34980A.write(':CONFigure:SCALar:CURRent:DC %G,%G,(%s)' % (range, res, channel))
        # Configure number of NPL cycles
        self.v34980A.write(':SENSe:CURRent:DC:NPLCycles %G,(%s)' % (npl_cycles, channel))
        # Sets offset compensation
        self.v34980A.write(':SENSe:CURRent:OCOMpensated %d,(%s)' % (offset, channel))

        # Take a current measurement
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:CURRent:DC?')
        # temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:CURRent:DC? (%s)' % ('@1001'))
        dcCurrent = temp_values[0]
        return dcCurrent

    def get_resistance(self, range=100.0, res=6.5, npl_cycles=10.0, offset=1, channel='@1001'):
        # Configure the range, resolution and channel for resistance measurement
        self.v34980A.write(':CONFigure:SCALar:RESistance %G,%G,(%s)' % (range, res, channel))
        # Configure number of NPL cycles
        self.v34980A.write(':SENSe:RESistance:NPLCycles %G,(%s)' % (npl_cycles, channel))
        # Sets offset compensation
        self.v34980A.write(':SENSe:RESistance:OCOMpensated %d,(%s)' % (offset, channel))

        # Take a resistance measurement
        temp_values = self.v34980A.query_ascii_values(':MEASure:SCALar:RESistance? (%s)' % (channel))
        resistance = temp_values[0]
        return resistance

    def log(self, data_arr):
        try:
            with open("data.csv", "a") as f:
                line = f"Date and Time: {datetime.datetime.now()}, {data_arr[2]}\n"
                f.write(line)
        except Exception as e:
            print(e)

    def close(self):
        self.v34980A.close()
        self.rm.close()


inst = _34980A()
inst.set_range()
inst.set_four_wire()
inst.set_channel_delay()
for i in range(1, 32):
    channel_string = '@' + str(1000 + i)
    print("Channel ", channel_string)
    voltage = inst.get_voltage(channel=channel_string)  # get voltage
    print("Voltage : ", voltage)
    print("=====================================")
    current = inst.get_current(channel=channel_string)  # get current
    print("Current : ", current)
    print("=====================================")
    resistance = inst.get_resistance(channel=channel_string)
    print("Resistance : ", resistance, "\n")  # get resistance
    inst.log([voltage, current, resistance])

inst.close()

data = pd.read_csv(r'data.csv', usecols=[0, 1], names=['colA', 'colB'], header=None)

y = data['colB'].tolist()
print(y)
x = list(range(1, (len(data['colA'].tolist()) + 1)))
print(x)

# plotting the points
plt.plot(x[0:82], y[0:82])  # initial pressure -> blue
plt.plot(x[81:174], y[81: 174], 'r')  # increased pressure -> red
plt.plot(x[173:236], y[173: 236], 'g')  # decreased pressure -> green
plt.plot(x[235:(len(data['colA'].tolist()) + 1)], y[235: (len(data['colA'].tolist()) + 1)])  # increased pressure -> orange

plt.xlabel('x - axis')
plt.ylabel('Resistance')

plt.title('Resistance')

# function to show the plot
plt.show()
