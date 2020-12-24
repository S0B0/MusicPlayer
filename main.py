from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Mp3 Player')
#root.iconbitmap('D:/Coding Tmp/GUI')
root.geometry("500x400")

#Initializing the pygame mixer
pygame.mixer.init()

#Add Song function
def add_song():
    song = filedialog.askopenfilename(initialdir='D:/Coding Tmp/audio',title = "Choose song",filetypes=(("mp3 Files","*.mp3"), ))

    # Hide the directory info and extension from name
    song = song.replace("D:/Coding Tmp/audio/", "")
    song = song.replace(".mp3", "")

    # Add song to list
    song_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='D:/Coding Tmp/audio',title = "Choose song",filetypes=(("mp3 Files","*.mp3"), ))

    #Loop song list and replace dir info and mp3
    for song in songs:

       song = song.replace("D:/Coding Tmp/audio/", "")
       song = song.replace(".mp3", "")
       song_box.insert(END, song)

def play():

    global stopped
    stopped = False

    song =song_box.get(ACTIVE)
    song=f'D:/Coding Tmp/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_time()

    # update slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position,value=0)

global stopped
stopped = False

def stop():

 #reset slider and status bar
 status_bar.config(text='')
 my_slider.config(value='0')

 #stop song from playing
 pygame.mixer.music.stop()
 song_box.selection_clear(ACTIVE)

 #Clear time bar at stop
 status_bar.config(text='')

 #Set stop variable to true
 global stopped
 stopped = True


 #Global pause variable and the pause function
global paused
paused = False

def next_song():

    status_bar.config(text='')
    my_slider.config(value='0')

    next = song_box.curselection()
    next = next[0]+1
    song = song_box.get(next)
    song = f'D:/Coding Tmp/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar
    song_box.selection_clear(0,END)

    #Activate next bar
    song_box.activate(next)

    #Draw the next bar bar
    song_box.selection_set(next,last=None)

def previous_song():

    status_bar.config(text='')
    my_slider.config(value='0')

    next = song_box.curselection()
    next = next[0] - 1
    song = song_box.get(next)
    song = f'D:/Coding Tmp/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar
    song_box.selection_clear(0, END)

    # Activate next bar
    song_box.activate(next)

    # Draw the next bar bar
    song_box.selection_set(next, last=None)

def pause(is_paused):

    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def delete_song():

    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():

    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()

def song_time():

    #Check for double timing
    if stopped:
        return
    #Current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000


   # slider_label.config(text=f'Slider:{int(my_slider.get())} and Song Pos: {int(current_time)}')


  #Get the current song
    #current_song = song_box.curselection()

  #get song title from playlist
    song = song_box.get(ACTIVE)
    song = f'D:/Coding Tmp/audio/{song}.mp3'

  #Load song using mutagen
    song_mutagen = MP3(song)

  #Get song length
    global  song_length
    song_length = song_mutagen.info.length

  #Convert to time format
    converted_song_length = time.strftime('%H:%M:%S',time.gmtime(song_length))
    #status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')


    current_time += 1
    if int(my_slider.get())== int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}  ')

    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
         #sldier hasn't been moved
         slider_position = int(song_length)
         my_slider.config(to=slider_position, value=int(current_time))
    else:
         #slider has been moved
         slider_position = int(song_length)
         my_slider.config(to=slider_position, value=int(my_slider.get()))
         # Convert to the time format
         converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))
         status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
         next_time=int(my_slider.get())+1
         my_slider.config(value=next_time)



#update slider value to current song pos

    #my_slider.config(value=int(current_time))



    status_bar.after(1000,song_time)

def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'D:/Coding Tmp/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))


#Creating the Playlist Dark Box
song_box =  Listbox(root,bg="black",fg="green",width=60,selectbackground="green",selectforeground="black")
song_box.pack(pady=20)

#Define music player buttons (images)

back_btn_img = PhotoImage(file='D:/Coding Tmp/GUI/back.png')
forward_btn_img =PhotoImage(file='D:/Coding Tmp/GUI/forward.png')
play_btn_img = PhotoImage(file='D:/Coding Tmp/GUI/play.png')
pause_btn_img  =PhotoImage(file='D:/Coding Tmp/GUI/pause.png')
stop_btn_img =PhotoImage(file='D:/Coding Tmp/GUI/stop.png')

# Create music player Buttons Frame

buttons_frame = Frame(root)
buttons_frame.pack()

# Create music player control buttons
back_btn = Button(buttons_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_btn = Button(buttons_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_btn = Button(buttons_frame,image=play_btn_img,borderwidth=0,command=play)
pause_btn = Button(buttons_frame,image=pause_btn_img,borderwidth=0,command=lambda : pause(paused))
stop_btn = Button(buttons_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_btn.grid(row=0,column=0,padx=10)
forward_btn.grid(row=0,column=1,padx=10)
play_btn.grid(row=0,column=2,padx=10)
pause_btn.grid(row=0,column=3,padx=10)
stop_btn.grid(row=0,column=4,padx=10)

#Menu

my_menu = Menu(root)
root.config(menu=my_menu)

# Song Insert Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add song to playlist",command=add_song)

#Add multiple songs
add_song_menu.add_command(label="Add multiple songs to playlist",command=add_many_songs)

#Create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(labe="Remove Songs",menu = remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist",command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist",command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#Create slider
my_slider = ttk.Scale(root,from_=0,to=100,orient = HORIZONTAL,value=0,command=slide,length=360)
my_slider.pack(pady=20)

#Slider label
#slider_label = Label(root,text="0")
#slider_label.pack(pady=10)
#root.configure(background='grey')
#slider_label.configure(background='grey')
root.mainloop()