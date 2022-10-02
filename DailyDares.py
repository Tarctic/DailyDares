import tkinter as tk
import csv
import random
import pickle
from datetime import timedelta as td
from datetime import datetime as dt
from datetime import time, date

# run once for crispy clarity
# =============================================================================
# import ctypes
# import sys
# 
# if __name__ == "__main__":   
#     if 'win' in sys.platform:
#         ctypes.windll.shcore.SetProcessDpiAwareness(1)
# =============================================================================

'''
To do:
    --- streak
    - calendar for marking days on which dares were done vs not done

    - radio buttons for deletion and changing (using for loop)
    - back button; change window instead of new windows
    - Fonts, button colors, background images
    - convert final to exe (auto-py-to-exe)
    
    --- buttons instead of typing for random and islamic options
    --- priorities 1,3,5 and -2 every usage
    --- condense code
    --- decrease priority
    --- serial number for easy deletion/changing
    --- fix order of columns in csv file
    ( 0 -> 1
      1 -> 2
      2 -> 4
      3 -> 0
      default priority -> 3
      final order: id, kind, dare, default_p, current_p)
    --- option to set default priority
    --- create and use a log file that keeps track of all dares, time at which they're marked as done, reset etc.
    Uses of log file:
        - to know at what date the values were last reset, so that they can be reset again in specified days
        - to know how many total dares we've done, streak
        - to keep a record of all the dares we've done in the past, including deleted ones
    Columns of log file:
        - command (add/remove/c_default/c_current/selected/completed/reset)
        - ID [-reset]
        - Dare name [-reset]
        - timestamp
    --- reset based on days/weeks
    --- separate reset for islamic and random 
    (check_reset only checks last reset, does not check kind) 
    (if islamic is reset on this sunday, random should not be reset along with islamic on next sunday)
    Alternatively, keep weekly reset separate from forced reset. 
    So the log will be checked only for natural resets every week.
    --- add a reset record to empty log files so that check_reset works properly
    --- show current dare and mark as done when done
    --- show time left to complete    
    --- NEW DARE SHOULD NOT BE POSSIBLE TO SELECT WHEN ONE IS CURRENTLY ONGOING (NOT DONE)
    --- total done
'''

root=tk.Tk()
def main_root():
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
    
def random_dare():
    screen1 = screen("Random Dare")
    choose('0', screen1)
    
def islamic():
    screen1 = screen("Islamic")
    choose('1', screen1)
    
def choose(ri, screen1):
    done, done_rec = is_done(k=ri)
    if not done==1:
        dares = get_dares()
        check_reset(dares, ri)
        
        prior_dares = []
        c = 0
        for d in dares:
            if d[1]==ri:
                c+=1
                prior_dares.extend([(d[0])]*int(d[4]))
        
        if c>0 and len(prior_dares) > 0:
                num = random.choice(prior_dares)
                dare = remove_dare(id_=num,comm='selected')[1]
                name = dare[2]
                dare[4] = int(dare[4]) - 2
                if dare[4]<0:
                    dare[4] = 0
                add_dare(*dare,comm="selected")
                
                ll(screen1, "")
                ll(screen1, "YOUR DARE:", height=4, fg="black")
                ll(screen1, name.upper(), fontsize=20)
                ll(screen1, "")
                ll(screen1, text=f"Time left to complete: {time_left(dare)}")
                
        else:
            ll(screen1, "No dares available!", height=4, fg="black")
    
    else:
        ll(screen1, "", height=5)
        ll(screen1, "Please complete current dare first!", fg="black")
        ll(screen1, f"Current dare: {done_rec[4]}", fg="black")
        ll(screen1, "", height=4)
        
        ll(screen1, text=f"Time left to complete: {time_left(get_dare(done_rec[2]))}")
        
def check_reset(dares, ri):
    
    try:
        f=open('files/log.dat','rb')
    except FileNotFoundError: # If no log file:
        add_log(comm='start') # Create log file and add an empty reset record
        last_reset = dt.now()
        f=open('files/log.dat','rb')

    # Note: For the first reset record, the time at which the user clicks for a random dare is set as first reset aka 'start'
    # After that, the next reset will be done after specified number of days (eg: a week)
    start=0 
    try:
        while True:
            rec = pickle.load(f)
            if rec[0]=='start':
                start=1
                last = rec
            if rec[0] == 'reset' and rec[3]==ri:
                last = rec
    except EOFError:
        f.close()
    
    if not start:
        add_log(comm='start')
        last_reset=dt.now()
        
    now = dt.now() # time now
    if start:
        last_reset = dt.strptime(last[1],"%Y-%m-%d %H:%M:%S.%f") # time of last reset
    
    if now > last_reset + td(weeks=1): # if a week has passed since last reset
        reset_p(ri=ri, dares=dares)
        
def reset_p(ri, dares, msg=0, screen1=None):
    for dare in dares:
        if dare[1]==ri:
            id_ = dare[0]
            remove_dare(id_=id_,comm='reset')
            dare[4] = dare[3] # Resetting current priority to default priority
            add_dare(*dare,comm="reset")
    
    if msg:
        ll(screen1, "Saved!")
    
''' 
if random button does both view current dare and select new dare: 
a new dare cannot be chosen until the old one is completed
random button will have to check if a dare has already been selected
and only if not should it show a new dare
this too can go two ways: 1) new dare ONLY on completion 2) refresh on a new day

if another button for viewing current dare, possibly allowing more than one dare at a time
in which case, we have to enter which dare we have completed or use radiobuttons
if only one dare at a time: random button should be disabled or show a go back message
'''
    
def time_left(dare):
    left = str(dt.combine((dt.today() + td(days=1)),time(00,00)) - dt.now())
    print(left)
    hm = left[:5].split(':')
    left_time = f"{int(hm[0])} hours, {int(hm[1])} minutes"
    print(hm)
    return left_time

def view_current():
    screen1 = screen("View Current Dares")
    
    for ri in ["0Random","1Islamic"]:
        ll(screen1, f"{ri[1:]}:", fg="black", height=2)
        
        k = ri[0]
        done, done_rec = is_done(k)
        
        if done == 1: # 'selected' record exists but not 'done' record (today)
            ll(screen1, done_rec[4])
            s,d = screen1, done_rec
            lb(screen1, "Mark as done", lambda s=s, d=d: mark_done(s,d))
        else:
            ll(screen1, "No dare chosen!")

def is_done(k):
    f=open('files/log.dat','rb')
    try:
        id_ = done = 0
        done_rec = []
        while True:
            rec = pickle.load(f)
            rec_time = dt.strptime(rec[1],"%Y-%m-%d %H:%M:%S.%f")
            today = dt.combine(date.today(),time(00,00)) # today at 00:00
            if rec[0]=='selected' and rec_time > today and str(rec[3])==k:
                id_ = rec[2]
                done_rec = rec
                done = 1
            if rec[2] == id_ and rec[0] == 'done' and rec_time > today:
                done = 2 
    except EOFError:
        f.close()
    
    return done, done_rec
            
def mark_done(screen1, rec):
    add_log(comm="done",id_=rec[2],k=rec[3],n=rec[4])
    cong = random.choice(['Good work!','Keep it up!', "Awesome!", "Way to go, buddy!", "COOL!", "WOOHOO!"])
    ll(screen1, cong)
        
def options():
    screen1 = screen("Options")
#    root.withdraw()
    
    lb(screen1, "View Dares", view, 3)
    lb(screen1, "Change Current Priority", lambda: change("current"))
    lb(screen1, "Change Default Priority", lambda: change("default"))
    lb(screen1, "Add Dare", add)
    lb(screen1, "Remove Dare", remove)
    lb(screen1, "Reset Priorities", reset)
#    lb(screen1, "BACK", lambda: [root.deiconify(), screen1.destroy()])
    # maybe use a single window and clear all widgets instead of destroying/hiding windows
    
    return screen1

def view():
    final = screen_height(10)
    screen1 = screen("View Dares", final)
    display(screen1=screen1,view=1)
    
def change(dorc):
    final = screen_height(3)
    screen1 = screen(f"Change {dorc} priority", final)
    display(screen1)
    id_ = tk.StringVar()
    priority = tk.StringVar()
    
    lle(screen1, "Enter dare ID:",id_)
    lle(screen1, f"Enter new {dorc} priority:",priority)
    lb(screen1, "Save", lambda: change_p(screen1, id_.get(), priority.get(), dorc))
    
def change_p(screen1, num, p, dorc):
    
    if dorc == "default":
        dorcnum = 3
    elif dorc == "current":
        dorcnum = 4
    
    comm="c_"+dorc
    c, dare = remove_dare(id_=num,p=p,comm=comm)
    
    text = "Saved!"
    if c==0:
        text = dare
    else:
        dare[dorcnum] = p
        text = add_dare(*dare,comm=comm)
    ll(screen1, text)

def add():
    screen1 = screen("Add Dare")
    
    name = tk.StringVar()
    kind = tk.StringVar()
    kind.set(value='0') #temporary
    default = tk.StringVar()
    
    lle(screen1,"Dare:",name)
    ll(screen1,"Dare Type:",fg="white")
    tk.Radiobutton(screen1, text="Random", variable=kind, value='0').pack(pady=(5,10))
    tk.Radiobutton(screen1, text="Islamic", variable=kind, value='1').pack()
    lle(screen1, "Default Priority:", default)
    lb(screen1, "Save", lambda: save(screen1=screen1, k=kind.get().strip(), n=name.get().strip(), dp=default.get().strip() ))
    
def save(screen1, k,n,dp):
    cp = dp
    text = add_dare(k=k,n=n,dp=dp,cp=cp,comm='add')
    ll(screen1, text)
    
def remove():
    final = screen_height(7)
    screen1 = screen("Remove Dare", final)
    display(screen1)
    id_ = tk.StringVar()
    
    lle(screen1,"Enter dare ID:",id_)
    lb(screen1, "Remove", lambda: delete(screen1, id_.get()))
    
def delete(screen1, id_):
    c = remove_dare(id_,comm='remove')[0]
            
    text="Removed!"
    if c==0:
        text = f"Dare ID '{id_}' not found!"
    
    ll(screen1, text)
    
def reset():
    screen1 = screen("Reset priorities")
    lb(screen1, "Random", lambda: reset_p(ri='0', dares=get_dares(), msg=1, screen1=screen1), lheight=4)
    lb(screen1, "Islamic", lambda: reset_p(ri='1', dares=get_dares(), msg=1, screen1=screen1))
    
    
def screen(title, final=380):
    screen1=tk.Toplevel(root)
    screen1.title(title)
    screen1.geometry(f"400x{final}")
    screen1.configure(bg="DarkSlateGray3")
    screen1.iconbitmap(r'Files/icon.ico')
    
    return screen1

def ll(screen1, text, fontsize=11, height=1, fg="green"):
    tk.Label(screen1,text="",bg="DarkSlateGray3", height=height).pack()
    tk.Label(screen1, text=text, fg=fg, bg="DarkSlateGray3", font=("calibri",fontsize)).pack()

def lle(screen1, text, textv):
    ll(screen1, text, fg="white")
    tk.Entry(screen1, textvariable=textv).pack()
    
def lb(screen1, btext, command, lheight=1):
    tk.Label(screen1, text="", bg="DarkSlateGray3", height=lheight).pack()
    tk.Button(screen1,text=btext,command=command, bg="white smoke").pack()

def display(screen1,view=0):
    dares_table(screen1,"Random",'0')
    if view: ll(screen1, f"Total done: {done_dares('0')}")
    dares_table(screen1,"Islamic",'1')
    if view: ll(screen1, f"Total done: {done_dares('1')}")
    
def done_dares(k):
    fh = open('files/log.dat','rb')
    try:
        c=0
        while True:
            rec = pickle.load(fh)
            if rec[3]==k and rec[0]=='done':
                c+=1
    except:
        fh.close()
    
    return c
    
def dares_table(screen1, kind, ri):
    dares = get_dares()
    ll(screen1,f"{kind.upper()}:", fg="black")
    if len(dares):
        tk.Label(screen1, text="ID\tDare\t\t\t\tDefault\tCurrent", bg="pink").pack(fill='both', padx=10)
        for i in dares:
            if i[1]==ri:
                space=0
                if ' ' in i[2]:
                    space = 1
                tab = "\t"*(4-((len(i[2])-space)//8))
                tk.Label(screen1, text=i[0]+'\t'+i[2]+tab+'     '+i[3]+'\t    '+i[4], bg="DarkSlateGray3", anchor='w').pack(fill='both', padx=(35,0))
    else:
        ll(screen1,"No dares available!")

def get_dares():
    fh = open('Files/dares.csv','r')
    read = csv.reader(fh)
    dares = list(read)
    fh.close()
    
    return dares

def get_dare(id_):
    for dare in get_dares():
        if int(dare[0])==id_:
            return dare

def add_dare(id_=0,k='0',n='',dp=0,cp=0,comm=''):
    fh = open('Files/dares.csv','a', newline='')
    adder = csv.writer(fh)
    
    text = "Saved!"
    status = 1
        
    if str(cp).isdigit() != True:
        text = f"'{cp}' is not a valid priority"
        status = 0
        
    if status:
        id_=int(id_)
        if id_==0:
            dares = get_dares()
            maxi=0
            if len(dares):
                for i in dares:
                    if int(i[0])>maxi:
                        maxi=int(i[0])
            id_=maxi+1
        adder.writerow([id_,k,n,dp,cp])
        
    print(text)
    fh.close()
    
    add_log(comm=comm, id_=id_, k=k, n=n)
    
    return text

def remove_dare(id_,p=0,comm=''):
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
            add_dares.writerow(i)
        else:
            c=c+1
            dare = i
    fh.close()
    
    add_log(comm=comm, id_=id_, n=dare[2])
    
    return c,dare

def screen_height(limit):
    dares = get_dares()
    size = len(list(dares))
    final=380
    if size>limit:
        extra = ((size-limit)*20)
        final = 380 + extra
    
    return final

def add_log(comm, id_=0, k='', n=''):
    f = open('files/log.dat','ab')
    timestamp = str(dt.now())
    log = [comm,timestamp,id_,k,n]
    pickle.dump(log,f)
    f.close()

main_root()