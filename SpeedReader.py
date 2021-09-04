#! python3
from tkinter import *
from tkinter import ttk
import time
from tkinter import filedialog
from tkinter import messagebox
import threading
import os
import sys


font_size = 28
words_default = 20
chars_default = 36
WPM_default = 300
text = ''
words = words_default
start_time = 0
words_read = 0
total_words = 0
spacers = (' ','\n','\t','—')
WPM = WPM_default
keep_going = False
show_multiple = 0
previous_text = []


def clear_text():
    log['state'] = 'normal'
    log.delete(1.0, 'end')
    log['state'] = 'disabled'


def return_words():
    global words_default
    global chars_default
    global words
    try:
        temp = my_entry.get().split(',')
        words = int(temp[0])
        chars = int(temp[1])
    except:
        words = words_default
        chars = chars_default
        my_entry.delete(0, END)
        my_entry.insert(0, str(words) + ', ' + str(chars))
    log.focus_set()
    line = ' '
    count = 0
    position = 0
    for y in text:
        position += 1
        if y in spacers:
            if line[-1] != ' ':
                line += ' '
                count += 1
                if (count == words) or (len(line) > chars):
                    return (line[1:], position, count)
        else:
            line += y
    return (line[1:], position, count)


def count_words(phrase='blankXYZ'):
    global text
    if phrase == 'blankXYZ':
        phrase = text
    line = ' '
    count = 0
    for y in phrase:
        if y in spacers:
            if line[-1] != ' ':
                line += ' '
                count += 1
        else:
            line += y
    return count


def show_text(placeHolder):
    global text
    global words
    global start_time
    global words_read
    global total_words
    global WPM
    global keep_going
    global show_multiple
    global previous_text
    font_size = spin_box.get()
    log.tag_configure('bold', font=('Arial', font_size, 'bold', 'underline'))
    log.tag_configure('plain', foreground='blue', font=('Arial', font_size, 'italic'))
    while len(text) > words and keep_going == True:
        part1, position, count = return_words()
        previous_text.append(part1)
        text = text[position:]
        clear_text()
        log['state'] = 'normal'
        log.insert(END, part1+"\n", 'bold')
        if show_multiple == 0:
            log.insert(END, text, 'plain')
        log['state'] = 'disabled'
        speed = int(words_read/(time.time()-start_time)*60)
        my_speed['text'] = 'Words per minute: '+str(speed)
        words_read += count
        words_remain = total_words - words_read
        my_remain['text'] = 'Words remain: ' + str(words_remain)
        my_progress['value'] = words_read / total_words * 100
        try:
            my_time['text'] = 'Time remain: ' + str(round(words_remain/speed,1)) + ' min.'
        except ZeroDivisionError:
            my_time['text'] = 'Time remain: ???'
        time.sleep(count/WPM*60)
    keep_going = False


def write_text():
    global text
    global words
    global start_time
    global words_read
    global total_words
    global keep_going
    global show_multiple
    global previous_text
    if keep_going:          # thread started and displaying words
        keep_going = False  # kill thread
    elif text != '':
        font_size = spin_box.get()
        log.tag_configure('bold', font=('Arial', font_size, 'bold', 'underline'))
        log.tag_configure('plain', foreground='blue', font=('Arial', font_size, 'italic'))
        part1, position, count = return_words()
        previous_text.append(part1)
        text = text[position:]
        clear_text()
        log['state'] = 'normal'
        log.insert(END, part1+"\n", 'bold')
        if show_multiple == 0:
            log.insert(END, text, 'plain')
        log['state'] = 'disabled'
        speed = int(words_read/(time.time()-start_time)*60)
        my_speed['text'] = 'Words per minute: '+str(speed)
        words_read += count
        words_remain = total_words - words_read
        my_remain['text'] = 'Words remain: ' + str(words_remain)
        my_progress['value'] = words_read / total_words * 100
        try:
            my_time['text'] = 'Time remain: ' + str(round(words_remain / speed, 1)) + ' min.'
        except ZeroDivisionError:
            my_time['text'] = 'Time remain: ???'


def back_text():
    global text
    global keep_going
    global previous_text
    global words
    global words_read
    global show_multiple
    global start_time
    global total_words
    if len(previous_text) > 1:
        count2 = count_words(previous_text[-2])
        count1 = count_words(previous_text[-1])
        text = previous_text[-2] + previous_text[-1] + text
        previous_text = previous_text[:-2]
        keep_going = False
        words_read -= count1 + count2
        font_size = spin_box.get()
        log.tag_configure('bold', font=('Arial', font_size, 'bold', 'underline'))
        log.tag_configure('plain', foreground='blue', font=('Arial', font_size, 'italic'))
        part1, position, count = return_words()
        previous_text.append(part1)
        text = text[position:]
        clear_text()
        log['state'] = 'normal'
        log.insert(END, part1+"\n", 'bold')
        if show_multiple == 0:
            log.insert(END, text, 'plain')
        log['state'] = 'disabled'
        speed = int(words_read/(time.time()-start_time)*60)
        my_speed['text'] = 'Words per minute: '+str(speed)
        words_read += count
        words_remain = total_words - words_read
        my_remain['text'] = 'Words remain: ' + str(words_remain)
        my_progress['value'] = words_read / total_words * 100
        try:
            my_time['text'] = 'Time remain: ' + str(round(words_remain / speed, 1)) + ' min.'
        except ZeroDivisionError:
            my_time['text'] = 'Time remain: ???'
        

def get_text():
    global text
    global words
    global start_time
    global words_read
    global total_words
    global WPM
    global keep_going
    global words_default
    global chars_default
    global WPM_default
    global previous_text
    try:
        temp = my_entry.get().split(',')
        words = int(temp[0])
    except:
        words = words_default
        my_entry.delete(0, END)
        my_entry.insert(0, str(words) + ', ' + str(chars_default))
    try:
        WPM = int(my_WPM.get())
    except:
        WPM = WPM_default
        my_WPM.delete(0, END)
        my_WPM.insert(0, WPM)
    log.focus_set()
    if keep_going == False:
        if text == '':
            text = log.get(1.0, 'end')
        previous_text = []
        keep_going = True
        total_words = count_words()
        my_wordCount['text'] = 'Number of words: ' + str(total_words)
        start_time = time.time() + 0.1
        words_read = 0
        t1 = threading.Thread(target=show_text, args=(1,), daemon=True)
        t1.start()
    else:
        keep_going = False

def speed_text():
    global text
    global words
    global WPM
    global keep_going
    global words_default
    global chars_default
    global WPM_default
    if keep_going: # thread is ongoing displaying text
        keep_going = False
    elif text != '': # there is remaining text to display
        try:
            temp = my_entry.get().split(',')
            words = int(temp[0])
        except:
            words = words_default
            my_entry.delete(0, END)
            my_entry.insert(0, str(words) + ', ' + str(chars_default))
        try:
            WPM = int(my_WPM.get())
        except:
            WPM = WPM_default
            my_WPM.delete(0, END)
            my_WPM.insert(0, WPM)
        log.focus_set()
        keep_going = True
        t1 = threading.Thread(target=show_text, args=(1,), daemon=True)
        t1.start()


def save_text():
    global text
    save_filename = save_entry.get()
    if len(save_filename) < 4 or save_filename[-4] != '.':
        save_filename = save_filename + '.txt'
    MsgBox = 'yes'
    if save_filename in [i for i in os.listdir() if i[-4:] == '.txt']:
        MsgBox = messagebox.askquestion('Save to File',
                                        'Are you sure you want to overwrite existing file ?',
                                        icon='warning')
    if MsgBox == 'yes':
        with open(save_filename, 'w') as out_file:
            out_file.write(log.get(1.0, 'end'))


def activate_text():
    global text
    global total_words
    global WPM
    global WPM_default
    log['state'] = 'normal'
    log.delete(1.0, 'end')
    text = root.clipboard_get()
    log.insert(END, text)
    total_words = count_words()
    my_wordCount['text'] = 'Number of words: ' + str(total_words)
    my_speed['text'] = 'Words per minute: '
    my_remain['text'] = 'Words remain: '
    try:
        WPM = int(my_WPM.get())
    except:
        WPM = WPM_default
        my_WPM.delete(0, END)
        my_WPM.insert(0, WPM)    
    my_time['text'] = 'Time remain: ' + str(round(total_words/WPM,1)) + ' min.'
    log['state'] = 'disabled'
    

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def read_file(filename):
    global text
    global total_words
    global WPM
    global WPM_default
    clear_text()
    log['state'] = 'normal'
    try:
        text = ''
        with open(filename, 'rt') as fin:
            for data in read_in_chunks(fin):
                log.insert(END, data)
        text = log.get(1.0, 'end')
        total_words = count_words()
        my_wordCount['text'] = 'Number of words: ' + str(total_words)
        my_speed['text'] = 'Words per minute: '
        my_remain['text'] = 'Words remain: '
        try:
            WPM = int(my_WPM.get())
        except:
            WPM = WPM_default
            my_WPM.delete(0, END)
            my_WPM.insert(0, WPM)    
        my_time['text'] = 'Time remain: ' + str(round(total_words/WPM,1)) + ' min.'        
        log['state'] = 'disabled'
    except FileNotFoundError as e:
        log.insert(END, 'No such file.\n')
        log['state'] = 'disabled'
    except:
        log.insert(END, 'Cannot read file.\nFile must be in ANSI txt form.\n')
        log['state'] = 'disabled'


def on_open():
    global text
    dlg = filedialog.Open()
    file_name = dlg.show()
    read_file(file_name)
    s = file_name
    s = s[s.rfind('/')+1:-4]
    save_entry.delete(0, 'end')
    if 'Marked' in s:
        save_entry.insert(0, s)
    else:
        save_entry.insert(0, s + 'Marked')


def radio_select():
    global show_multiple
    show_multiple = var.get()


def paste():    
    global text
    log['state'] = 'normal'
    log.delete(1.0, 'end')
    log.focus_set()
    r = Tk()      # use tkinter to get access to the clipboard
    r.withdraw()  # keep the r window from showing
    try:
        text = r.clipboard_get()
    except:
        text = 'Clipboard cannot be pasted.'
    log.insert(END, text)
    log['state'] = 'disabled'


def increase_speed():
    global WPM
    global WPM_default
    try:
        WPM = int(my_WPM.get())
    except:
        WPM = WPM_default
    WPM += 10
    my_WPM.delete(0, END)
    my_WPM.insert(0, WPM)


def decrease_speed():
    global WPM
    global WPM_default
    try:
        WPM = int(my_WPM.get())
    except:
        WPM = WPM_default
    WPM -= 10
    my_WPM.delete(0, END)
    my_WPM.insert(0, WPM)


def frag_file():
    global text
    try:
        words_size = int(my_frag.get())
    except:
        words_size = 1000
        my_frag.delete(0, END)
        my_frag.insert(0, words_size)
    if text == '':
        text = log.get(1.0, 'end')
    total_words = count_words(text)
    parts = int(total_words / words_size) + 1
    lines = text.split('\n')
    number_of_lines = len(lines)
    line_limit = int(number_of_lines / parts) + 1
    count = 0
    for i in range(parts):
        file_name = save_entry.get()
        if '.txt' in file_name:
            file_name = file_name[:-4]
        file_name = file_name + '-' + str(i) + '.txt'
        count_limit = 0
        with open(file_name, 'wt') as fin:
            while (count_limit < line_limit and count < number_of_lines):
                fin.write(lines[count] + '\n')
                count += 1
                count_limit += 1


if __name__ == "__main__":
    root = Tk()
    root.title("Speed Reader 20")

    my_frame = ttk.Frame(root, padding="3 3 12 12")
    my_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    my_frame.columnconfigure(0, weight=1)
    my_frame.rowconfigure(0, weight=1)

    my_label0 = Label(my_frame, text='Words Per Minute set to: ', font=('Arial', 12))
    my_label0.grid(column=2, row=0, sticky=E)
    myButton1 = Button(my_frame, text="Paste              <  p  >", fg='blue', bg='orange',
                       font=('Arial', 12), command=activate_text)
    myButton1.grid(column=4, row=0, sticky=E)
    myButton2 = Button(my_frame, text='Start/Stop <Enter>', fg='blue', bg='orange',
                       font=('Arial', 12), command=get_text)
    myButton2.grid(column=4, row=1, sticky=W)
    myButton3 = Button(my_frame, text='Step          <Space>', fg='blue', bg='orange',
                       font=('Arial', 12), command=write_text)
    myButton3.grid(column=4, row=2, sticky=E)
    
    my_label4 = Label(my_frame, text='Highlighted words: ', font=('Arial', 12))
    my_label4.grid(column=0, row=0, sticky=E)
    my_wordCount = Label(my_frame, text='Number of words: ', font=('Arial', 12))
    my_wordCount.grid(column=0, row=1, sticky=E)
    my_speed = Label(my_frame, text='Words per minute: ', font=('Arial', 12),
                     bg='blue', fg='yellow')
    my_speed.grid(column=2, row=1, sticky=W)
    my_remain = Label(my_frame, text='Words remain: ', font=('Arial', 12))
    my_remain.grid(column=0, row=2, sticky=E)
    my_time = Label(my_frame, text='Time remain: ', font=('Arial', 12))
    my_time.grid(column=0, row=3, sticky=E)
    var = IntVar()
    my_radio1 = Radiobutton(my_frame, text='Single Line', variable=var, value=1,
                            command=radio_select)
    my_radio1.grid(column=4, row=3, sticky=W)
    my_radio2 = Radiobutton(my_frame, text='Multiple Lines', variable=var, value=0,
                            command=radio_select)
    my_radio2.grid(column=4, row=4, sticky=W)

    myButton4 = Button(my_frame, text="Back              <  b  >", fg='blue', bg='orange',
                       font=('Arial', 12), command=back_text)
    myButton4.grid(column=4, row=6, sticky=E)
    myButton5 = Button(my_frame, text="Restart           <  r  >", fg='blue', bg='orange',
                       font=('Arial', 12), command=speed_text)
    myButton5.grid(column=4, row=7, sticky=E)
    myButton6 = Button(my_frame, text="Save to      <  s  >", fg='blue', bg='orange',
                       font=('Arial', 12), command=save_text)
    myButton6.grid(column=0, row=8, sticky=E)
    save_entry = Entry(my_frame, width=13, borderwidth=5)
    save_entry.grid(column=1, row=8, sticky=W)
    save_entry.insert(0, 'bookmark.txt')
    myButton7 = Button(my_frame, text="Frag file  <  f  >", fg='blue', bg='orange',
                       font=('Arial', 12), command=frag_file)
    myButton7.grid(column=2, row=8, sticky=E)

    my_progress = ttk.Progressbar(my_frame, orient=HORIZONTAL,
                                  length=1084, mode='determinate')
    my_progress.grid(column=2, row=4, sticky=E)
    
    my_entry = Entry(my_frame, width=13, borderwidth=5)
    my_entry.grid(column=1, row=0, sticky=W)
    my_entry.insert(0, str(words) + ', ' + str(chars_default))
    my_WPM = Entry(my_frame, width=5, borderwidth=5)
    my_WPM.grid(column=3, row=0, sticky=E)
    my_WPM.insert(0, WPM)
    my_frag = Entry(my_frame, width=5, borderwidth=5)
    my_frag.grid(column=3, row=8, sticky=W)
    my_frag.insert(0, 1000)

    xscrollbar = Scrollbar(my_frame, orient=HORIZONTAL)
    xscrollbar.grid(column=2, row=6, sticky=N+W+E+W)
    yscrollbar = Scrollbar(my_frame)
    yscrollbar.grid(column=3, row=5, sticky=N+S+W)

    log = Text(my_frame, state='disabled', width=120, height=30, wrap=CHAR,
               bg = 'black',
               fg = 'orange',
               font=('Arial', 12),
               xscrollcommand=xscrollbar.set,
               yscrollcommand=yscrollbar.set)
    log.grid(column=2, row=5, sticky=S)
    
    xscrollbar.config(command=log.xview)
    yscrollbar.config(command=log.yview)

    my_label5 = Label(my_frame, text='Font Size: ', font=('Arial', 12))
    my_label5.grid(column=0, row=7, sticky=E)
    spin_box = Spinbox(my_frame, width=13, fg='blue', bg='orange',
                        from_=12, to=28)
    spin_box.grid(column=1, row=7, sticky=W)
    spin_box.delete(0, 'end')
    spin_box.insert(0, font_size)

    #text = read_file(filename)

    log.bind('p', lambda e: activate_text())
    root.bind('<Return>', lambda e: get_text())
    log.bind('<space>', lambda e: write_text())
    log.bind('b', lambda e: back_text())
    log.bind('r', lambda e: speed_text())
    log.bind('s', lambda e: save_text())
    log.bind(',', lambda e: decrease_speed())
    log.bind('.', lambda e: increase_speed())
    log.bind('f', lambda e: frag_file())
    
    menubar = Menu(root)
    root.config(menu=menubar)
    file_menu = Menu(menubar)
    file_menu.add_command(label="Open", command=on_open)
    file_menu.add_command(label="Paste", command=paste)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    file_list = sys.argv[1:]
    if len(file_list) == 0:
        txt_files = [i for i in os.listdir() if i[-4:] == '.txt']
        if len(txt_files) > 0:
            txt_files.sort()
            read_file(txt_files[0])
    else:
        read_file(file_list[0])
        s = file_list[0]
        s = s[s.rfind('\\')+1:-4]
        save_entry.delete(0, 'end')
        if 'Marked' in s:    
            save_entry.insert(0, s)
        else:
            save_entry.insert(0, s + 'Marked')

    root.mainloop()

