# Fractal builder on python

You can create complicated fractals from simple shapes with python and tkinter! All you need to do is draw a shape in the right canvas with LMB, 
change the amount of iterations (recommended is 50 divided by the number of dots in your shape, though you can change it around and see what happens) 
and press button `Build fractal`!

# UI of the application
<img src=https://github.com/vitosotdihaet/fractal-builder/assets/67521698/8e0d86cc-d393-4df0-9191-18151a72f3af width=1000/>

# Controls
`Shift` - press it while drawing shape to create horizontal or vertical lines

`Ctrl + Z` - undo

`Ctrl + Y`, `Ctrl + Alt + Z` - redo


# Buttons
`Build fractal` - builds fractal from drawn shape

`Clear fractal` - clears the fractal canvas

`Import shape` - downloads the shape from .txt file, where every line contains x and y of a shape divided with a whitespace

`Export shape` - saves the shape to filename.txt file where filename is the text you write before (!) pushing the button 

`Clear` - clears both canvases

# Requirements
Python 3.x with Tkinter

# How to install
## Windows
Python can be installed in Microsoft store or here -> https://www.python.org/downloads/ (Choose any Python 3 version)

To start a programm, double click `main.py` in file explorer or run the following command in a terminal:
```cmd
py main.py
```

## Unix
Python almost certainly is pre-installed, otherwise install it with your favorite package manager

To start the programm simply run the following command in a terminal:
```bash
$ python3 main.py
```

Enjoy!
