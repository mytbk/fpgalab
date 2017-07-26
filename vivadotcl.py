#!/usr/bin/env python2

import pexpect

VIVADO_PROMPT = '[Vv]ivado.*% '


class VivadoInstance():

    def __init__(self, path):
        self.vivado = pexpect.spawn(
            path, ['-nojournal', '-nolog', '-mode', 'tcl'])
        self.vivado.expect(VIVADO_PROMPT)
        self.hw_opening = None

    def send_command(self, s):
        self.vivado.sendline(s)
        self.vivado.expect('\r\n')
        self.vivado.expect(VIVADO_PROMPT)
        return self.vivado.before

    def source_tcl(self, tclfile):
        result = self.send_command('source ' + tclfile)
        return result

    def connect_hw_server(self):
        self.send_command('open_hw')
        self.send_command('connect_hw_server')

    def get_hw_targets(self):
        self.send_command('refresh_hw_server')
        hws = self.send_command('puts [get_hw_targets -quiet]')
        return hws.split()

    def program_target(self, target, bitfile):
        if self.hw_opening is not None:
            if self.hw_opening != target:
                self.send_command('close_hw_target')
                self.send_command('open_hw_target ' + target)
        else:
            self.send_command('open_hw_target ' + target)

        self.send_command(
            'set_property PROGRAM.FILE { ' + bitfile + '} [current_hw_device]')
        return self.send_command('program_hw_devices [current_hw_device]')

if __name__ == "__main__":
    import sys
    # example: python2 vivadotcl.py \
    # /usr/local/Vivado_Lab/2017.2/bin/vivado_lab test.bit
    # Tested with Vivado WebPACK 2017.2 and Vivado Lab Edition 2017.2
    vivado_path = sys.argv[1]
    bit_path = sys.argv[2]
    v = VivadoInstance(vivado_path)
    v.connect_hw_server()
    hw = v.get_hw_targets()
    print 'all hardware targets: ' + str(hw)
    print v.program_target(hw[0], bit_path)
