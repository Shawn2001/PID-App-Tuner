# Import the required libraries
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
# Create an instance of tkinter frame or window
win=Tk("PID Controller")
win.title("PID Controller Workshop")


WIDTH = 500
HEIGHT = 500
# Set the size of the window
win.geometry("500x500")

# Make the window size fixed
win.resizable(False,False)

# Create a canvas widget
canvas=Canvas(win, width=WIDTH, height=HEIGHT)
canvas.configure(bg='#e8cafa')
canvas.pack()

# Target point, range need to be 110 to 450
ppoint = 200

# Create an oval or ball in the canvas widget
ball=canvas.create_oval(230,100,270,150, fill="green3")
rectangle = canvas.create_rectangle(190,50, 310, 490, width = 2)
equilibrium_line = canvas.create_line((190,ppoint,310,ppoint), dash=(5,1))
pumper1 = canvas.create_rectangle((190,480,310,490), fill = "blue")
pumper2 = canvas.create_rectangle((220,470,280,480), fill ="blue")



xdata = []
ydata = []

# Set the maximum time running
tmax = 300
def plotting():
    global xdata, ydata, tmax
    if len(xdata) > tmax:
        xdata = xdata[0:tmax]
        ydata = ydata[0:tmax]
    top= Toplevel(win)
    top.geometry("750x250")
    top.title("My testing")
    f = plt.figure()
    canvas1 = FigureCanvasTkAgg(f,top)
    canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH)
    # canvasfig = FigureCanvasTkAgg(f, win)
    plt.plot(xdata,ydata)
    return

btn = Button(win, text='Plot the graph', width=10,
             height=2, bd='5', command=plotting)
btn.place(x=30, y=40)

## Reset Ball
def reset():
    global ball
    canvas.delete(ball)
    ball=canvas.create_oval(230,100,270,150, fill="green3")

btn = Button(win, text='Reset the ball', width=10,
             height=2, bd='5', command=reset)
btn.place(x=30, y=100)

# Initial speed of the ball
yspeed=5
xspeed=0

# Mass of the ball
mass = 1 
gravity = 9.8 # In Earth Gravity

# Current time and timestep
current_time = 0
timestep = 1


############# The workshop need to change from here #########################

# Parameters for PID Control
Kp = 0
Ki = 0
Kd = 0

# Previous error
error_prev = 0
# For Integral purpose
Ivalue = 0

############################## Please Tune this #######################################
def PID_control(yspeed, current_pos, target_pos):
    '''
        yspeed : the current speed of the ball (+ve is going down, -ve is going up)
        current_pos : current position of the ball (Range from 51, 489)
    '''
    global error_prev, current_time, total_error, Ivalue, Kp, Ki, Kd


    return yspeed

Kplabel= Label(canvas, text="Kp: ", fg = 'black')
Kplabel.place(x=30, y=160)
Kpentry= Entry(canvas,width=5)
Kpentry.insert(0, Kp)
Kpentry.place(x=60, y=160)
Kilabel= Label(canvas, text="Ki: ")
Kilabel.place(x=30, y=200)
Kientry= Entry(canvas,width=5) 
Kientry.insert(0, Ki)
Kientry.place(x=60, y=200)
Kdlabel= Label(canvas, text="Kd: ")
Kdlabel.place(x=30, y=240)
Kdentry= Entry(canvas,width=5) 
Kdentry.insert(0, Kd)
Kdentry.place(x=60, y=240)

def updatePID():
    global Kp, Ki, Kd, xdata, ydata, ball, current_time
    # Update Data
    Kp = float(Kpentry.get())
    Ki = float(Kientry.get())
    Kd = float(Kdentry.get())
    # Delete the ball
    canvas.delete(ball)
    # Create a new ball
    ball=canvas.create_oval(230,100,270,150, fill="green3")
    # Reset x and y data
    xdata = []
    ydata = []
    current_time = 0
    print(Kp,Ki,Kd)
    

btn = Button(win, text='Update PID', width=10,
             height=2, bd='5', command=updatePID)
btn.place(x=30, y=310)

# Move the ball
def move_ball():
    global xspeed, yspeed, current_time, ppoint, timestep, xdata, ydata
    current_time += timestep
    yspeed = yspeed + gravity * timestep 
    
    canvas.move(ball, xspeed, yspeed)
    (leftpos, toppos, rightpos, bottompos)=canvas.coords(ball)
    yspeed = PID_control(yspeed, int(toppos+bottompos)/2, ppoint)

    # Append Data For Plotting Purpose
    xdata.append(current_time)
    ydata.append(int(toppos+bottompos)/2) 
    if bottompos >=490:
        yspeed = -abs(yspeed) 
        canvas.move(ball, xspeed, yspeed)

    if toppos <=30:
        yspeed = abs(yspeed) 
        canvas.move(ball, xspeed, yspeed)
    canvas.after(30,move_ball)



canvas.after(30, move_ball)



win.mainloop()