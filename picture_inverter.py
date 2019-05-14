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
for i in range(1):
    input = pos_ins[0]
    ouputs = neural_net.new_gen()
    output = -(ouputs[0]+input)
    canvas.create_rectangle(400,400,500,500)

root.mainloop()
