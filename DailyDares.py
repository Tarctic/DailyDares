import tkinter as tk
import csv
import random

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
    - Fonts, button colors, background images
    - convert final to exe (auto-py-to-exe)
    --- serial number for easy deletion/changing
    - back button; change window instead of new windows
    --- buttons instead of typing for random and islamic options
    --- priorities 1,3,5 and -2 every usage
    --- condense code
    --- decrease priority
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
    button3 = tk.Button(root, text = "OPTIONS", command=options, bg="gray20", fg="white", padx=6, pady=6, font="Calibri")
      
    # Display Buttons
    canvas1.create_window( 180, 380, anchor = "nw", window = button1)   
    canvas1.create_window( 295, 380, anchor = "nw", window = button2)
    canvas1.create_window( 235, 460, anchor = "nw", window = button3)
    
    root.mainloop()
    
def random_dare():
    screen1 = screen("Random Dare")
    choose('0', screen1)
    
def islamic():
    screen1 = screen("Islamic")
    choose('1', screen1)
    
def choose(ri, screen1):
    dares = get_dares()
    check_reset(dares, ri)
    
    prior_dares = []
    c = 0
    for d in dares:
        if d[0]==ri:
            c+=1
            prior_dares.extend([(d[3])]*int(d[2]))
    
    if c>0 and len(prior_dares) > 0:
            num = random.choice(prior_dares)
            dare = remove_dare(num)[1]
            name = dare[1]
            dare[2] = int(dare[2]) - 2
            if dare[2]<0:
                dare[2] = 0
            add_dare(*dare[:3])
            
            ll(screen1, "YOUR DARE:", height=4, fg="black")
            ll(screen1, name.upper(), fontsize=20)
            
    else:
        ll(screen1, "No dares available!", height=4, fg="black")
        
def check_reset(dares, ri):
    sum_ri,total_p = 0,0
    for i in dares:
        if i[0]==ri: # NUM -> 0 = RANDOM, 1 = ISLAMIC
            sum_ri += 1 # TOTAL NUMBER OF ALL ISLAMIC OR RANDOM DARES
            total_p += int(i[2]) # TOTAL PRIORITY OF ALL ISLAMIC OR RANDOM DARES
          
    max_p = 5
    max_total_p = sum_ri * max_p
    max_minus = 14 # AFTER 7 PRIORITY POINTS OF RANDOM OR ISLAMIC ARE REDUCED, RESET THOSE BACK TO 5
    if total_p <= (max_total_p - max_minus):
        reset_p(ri, dares)
        
def reset_p(ri, dares, msg=0, screen1=None):
    for d in dares:
        if d[0]==ri:
            name = d[1]
            num = d[3]
            remove_dare(num)
            add_dare(ri,name,5,num)
    
    if msg:
        ll(screen1, "Saved!")

def options():
    screen1 = screen("Options")
#    root.withdraw()
    
    lb(screen1, "View Dares", view, 3)
    lb(screen1, "Change priority", change)
    lb(screen1, "Add Dare", add)
    lb(screen1, "Remove Dare", remove)
    lb(screen1, "Reset priorities", reset)
#    lb(screen1, "BACK", lambda: [root.deiconify(), screen1.destroy()])
    
    return screen1

def view():
    final = screen_height(10)
    screen1 = screen("View Dares", final)
    display(screen1)
    
def change():
    final = screen_height(3)
    screen1 = screen("Change priority", final)
    display(screen1)
    num = tk.StringVar()
    priority = tk.StringVar()
    
    lle(screen1,"Enter dare No.:",num)
    lle(screen1,"Enter new priority:",priority)
    lb(screen1, "Save", lambda: change_p(screen1, num.get(), priority.get()))
    
def change_p(screen1, num, p):
    c, dare = remove_dare(num,p)
    
    text = "Saved!"
    if c==0:
        text = dare
    else:
        dare[2] = p
        text = add_dare(*dare)
    ll(screen1, text)

def add():
    screen1 = screen("Add Dare")
    
    name = tk.StringVar()
    kind = tk.StringVar()
    kind.set(value='0') #temporary
    priority = tk.StringVar()
    
    lle(screen1,"Dare:",name)
    ll(screen1,"Dare Type:",fg="white")
    tk.Radiobutton(screen1, text="Random", variable=kind, value='0').pack(pady=(5,10))
    tk.Radiobutton(screen1, text="Islamic", variable=kind, value='1').pack()
    lle(screen1,"Priority:",priority)
    lb(screen1, "Save", lambda: save(screen1, kind.get().strip(), name.get().strip(), priority.get().strip()))
    
def save(screen1, k,n,p):
    text = add_dare(k,n,p)
    ll(screen1, text)
    
def remove():
    final = screen_height(7)
    screen1 = screen("Remove Dare", final)
    display(screen1)
    num = tk.StringVar()
    
    lle(screen1,"Enter dare No.:",num)
    lb(screen1, "Remove", lambda: delete(screen1, num.get()))
    
def delete(screen1, num):
    c = remove_dare(num)[0]
            
    text="Removed!"
    if c==0:
        text = f"Dare no. '{num}' not found!"
    
    ll(screen1, text)
    
def reset():
    screen1 = screen("Reset priorities")
    lb(screen1, "Random", lambda: reset_p('0', get_dares(), 1, screen1), lheight=4)
    lb(screen1, "Islamic", lambda: reset_p('1', get_dares(), 1, screen1))
    
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

def display(screen1):
    dares_table(screen1,"Random",'0')
    dares_table(screen1,"Islamic",'1')
    
def dares_table(screen1, kind, num):
    dares = get_dares()
    ll(screen1,f"{kind.upper()}:", fg="black")
    tk.Label(screen1, text="No.\tDare\t\t\t\t\tPriority", bg="pink").pack(fill='both', padx=10)
    for i in dares:
            if i[0]==num:
                space=0
                if ' ' in i[1]:
                    space = 1
                tab = "\t"*(5-((len(i[1])-space)//8))
                tk.Label(screen1, text=i[3]+'\t'+i[1]+tab+'     '+i[2], bg="DarkSlateGray3", anchor='w').pack(fill='both', padx=(35,0))


def get_dares():
    fh=open('Files/Dares.csv','r')
    dares=list(csv.reader(fh))
    fh.close()
    
    return dares

def add_dare(k,n,p,num=0):
    fh = open('Files/Dares.csv','a', newline='')
    add_dare = csv.writer(fh)
    
    text = "Saved!"
    status = 1
    
    if k not in ['0','1']:
        if k.lower() == 'random':
            k=0
        elif k.lower() == 'islamic':
            k=1
        else:
            text=f"'{k}' is not a valid entry for dare type"
            status = 0
        
    if str(p).isdigit() != True:
        text = f"'{p}' is not a valid priority"
        status = 0
        
    if status:
        num=int(num)
        if num==0:
            dares = get_dares()
            maxi=0
            for i in dares:
                if int(i[3])>maxi:
                    maxi=int(i[3])
            num=maxi+1
        add_dare.writerow([k,n,p,num])
        
    print(text)
    fh.close()
    return text

def remove_dare(num,p=0):
    dare = f"Dare No. '{num}' not found!"
    if not str(num).isdigit():
        return 0,dare
    if not str(p).isdigit():
        return 0,f"'{p}' is not a valid priority!"
    
    dares = get_dares()
    
    fh = open('Files/Dares.csv','w', newline='')
    add_dares = csv.writer(fh)
    
    c=0
    for i in dares:
        if int(i[3])!=int(num):
            add_dares.writerow(i)
        else:
            c=c+1
            dare = i
    fh.close()
    
    return c,dare

def screen_height(limit):
    dares = get_dares()
    size = len(list(dares))
    final=380
    if size>limit:
        extra = ((size-limit)*20)
        final = 380 + extra
    
    return final

main_root()