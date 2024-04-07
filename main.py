
# import all libraries
from tkinter import Tk, Button, Label, Entry, StringVar, Frame
import cv2
from ffpyplayer.player import MediaPlayer
from openpyxl import load_workbook
import time

CONTINUE = "SUMI"
END = "DISASTER"

def lastSeq(window):
    global key
    key = key_in_window.get()
    if key != CONTINUE and key != END:
        return
    window.destroy()

def retrieveUID(window):
    global uid, id_database
    uid = uid_in_window.get()
    if uid == "" or uid not in id_database:
        return
    window.destroy()

def keydown(e, window, tag):
    if tag == "start":
        if (e.char == " "):
            window.destroy()

    elif tag == "vid1" or tag == "vid2":
        global keystroke1, keystroke2
        if (e.char >= 'a' and e.char <= 'z') or (e.char >= 'Z' and e.char <= 'Z'):
            if tag == "vid1":
                keystroke1 = e.char
            elif tag == "vid2":
                keystroke2 = e.char
            window.destroy()

def PlayVideo(video_path):
    video = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame = video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(27) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()

def done(window):
    window.destroy()

if __name__ == '__main__':

    # declare variables
    id_database = ['user1', 'user2', 'user3']
    uid = "abcd"
    keystroke1 = "a"
    keystroke2 = "a"

    # open connection to an existing Excel file you want to store data in, find library to do this
    existing_file = '/Users/maryamimran/Desktop/sumiProject/experiment data.xlsx'

    key = CONTINUE
    while (key != END):

        # do tkinter magic to display dialogue box 1 with field for user id
        # do more tkinter magic to retrieve user id entered in dialogue box 1
        # close dialogue box 1
        db1 = Tk()
        uid_in_window = StringVar()
        db1.title('Welcome')
        Label(db1, text='UID').grid(row=0, column=0)
        e1 = Entry(db1, width=30, textvariable=uid_in_window)
        e1.grid(row=0, column=1)
        next_button = Button(db1, text='Next', command=lambda: retrieveUID(db1))
        next_button.grid(row=1, column=1)
        db1.mainloop()

        # wait for 'space' key
        inb1 = Tk()
        inb1.title("")
        text = Label(inb1, text="Welcome!\n"
                                "Please read the following instructions:\n\n"
                                "   1. You will be shown video 1 only once\n"
                                "   2. You will be prompted to type the letter key corresponding to the sound you heard in the video\n"
                                "   3. This will be followed by a waiting period lasting a few seconds\n"
                                "   4. Then you will be showed video 2 only once\n"
                                "   5. You will then be prompted to type the letter key corresponding to the sound you heard in the video\n\n"
                                "Please press the 'Spacebar' key when you are ready", padx=20, pady=20)
        text.pack()
        frame = Frame(inb1, width=100, height=20)
        frame.bind("<KeyPress>", lambda e: keydown(e, inb1, 'start'))
        frame.pack()
        frame.focus_set()
        inb1.mainloop()

        # play video 1 using tkinter or smth else, find a library for this
        # close video window
        PlayVideo(r"/Users/maryamimran/Desktop/sumiProject/video1.mp4")

        # do tkinter magic to display dialogue box 2 with prompt to enter key corresponding to sound
        # wait for keystroke
        # store keystroke in variable 1
        db2 = Tk()
        db2.title("")
        text = Label(db2, text="Please press the letter key you think the pronounced sound matched the most", padx=20, pady=20)
        text.pack()
        frame = Frame(db2, width=100, height=20)
        frame.bind("<KeyPress>", lambda e: keydown(e, db2, 'vid1'))
        frame.pack()
        frame.focus_set()
        db2.mainloop()

        # call function to wait 7 seconds (could be custom function or using some library)
        inb2 = Tk()
        inb2.title("")
        text = Label(inb2, text="Please wait...", padx=20, pady=20)
        text.pack()
        inb2.update()
        time.sleep(7)
        inb2.destroy()
        inb2.mainloop()


        # play video 2 using tkinter or smth else, find a library for this
        # close video window
        PlayVideo(r"/Users/maryamimran/Desktop/sumiProject/video2.mp4")

        # do tkinter magic to display dialogue box 3 with prompt to enter key corresponding to sound
        # wait for keystroke
        # store keystroke in variable 2
        db3 = Tk()
        db3.title("")
        text = Label(db3, text="Please press the letter key you think the pronounced sound matched the most", padx=20,
                     pady=20)
        text.pack()
        frame = Frame(db3, width=100, height=20)
        frame.bind("<KeyPress>", lambda e: keydown(e, db3, 'vid2'))
        frame.pack()
        frame.focus_set()
        db3.mainloop()

        # append user id, variable 1 & variable 2 to the opened Excel file
        new_data = [[uid, keystroke1, keystroke2]]
        wb = load_workbook(existing_file)
        ws = wb.active
        for row in new_data:
            ws.append(row)
        wb.save(existing_file)

        # do tkinter magic to display dialogue box 4 with goodbye message and done button
        db4 = Tk()
        uid_in_window = StringVar()
        db4.title('Goodbye')
        Label(db4, text='You can now leave. Thankyou for you participation!').pack()
        done_button = Button(db4, text='Done', command=lambda: done(db4))
        done_button.pack()
        db4.mainloop()

        # when ok button pressed, do tkinter magic to display dialogue box 5 with message for end or continue sequence,
        # entry field for sequence and ok button
        # when ok pressed, store sequence and validate it to ensure it's either of end or continue
        db5 = Tk()
        key_in_window = StringVar()
        db5.title('Welcome')
        Label(db5, text='Key').grid(row=0, column=0)
        e2 = Entry(db5, width=30, textvariable=key_in_window)
        e2.grid(row=0, column=1)
        ok_button = Button(db5, text='Next', command=lambda: lastSeq(db5))
        ok_button.grid(row=1, column=1)
        db5.mainloop()

    print("Hi Sumi!")

    # close Excel file connection





