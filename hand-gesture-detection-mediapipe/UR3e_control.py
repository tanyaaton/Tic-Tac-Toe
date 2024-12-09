#####################################################################################################################

import socket, struct, time
from pymodbus.client import ModbusTcpClient
import numpy,time
import math
from gripper import Gripper
from minimax_tictactoe import winner_row

# from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move

def UR_set_up():
        global tcp, joint_rad, joint_deg, joint_rev
        robot = '10.10.0.61'
        # robot = '192.168.1.106'
        port = 30003
        gripper_port  = 63352
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
#####################################################################################################################
def home():
        radians_list = [round(math.radians(degree), 3) for degree in [90, -90, -90, 0, 90, 360]] #Home2
        cmd_move = str.encode(f'movej({radians_list},1, 1)\n')
        s.send(cmd_move)
        time.sleep(2)
        print("Home command done")

def send_nothing():
        s.send(b'\n')
        print("Nothing")

def play_position():
        # s.send(b'movel(p[0.0818,0.4126,0.4305, -1.572, 0, 0],1,0.2,0,0)\n')
        # y -5
        movel("p[0.0818,0.4126,0.4305, -1.572, 0, 0]")
        print("Play position")
        time.sleep(1) 

def movel(p):
        cmb_move = str.encode(f'movel({str(p)},1,0.2,0,0)\n')
        s.send(cmb_move)
        time.sleep(1) 

def play_position_fromhome():
        cmb_move = str.encode('movel(pose_add(get_actual_tcp_pose(),p[-0.05,-0.05,-0.05,0,0,0]),1,0.2,0,0)\n')
        s.send(cmb_move)
        print("Play position")
        time.sleep(1) 

def grid():
        # First Hori. line
        time.sleep(1)
        move_out()
        time.sleep(1)
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1)
        move_in()
        time.sleep(2)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.3,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(3) 
        move_out()
        s.send(b'movel(p[0.1318,0.4625-0.05, 0.4805, -1.572, 0, 0],1,0.2,0,0)\n')
        time.sleep(2)  
        # Second Hori. line  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.25,0,0)\n')
        time.sleep(1)
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1)
        move_in()
        time.sleep(1)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.3,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(3)
        move_out()
        s.send(b'movel(p[0.1318,0.4625-0.05, 0.3805, -1.572, 0, 0],1,0.2,0,0)\n')
        time.sleep(2)  
        #First vertical line
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1)   
        move_in()
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,0.3,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(2) 
        move_out() 
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1) 
        #Second vertical line
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.1,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(1)
        move_in()
        time.sleep(1)   
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.3,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(2)  
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,-0.05,0.1,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2) 
        play_position()

def draw_vertical_line():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0,-0.2,0,0,0]),1,0.2,0,0)\n')     
        time.sleep(2)

def draw_horizontal_line():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.2,0,0,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)

def draw_diagonal_line_0():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0.2,0,-0.2,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)

def draw_diagonal_line_2():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.2,0,-0.2,0,0,0]),1,0.2,0,0)\n')
        time.sleep(2)

def draw_end_line(player):
        winner = winner_row(player)
        first_position = winner[0]
        middle_position = winner[1]
        rows = [[0, 1], [3, 4], [6, 7]]
        columns = [[0, 3], [1, 4], [2, 5]]
        diagonals = [[0, 4], [2, 4]]
        time.sleep(1)
        move_to_position(position[str(first_position+1)])
        time.sleep(1)
        move_in()
        time.sleep(1)
        if [first_position, middle_position] in rows:
                draw_horizontal_line()
        elif [first_position, middle_position] in columns:
                draw_vertical_line()
        elif [first_position, middle_position] in diagonals:
                if first_position == 0:
                        draw_diagonal_line_0()
                else:
                        draw_diagonal_line_2()
        time.sleep(1)
        play_position()
        home()

        print("Winner row: ", winner)

#####################################################################################################################

position = {
    "0": "p[0.0818, 0.4126, 0.4305, -1.572, 0, 0]",
    "1": "p[-0.1, 0.0, 0.1,  0.0, 0.0, 0.0]",
    "2": "p[0.0,  0.0, 0.1,  0,   0.0, 0.0]",
    "3": "p[0.1,  0.0, 0.1,  0.0, 0.0, 0.0]",
    "4": "p[-0.1, 0.0, 0.0,  0.0, 0.0, 0.0]",
    "5": "p[0.0,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "6": "p[0.1,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "7": "p[-0.1, 0.0, -0.1,  0.0, 0.0, 0.0]",
    "8": "p[0.0,  0.0, -0.1,  0.0, 0.0, 0.0]",
    "9": "p[0.1,  0.0, -0.1,  0.0, 0.0, 0.0]",
}

# position_X = {
#     "q1": "p[0.02, 0.0, 0.02,  0.0, 0.0, 0.0]",
#     "q2": "p[-0.02,  0.0, -0.02,  0.0, 0.0, 0.0]",
#     "q3": "p[0.0, 0.0, 0.02828,  0.0, 0.0, 0.0]",
#     "q4": "p[0.02, 0.0, -0.02,  0.0, 0.0, 0.0]"
# }
position_X = {
    "q1": "p[0.02828, 0.0, 0.02828,  0.0, 0.0, 0.0]",
    "q2": "p[-0.02828*2,  0.0, -0.02828*2,  0.0, 0.0, 0.0]",
    "q3": "p[0.0, 0.0, 0.02828*2,  0.0, 0.0, 0.0]",
    "q4": "p[0.02828*2, 0.0, -0.02828*2,  0.0, 0.0, 0.0]"
}

position_T = {
        "q0_1": "p[0, 0.0, -0.02,  0.0, 0.0, 0.0]",
        "q0_2": "p[0.02, 0.0, 0,  0.0, 0.0, 0.0]",
        "q1": "p[-0.02, 0.0, 0.04,  0.0, 0.0, 0.0]",
        "q2": "p[-0.02,  0.0, -0.04,  0.0, 0.0, 0.0]",
        "q3": "p[0.04, 0.0, 0,  0.0, 0.0, 0.0]"
}


def draw_X():
        move_to_position(position_X["q1"])
        move_to_position(position_X["q2"])
        move_out()
        move_to_position(position_X["q3"])
        move_in()
        move_to_position(position_X["q4"])
        return None

def draw_Tri():
        move_to_position(position_T["q0_1"])
        move_to_position(position_T["q0_2"])
        move_to_position(position_T["q1"])
        move_to_position(position_T["q2"])
        move_to_position(position_T["q3"])
        return None

def draw_O():
        radius = 0.04  # Radius of the circle
        #move-up and waypoint1
        move_out()
        cmd_move = relative_command(f'p[0, 0.0, {radius},  0.0, 0.0, 0.0]')
        s.send(cmd_move)
        time.sleep(1)
        move_in()
        time.sleep(1)
        #Waypoint2
        cmd_move = str.encode(f'movep(get_actual_tcp_pose(),0.1,0.1,r={radius})\n')
        s.send(cmd_move)
        time.sleep(2)
        #waypoint3
        cmd_move = str.encode(f'movec(pose_add(get_actual_tcp_pose(),p[-1*{radius}, 0.0, -1*{radius},  0.0, 0.0, 0.0]),pose_add(get_actual_tcp_pose(),p[0, 0.0, -2*{radius},  0.0, 0.0, 0.0]),0.1,0.05,r=0,mode=0)\n')
        s.send(cmd_move)
        time.sleep(3)
        #waypoint4
        cmd_move = str.encode(f'movec(pose_add(get_actual_tcp_pose(),p[1*{radius}, 0.0, 1*{radius},  0.0, 0.0, 0.0]),pose_add(get_actual_tcp_pose(),p[0, 0.0, 2*{radius},  0.0, 0.0, 0.0]),0.1,0.05,r=0,mode=0)\n')
        s.send(cmd_move)
        time.sleep(3)
        # #waypoint5
        # cmd_move = str.encode(f'movec(pose_add(get_actual_tcp_pose(),p[-1*{radius}, 0.0, -1*{radius},  0.0, 0.0, 0.0]),pose_add(get_actual_tcp_pose(),p[1*{radius}, 0.0, -1*{radius},  0.0, 0.0, 0.0]),0.1,0.1,r=0.015)\n')
        # s.send(cmd_move)
        # time.sleep(1)

def relative_command(p):
    return str.encode(f'movel(pose_add(get_actual_tcp_pose(),{p}),1,0.2,0,0)\n')

def move_to_position(p):
    cmd_move = relative_command(p)
    s.send(cmd_move)
    time.sleep(1)

def move_in():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,0.05,0,0,0,0]),1,0.25,0,0)\n')
        time.sleep(1)

def move_out():
        s.send(b'movel(pose_add(get_actual_tcp_pose(),p[0,-0.05,0,0,0,0]),1,0.25,0,0)\n')
        time.sleep(1)
        
def human_move(i, symbol):
        time.sleep(1)
        move_to_position(position[str(i)])
        time.sleep(1)
        move_in()
        if symbol == "X":
                draw_X()
        elif symbol == "O":
                draw_O()
        play_position()

def robot_move(i, symbol):
        #xo algorithm
        time.sleep(1)
        move_to_position(position[str(i)])
        time.sleep(1)
        move_in()
        if symbol == "X":
                draw_X()
        elif symbol == "O":
                draw_O()
        play_position()


def test():
        radians_list = [round(math.radians(degree), 3) for degree in [90, -90, -90, 0, 90, 360]] #Home2
        cmd_move = str.encode(f'movej({radians_list},1, 1)\n')
        s.send(cmd_move)

position = {
    "0": "p[0.073, -0.269, 0.3046, 3, 0, 0]",
    "1": "p[-0.1, 0.0, 0.1,  0.0, 0.0, 0.0]",
    "2": "p[0.0,  0.0, 0.1,  0,   0.0, 0.0]",
    "3": "p[0.1,  0.0, 0.1,  0.0, 0.0, 0.0]",
    "4": "p[-0.1, 0.0, 0.0,  0.0, 0.0, 0.0]",
    "5": "p[0.0,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "6": "p[0.1,  0.0, 0.0,  0.0, 0.0, 0.0]",
    "7": "p[-0.1, 0.0, -0.1,  0.0, 0.0, 0.0]",
    "8": "p[0.0,  0.0, -0.1,  0.0, 0.0, 0.0]",
    "9": "p[0.1,  0.0, -0.1,  0.0, 0.0, 0.0]",
}

if __name__ == '__main__':
        # gripper_test()
        # gripper_close()
        # gripper_open()

        UR_set_up()
        # gripper_connection()
        # gripper_open()
        # time.sleep(3)
        # gripper_close()
        home()
        # draw_X()
        # play_position()
        # draw_Tri()
        # draw_O()
        
        # play_position()
        # robot_move(1, 'X')
        # play_position()
        # test()
        # grid()
        # read_pos()
        # human_move(1, 'X')
