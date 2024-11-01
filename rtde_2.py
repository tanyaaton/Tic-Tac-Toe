# encoding: utf=8

""" 
#UR Controller Primary Client Interface Reader
# For software version 3.0
#
# Datastream info found here: http://support.universal-robots.com/Technical/PrimaryAndSecondaryClientInterface
# Struct library used to extract data, info found here: https://docs.python.org/2/library/struct.html
"""

import socket, struct, time
from pymodbus.client import ModbusTcpClient
import numpy,time



robot = '10.10.0.61'
port = 30003
gripper_port    = 63352
tcp = {}
joint_rad = {}
joint_deg = {}
joint_rev = {}

stop_robot = False

#####################################################################################################################
#Establish connection to controller
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((robot, port))

client = ModbusTcpClient(robot)

if client.connect() :
        print ('Connection established')
else :
        print ('Connection failed')
#####################################################################################################################


def gripper_connection() :
        global g
        #Socket communication
        g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        g.connect((robot, gripper_port))
        g.sendall(b'GET POS\n')
        g_recv = str(g.recv(10), 'UTF-8')
        if g_recv :
                g.send(b'SET ACT 1\n')
                g_recv = str(g.recv(10), 'UTF-8')
                print (g_recv)
                time.sleep(3)
                g.send(b'SET GTO 1\n')
                g.send(b'SET SPE 255\n')
                g.send(b'SET FOR 255\n')
                print ('Gripper Activated')

                g.send(b'SET POS 0\n')
                
def read_pos():


        #Read tcp value from Modbus server
        t = client.read_holding_registers(400,6)
        
        #Extract and convert values
        for i in range(0,6):
                tcp[i] = t.registers[i]
                if tcp[i] > 32768:
                        tcp[i] = tcp[i] - 65535
                if i < 3 :
                        tcp[i] = float(tcp[i])/10000
                else :
                        tcp[i] = float(tcp[i])/1000
        #Read joint angles from Modbus server
        j = client.read_holding_registers(270,6)                        
        r = client.read_holding_registers(320,6)        
        #Extract and convert values	
        for i in range(0,6):	
                joint_rad[i] = j.registers[i]
                joint_rev[i] = r.registers[i]

                if joint_rev[i] == 65535:
                        joint_rad[i] = joint_rad[i] - 6283             
                joint_rad[i] = float(joint_rad[i])/1000                     
                joint_deg[i] = "{:.2f}".format(numpy.degrees(joint_rad[i]))

        if 1:
                #Print title to screen
                print ('*******')
                print ('UR Controller Primary Client Interface Reader' )
                print ('*******')
                #extract packet length, timestamp and packet type from start of packet and print to screen
                #if message type is cartesian data, extract doubles for 6DOF pos of TCP and print to screen
                print ('X  ' +  '%20s' % str(tcp[0]))
                print ('Y  ' +  '%20s' % str(tcp[1]))
                print ('Z  ' +  '%20s' % str(tcp[2]))
                print ('RX ' +  '%20s' % str(tcp[3]))
                print ('RY ' +  '%20s' % str(tcp[4]))
                print ('RZ ' +  '%20s' % str(tcp[5]))
                print ('****************************************\n')

                print ('Base    ' +  '%20s' % str(joint_deg[0]))
                print ('Shoulder' +  '%20s' % str(joint_deg[1]))
                print ('Elbow   ' +  '%20s' % str(joint_deg[2]))
                print ('Wrist 1'  +  '%20s' % str(joint_deg[3]))
                print ('Wrist 2'  +  '%20s' % str(joint_deg[4]))
                print ('Wrist 3'  +  '%20s' % str(joint_deg[5]))
                print ('****************************************\n')
                time.sleep(1)


def main():

        # read_pos()

        while 1   :
                g.send(b'SET POS 255\n')
                g_recv = str(g.recv(255), 'UTF-8')
                print (g_recv)
                time.sleep(2)
                g.send(b'SET POS 0\n')
                g_recv = str(g.recv(255), 'UTF-8')
                print (g_recv)
                time.sleep(2)




if __name__ == '__main__':
    import sys
    gripper_connection()
    main()
