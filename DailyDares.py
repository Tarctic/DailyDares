import tkinter as tk
import csv
import random
import pickle
from datetime import timedelta as td
from datetime import datetime as dt
from datetime import time, date

root=tk.Tk()
def main_root():
    '''
    Main screen of DailyDares.  
    Comes with an icon, a title, buttons for main features and a background image
    '''
    root.geometry("600x600")
    root.title('Daily Dares')
    root.iconbitmap(r'Files/icon.ico')
      
    # Create Canvas
    canvas1 = tk.Canvas( root, width = 600, height = 600)  
    canvas1.pack(fill = "both", expand = True)
      
    # Add image file
    bg = tk.PhotoImage(file = "Files/main.png")
    
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
      
    # Create Buttons
    button1 = tk.Button(root, text = "RANDOM", command=random_dare, bg="gray20", fg="white", padx=6, pady=6, font="Calibri")
    button2 = tk.Button(root, text = "ISLAMIC", command=islamic, bg="gray20", fg="white", padx=6, pady=6, font="Calibri")
    button3 = tk.Button(root, text = "VIEW CURRENT DARES", command=view_current, bg="gray20", fg="white", padx=6, pady=6, font="Calibri")
    button4 = tk.Button(root, text = "OPTIONS", command=options, bg="gray20", fg="white", padx=6, pady=6, font="Calibri") 

    # Display Buttons
    canvas1.create_window( 252, 280, anchor = "nw", window = button1)   
    canvas1.create_window( 257, 340, anchor = "nw", window = button2)
    canvas1.create_window( 207, 400, anchor = "nw", window = button3)
    canvas1.create_window( 252, 460, anchor = "nw", window = button4)
    
    root.mainloop()

# format of a dare record: [id_, dare_type/kind, name, default priority, current priority]
    
def random_dare():
    '''Chooses and displays a dare of type 'Random' '''
    screen1 = screen("Random Dare") # create a new window
    choose(dare_type='0', screen1=screen1) # '0' represents dare type (here, Random)
    
def islamic():
    '''Chooses and displays a dare of type 'Islamic' '''
    screen1 = screen("Islamic")
    choose(dare_type='1', screen1=screen1) # '1' represents dare type (here, Islamic)
    
def choose(dare_type, screen1):
    '''
    - Creates a list of dares multiplied by their priorities
    - Chooses a random dare from the list
    - Reduces current priority by 2
    - Adds the dare to log with 'selected' command
    - Displays time left to complete dare
    '''

    done, done_rec = get_todays_dare(k=dare_type) # get todays dare record if it exists and info on whether it has been completed or not
    if not done==1: # if no dare has began or if todays dare has been completed
        dares = get_dares() # get the list of all dares
        check_reset(dares, dare_type) # check if it's time to reset the dares
        
        prior_dares = [] # list of all dares multiplied by priority (will be added)
        c = 0
        for d in dares:
            if d[1]==dare_type:
                c+=1
                prior_dares.extend([(d[0])]*int(d[4])) # multiply each dare by it's priority and add it to the list
        
        if c>0 and len(prior_dares) > 0: # if there is at least one dare
                num = random.choice(prior_dares) # get a random dare from the list
                dare = remove_dare(id_=num,command='selected')[1] # remove the dare from the csv file and get the record of the removed dare
                name = dare[2] # get the name of the dare from the record
                dare[4] = int(dare[4]) - 2 # reduce the current priority by 2
                if dare[4]<0: # if the current priority is negative
                    dare[4] = 0 # change it to 0
                add_dare(*dare,command="selected") # add the edited record to the csv file
                
                ll(screen1, "")
                ll(screen1, "YOUR DARE:", height=4, fg="black")
                ll(screen1, name.upper(), fontsize=20) # display the dare content
                ll(screen1, "")
                ll(screen1, text=f"Time left to complete: {time_left()}") # display time left to complete
                
        else:
            ll(screen1, "No dares available!", height=4, fg="black")
    
    else:
        ll(screen1, "", height=5)
        ll(screen1, "Please complete current dare first!", fg="black")
        ll(screen1, f"Current dare: {done_rec[4]}", fg="black")
        ll(screen1, "", height=4)
        
        ll(screen1, text=f"Time left to complete: {time_left()}")
        
def check_reset(dares, dare_type):
    '''Checks if it's time to reset the current priorities'''
    
    try:
        f = open('files/log.dat','rb')
    except FileNotFoundError: # If no log file is found:
        add_to_log(command='start') # Create a log file and add an empty record with 'start' command
        last_reset = dt.now()
        f = open('files/log.dat','rb')

    # 'start' is the first record in a log file. The time at which the user asks for a dare is set as first reset time and is stored in 'start' record.
    # After that, the next reset will be done after specified number of days (eg: a week)
    start = 0 
    try:
        while True:
            rec = pickle.load(f)
            if rec[0]=='start':
                start = 1
                last = rec # get the last start record
            if rec[0]=='reset' and rec[3]==dare_type:
                last = rec # get the last reset record
    except EOFError:
        f.close()
    
    now = dt.now() # time now
    if not start: # if there is no 'start' record
        add_to_log(command='start') # add it
        last_reset = now
        
    if start:
        last_reset = dt.strptime(last[1],"%Y-%m-%d %H:%M:%S.%f") # time of last reset
    
    if now > last_reset + td(weeks=1): # if a week has passed since last reset: 
        reset_priorities(dare_type=dare_type, dares=dares) # reset priorities (of the dare_type)
        
def reset_priorities(dare_type, dares, msg=0, screen1=None):
    '''Resets the current priorities to their default values'''

    for dare in dares:
        if dare[1]==dare_type:
            id_ = dare[0]
            remove_dare(id_=id_,command='reset')
            dare[4] = dare[3] # Resetting current priority of dare to default priority
            add_dare(*dare,command="reset")
    
    if msg:
        ll(screen1, "Saved!")
    
def time_left():
    '''Calculates time left to midnight'''
    left = str(dt.combine((dt.today() + td(days=1)),time(00,00)) - dt.now()) # calculate time left to the end of day (midnight)
    hm = left[:5].split(':') # split into hours and minutes
    left_time = f"{int(hm[0])} hours, {int(hm[1])} minutes"
    return left_time

def view_current():
    '''Shows current selected dare and button to mark it as done'''

    screen1 = screen("View Current Dares")
    
    for dare_type in ["0Random","1Islamic"]:
        ll(screen1, f"{dare_type[1:]}:", fg="black", height=2) # Display dare type as heading
        
        kind = dare_type[0] # kind = '0' or '1'
        done, done_rec = get_todays_dare(k=kind)
        
        if done == 1: # dare has began but has not been completed
            ll(screen1, done_rec[4]) # display current priority
            s,d = screen1, done_rec
            lb(screen1, "Mark as done", lambda s=s, d=d: mark_done(s,d)) # button to mark current dare as done
        else:
            ll(screen1, "No dare chosen!")

def get_todays_dare(k):
    '''
    Returns 0/1/2 and associated record
    - 0 - No dare selected (empty record)
    - 1 - Dare selected but not completed
    - 2 - Dare selected and completed (empty record)
    '''

    f = open('files/log.dat','rb')
    try:
        id_ = done = 0 # There is no dare today that has either began or been completed
        done_rec = []
        while True:
            rec = pickle.load(f)
            rec_time = dt.strptime(rec[1],"%Y-%m-%d %H:%M:%S.%f") # time given in the record
            today = dt.combine(date.today(),time(00,00)) # date and time today at 00:00
            if rec[0]=='selected' and rec_time > today and str(rec[3])==k: # If there is a selected dare after today began (midnight) and the dare type matches:
                id_ = rec[2] # collect it's ID
                done_rec = rec # collect the whole record
                done = 1 # Note that the dare has began but has not been completed
            if rec[2] == id_ and rec[0] == 'done' and rec_time > today: # if there is a completed dare id after today began that matches the selected dare id from earlier:
                done = 2 # Note that the dare has been completed in time
    except EOFError:
        f.close()
    
    return done, done_rec # return whether the dare has been completed and the record of the dare
            
def mark_done(screen1, rec):
    '''Adds 'done' record to log and show congratulatory message'''

    add_to_log(command="done",id_=rec[2],kind=rec[3],name=rec[4])
    cong = random.choice(['Good work!','Keep it up!', "Awesome!", "Way to go, buddy!", "COOL!", "WOOHOO!"]) # select a random congrats message
    ll(screen1, cong)
        
def options():
    '''Shows buttons for options'''
    screen1 = screen("Options")

    # display buttons for each option
    lb(screen1, "View Dares", view, 3)
    lb(screen1, "Change Current Priority", lambda: change(priority_type="current"))
    lb(screen1, "Change Default Priority", lambda: change(priority_type="default"))
    lb(screen1, "Add Dare", add)
    lb(screen1, "Remove Dare", remove)
    lb(screen1, "Reset Priorities", reset)
    return screen1

def view():
    '''Shows all dares'''
    final_height = screen_height(limit=10) # get calculated screen height (screen height needs to be increased when there are too many dares)
    screen1 = screen("View Dares", final_height)
    display(screen1=screen1,total_done=1) # display all dares (along with number of completed dares so far)
    
def change(priority_type):
    '''Screen for changing priority'''
    final_height = screen_height(limit=3)
    screen1 = screen(f"Change {priority_type} priority", final_height)
    display(screen1) # display all dares
    id_ = tk.StringVar()
    priority = tk.StringVar()
    
    lle(screen1, "Enter dare ID:",id_) # create a user input field for id_
    lle(screen1, f"Enter new {priority_type} priority:",priority) # create a user input field for priority
    lb(screen1, "Save", lambda: save_priority(screen1, id_.get(), priority.get(), priority_type)) # button to save the new priority
    
def save_priority(screen1, num, p, priority_type):
    '''Saves the new priority'''
    
    if priority_type == "default": priority_type_num = 3
    elif priority_type == "current": priority_type_num = 4
    
    command="c_"+priority_type
    c, dare = remove_dare(id_=num,p=p,command=command) # remove previous record
    
    text = "Saved!"
    if c==0:
        text = dare
    else:
        dare[priority_type_num] = p # set new priority
        text = add_dare(*dare,command=command) # add new record
    ll(screen1, text)

def add():
    '''Screen for adding a new dare'''
    screen1 = screen("Add Dare")
    
    name = tk.StringVar()
    kind = tk.StringVar()
    kind.set(value='0') # temporary selected value before user chooses (for radio buttons)
    default = tk.StringVar()
    
    lle(screen1,"Dare:",name)
    ll(screen1,"Dare Type:",fg="white")
    tk.Radiobutton(screen1, text="Random", variable=kind, value='0').pack(pady=(5,10))
    tk.Radiobutton(screen1, text="Islamic", variable=kind, value='1').pack()
    lle(screen1, "Default Priority:", default)
    lb(screen1, "Save", lambda: save(screen1=screen1, kind=kind.get().strip(), name=name.get().strip(), def_priority=default.get().strip() )) # save new dare
    
def save(screen1, kind,name,def_priority):
    '''Adds new dare to list of dares and 'add' record to log'''
    cur_priority = def_priority # current priority is set to default priority
    text = add_dare(kind=kind,name=name,def_priority=def_priority,cur_priority=cur_priority,command='add') # add new dare record to csv file
    ll(screen1, text)
    
def remove():
    '''Screen for removing dare'''
    final_height = screen_height(limit=7)
    screen1 = screen("Remove Dare", final_height)
    display(screen1)
    id_ = tk.StringVar()
    
    lle(screen1,"Enter dare ID:",id_)
    lb(screen1, "Remove", lambda: delete(screen1, id_.get())) # button to delete dare
    
def delete(screen1, id_):
    '''Deletes dare from list of dares and adds 'delete' record to log'''
    c = remove_dare(id_,command='remove')[0] # remove the dare matching id_ from csv file and get the record
            
    text="Removed!"
    if c==0: # if id_ of record returned is 0:
        text = f"Dare ID '{id_}' not found!" # display error message
    
    ll(screen1, text)
    
def reset():
    '''Screen for resetting priorities to their default values'''
    screen1 = screen("Reset priorities")
    # buttons for force resetting current priorities to their defaults
    lb(screen1, "Random", lambda: reset_priorities(dare_type='0', dares=get_dares(), msg=1, screen1=screen1), label_height=4)
    lb(screen1, "Islamic", lambda: reset_priorities(dare_type='1', dares=get_dares(), msg=1, screen1=screen1))
    
    
def screen(title, final_height=380):
    '''Creates a screen of given height and returns the screen'''
    screen1=tk.Toplevel(root)
    screen1.title(title)
    screen1.geometry(f"400x{final_height}") # height depends on arguments passed, default=380
    screen1.configure(bg="DarkSlateGray3")
    screen1.iconbitmap(r'Files/icon.ico')
    
    return screen1

def ll(screen1, text, fontsize=11, height=1, fg="green"):
    '''Creates two labels to passed screen, customized according to arguments'''
    # ll stands for Label Label
    # this function helps shorten code by creating two labels in one line of code
    tk.Label(screen1,text="",bg="DarkSlateGray3", height=height).pack()
    tk.Label(screen1, text=text, fg=fg, bg="DarkSlateGray3", font=("calibri",fontsize)).pack()

def lle(screen1, text, textv):
    '''Creates two labels and an input field to passed screen, customized according to arguments'''
    # lle stands for Label Label Entry
    # this function helps shorten code by creating two labels and an entry (input field) in one line of code
    ll(screen1, text, fg="white")
    tk.Entry(screen1, textvariable=textv).pack()
    
def lb(screen1, button_text, command, label_height=1):
    '''Creates a label and a button to passed screen, customized according to arguments'''
    # lb stands for Label Button
    # this function helps shorten code by creating a label and a button in one line of code
    tk.Label(screen1, text="", bg="DarkSlateGray3", height=label_height).pack()
    tk.Button(screen1,text=button_text,command=command, bg="white smoke").pack()

def display(screen1,total_done=0):
    '''Displays all dares and total number of completed dares'''
    dares_table(screen1,"Random",'0') # display a table of all random dares
    if total_done: tk.Label(screen1, text=f"Total done: {done_dares(kind='0')}", fg="green", bg="DarkSlateGray3", font=("calibri",11)).pack()
    dares_table(screen1,"Islamic",'1')
    if total_done: tk.Label(screen1, text=f"Total done: {done_dares(kind='1')}", fg="green", bg="DarkSlateGray3", font=("calibri",11)).pack()
    
def done_dares(kind):
    '''Returns number of completed dares'''
    fh = open('files/log.dat','rb')
    try:
        total_done=0 
        while True:
            rec = pickle.load(fh)
            if rec[3]==kind and rec[0]=='done': # if dare of date_type has been completed:
                total_done+=1
    except:
        fh.close()
    
    return total_done # number of completed dares
    
def dares_table(screen1, kind, dare_type):
    '''Display all dares with proper spacing'''
    dares = get_dares()
    ll(screen1,f"{kind.upper()}:", fg="black")
    if len(dares):
        tk.Label(screen1, text="ID\tDare\t\t\t\tDefault\tCurrent", bg="pink").pack(fill='both', padx=10)
        for i in dares:
            if i[1]==dare_type:
                space=0
                if ' ' in i[2]:
                    space = 1
                tab = "\t"*(4-((len(i[2])-space)//8))
                tk.Label(screen1, text=i[0]+'\t'+i[2]+tab+'     '+i[3]+'\t    '+i[4], bg="DarkSlateGray3", anchor='w').pack(fill='both', padx=(35,0)) # spacing according to length of dare content
    else:
        ll(screen1,"No dares available!")

def get_dares():
    '''Returns list of all dares (records)'''
    fh = open('Files/dares.csv','r')
    read = csv.reader(fh)
    dares = list(read)
    fh.close()
    
    return dares

def get_dare(id_):
    '''Returns dare record with matching id'''
    for dare in get_dares():
        if int(dare[0])==id_:
            return dare

def add_dare(id_=0,kind='0',name='',def_priority=0,cur_priority=0,command=''):
    '''Creates and adds dare record to csv file and to log with passed command'''

    # if entered value for current priority is invalid
    if str(cur_priority).isdigit() != True:
        return f"'{cur_priority}' is not a valid priority"

    fh = open('Files/dares.csv','a', newline='')
    adder = csv.writer(fh)
        
    id_=int(id_)
    if id_==0:
        dares = get_dares()
        last_id=0
        if len(dares):
            for i in dares:
                if int(i[0])>last_id:
                    last_id=int(i[0])
        id_=last_id+1 # value of new id_ number is one more than the last id_ number
    adder.writerow([id_,kind,name,def_priority,cur_priority])
        
    text = "Saved!"
    print(text)
    fh.close()
    
    add_to_log(command=command, id_=id_, kind=kind, name=name)
    
    return text

def remove_dare(id_,p=0,command=''):
    '''
    - Deletes dare by passed id 
    - Returns the record of that dare id
    - Adds record to log with passed command
    '''
    dare = f"Dare ID '{id_}' not found!"
    if not str(id_).isdigit():
        return 0,dare
    if not str(p).isdigit():
        return 0,f"'{p}' is not a valid priority!"
    
    dares = get_dares()
    
    fh = open('Files/dares.csv','w', newline='')
    add_dares = csv.writer(fh)
    
    c=0
    for i in dares:
        if int(i[0])!=int(id_):
            add_dares.writerow(i) # write each row except for the one to be removed
        else:
            c=c+1
            dare = i
    fh.close()
    
    add_to_log(command=command, id_=id_, name=dare[2])
    
    return c,dare

def screen_height(limit):
    '''Returns height calculated according to number of dares'''
    dares = get_dares()
    size = len(list(dares)) # number of dares to be displayed
    final_height=380
    if size>limit: # if number of dares is more than maximum number of dares for height=380:
        extra = ((size-limit)*20) 
        final_height = 380 + extra # add that much extra height
    
    return final_height

def add_to_log(command, id_=0, kind='', name=''):
    '''Creates new record from arguments and adds it to log'''
    f = open('files/log.dat','ab')
    timestamp = str(dt.now())
    log_rec = [command,timestamp,id_,kind,name] # create a record to add in the log
    pickle.dump(log_rec,f)
    f.close()

main_root()