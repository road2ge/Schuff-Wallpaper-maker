##################################################
##################################################
###Patrick Spychalski and Kale Miller made this###
##################################################
###It makes something very special just for you###
##################################################
##################################################

'''Todo:
~~~~Add more Memes (Schuffs)~~~~
Add save functionality
Improve accuracy/ability to use arrow keys to move sliders
redo button
Auto-detection of resolution
Name to window
Insert tool name "Schuff Wallpaper Generator"
Clean-up of interface, general improvements to ux
Ezpz basic tutorial of how to meme
Better commenting of code, more readability
More efficient/intuitive/better arranged functions and sliders
Cleanup of images after done/Improvement to images in general'''

from Tkinter import *
from functools import partial
import PIL
# Please note, the below try/except code was written because I had not correctly set up things on my Ubuntu machine.
# I kept it here because I thought it was funny
try:
    from PIL import ImageTk
    print('ImageTK imported (¬_¬)')
except:
    print('Importing ImageTK from PIL has failed. Attempting to import ImageTK (╯°□°）╯︵ ┻━┻')
    try:
        import ImageTK
    except:
        print('Attempting to import PIL (;´༎ຶД༎ຶ`)')
        try:
            import PIL
        except:
            print('Import failed (ノಠ益ಠ)ノ彡┻━┻')
        print('Importing PIL seems to have worked [̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]')

import os.path

root = Tk()

canvas = Canvas(root, height=1000, width=6000, bg='white')
canvas.grid(column=1, row=0, rowspan=4, sticky=W)
canvas.imglist=[]

m1 = '<ButtonPress-1>'

def stamp_schuff(m1):
    '''This function is called when you click on the canvas. It puts
    a Schuff head where you click.'''
    # Open the original img, retrieve the dimensions, resize and rotate it depending
    # on where the sliders are.
    iterated_img = PIL.Image.open('Schuff' + head + 'v2.png')
    width, height = iterated_img.size 
    iterated_img = iterated_img.resize((int(width*resize_percent.get()/100),
                                       (int(height*resize_percent.get())/100)))
    degrees = rotate_degrees.get() * len(canvas.imglist)
    iterated_img = iterated_img.rotate(degrees, expand=True)    
    
    # Converts iterated_img to an RGBA image, crops it to its bbox (why Patrick??)
    iterated_img = iterated_img.convert('RGBA')
    bounds = iterated_img.getbbox()
    iterated_img = iterated_img.crop(bounds)
    
    # Puts the iterated_img onto the canvas
    tkimg = PIL.ImageTk.PhotoImage(iterated_img)
    canvas.imglist += [tkimg]
    canvas.create_image(m1.x, m1.y, image=tkimg)
    
    # The program can get laggy if there are too many images on the canvas.
    # A delay makes it so that you can add 25 schuffs per second.
    # You'd have to click pretty fast for this, but I find it reasonable.
    canvas.after(40)    

'''def call_stamp(head):
    Made because partial cannot call functions with more
    than one argument...
    return stamp_schuff(m1, head)
stamp_schuff1 = partial(call_stamp,m1,'1')
stamp_schuff2 = partial(call_stamp,m1,'2')
stamp_schuff3 = partial(call_stamp,m1,'3')
stamp_schuff4 = partial(call_stamp,m1,'4')
stamp_schuff5 = partial(call_stamp,m1,'5')
stamp_schuff6 = partial(call_stamp,m1,'6')'''

def schuff(argument_head):
    # Retrieve directory and filename.
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(__dir__, 'Schuff'
                            + argument_head + 'new.png')
    img = PIL.Image.open(filename)
    img = img.convert("RGBA")
    
    # Makes the white pixels of the image transparent, and saves that
    # modified image for later. Useful for stacking heads. 
    datas = img.getdata()
    newData = []
    for item in datas:
            
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save('Schuff' + argument_head + 'v2.png', "PNG")
    
    # Binds left click to the stamp function.
    canvas.bind(m1, stamp_schuff)
    
    # The Python community frowns upon the use of globals.
    # I'm not really sure why, so I'm just gonna do this.
    # Makes the head argument global for the stamp function.
    global head
    head = argument_head

def clear_imglist():
    '''This is the callback command for the clear button later on. It
    resets every slider, clears the image list, and deletes all items
    on the canvas.'''
    canvas.delete('all')
    canvas.imglist = []
    resizeslider.set(100)
    rotateslider.set(30)

def undo_redo(undo):
    # If given True, then all the actions needed for undo are taken.
    # If given False, well, redo is a Work in Progress.
    if undo:
        try:
            global undolist
            undolist = canvas.imglist[len(canvas.imglist)-1]
            canvas.imglist = canvas.imglist[0:len(canvas.imglist)-1]
        except IndexError:
            # I used to get IndexError's before I added anything to the canvas.
            pass
    else:
        pass # This is actually really hard

resize_percent = DoubleVar()
resizeslider = Scale(canvas, variable=resize_percent, from_=200, 
                     to=2, orient=VERTICAL, label='Resize %: ')
resizeslider.set(100)
resizeslider.place(x=10,y=300)

rotate_degrees = DoubleVar()
rotateslider = Scale(canvas, variable=rotate_degrees, from_=359,
                     to=0, orient=VERTICAL, label='Rotation')
rotateslider.set(30)
rotateslider.place(x=10,y=500)

CLEARBUTTON = Button(canvas, text='Clear', 
                     command=clear_imglist)
CLEARBUTTON.place(x=10,y=10)
CLEARBUTTON.configure(activebackground="#33B5E5")

undo = partial(undo_redo, True)
redo = partial(undo_redo, False)

schuff1 = partial(schuff, '1')
schuff2 = partial(schuff, '2')
schuff3 = partial(schuff, '3')
schuff4 = partial(schuff, '4')
schuff5 = partial(schuff, '5')
schuff6 = partial(schuff, '6')

UNDOBUTTON = Button(canvas, text='Undo',
                    command=undo)
UNDOBUTTON.place(x=80,y=10)

#REDOBUTTON = Button(canvas, text='Redo',
#                    command=redo)
#REDOBUTTON.place(x=150,y=10)

schuff('2')
schuff('3')
schuff('4')
schuff('5')
schuff('6')
schuff('1')

# Initializes Schuff pictures

# SCHUFF1 = PIL.Image.open('Schuff1v2.png')
# SCHUFF1 = PIL.ImageTk.PhotoImage(SCHUFF1) not sure why I put these here

SCHUFF1BUTTON = Button(canvas,
                       text='1st Schuff', command = schuff1)
SCHUFF1BUTTON.place(x=10, y=50)
SCHUFF2BUTTON = Button(canvas,
                       text='2nd Schuff', command = schuff2)
SCHUFF2BUTTON.place(x=10, y=79)
SCHUFF3BUTTON = Button(canvas,
                       text='3rd Schuff', command = schuff3)
SCHUFF3BUTTON.place(x=10, y=109)
SCHUFF4BUTTON = Button(canvas,
                       text='4th Schuff', command = schuff4)
SCHUFF4BUTTON.place(x=10, y=139)
SCHUFF5BUTTON = Button(canvas,
                       text='5th Schuff', command = schuff5)
SCHUFF5BUTTON.place(x=10, y=169)
SCHUFF6BUTTON = Button(canvas,
                       text='6th Schuff', command = schuff6)
SCHUFF6BUTTON.place(x=10, y=199)

#canvas.create_text((640, 35),
#                    text='Schuff Wallpaper Generator', font=('Arial', -69))
# I decided I didn't want this

root.mainloop()
print('I hope you enjoyed our project (ó ì_í)=óò=(ì_í ò)')