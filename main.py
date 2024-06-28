from PIL import Image
import tkinter
from tkinter import filedialog
import os


root = tkinter.Tk()
root.iconbitmap(r'icon.ico')
root.resizable(width=False,height=False)
CountSprite = 0
Sprits_row = None

def Slice(image):
    with Image.open(image,'r') as img:
        xy = img.size
        endX = 0
        isSprite = 0
        spritesSize = []
        sprites = []
        for x in range(xy[0]):
            for y in range(xy[1]):
                if img.getpixel([x,y])[3] > 0:
                    if not isSprite:
                        isSprite = 1
                        startX = x
                    break
            else:
                if isSprite:
                    isSprite = 0
                    endX = x
                    spritesSize.append((startX,endX))

        for sprite in spritesSize:
            raw = img.crop((sprite[0], 0, sprite[1], xy[1]))
            sprites.append(raw)
        return(sprites)

def Glue(sprites):
    lenX = len(sprites)-1
    lenY = sprites[0].size[1]
    for sprite in sprites:
        lenX += sprite.size[0]
    back = Image.new('RGBA',(lenX,lenY),0)
    nowX = 0
    for sprite in sprites:
        back.paste(sprite, (nowX, 0))
        nowX += sprite.size[0]+1
    return back

def Open_file():
    filepath = filedialog.askopenfilename(filetypes=(("image files","*.png"),("all","*.*")))
    if filepath !='':
        global Sprits_row
        Sprits_row = Slice(filepath)
        count_sprites.config(text="Количество спрайтов: " + str(len(Sprits_row)))
        button2.config(state=tkinter.ACTIVE)

def Save_file():
    global Sprits_row
    if Sprits_row is not None:
        filepath = filedialog.asksaveasfilename(filetypes=(("image files","*.png"),("all","*.*")))
        if filepath !='':
            result = Glue(Sprits_row)
            result.save(filepath+'.png')


root.title("Slicer")
root.geometry("300x400")
button1 = tkinter.Button(root, text='Выбрать файл', command=Open_file, font=40)
button1.pack(pady=40)

count_sprites = tkinter.Label(root, text="Количество спрайтов: -")
count_sprites.pack()


button2 = tkinter.Button(root, text='Резать', font=40,command=Save_file, state=tkinter.DISABLED)
button2.pack(side=tkinter.BOTTOM,pady=40)

root.mainloop()
