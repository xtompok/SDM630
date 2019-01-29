# -*- coding: utf_8 -*-

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

import serial
import time
import csv

class SDM630(object):
	(TCP,RS485) = (0,1)
	# connecting using tcp
	def __init__(self,host,port,aid,regfile):
		self.connection_type = self.TCP
		self.__fill_registers__(regfile)
		self.aid = aid
		self.host = host
		self.port = port

	# connecting using serial port
	def __init__(self,port, baudrate, bytesize, parity, stopbits, xonxoff, dsrdtr, aid, regfile):
		self.connection_type = self.RS485
		self.__fill_registers__(regfile)
		self.port = port
		self.baudrate = baudrate
		self.bytesize = bytesize
		self.parity = parity
		self.stopbits = stopbits
		self.xonxoff = xonxoff
		self.dsrdtr = dsrdtr
		self.aid = aid


	def __fill_registers__(self, regfile):
		self.registers = {}
		with open(regfile) as regs:
			reader = csv.reader(regs,delimiter=';')
			for line in reader:
				self.registers[line[1]] = int(line[0],base=16)
	

	def connect(self):
		if (self.connection_type == self.TCP):
			self.master = ModbusTcpClient(host=self.host,port=self.port)
		elif (self.connection_type == self.RS485):
			self.master = modbus_rtu.RtuMaster(serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.xonxoff, self.dsrdtr))
			self.master.set_timeout(1.0)
			#self.master.set_verbose(True)

		
	def __getattr__(self,attr):
		if attr == "voltx3":
			return self.read_registers(self.registers['v1'],3)
		if attr == "ampx3":
			return self.read_registers(self.registers['a1'],3)
		if attr == "powx3":
			return self.read_registers(self.registers['p1'],3)

		if attr in self.registers:
			return self.read_registers(self.registers[attr],1)


	def read_registers(self,addr,count):
		res = self.master.read_input_registers(
			unit=self.aid, 
			address=addr, 
			count=2*count)
		decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>')
		if count == 1:
			return decoder.decode_32bit_float()
		return tuple(decoder.decode_32bit_float() for _ in range(count))

