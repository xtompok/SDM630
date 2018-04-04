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
sdm630 = SDM630(config.get("sdm630","port"),config.getint("sdm630","id"))

logging.info("Entering endless loop")
while (True):
	sdm630.get_data()
	publish("voltage/l1",sdm630.voltage[0])
	publish("voltage/l2",sdm630.voltage[1])
	publish("voltage/l3",sdm630.voltage[2])
	publish("current/l1",sdm630.current[0])
	publish("current/l2",sdm630.current[1])
	publish("current/l3",sdm630.current[2])
	publish("power/l1",sdm630.power[0])
	publish("power/l2",sdm630.power[1])
	publish("power/l3",sdm630.power[2])
	publish("power/total",sdm630.total_power)
	publish("voltamps/l1",sdm630.va[0])
	publish("voltamps/l2",sdm630.va[1])
	publish("voltamps/l3",sdm630.va[2])
	publish("voltage/avg",sdm630.avg_voltage)
	publish("current/avg",sdm630.avg_current)
	publish("current/sum",sdm630.sum_current)
	publish("frequency",sdm630.frequency)
	publish("voltage/l1l2",sdm630.line2line_v[0])
	publish("voltage/l2l3",sdm630.line2line_v[1])
	publish("voltage/l3l1",sdm630.line2line_v[2])
	publish("curent/neutral",sdm630.neutral_current)
	publish("wh/import",sdm630.import_wh)
	publish("wh/export",sdm630.export_wh)
	publish("time",sdm630.time)
	time.sleep(1)
