import pygame 
import tkinter as tkr 
from tkinter.filedialog import askdirectory 
import os ,eyed3 , datetime , io
from tkinter import *
from tkinter.tix import *
from PIL import Image,ImageTk,ImageDraw,ImageFilter
from itertools import count, cycle
from mutagen import File
from mutagen.id3 import ID3

music_player = Tk() 
music_player.title("Mp3 Player") 
music_player.geometry("450x600")
window_color = '#eeeeee'
music_player.configure(bg=window_color)
widgetcolor = window_color
global status
global prev
global n
global directory
n = 0

def rounded_img(ims) : # Round corner of song thumbnail
    blur_radius = 0
    offset = 4
    back_color = Image.new(ims.mode, ims.size, color=widgetcolor)
    offset = blur_radius * 2 + offset
    mask = Image.new("L", ims.size, 0)
    draw = ImageDraw.Draw(mask)
    #draw.ellipse((offset-10, offset+10, ims.size[0] - offset, ims.size[1] - offset), fill=255)
    draw.rounded_rectangle(((offset,offset), (ims.size[0]-offset, ims.size[1]-offset)), 20, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    img_round = Image.composite(ims, back_color, mask)
    return img_round

def get_detail(selected_entry) : # Get song artist,title,duration
    global song_detail,duration
    
    audiofile = eyed3.load(selected_entry)

    try:
        duration = str(datetime.timedelta(seconds=int(audiofile.info.time_secs)))
    except Exception:
        duration = '00:00:00'
    ####################################
    try :
        Stitle = audiofile.tag.title
        Sartist = audiofile.tag.artist
            
    except Exception:
        song_detail = selected_entry.replace('.mp3','')
    else :
        if Stitle == None or Sartist == None :
            song_detail = selected_entry
        else :
            song_detail = Sartist+' - '+Stitle

def get_thumb(activemp3) : # Get song thumbnail if exists
    global newimg,directory

    try:
        song_loc = directory+'/'+activemp3
        mp3file =  ID3(song_loc)
        artwork = mp3file.get("APIC:").data
        img = Image.open(io.BytesIO(artwork))
        img = img.resize((256,256), resample=0) 
    except Exception :
        newimg = None
    else:
        newimg = rounded_img(img)
        newimg = ImageTk.PhotoImage(newimg)

        return newimg

currdir = os.path.abspath(os.path.curdir)

img0 = Image.open(currdir+"\\files\\oie_trans.gif")
img0 = img0.resize((256,256), Image.ANTIALIAS)
coverart = ImageTk.PhotoImage(img0)

img1 = Image.open(currdir+"\\files\\button_black_play.png")
img1 = img1.resize((66,66), Image.ANTIALIAS)
play_icon = ImageTk.PhotoImage(img1)

img2 = Image.open(currdir+"\\files\\button_black_stop.png")
img2 = img2.resize((50,50), Image.ANTIALIAS)
stop_icon = ImageTk.PhotoImage(img2)

img3 = Image.open(currdir+"\\files\\button_black_pause.png")
img3 = img3.resize((66,66), Image.ANTIALIAS)
pause_icon = ImageTk.PhotoImage(img3)

img4 = Image.open(currdir+"\\files\\button_black_previous.png")
img4 = img4.resize((50,50), Image.ANTIALIAS)
prev_icon = ImageTk.PhotoImage(img4)

img5 = Image.open(currdir+"\\files\\button_black_next.png")
img5 = img5.resize((50,50), Image.ANTIALIAS)
next_icon = ImageTk.PhotoImage(img5)

img6 = Image.open(currdir+"\\files\\button_black_load.png")
img6 = img6.resize((50,50), Image.ANTIALIAS)
load_icon = ImageTk.PhotoImage(img6)

status = 'DEFAULT'


Frame0 = tkr.Frame(music_player, width=600, height=600, bg=widgetcolor)
Frame0.grid(row=1,sticky='nesw',padx=88,pady=6)
Frame11 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame11.grid(row=2,sticky='nesw',padx=80,pady=3)
Frame1 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame1.grid(row=3,sticky='nesw',padx=5,pady=3)
#Frame1.grid_columnconfigure(0, weight=1)
Frame2 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame2.grid(row=4,sticky='nesw',pady=3,padx=60)
#Frame2.grid_columnconfigure(0, weight=1)
Frame3 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame3.grid(row=5,sticky='nesw',pady=3,padx=3)
#Frame3.grid_columnconfigure(0, weight=1)

song_list = []
directory =  os.popen('echo %userprofile%').read().replace('\n','')+'\\Downloads'
os.chdir(directory)         # changing directory to downloads
for files in os.listdir() :
    if files[-3:] == 'mp3' :
        song_list.append(files) 

def dbl_click(event) :
    global song_detail,duration,status

    stop()
    Button1['image'] = pause_icon
    #####

    activemp3 = play_list.get(tkr.ACTIVE)
    pygame.mixer.music.load(activemp3)
    get_detail(activemp3)
    newimg = get_thumb(activemp3)
    var.set(song_detail)
    var1.set(duration)
    marquee_set(song_detail)
    lbl.unload()
    if newimg is None :
        lbl.load(currdir+'\\files\\mp3animtion256.gif')
    else :
        lbl['image'] = newimg
    pygame.mixer.music.play()
    status='PLAYED'

# Playlist ListBox
play_list = tkr.Listbox(Frame3,width='49',height='9', font="Helvetica 12 bold", bg="#1581bf",fg="white",selectbackground='#11469c',selectforeground='#000000',activestyle='none',selectmode=tkr.SINGLE)
play_list.grid(row=4)
play_list.bind('<Double-1>',dbl_click)
prev = play_list.get(tkr.ACTIVE)
for item in song_list:
    pos = 0
    play_list.insert(pos, item)
    pos += 1

# Select first item in ListBox
play_list.selection_clear(0,END)
play_list.selection_set(first=0)
play_list.see(0)
play_list.activate(0)

def load_folder() : # Select folder to load all songs (.mp3)
    play_list.delete(0, END)
    song_list = []
    directory =  askdirectory()
    os.chdir(directory) 
    for files in os.listdir() :
        if files[-3:] == 'mp3' :
            song_list.append(files) 
    
    for item in song_list:
        pos = 0
        play_list.insert(pos, item)
        pos += 1


#pygame.init()
pygame.mixer.init()
song_end = False

def play_next_auto(): # autoplay next song
    global song_end,status
    if pygame.mixer.music.get_busy():
        song_end = False
    else :
        song_end = True
        if status=='PLAYED' or status=='UNPAUSED' :
            stop()
            Next()

    music_player.after(1000, play_next_auto)

def marquee_set(song_name) :
    canvas.itemconfigure("marquee", text=song_name)
    # Change marquee label text

def shift(): # animate label marquee
    global canvas,fps

    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): 
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

def play():  # Play/Pause/Unpause song

    play_next_auto()

    global status , curr , prev , n , newimg
    n += 1
    activemp3 = play_list.get(tkr.ACTIVE)
    curr = activemp3
    print(prev,'<####>',curr)
    print('Count : ',n)
    get_thumb(activemp3)
    get_detail(activemp3)
    
    if n == 1 :  # Play if clicked on start
        Button1['image'] = pause_icon
        #####
        activemp3 = play_list.get(tkr.ACTIVE)
        pygame.mixer.music.load(activemp3)
        var.set(song_detail)
        var1.set(duration)
        marquee_set(song_detail)
        lbl.unload()
        if newimg is None :
            lbl.load(currdir+'\\files\\mp3animtion256.gif')
        else :
            lbl['image'] = newimg
        pygame.mixer.music.play()
        status = 'PLAYED'

    elif status == 'PLAYED' or status == 'UNPAUSED' : # Pause if last action is played or unpaused
        Button1['image'] = play_icon 
        #####
        pygame.mixer.music.pause() 
        lbl.unload() 
        if newimg is None :
            lbl.load(currdir+'\\files\\mp3fixed256.gif')
        else :
            lbl['image'] = newimg
        status = 'PAUSED'

    elif status == 'PAUSED' and curr==prev : # Unpause if last action is paused
        Button1['image'] = pause_icon
        #####
        pygame.mixer.music.unpause()
        lbl.unload()
        if newimg is None :
            lbl.load(currdir+'\\files\\mp3animtion256.gif')
        else :
            lbl['image'] = newimg
        status = 'UNPAUSED' 

    elif status == "STOPPED" or curr!=prev : # Play if last action is stopped or selected track changed
        Button1['image'] = pause_icon
        #####
        activemp3 = play_list.get(tkr.ACTIVE)
        pygame.mixer.music.load(activemp3)
        var.set(song_detail)
        var1.set(duration)
        marquee_set(song_detail)
        lbl.unload()
        if newimg is None :
            lbl.load(currdir+'\\files\\mp3animtion256.gif')
        else :
            lbl['image'] = newimg
        pygame.mixer.music.play()
        status='PLAYED'

    prev = curr
    print(status)
    

def stop(): # Stop song
    lbl.load(currdir+'\\files\\mp3fixed256.gif') 
    Button1['image'] = play_icon
    #####
    global status
    pygame.mixer.music.stop()
    status = 'STOPPED'
    print(status)

def Next() : # Play next song
    play_next_auto()

    global status,newimg
    pygame.mixer.music.stop()

    next_mp3 = ''
    for index in play_list.curselection() :
        next_mp3 = play_list.get(index+1)
        if str(next_mp3).replace(' ','') == '' :
            next_mp3 = play_list.get(0)
            play_list.selection_clear(first=index)
            play_list.selection_set(first=0)
            play_list.see(0)
            play_list.activate(0)
        else :
            play_list.selection_clear(first=index)
            play_list.selection_set(first=index+1)
            play_list.see(index+1)
            play_list.activate(index+1)

    get_detail(play_list.get(tkr.ACTIVE))
    
    
    Button1['image'] = pause_icon
    #####
    var.set(song_detail)
    var1.set(duration)
    marquee_set(song_detail)

    newimg = get_thumb(play_list.get(tkr.ACTIVE))

    lbl.unload()
    if newimg is None :
        lbl.load(currdir+'\\files\\mp3animtion256.gif')
    else :
        lbl['image'] = newimg

    status = 'PLAYED'
    print('Next & Play')

    pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
    pygame.mixer.music.play()
    
def Prev() : # Play previous song
    play_next_auto()
    
    global status,newimg
    pygame.mixer.music.stop()

    prev_mp3 = ''
    list_size = play_list.size()

    for index in play_list.curselection() :
        prev_mp3 = play_list.get(index-1)
        if str(prev_mp3).replace(' ','') == '' :
            prev_mp3 = play_list.get(list_size-1)
            play_list.selection_clear(first=index)
            play_list.selection_set(first=list_size-1)
            play_list.see(list_size-1)
            play_list.activate(list_size-1)
        else :
            play_list.selection_clear(first=index)
            play_list.selection_set(first=index-1)
            play_list.see(index-1)
            play_list.activate(index-1) 
    
    get_detail(play_list.get(tkr.ACTIVE))
    
    Button1['image'] = pause_icon
    #####
    var.set(song_detail)
    var1.set(duration)
    marquee_set(song_detail)

    newimg = get_thumb(play_list.get(tkr.ACTIVE))

    lbl.unload()
    if newimg is None :
        lbl.load(currdir+'\\files\\mp3animtion256.gif') 
    else :
        lbl['image'] = newimg

    status = 'PLAYED'
    print('Prev & Play')

    pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
    pygame.mixer.music.play()

class ImageLabel(tkr.Button): # Playing Gif animation
    
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
    

lbl = ImageLabel(Frame0,width=256,height=256,highlightthickness=0,relief=FLAT,bd=0,bg=widgetcolor)
lbl.grid(row=1,padx=10)
lbl.load(currdir+'\\files\\mp3fixed256.gif') 


#Button0 = tkr.Button(Frame0, text="",image=coverart,highlightthickness=0,relief=FLAT,bd=0)
#Button0.grid(row=1,padx=5)
var1 = tkr.StringVar() 
Label1 = tkr.Label(Frame11, font=("Helvetica 12 bold"),textvariable=var1,bg=widgetcolor)
Label1.grid(row=1,padx=110)
Button1 = tkr.Button(Frame2, text="",image=play_icon, bg=widgetcolor,borderwidth=0)
Button1['command'] = play
Button1.grid(row=2,column=3,padx=5)
Button2 = tkr.Button(Frame2, text="",image=stop_icon, command=stop, bg=widgetcolor,borderwidth=0)
Button2.grid(row=2,column=5,padx=5)
Button3 = tkr.Button(Frame2, text="",image=prev_icon, command=Prev, bg=widgetcolor,borderwidth=0)
Button3.grid(row=2,column=2,padx=12)
Button4 = tkr.Button(Frame2, text="",image=next_icon, command=Next, bg=widgetcolor,borderwidth=0)
Button4.grid(row=2,column=4,padx=5)
Button5 = tkr.Button(Frame2, text="",image=load_icon, command=load_folder, bg=widgetcolor,borderwidth=0)
Button5.grid(row=2,column=1,padx=5)

tooltip1 = Balloon(music_player)
tooltip1.bind_widget(Button1,balloonmsg="Play/Pause")
tooltip2 = Balloon(music_player)
tooltip2.bind_widget(Button4,balloonmsg="Next")
tooltip3 = Balloon(music_player)
tooltip3.bind_widget(Button3,balloonmsg="Previous")
tooltip4 = Balloon(music_player)
tooltip4.bind_widget(Button5,balloonmsg="load songs")
tooltip5 = Balloon(music_player)
tooltip5.bind_widget(Button2,balloonmsg="stop")

var = tkr.StringVar() 
#song_title = tkr.Label(Frame1,width=44, font="Helvetica 12 bold", textvariable=var)
#song_title.grid(row=1,column=1)

canvas=Canvas(Frame1,bg=widgetcolor,highlightthickness=0)
canvas.grid(row=1)
text_var= ''
text=canvas.create_text(0,-2000,text=text_var,font=('consolas',20,'bold'),fill='#110a6e',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = x2-x1
height = y2-y1
canvas['width']='440'
canvas['height']=height
fps=40  
shift()

marquee_set('Python Music Player')
var1.set('00:00:00')

music_player.mainloop()
