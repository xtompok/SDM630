# -*- coding: utf_8 -*-

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

import serial
import time
import csv

class SDM630(object):
	def __init__(self, regfile):
		self.__fill_registers__(regfile)
	
	def __fill_registers__(self, regfile):
		self.registers = {}
		with open(regfile) as regs:
			reader = csv.reader(regs,delimiter=';')
			for line in reader:
				self.registers[line[1]] = int(line[0],base=16)
	
		
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

# connecting using tcp
class SDM630TCP(SDM630):
	def __init__(self,host,port,aid,regfile):
		SDM630.__init__(self,regfile)

		self.aid = aid
		self.host = host
		self.port = port
		
		self.master = ModbusTcpClient(host=self.host,port=self.port)


# connecting using serial port
class SDM630RS485(SDM630):
	def __init__(self, port, baudrate, aid, regfile):
		SDM630.__init__(self,regfile)

		self.port = port
		self.baudrate = baudrate
		self.aid = aid

		self.master = ModbusSerialClient("rtu", port=self.port, baudrate=self.baudrate, timeout=1)


