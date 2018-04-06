#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from sdm630 import SDM630

import sys
import serial
import time
import paho.mqtt.client as mqtt
import logging
import os
import traceback
import configparser as ConfigParser

CONFIG_FILE = 'sdm630-mqtt.conf'

logging.getLogger().setLevel(logging.DEBUG)

def publish(topic,value):
	info = mqclient.publish("/".join((config.get("mqtt","topic_prefix"),topic)),value,qos=1)
	info.wait_for_publish()

	
if ((len(sys.argv) == 3) and sys.argv[1] == '-c'):
	CONFIG_FILE = sys.argv[2]
logging.info("Reading config...")
config = ConfigParser.ConfigParser()
confread = config.read(CONFIG_FILE)
logging.info("Read config {}".format(confread))
logging.info("Opening port {}".format(config.get("sdm630","port")))
port = serial.Serial(port=config.get("sdm630","port"), baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, dsrdtr=True)

logging.info("Connecting to MQTT server...")
mqclient = mqtt.Client()
try:
	mqclient.connect(config.get("mqtt","server"),
		config.getint("mqtt","port"),
		config.getint("mqtt","keepalive"))
	mqclient.loop_start()
except:
	traceback.print_exc()
	logging.error("Cannot connect to MQTT server")
	sys.exit(1)

logging.info("Setup...")
num_meters = config.getint("sdm630","num_meters")
meters = []
for i in range(num_meters):
	meters.append(SDM630(port,config.getint("sdm630","id"+str(i+1))))

logging.info("Entering endless loop")
while (True):
	for (num,sdm630) in enumerate(meters):
		num += 1
		sdm630.get_data()
		publish(str(num)+"/voltage/l1",sdm630.voltage[0])
		publish(str(num)+"/voltage/l2",sdm630.voltage[1])
		publish(str(num)+"/voltage/l3",sdm630.voltage[2])
		publish(str(num)+"/current/l1",sdm630.current[0])
		publish(str(num)+"/current/l2",sdm630.current[1])
		publish(str(num)+"/current/l3",sdm630.current[2])
		publish(str(num)+"/power/l1",sdm630.power[0])
		publish(str(num)+"/power/l2",sdm630.power[1])
		publish(str(num)+"/power/l3",sdm630.power[2])
		publish(str(num)+"/power/total",sdm630.total_power)
		publish(str(num)+"/voltamps/l1",sdm630.va[0])
		publish(str(num)+"/voltamps/l2",sdm630.va[1])
		publish(str(num)+"/voltamps/l3",sdm630.va[2])
		publish(str(num)+"/voltage/avg",sdm630.avg_voltage)
		publish(str(num)+"/current/avg",sdm630.avg_current)
		publish(str(num)+"/current/sum",sdm630.sum_current)
		publish(str(num)+"/frequency",sdm630.frequency)
		publish(str(num)+"/voltage/l1l2",sdm630.line2line_v[0])
		publish(str(num)+"/voltage/l2l3",sdm630.line2line_v[1])
		publish(str(num)+"/voltage/l3l1",sdm630.line2line_v[2])
		publish(str(num)+"/curent/neutral",sdm630.neutral_current)
		publish(str(num)+"/wh/import",sdm630.import_wh)
		publish(str(num)+"/wh/export",sdm630.export_wh)
		publish(str(num)+"/time",sdm630.time)
	time.sleep(1)
