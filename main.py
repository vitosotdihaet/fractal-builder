import tkinter as tk
from tkinter import filedialog
from tkinter.constants import *
from math import sin, cos, atan, sqrt
import os

DOT_RADIUS = 4
frac_dts = []

# resizes the window
def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height
    canvas_output['width'] = min(event.width, event.height) - 300
    canvas_output['height'] = canvas_output['width']

    blit()

# clears both canvases
def clear():
    global shape, frac_dts
    shape = []
    canvas_shape.delete('all')
    clear_fractal()

# clears fractal canvas
def clear_fractal():
    global frac_dts
    frac_dts = []
    canvas_output.delete('all')

# opens a .txt file with shape coordinates [(x, y), (x1, y1)...]
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
        f = open('err.txt')

    clear()
    for line in f:
        shape.append(tuple(map(int, line.split())))

    f.close()

    draw_shape()

# adds dot's coordinates to shape
def add_to_shape_by_click(event):
    global shape
    shape.append((event.x, event.y))
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

    if len(shape) > 1:
        canvas_shape.create_line(*shape)
    canvas_shape.create_oval(x1, y1, x2, y2, fill="black")

    # print('---SHAPE---')
    # print(shape)

# creates a list of coordinates that form a fractal (frac_dts)
def build_fractal(xn, yn, xe, ye, depth):
    global frac_dts
    dotsc = len(shape)

    if dotsc < 3: return

    # print('iter number', depth)

    # first dot
    # print('1 dot -', xn, yn)
    coords = [(round(xn, 4), round(yn, 4))]

    for i in range(1, dotsc - 1):
        # calculating next step vector
        x = xe - xn
        y = ye - yn
        xr = (x * cF[i] + y * sF[i]) * veclengthcomp[i]
        yr = (-x * sF[i] + y * cF[i]) * veclengthcomp[i]
        # print(i + 1, 'dot -', xr + xn, yr + yn)
        coords.append((round(xr + xn, 4), round(yr + yn, 4)))

    # last dot
    # print(dotsc, 'dot -', xe, ye)
    coords.append((round(xe, 4), round(ye, 4)))

    if depth == 0:
        for i in range(dotsc):
            frac_dts.append(coords[i])
        return

    for i in range(1, dotsc):
        build_fractal(coords[i-1][0], coords[i-1][1], coords[i][0], coords[i][1], depth - 1)

def change_frac():
    global frac_dts

    minx, miny = frac_dts[0]
    maxx, maxy = frac_dts[0]

    for i in range(len(frac_dts)):
        if minx > frac_dts[i][0]:
            minx = frac_dts[i][0]
        elif maxx < frac_dts[i][0]:
            maxx = frac_dts[i][0]

        if miny > frac_dts[i][1]:
            miny = frac_dts[i][1]
        elif maxy < frac_dts[i][1]:
            maxy = frac_dts[i][1]

    facX = int(canvas_output['width']) / (maxx - minx)
    facY = int(canvas_output['height']) / (maxy - miny)
    fac = min(facX, facY)

    for i in range(len(frac_dts)):
        frac_dts[i] = ((frac_dts[i][0] - minx) * fac + 10, (frac_dts[i][1] - miny) * fac + 10)

    # print('resized fractal:')
    # for e in frac_dts:
    #     print('(' + str(round(e[0])), str(round(e[1])) + ')', end=' ')
    # print()

def fractal():
    global cF, sF, veclength, veclengthcomp
    dotsc = len(shape)

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
        if (vecn[0] - vecf[0]) * (-vecf[1]) / (-vecf[0]) + vecf[1] > vecn[1]:
            sF[i] = round(sqrt(1 - cF[i]**2), 8)
        else:
            sF[i] = -round(sqrt(1 - cF[i]**2), 8)

        veclengthcomp[i] = round(veclength[i] / veclength[0], 4)

    # print('SINUS AND COSINUS:')
    # print(sF)
    # print(cF)
    # print(veclengthcomp)

    build_fractal(
            100,
            int(canvas_output['height']) // 2,
            int(canvas_output['width']) - 100,
            int(canvas_output['height']) // 2,
            int(depth_val.get()) - 1
    )
    change_frac()
    blit()

def blit():
    canvas_output.delete('all')

    if frac_dts != []:
        change_frac()
        canvas_output.create_line(*frac_dts)


if __name__ == "__main__":
    # root stuff
    root = tk.Tk()
    root.title("Fractal Builder by Vitaly Klimenko")
    root.minsize(1000, 500)
    root.resizable(width=True, height=True)

    # FRAMES
    # main frame
    frame_main = tk.Frame(
        root,
        borderwidth=0, relief=FLAT)
    frame_main.pack(fill=BOTH, expand=YES)

    # frame with all the inputs
    frame_input = tk.Frame(
        frame_main,
        width=400,
        borderwidth=0, relief=RAISED, bg="grey40"
    )
    frame_input.pack(fill=Y, side=RIGHT, expand=NO)

    # top line
    frame_top_input = tk.Frame(frame_input, borderwidth=0, relief=FLAT)
    frame_top_input.pack(side=TOP, expand=NO)

    # CANVASES
    # canvas that displays fractal
    canvas_output = tk.Canvas(
        frame_main,
        borderwidth=0, relief=FLAT,
        highlightthickness=0
    )
    canvas_output.pack(fill=BOTH, side=LEFT, expand=YES)

    # canvas that contains drawn shape
    canvas_shape = tk.Canvas(
        frame_input,
        height=300,
        borderwidth=0, relief=FLAT, bg="grey"
    )
    canvas_shape.pack(fill=BOTH, side=TOP, expand=NO)
    canvas_shape.bind("<ButtonPress-1>", add_to_shape_by_click)

    # BUTTONS
    # button for importing shape
    btn_import = tk.Button(
        frame_top_input,
        text="Import shape",
        padx=30, pady=15
    )
    btn_import.pack(side=LEFT)
    btn_import.bind("<ButtonPress-1>", import_shape)

    # clear all button
    btn_clear = tk.Button(
        frame_top_input,
        text="Clear",
        command=clear,
        padx=30, pady=15
    )
    btn_clear.pack(side=RIGHT)

    # button that creates and displays a fractal
    btn_build = tk.Button(
        frame_input,
        text="Build fractal",
        command=fractal,
        width=20, height=2
    )
    btn_build.pack(side=TOP)

    # clear fractal button
    btn_clear_fractal = tk.Button(
        frame_input,
        text="Clear fractal",
        command=clear_fractal,
        width=20, height=2
    )
    btn_clear_fractal.pack(side=TOP)

    # input box for number of iterations
    depth_txt = tk.Label(frame_top_input, text="Iterations:")
    depth_txt.pack(side=LEFT)

    depth_val = tk.StringVar()
    depth_str = tk.Entry(frame_top_input, width=7, textvariable=depth_val)
    depth_str.pack(side=LEFT)

    canvas_output.bind("<Configure>", resize)

    shape = []
    depth_val.set("5")

    root.mainloop()