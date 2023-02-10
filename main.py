import tkinter as tk

from tkinter import filedialog
from tkinter.constants import *

from math import sqrt

import os

DOT_RADIUS = 4
frac_dts = []
shape = []
temp = []

# resizes the window
def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height
    canvas_output['width'] = event.width - 600
    canvas_output['height'] = event.height

    blit()

# clears both canvases
def clear():
    clear_shape()
    clear_fractal()
    shape_name_val.set('')

def clear_shape():
    global shape
    shape = []
    canvas_shape.delete('all')

# clears fractal canvas
def clear_fractal():
    global frac_dts
    frac_dts = []
    canvas_output.delete('all')

# opens a .txt file with shape coordinates [(x, y), (x1, y1)...]
# where 0 < x < 600 and 0 < y < 300
def import_shape(event):
    global shape
    import_dialog = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Choose a shape that you want",
        filetypes=(("Text Files", "*.txt"),)
    )

    try:
        f = open(import_dialog)
    except FileNotFoundError or TypeError:
        f = open(os.path.join(os.getcwd(), 'err.txt'))
    clear()

    for line in f:
        shape.append(tuple(map(int, line.split())))
    f.close()

    draw_shape()

def export_shape(event):
    if not os.path.exists("shapes"):
        os.makedirs("shapes")

    f = open(os.path.join("shapes", shape_name_val.get() + '.txt'), 'w')

    for i in range(len(shape)):
        f.write(str(shape[i][0]) + ' ' + str(shape[i][1]) + '\n')

# adds dot's coordinates to shape
def add_to_shape_by_click(event):
    global shape, temp
    dotsc = len(shape)

    if dotsc > 0:
        if event.state in [1, 9]: # checks if shift is pressed
            if abs(event.x - shape[-1][0]) > abs(event.y - shape[-1][1]):
                shape.append((event.x, shape[-1][1]))
            else:
                shape.append((shape[-1][0], event.y))
        else:
            shape.append((event.x, event.y))
    else:
        shape.append((event.x, event.y))

    temp = []
    draw_shape()

def undo(event):
    if len(shape) != 0:
        temp.append(shape.pop(-1))
        canvas_shape.delete('all')
        draw_shape()

def redo(event):
    if len(temp) != 0:
        shape.append(temp.pop(-1))
        canvas_shape.delete('all')
        draw_shape()

# draws a shape in canvas_shape 
def draw_shape():
    global shape
    x1, y1, x2, y2 = 0, 0, 0, 0
    for c in shape:
        x1 = c[0] - DOT_RADIUS
        y1 = c[1] - DOT_RADIUS
        x2 = c[0] + DOT_RADIUS
        y2 = c[1] + DOT_RADIUS
        canvas_shape.create_oval(x1, y1, x2, y2, fill="black")

    if len(shape) > 1:
        canvas_shape.create_line(*shape, width=2)


def fractal():
    global cF, sF, veclength, veclengthcomp
    clear_fractal()

    dotsc = len(shape)
    if dotsc < 3: return

    sF = [0.0] * dotsc
    cF = [1.0] * dotsc
    veclength = [sqrt((shape[-1][0] - shape[0][0])**2 + (shape[-1][1] - shape[0][1])**2)] * dotsc
    veclengthcomp = [1.0] * dotsc

    x0 = shape[0][0]
    y0 = shape[0][1]

    xL = shape[-1][0]
    yL = shape[-1][1]

    vecf = (xL - x0, yL - y0)

    for i in range(1, dotsc):
        xn = shape[i][0]
        yn = shape[i][1]
        vecn = (xn - x0, yn - y0)

        veclength[i] = sqrt(vecn[0]**2 + vecn[1]**2)
        cF[i] = round((vecn[0] * vecf[0] + vecn[1] * vecf[1]) / (veclength[i] * veclength[0]), 4)
        sF[i] = round(sqrt(1 - cF[i]**2), 8)

        veclengthcomp[i] = round(veclength[i] / veclength[0], 4)

    build_fractal(
        100,
        int(canvas_output['height']) // 2,
        int(canvas_output['width']) - 100,
        int(canvas_output['height']) // 2,
        int(iter_val.get()) - 1
    )
    scale_fractal()
    blit()

# creates a list of coordinates that form a fractal (frac_dts)
def build_fractal(xn, yn, xe, ye, iter):
    global frac_dts
    dotsc = len(shape)

    # first dot
    coords = [(round(xn, 4), round(yn, 4))]

    for i in range(1, dotsc - 1):
        # calculating next step vector
        x = xe - xn
        y = ye - yn
        xr = (x * cF[i] + y * sF[i]) * veclengthcomp[i]
        yr = (-x * sF[i] + y * cF[i]) * veclengthcomp[i]
        coords.append((round(xr + xn, 4), round(yr + yn, 4)))

    # last dot
    coords.append((round(xe, 4), round(ye, 4)))

    if iter == 0:
        for i in range(dotsc):
            frac_dts.append(coords[i])
        return

    for i in range(1, dotsc):
        build_fractal(
            coords[i-1][0],
            coords[i-1][1],
            coords[i][0],
            coords[i][1],
            iter - 1
        )

def scale_fractal():
    global frac_dts

    minx, miny = maxx, maxy = frac_dts[0]

    for i in range(len(frac_dts)):
        xc, yc = frac_dts[i]
        if minx > xc:
            minx = xc
        elif maxx < xc:
            maxx = xc

        if miny > yc:
            miny = yc
        elif maxy < yc:
            maxy = yc

    facX = (int(canvas_output['width']) + 400) / (maxx - minx)
    facY = (int(canvas_output['height']) - 20) / (maxy - miny)
    fac = min(facX, facY)

    for i in range(len(frac_dts)):
        frac_dts[i] = (round((frac_dts[i][0] - minx) * fac, 6) + 10,
                       round((frac_dts[i][1] - miny) * fac, 6) + 10)


def blit():
    canvas_output.delete('all')

    if frac_dts != []:
        scale_fractal()
        canvas_output.create_line(*frac_dts)


if __name__ == "__main__":
    # root stuff
    root = tk.Tk()
    root.title("Fractal Builder")
    root.minsize(1500, 700)
    root.resizable(width=True, height=True)

    # FRAMES AND CANVASES
    # main frame
    frame_main = tk.Frame(
        root,
        borderwidth=0, relief=FLAT)
    frame_main.pack(expand=YES, fill=BOTH)

    # frame with all the inputs
    frame_input = tk.Frame(
        frame_main,
        width=600,
        borderwidth=0, relief=FLAT, bg="grey"
    )
    frame_input.pack(side=RIGHT, expand=NO, fill=Y)

    # frame with building buttons and parameters
    frame_building = tk.Frame(
        frame_input,
        borderwidth=0,
        relief=FLAT
    )
    frame_building.pack(side=TOP, expand=NO, fill=X)

    # canvas that displays a fractal
    canvas_output = tk.Canvas(
        frame_main,
        borderwidth=0, relief=FLAT, bg="silver",
        highlightthickness=0
    )
    canvas_output.pack(side=LEFT, expand=YES, fill=BOTH)

    # canvas that contains a drawn shape
    canvas_shape = tk.Canvas(
        frame_input,
        height=300, width=600,
        borderwidth=0, relief=FLAT, bg="white"
    )
    canvas_shape.pack(side=TOP, expand=NO, fill=BOTH)
    canvas_shape.bind("<ButtonPress-1>", add_to_shape_by_click)

    # frame under the input canvas
    frame_bottom_input = tk.Frame(
        frame_input,
        borderwidth=0,
        relief=FLAT
    )
    frame_bottom_input.pack(side=TOP, expand=NO, fill=X)

    # BUTTONS
    # button that creates and displays a fractal
    btn_build_fractal = tk.Button(
        frame_building,
        text="Build fractal",
        command=fractal,
        width=15, height=2
    )
    btn_build_fractal.pack(side=LEFT, fill=X)

    # clear fractal button
    btn_clear_fractal = tk.Button(
        frame_building,
        text="Clear fractal",
        command=clear_fractal,
        width=15, height=2
    )
    btn_clear_fractal.pack(side=RIGHT, fill=X)

    # button for importing shape
    btn_import = tk.Button(
        frame_bottom_input,
        text="Import shape",
        width=10, height=2
    )
    btn_import.pack(side=LEFT)
    btn_import.bind("<ButtonPress-1>", import_shape)

    # button for exporting shapes
    btn_export = tk.Button(
        frame_bottom_input,
        text="Export shape",
        width=10, height=2
    )
    btn_export.pack(side=LEFT)
    btn_export.bind("<ButtonPress-1>", export_shape)

    # clear all button
    btn_clear = tk.Button(
        frame_bottom_input,
        text="Clear",
        command=clear,
        width=5, height=2
    )
    btn_clear.pack(side=RIGHT)

    # input box for number of iterations
    iter_txt = tk.Label(frame_building, text="Iterations:")
    iter_txt.pack(side=LEFT)

    iter_val = tk.StringVar()
    iter_val.set('5')
    iter_str = tk.Entry(frame_building, width=7, textvariable=iter_val)
    iter_str.pack(side=LEFT)

    # input box for a file that contains your shape
    shape_name_txt = tk.Label(frame_bottom_input, text="Shape name:")
    shape_name_txt.pack(side=LEFT)

    shape_name_val = tk.StringVar()
    shape_name_val.set('')
    shape_name_entry = tk.Entry(frame_bottom_input, width=12, textvariable=shape_name_val)
    shape_name_entry.pack(side=LEFT)

    root.bind("<Control-z>", undo)
    root.bind("<Control-y>", redo)
    root.bind("<Control-Alt-z>", redo)

    canvas_output.bind("<Configure>", resize)

    root.mainloop()
