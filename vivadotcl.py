#!/usr/bin/env python2

import pexpect

class VivadoInstance():
	def __init__(self, path):
		self.vivado = pexpect.spawn(path, ['-nojournal', '-nolog', '-mode', 'tcl'])
		self.vivado.expect('% ')
		self.hw_opening = False

	def send_command(self, s):
		self.vivado.sendline(s)
		self.vivado.expect('\r\n')
		self.vivado.expect('vivado.*% ')
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
		if self.hw_opening:
			self.send_command('close_hw_target')
			self.hw_opening = False

		self.send_command('open_hw_target ' + target)
		self.hw_opening = True
		self.send_command('set_property PROGRAM.FILE { ' + bitfile + '} [current_hw_device]')
		return self.send_command('program_hw_devices [current_hw_device]')
