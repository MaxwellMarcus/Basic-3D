try:
    from tkinter import *
except:
    from Tkinter import *
import neural_net
import time

root = Tk()

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

neural_net.create_net_of_nets(100)
pos_ins = neural_net.possible_inputs
for i in range(1000):
    canvas.delete(ALL)
    input = pos_ins[0]
    outputs = neural_net.new_gen()
    output = outputs[0][0]
    canvas.create_rectangle(400,100,450,150,fill='grey'+str(int((input[0]+1)*50)))
    canvas.create_rectangle(450,100,500,150,fill='grey'+str(int((input[1]+1)*50)))
    canvas.create_rectangle(450,150,500,200,fill='grey'+str(int((input[2]+1)*50)))
    canvas.create_rectangle(400,150,450,200,fill='grey'+str(int((input[3]+1)*50)))
    canvas.create_rectangle(600,100,650,150,fill='grey'+str(int((output[0]+1)*50)))
    canvas.create_rectangle(650,100,700,150,fill='grey'+str(int((output[1]+1)*50)))
    canvas.create_rectangle(650,150,700,200,fill='grey'+str(int((output[2]+1)*50)))
    canvas.create_rectangle(600,150,650,200,fill='grey'+str(int((output[3]+1)*50)))

    input = pos_ins[8]
    output = outputs[0][8]
    canvas.create_rectangle(400,300,450,350,fill='grey'+str(int((input[0]+1)*50)))
    canvas.create_rectangle(450,300,500,350,fill='grey'+str(int((input[1]+1)*50)))
    canvas.create_rectangle(450,350,500,400,fill='grey'+str(int((input[2]+1)*50)))
    canvas.create_rectangle(400,350,450,400,fill='grey'+str(int((input[3]+1)*50)))

    canvas.create_rectangle(600,300,650,350,fill='grey'+str(int((output[0]+1)*50)))
    canvas.create_rectangle(650,300,700,350,fill='grey'+str(int((output[1]+1)*50)))
    canvas.create_rectangle(650,350,700,400,fill='grey'+str(int((output[2]+1)*50)))
    canvas.create_rectangle(600,350,650,400,fill='grey'+str(int((output[3]+1)*50)))
    canvas.create_text(500,500,text='fitness: '+str(outputs[1]))
    root.update()
    #time.sleep(.01)

root.mainloop()
