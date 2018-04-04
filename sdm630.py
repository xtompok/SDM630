# -*- coding: utf_8 -*-

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import time

class SDM630(object):
	def __init__(self,port,aid):
		self.voltage = [0,0,0]
		self.current = [0,0,0]
		self.total_power = 0
		# TODO rest

		self.aid = aid
		self.master = modbus_rtu.RtuMaster(
			serial.Serial(port=port, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, dsrdtr=True)
		)
		self.master.set_timeout(1.0)
#		self.master.set_verbose(True)

	def read_register(self,addr):
		return self.master.execute(slave=self.aid, function_code=cst.READ_INPUT_REGISTERS, starting_address=addr, quantity_of_x=2, data_format='>f')[0]
		

	def get_data(self):
		v1 = self.read_register(0x0000)
		v2 = self.read_register(0x0002)
		v3 = self.read_register(0x0004)
		a1 = self.read_register(0x0006)
		a2 = self.read_register(0x0008)
		a3 = self.read_register(0x000A)
		p1 = self.read_register(0x000C) 
		p2 = self.read_register(0x000E) 
		p3 = self.read_register(0x0010) 
		va1 = self.read_register(0x0012) 
		va2 = self.read_register(0x0014) 
		va3 = self.read_register(0x0016) 
		var1 = self.read_register(0x0018) 
		var2 = self.read_register(0x001A) 
		var3 = self.read_register(0x001C) 
		pf1 = self.read_register(0x001E) 
		pf2 = self.read_register(0x0020) 
		pf3 = self.read_register(0x0022) 
		ang1 = self.read_register(0x0024) 
		ang2 = self.read_register(0x0026) 
		ang3 = self.read_register(0x0028) 
		self.avg_voltage = self.read_register(0x002A) 
		self.avg_current = self.read_register(0x002E) 
		self.sum_current = self.read_register(0x0030) 
		self.total_power = self.read_register(0x0034) 
		self.total_va = self.read_register(0x0038) 
		self.total_var = self.read_register(0x003C) 
		self.total_pf = self.read_register(0x003E) 
		self.total_angle = self.read_register(0x0042) 
		self.frequency = self.read_register(0x0046) 
		self.import_wh = self.read_register(0x0048) 
		self.export_wh = self.read_register(0x004A) 
		self.import_vah = self.read_register(0x004C) 
		self.export_vah = self.read_register(0x004E) 
		self.vah = self.read_register(0x0050) 
		self.ah = self.read_register(0x0052) 
		self.total_power_demand = self.read_register(0x0054) 
		self.max_total_power_demand = self.read_register(0x0056) 
		self.total_va_demant = self.read_register(0x0064) 
		self.max_total_va_demand = self.read_register(0x0066) 
		self.neutral_current_demand = self.read_register(0x0068) 
		self.max_neutral_current_demand = self.read_register(0x006A) 
		v1v2 = self.read_register(0x00C8) 
		v2v3 = self.read_register(0x00CA) 
		v3v1 = self.read_register(0x00CC) 
		self.avg_line2line_v = self.read_register(0x00CE) 
		self.neutral_current = self.read_register(0x00E0) 
		thd1 = self.read_register(0x00EA) 
		thd2 = self.read_register(0x00EC) 
		thd3 = self.read_register(0x00EE) 
		currthd1 = self.read_register(0x00F0) 
		currthd2 = self.read_register(0x00F2) 
		currthd3 = self.read_register(0x00F4) 
		self.avg_ln_v_thd= self.read_register(0x00F8) 
		self.avg_current_thd = self.read_register(0x00FA) 
		self.total_power_factor = self.read_register(0x00FE) 
		a1d = self.read_register(0x0102) 
		a2d = self.read_register(0x0104) 
		a3d = self.read_register(0x0106) 
		maxa1d = self.read_register(0x0108) 
		maxa2d = self.read_register(0x010A) 
		maxa3d = self.read_register(0x010C) 
		thd12 = self.read_register(0x014E) 
		thd23 = self.read_register(0x0150) 
		thd31 = self.read_register(0x0152) 
		self.avg_line2line_v_thd = self.read_register(0x0154) 
		self.voltage = [v1,v2,v3]
		self.current = [a1,a2,a3]
		self.power = [p1,p2,p3]
		self.va = [va1,va2,va3]
		self.var = [var1,var2,var3]
		self.pf = [pf1,pf2,pf3]
		self.angle = [ang1,ang2,ang3]
		self.line2line_v = [v1v2,v2v3,v3v1]
		self.thd_v = [thd1,thd2,thd3]
		self.thd_a = [currthd1,currthd2,currthd3]
		self.demand = [a1d,a2d,a3d]
		self.max_demand = [maxa1d,maxa2d,maxa3d]
		self.line2line_thd = [thd12,thd23,thd31]
	
		self.time = time.time()
