# -*- coding: utf_8 -*-

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import time
import csv

class SDM630(object):
	def __init__(self,port,aid,regfile):
		self.registers = {}
		with open(regfile) as regs:
			reader = csv.reader(regs,delimiter=';')
			for line in reader:
				self.registers[line[1]] = line[0]
		self.aid = aid
		self.master = modbus_rtu.RtuMaster(port)
		self.master.set_timeout(1.0)
#		self.master.set_verbose(True)

		
	def __getattr__(self,attr):
		if attr in self.registers:
			return read_register(self.registers[attr])


	def read_register(self,addr):
		return self.master.execute(slave=self.aid, function_code=cst.READ_INPUT_REGISTERS, starting_address=addr, quantity_of_x=2, data_format='>f')[0]
		

