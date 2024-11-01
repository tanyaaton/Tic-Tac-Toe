#####################################################################################################################

import socket, struct, time
from pymodbus.client import ModbusTcpClient
import numpy,time
import math
from gripper import Gripper

# from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move

def UR_set_up():
        global tcp, joint_rad, joint_deg, joint_rev
        robot = '10.10.0.61'
        port = 30003
        gripper_port    = 63352
        tcp = {}
        joint_rad = {}
        joint_deg = {}
        joint_rev = {}

        stop_robot = False

        #Establish connection to controller
        global s, client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((robot, port))
        print("Start")

        client = ModbusTcpClient(robot)

        if client.connect() :
                print ('Connection established')
        else :
                print ('Connection failed')
#####################################################################################################################
                
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

def robot_turn(input_int):
        # read_pos()
        if input_int == 0:
                print("Zero command")
                cmd_move = str.encode('x = get_actual_joint_positions()\n')
                s.send(cmd_move)
                cmd_move = str.encode('movej([x[0],x[1],x[2],x[3],x[4],x[5]+0.05]), 0.5, 0.2,0.01, 0.1, 300)\n')
                s.send(cmd_move)
        if input_int == 1:
                print("First command")
                s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.03,0,0,0,0,0]),0.5,0.2,0,0)\n')
                time.sleep(0.5)
        if input_int == 2:
                print("Second command")
                s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.03,0,0,0,0,0]),0.5,0.2,0,0)\n')
                time.sleep(0.5)
def home():
        count = 0
        while count < 7000:
                print("First command")
                # radians_list = [round(math.radians(degree), 3) for degree in [-90, -90, -90, -90, 90, 0]]
                radians_list = [round(math.radians(degree), 3) for degree in [90, -90, -90, 0, 90, 360]]
                cmd_move = str.encode(f'servoj({radians_list}, 0, 0,0.01, 0.1, 100)\n')
                s.send(cmd_move)
                print("Done send command")
                count += 1
        print("Home command")

def play_position():
        # s.send(b'movel(p[0.0818,0.4126,0.4305, -1.572, 0, 0],1,0.2,0,0)\n')
        # y -5
        cmb_move = str.encode('movel(p[0.0818,0.4126,0.4305, -1.572, 0, 0],1,0.2,0,0)\n')
        s.send(cmb_move)
        time.sleep(4) 



def grid():
        # First Hori. line
        time.sleep(1)
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.1,0,0,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(2)  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.2,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(3) 
        s.send(b'movel(p[0.1318,0.4625, 0.4805, -1.572, 0, 0],1,0.2,0,0)\n')
        time.sleep(3)  
        # Second Hori. line  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.25,0,0)\n')
        time.sleep(1)
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.1,0,0,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(2)  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.2,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)
        s.send(b'movel(p[0.1318,0.4625, 0.3805, -1.572, 0, 0],1,0.2,0,0)\n')
        time.sleep(3)  
        #First vertical line
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,0.3,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(3)  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(3) 
        #Second vertical line
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.3,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(3)  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0.05,0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(3) 
        play_position()
#####################################################################################################################

position = {
    "p0": "p[0.0818, 0.4126, 0.4305, -1.572, 0, 0]",
    "p1": "p[-0.1, 0.0, 0.1,  0.0, 0.0, 0.0]",
    "p2": "p[0.0,  0.0, 0.1,  0,   0.0, 0.0]",
    "p3": "p[0.1,  0.0, 0.1,  0.0, 0.0, 0.0]",
    "p4": "p[-0.1, 0.0, 0.0,  0.0, 0.0, 0.0]",
    "p5": "p[0.0,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "p6": "p[0.1,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "p7": "p[-0.1, 0.0, -0.1,  0.0, 0.0, 0.0]",
    "p8": "p[0.0,  0.0, -0.1,  0.0, 0.0, 0.0]",
    "p9": "p[0.1,  0.0, -0.1,  0.0, 0.0, 0.0]",
}

position_X = {
    "q1": "p[0.02, 0.0, 0.02,  0.0, 0.0, 0.0]",
    "q2": "p[-0.02,  0.0, -0.02,  0.0, 0.0, 0.0]",
    "q3": "p[0.0, 0.0, 0.02828,  0.0, 0.0, 0.0]",
    "q4": "p[0.02, 0.0, -0.02,  0.0, 0.0, 0.0]"

}

def relative_command(p):
    return str.encode(f'movel(pose_add(get_actual_tcp_pose(),{p}),1,0.2,0,0)\n')

def move_to_position(p):
    cmd_move = relative_command(p)
    s.send(cmd_move)
    time.sleep(1)

def move_in():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0.05,0,0,0,0]),1,0.25,0,0)\n')
        time.sleep(1)



def draw_X():
        move_to_position(position_X["q1"])
        move_to_position(position_X["q2"])
        move_to_position(position_X["q3"])
        move_to_position(position_X["q4"])
        return None

def draw_O():
        return None

def player_turn(position, symbol):
        move_to_position(position)
        if symbol == "X":
                draw_X()
        elif symbol == "O":
                draw_O()
        return None

def robot_turn(position, symbol):
        #xo algorithm
        move_to_position(position)
        if symbol == "X":
                draw_X()
        elif symbol == "O":
                draw_O()
        return None



def test():
        # s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.05,0,0,0,0,0]),1,0.25,0,0)\n')
        # time.sleep(1)
        # s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,0.05,0,0,0]),1,0.25,0,0)\n')
        # time.sleep(1)
        # s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.05,0,0,0,0,0]),1,0.25,0,0)\n')
        # time.sleep(1)
        # s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.05,0,0,0]),1,0.25,0,0)\n')
        # time.sleep(1)
        # s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.05,-0.05,-0.05,0,0,0]),1,0.25,0,0)\n')     
        # time.sleep(1) 
        play_position()
        i=1
        print(f"p{i}")
        print(position[f"p{i}"])
        move_to_position(position[f"p{i}"])
        move_in()
        draw_X()
        print("Done")
        play_position()

def gripper_connection():
        global gripper
        gripper = Gripper('10.10.0.61', 63352)
        gripper.connection()

def gripper_test():
        gripper.control(255)
        time.sleep(3)
        gripper.control(0)

def gripper_close():
        gripper.control(255)

def gripper_open():
        gripper.control(0)

if __name__ == '__main__':
        # gripper_connection()
        # gripper_test()
        # gripper_close()
        # gripper_open()

        UR_set_up()
        # robot_turn()
        # robot_turn(0)
        # home()
        # test()
        # grid()
        # read_pos()