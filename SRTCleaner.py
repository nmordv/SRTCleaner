# Author: Natalia Mordvanyuk
# Created on 9/12/2021
# Template of UI: TKinter example

from tkinter import *
from tkinter import filedialog
import io
from tkinter.messagebox import showinfo
from datetime import datetime
import datetime as dt
import math

class Perevod:

  def __init__(self, id, start_time, t):
    self.id = id
    self.start_time = start_time
    self.end_time = start_time
    self.t = t

  def set_end_time(self, end_time):
    if end_time == self.start_time:
      print("El temps d'inici es igual al temps final!:",self.start_time)
    self.end_time = end_time

def to_srt_format_text(t):
  nt = t
  if len(t)>0 and t != " " and t != "" and t != "\n":

    if t[-1] == "\n":
      nt = t[:-1]

      if t[-1] == "\n":
        nt = t[:-1]

    if t[0] == "\n":
      nt = t[0:]

  return nt

def check_and_correctTimes(dict_of_dialogs):
    time_error_log = ""
    for key, p in dict_of_dialogs.items():

        dt_obj_start = datetime.strptime("01/01/2021 " + p.start_time, '%d/%m/%Y %H:%M:%S,%f')
        dt_obj_end = datetime.strptime("01/01/2021 " + p.end_time, '%d/%m/%Y %H:%M:%S,%f')

        if (dt_obj_end.timestamp() - dt_obj_start.timestamp()) < 1.0:  # minimum 1 seccond
            if (key + 1) in dict_of_dialogs:
                dt_next_end_time = datetime.strptime("01/01/2021 " + dict_of_dialogs[key + 1].end_time,
                                                     '%d/%m/%Y %H:%M:%S,%f')
                secs = math.floor((dt_next_end_time.timestamp() - dt_obj_start.timestamp()) / 2)
                dt_obj_new_start = dt_obj_start + dt.timedelta(seconds=secs)
                dt_obj_end = dt_obj_new_start
                new_time_str = (dt_obj_new_start.strftime('%Y-%m-%d %H:%M:%S,%f')).split(" ")[1]
                dict_of_dialogs[key + 1].start_time = new_time_str
                dict_of_dialogs[key].end_time = new_time_str

                if (dt_obj_end.timestamp() - dt_obj_start.timestamp()) < 1.0:  # minimum 1 seccond
                    if (key - 1) in dict_of_dialogs:
                        dt_prev_start_time = datetime.strptime("01/01/2021 " + dict_of_dialogs[key - 1].start_time,
                                                               '%d/%m/%Y %H:%M:%S,%f')
                        secs = math.floor((dt_obj_end.timestamp() - dt_prev_start_time.timestamp()) / 2)
                        dt_obj_new_start = dt_prev_start_time + dt.timedelta(seconds=secs)
                        new_time_str = (dt_obj_new_start.strftime('%Y-%m-%d %H:%M:%S,%f')).split(" ")[1]
                        dt_obj_start = dt_obj_new_start
                        dict_of_dialogs[key].start_time = new_time_str
                        dict_of_dialogs[key - 1].end_time = new_time_str

                        if (dt_obj_end.timestamp() - dt_obj_start.timestamp()) < 1.0:  # minimum 1 seccond
                            time_error_log = time_error_log + " " + str(key) + ","
                    else:
                        time_error_log = time_error_log + " " + str(key) + ","
            else:
                time_error_log = time_error_log + " " + str(key) + ","

    return dict_of_dialogs, time_error_log


def clean_srt_file(file_name_to_read, final_file_name, final_time_of_video=None):
  num_frame = 1
  dict_of_dialogs = dict()
  f = io.open(file_name_to_read, mode="r", encoding="utf-8")

  # eliminate "\n" in the end of the file
  all_lines = f.readlines()
  i = len(all_lines)-1
  while i > 0 and all_lines[i]=="\n":
    i-=1
  all_lines = all_lines[:(i+1)]
  with open(final_file_name, 'w', encoding='utf-8') as o_file:
    for line in all_lines:
      o_file.write(line)

  f = io.open(final_file_name, mode="r", encoding="utf-8")
  # end eliminate "\n" in the end of the file

  frame_read = False
  tini_tfi = []
  for text in f:
    if frame_read:
      time_ini_time_fi = text
    else:
      time_ini_time_fi = ""

    if num_frame == 1:
      if not frame_read:
        while not (len(text) < 6 and text[:-1].isdigit()):
          text = f.readline()

        time_ini_time_fi = f.readline()  # temps ini --> temps fi

      tini_tfi = time_ini_time_fi.split("-->")
      time_ini = tini_tfi[0]
      while time_ini[-1] == " ":
        time_ini = time_ini[:-1]
      text = f.readline()
      while text == "\n" or text == " \n":
        text = f.readline()  # text
      new_text = text
      while text[-2] != "\n" and new_text != "" and new_text != " \n":
        new_text = f.readline()
        if len(new_text) < 6 and new_text[:-1].isdigit():
          frame_read = True
          break
        else:
          frame_read = False
          if new_text != " \n":
            text += new_text
          # else:
          #   print(str(num_frame) + "")

      if text[-2] != "\n":
        text = text + "\n"

      dict_of_dialogs[num_frame] = Perevod(num_frame,time_ini,text)

    else:
      # altres vegades
      if not frame_read:
        while not (len(text) < 6 and text[:-1].isdigit()):
          text = f.readline()
        time_ini_time_fi = f.readline()  # temps ini --> temps fi

      tini_tfi = time_ini_time_fi.split("-->")
      time_ini = tini_tfi[0]
      while time_ini[-1] == " ":
        time_ini = time_ini[:-1]
      text = f.readline()  # text
      while text == "\n" or text == " \n":
        text = f.readline()  # text
      new_text = text
      while text[-2] != "\n" and new_text != "" and new_text != " \n":
        new_text = f.readline()
        if len(new_text) < 6 and new_text[:-1].isdigit():
          frame_read = True
          break
        else:
          frame_read = False
          if new_text != " \n":
            text += new_text
          # else:
          #   print(str(num_frame) + "")

      if text[-2] != "\n":
        text = text + "\n"

      dict_of_dialogs[num_frame] = Perevod(num_frame, time_ini, text)
      dict_of_dialogs[(num_frame-1)].set_end_time(time_ini)

    # if num_frame == 188:
    #   hola = 1
    print(num_frame)
    print(text)
    num_frame +=1

  if not final_time_of_video:
    final_time_of_video = tini_tfi[1]
    while final_time_of_video[-1] == " " or final_time_of_video[-1] == "\n":
      final_time_of_video = final_time_of_video[:-1]
    while final_time_of_video[0] == " ":
      final_time_of_video = final_time_of_video[1:]

  dict_of_dialogs[(num_frame - 1)].set_end_time(final_time_of_video)
  dict_of_dialogs, time_error_log = check_and_correctTimes(dict_of_dialogs)

  with open(final_file_name, 'w', encoding='utf-8') as o_file:
    for key,p in dict_of_dialogs.items():
      o_file.write(str(key)+"\n")

      dt_obj_start = datetime.strptime("01/01/2021 " + p.start_time,'%d/%m/%Y %H:%M:%S,%f')
      dt_obj_end = datetime.strptime("01/01/2021 " + p.end_time,'%d/%m/%Y %H:%M:%S,%f')

      if (dt_obj_end.timestamp() - dt_obj_start.timestamp()) < 1.0:  # minimum 1 second
          time_error_log = time_error_log + " " + str(key) + ","

      o_file.write(str(p.start_time)+" --> "+str(p.end_time) + "\n")
      o_file.write(p.t)

  if len(time_error_log)>0:
      time_error_log = time_error_log[:-1]  # eliminar ultima coma

  return time_error_log


def openFile():
    tf = filedialog.askopenfilename(
        title="Open Text file",
        filetypes=(("Text Files", "*.txt  *.srt"),)
        )
    myLabelDestination.configure(text="")
    myLabelError.configure(text="")
    pathh.delete(0, END)
    pathh.insert(0, tf)
    tf = io.open(tf, mode="r", encoding="utf-8")
    # tf = open(tf)  # or tf = open(tf, 'r')
    data = tf.read()
    txtarea.delete("1.0","end")
    txtarea.insert(END, data)
    tf.close()

def cleanFile():

    origin_path = pathh.get()
    processed_text = "Your processed file has been successfully stored in\n"
    format_error = "The "+ origin_path[-4:] +" file format is not supported.\nSupported formats are: .srt and .txt\n"
    if origin_path[-4:] == ".srt": #srt
        file_name = origin_path.split(".srt")
        destination_file = file_name[0]+"_processed"+".srt"
        err_log = clean_srt_file(origin_path,destination_file)
        myLabelDestination.configure(text=processed_text + destination_file)
        if err_log != "":
            myLabelError.configure(text="Please check the start and end times of the following frames:\n" + err_log)
        showinfo("DONE!", processed_text + destination_file)

    elif origin_path[-4:] == ".txt": #txt
        file_name = origin_path.split(".txt")
        destination_file = file_name[0] + "_processed" + ".srt"
        err_log = clean_srt_file(origin_path, destination_file)
        myLabelDestination.configure(text=processed_text + destination_file)
        if err_log != "":
            myLabelError.configure(text="Please check the start and end times of the following frames:\n"+err_log)
        showinfo("DONE!", processed_text + destination_file)

    else:
        myLabelError.configure(text=format_error)
        showinfo("ERROR", format_error)

ws = Tk()
ws.title("SRT Cleaner")
# ws.wm_iconbitmap('logo.ico')
ws.geometry("400x600")
ws['bg']='#fb0'

myLabelAuthor = Label(ws, text="Created by Natalia Mordvanyuk",background='#fb0')
myLabelAuthor.pack(side=BOTTOM)

# el text area on anira el text a 20 amb pady
txtarea = Text(ws, width=40, height=20)
txtarea.insert(END, "The content of the file")
txtarea.pack(pady=20)

infoLabel = Label(ws, text="The procedure is:\n1 - Select the file and wait until the file is loaded\n2 - Clean file and wait until process finishes",background='#fb0')
infoLabel.pack(pady=5)

myLabelDestination = Label(ws, text="",background='#fb0',fg="blue")
myLabelDestination.pack()

myLabelError = Label(ws, text="",background='#fb0',fg="red")
myLabelError.pack()

# el posa a lesquerra
pathh = Entry(ws)
pathh.insert(0, " ")
pathh.pack(side=LEFT, expand=True, fill=X, padx=20,pady=10)


Button(
    ws,
    text="Clean File",
    command=cleanFile
    ).pack(side=RIGHT, expand=True, fill=X, padx=20,pady=10)

Button(
    ws,
    text="Select File",
    command=openFile
    ).pack(side=RIGHT, expand=True, fill=X, padx=20, pady=10)


# b2.place(x=300, y=600)

ws.mainloop()
