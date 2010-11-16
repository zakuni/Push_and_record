#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.7'
__date__ = 'May 17 2010'

#Basic imports
from ctypes import *
import sys
import random
import socket
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit




#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)
    
#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))
    
#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))
    
def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))
    
def interfaceKitError(e):
    source = e.device
    print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    
def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))
    
def interfaceKitSensorChanged(e):
    source = e.device
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

 # サーバーに値を送る
    try:
        conn, addr = s.accept()
        print 'Connected by', addr
        conn.send("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
        conn.close()
    except socket.error, e:
        print 'Error: %s' % e


                            
def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

    
#Main Program Code

try:
    interfaceKit.setOnAttachHandler(interfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
    
    print("Opening phidget object....")

    
try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

    print("Waiting for attach....")


try:
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()


print("Setting the data rate for each sensor index to 4ms....")
for i in range(interfaceKit.getSensorCount()):
    try:        
        interfaceKit.setDataRate(i, 4)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        

HOST = ''                                             
PORT = 20000       
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))                            
s.listen(1)


print("Press Enter to quit....")
    

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

