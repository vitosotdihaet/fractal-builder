import tkinter as tk

from tkinter import filedialog

from tkinter_consts import *
from calculations import *

import os


DOT_RADIUS = 4
SHAPE_WIDTH = 3
FRACTAL_WIDTH = 2

fractal_dots = []
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
    global fractal_dots
    fractal_dots = []
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
        return
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
    dots_count = len(shape)

    if dots_count > 0:
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
    fractal()

def undo(event):
    if len(shape) != 0:
        temp.append(shape.pop(-1))
        canvas_shape.delete('all')
        draw_shape()
    fractal()

def redo(event):
    if len(temp) != 0:
        shape.append(temp.pop(-1))
        canvas_shape.delete('all')
        draw_shape()
    fractal()

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
        canvas_shape.create_line(*shape, width=SHAPE_WIDTH)

# calculate all the sines and coses, vector lengths, relative vector lengths
def fractal():
    clear_fractal()

    dots_count = len(shape)
    if dots_count < 3: return

    xf, yf = shape[0]
    xl, yl = shape[-1]

    vecm = x, y = (xl - xf, yl - yf)

    vec_length = [calc_vector_length(vecm)]
    length_ratio_to_main = [1.]

    norm_main_vec_y = y/vec_length[0]

    coses = [1.]
    sines = [0.]

    for i in range(1, dots_count - 1):
        xn, yn = shape[i]
        vecn = (xn - xf, yn - yf)

        vec_length.append(calc_vector_length(vecn))
        length_ratio_to_main.append(vec_length[i] / vec_length[0])

        norm_i_vec_y = vecn[1]/vec_length[i]

        coses.append(calc_cos(vecn, vecm, vec_length[i], vec_length[0]))
        sines.append(calc_sin(norm_i_vec_y - norm_main_vec_y, coses[i]))

    build_fractal(
        dots_count,
        xf, yf,
        xl, yl,
        sines, coses,
        length_ratio_to_main,
        int(iter_val.get()) - 1
    )
    scale_fractal()
    blit()

# creates a list of coordinates that form a fractal (fractal_dots)
def build_fractal(dots_count, xn, yn, xe, ye, sines, coses, length_ratio_to_main, iteration):
    global fractal_dots
    x, y = (xe - xn, ye - yn)

    # first dot
    coords = [(xn, yn)]
    for i in range(1, dots_count - 1):
        # calculating next step vector
        xr = (x * coses[i] - y * sines[i]) * length_ratio_to_main[i]
        yr = (x * sines[i] + y * coses[i]) * length_ratio_to_main[i]
        coords.append((xr + xn, yr + yn))

    # last dot
    coords.append((xe, ye))

    if iteration == 0:
        fractal_dots.extend(coords)
        return

    for i in range(1, dots_count):
        build_fractal(
            dots_count,
            coords[i-1][0], coords[i-1][1],
            coords[i][0], coords[i][1],
            sines, coses,
            length_ratio_to_main,
            iteration - 1
        )

def scale_fractal():
    global fractal_dots

    minx, miny = maxx, maxy = fractal_dots[0]

    for i in range(len(fractal_dots)):
        xc, yc = fractal_dots[i]
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

    for i in range(len(fractal_dots)):
        fractal_dots[i] = ((fractal_dots[i][0] - minx) * fac + 10,
                           (fractal_dots[i][1] - miny) * fac + 10)


def blit():
    canvas_output.delete('all')

    if fractal_dots != []:
        scale_fractal()
        canvas_output.create_line(*fractal_dots, width=FRACTAL_WIDTH)


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

    # bind hotkeys
    root.bind("<Control-z>", undo)
    root.bind("<Control-y>", redo)
    root.bind("<Control-Alt-z>", redo)

    canvas_output.bind("<Configure>", resize)

    root.mainloop()
