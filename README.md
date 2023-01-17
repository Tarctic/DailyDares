# DailyDares
DailyDares is a [tkinter](https://docs.python.org/3/library/tkinter.html)-based GUI app that selects a random challenge from a list of challenges

## Inspiration
I've always had trouble keeping track of all the things I wanted to do and actually doing them. In addition, my indecision made it harder for me to get started on anything. As a solution, I decided to create an app that would help me keep track of all that I wanted to do, challenge me to do them in time and choose the tasks for me. The result was DailyDares.

## Installation instructions
Download the code and open it in your file explorer. Inside the .exe folder, you will find a shortcut to DailyDares application. Open it and use it as you wish!  
For those who want to edit the existing settings before using the app, use the DailyDares.py file. To run this file, you will need python and the following modules - tkinter, csv, random, datetime and pickle (all of these are standard python libraries). Otherwise, it is the same as the app inside the .exe folder.

## Features  

<img width="309" alt="image" src="https://user-images.githubusercontent.com/85291498/212910917-b92116b3-34af-462e-ac89-fca23419a44a.jpg">

- RANDOM / ISLAMIC:
    - Get a random dare from the list of added dares
    - Shows time left to complete dare
    - Decrease priority of a dare by 2 everytime it is chosen
- VIEW CURRENT DARE:
    - Shows the dare to be completed
    - 'Mark as done' button to click after dare has been completed
- OPTIONS:  

  <img width="309" alt="image" src="https://user-images.githubusercontent.com/85291498/212910767-bb8a8721-110d-426e-8994-69256c85b37b.png">

    - VIEW DARES:
        - Shows all dares and their related information
        - Shows count of completed dares
    - CHANGE CURRENT PRIORITY:
        - Enter dare ID to change its current priority
    - CHANGE DEFAULT PRIORITY:
        - Enter dare ID to change its default priority
    - ADD DARE:
        - Enter a dare name, choose a type, enter its default priority
        - Higher the priority, the more likely it is to be chosen
    - REMOVE DARE:
        - Enter dare ID to remove it
    - RESET PRIORITIES:
        - Reset current priorities of all dares to their default priorities

NOTE: Current priorities of all dares are reset to their default priorities every week
