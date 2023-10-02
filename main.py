from tkinter import *
import os
from os import access, listdir
from os.path import isfile, join
from tkinter.font import families
import PIL.Image, PIL.ImageTk, PIL.ImageOps
from tkscrolledframe import ScrolledFrame
import json 

#Universell filbane til mappa hvor alle filene er
base_path = os.path.realpath(os.path.dirname(__file__))

#oppdaterer alt det visuelle i programmet
def reset():
    global main
    main.pack_forget()
    main.destroy()
    gui()

#bytter item color
def left_click(event):
    #kjekker hvilket item som skal oppdateres ved en skjult variabel jeg la inn
    for x in range(1, 43):
        if event.widget['text'] == x:
            nr = x
            break

    grey_img_lst = grey_lst[nr-1]
    color = grey_img_lst[-1]   

    use_lst = grey_img_lst[0]
    use_lst__original_len = grey_img_lst[1]

    if color == 0:
        color = 1

    elif color == 1:
        color = 0

    #skriver data for midlertidlig lagring
    write_lst = [use_lst, use_lst__original_len, color]
    grey_lst[nr-1]= write_lst

    reset()

#bytter item state
def right_click(event):
    for x in range(1, 43):
        if event.widget['text'] == x:
            nr = x
            break

    img_lst = normal_lst[nr-1]
    grey_img_lst = grey_lst[nr-1]
    color = grey_img_lst[-1]   

    use_lst = grey_img_lst[0]
    use_lst__original_len = grey_img_lst[1]

    #dupliserer elementene i lista for å så bli kvitt den første for å bla videre
    failsafe = 0

    if use_lst__original_len == len(use_lst):
        for x in use_lst:
            if failsafe == use_lst__original_len:
                break
            use_lst.append(x)
            failsafe+=1
            

    use_lst.pop(0)

    write_lst = [use_lst, use_lst__original_len, color]
    grey_lst[nr-1]= write_lst

    use_lst = img_lst[0]
    use_lst__original_len = img_lst[1]

   #dupliserer elementene i lista for å så bli kvitt den første for å bla videre gjør det samme for begge listene for at de skal være in sync
    failsafe = 0

    if use_lst__original_len == len(use_lst):
        for x in use_lst:
            if failsafe == use_lst__original_len:
                break
            use_lst.append(x)
            failsafe+=1

    use_lst.pop(0)

    write_lst = [use_lst, use_lst__original_len, color]
    normal_lst[nr-1]= write_lst

    reset()    

#midlertidlig lagring
normal_lst = []
grey_lst = []

done_loc_lst = []

#leser inn data fra img mappene og skriver de til midlertidlig lagring
for x in range(1, 43):
    temp_list1 =[]
    temp_list2 =[]
    path = base_path+ '/img/'+str(x)+'/normal'
    path2 = base_path+ '/img/'+str(x)+'/gray'

    for root, dirs, files in os.walk(os.path.abspath(path)):
        for file in files:
            temp_list1.append((os.path.join(root, file)))

    for root, dirs, files in os.walk(os.path.abspath(path2)):
        for file in files:
            temp_list2.append((os.path.join(root, file)))
#lagrer data i en liste på formen [filbane til bildene, original antall bilder, fargestatus]
    normal_lst.append([temp_list1, len(temp_list1)])
    grey_lst.append([temp_list2, len(temp_list2), 0])

#behandler json data som er skrevet på en smart måte.
def locations():
    with open(base_path+"/data.json", "r") as file:
        data = json.load(file)
#output fra file er en liste med dicts som igjenn inneholder en liste med dicts som er våre locations
#kjekker om du har items som stemmer med krava på area nivå for å så fortsette
    for area in data:
        req = area["req"]
        area_req_met = False
        for options in req:
            req_met = 0
            for items in options:
                if str(items) in inventory:
                    req_met+=1
            if req_met == len(options):
                area_req_met = True
#kjekker om du har items som stemmer med krava på locations nivå
        if area_req_met == True:
            loactions = area["children"]
            for place in loactions:
#vanligse type data passer inn her
                try:
                    req1 = place["req"]
                    place_req_met = False
                    for options in req1:
                        req_met = 0
                        for items in options:
                            if str(items) in inventory:
                                req_met+=1
                        if req_met == len(options):
                            place_req_met = True
                    if place_req_met == True:
                        allredy_in_lst= False
                        allredy_done = False
#kjekker om lacation allere er i lista eller ferdig for å ungå duplikater siden funksjonen vil kjøre hver gang reset() er brukt
                        for x in loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_in_lst = True
                        for x in done_loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_done = True
#data blir lagret i en liste hvor hvert element er [navn på plassen, antallet items den har, og om den er 100% beatable]
                        if allredy_in_lst == False and allredy_done==False:
                            loc_lst.append([place["name"], place["items"], 1])
#data med "sections" element behandles her og litt annledes
                except:
                    sections = place["sections"]
                    place_req_met = 0
                    for room in sections:
                        req1 = room["req"]
                        room_req_met = False
                        for options in req1:
                            req_met = 0
                            for items in options:
                                if str(items) in inventory:
                                    req_met+=1
                            if req_met == len(options):
                                room_req_met = True
                        if room_req_met == True:
                            place_req_met+=1
                    if place_req_met == len(sections):
                        allredy_in_lst= False
                        allredy_done = False
#kjekker om lacation allere er i lista eller ferdig for å ungå duplikater siden funksjonen vil kjøre hver gang reset() 
# er brukt, denne gangen skjekker også om den må erstatte en location som var delvis clearable
                        for x in loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_in_lst = True
                            if x == [place["name"], place["items"], 0]:
                                loc_lst.remove(x)
                        for x in done_loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_done = True
#data blir lagret i en liste hvor hvert element er [navn på plassen, antallet items den har, og om den er 100% beatable]
                        if allredy_in_lst == False and allredy_done==False:
                            loc_lst.append([place["name"], place["items"], 1])

                    elif place_req_met >0:
                        allredy_in_lst= False
                        allredy_done = False
                        for x in loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_in_lst = True
                            if x == [place["name"], place["items"], 0]:
                                allredy_in_lst = True
                        for x in done_loc_lst:
                            if x == [place["name"], place["items"], 1]:
                                allredy_done = True                        
#data blir lagret i en liste hvor hvert element er [navn på plassen, antallet items den har, om den er 100% beatable],
#  denne gangen er den bare delvis beatable
                        if allredy_in_lst == False and allredy_done==False:
                            loc_lst.append([place["name"], place["items"], 0])  

#skriver plassen som du er ferdig med til done_loc_lst
def done(x):
    done_loc_lst.append(x)
    reset()

#sorterer lista etter om plassen er fullt clearable så etter anntall items
def sort_loc():
    global loc_lst
    loc_lst = sorted(loc_lst, key=lambda x: x[1], reverse=True)
    loc_lst = sorted(loc_lst, key=lambda x: x[-1], reverse=True)

#leser av data fra midlertidlig lagring og lager knapper ut fra det
def img(nr, x, y):
    img_lst = normal_lst[nr-1]
    grey_img_lst = grey_lst[nr-1]
    color = grey_img_lst[-1]
    if color == 0:
        use_lst = grey_img_lst[0]
        img1 = PhotoImage(file=use_lst[0])

    else:
        use_lst = img_lst[0]
        img1= PhotoImage(file=use_lst[0])

#legger til en skjult variabel i text elementet for å bruke senere
    btn = Label(item_ui_frame, highlightthickness = 0, bd = 0, text=nr, image=img1)
    btn.grid(column=x, row= y, ipady=1, ipadx=1)
    btn.img= img1
    btn.bind("<Button-1>", left_click)
    btn.bind("<Button-2>", right_click)
    btn.bind("<Button-3>", right_click)

#litt hard coding her for å lage inventory lista som stemmer med navn brukt i json fila
def inventory_calc():
    if grey_lst[0][-1] == 1:
        inventory.append("bow") 

    if grey_lst[2][-1] == 1:
        inventory.append("hookshot")

    if grey_lst[3][-1] == 1:
        inventory.append("mushroom")

    if grey_lst[4][-1] == 1:
        inventory.append("powder")

    if grey_lst[6][-1] == 1:
        if len(normal_lst[6][0]) == normal_lst[6][1]:
            inventory.append("crystal")
        elif len(normal_lst[6][0]) == 2*(normal_lst[6][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[6][0]) == 2*(normal_lst[6][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[7][-1] == 1:
        inventory.append("firerod")

    if grey_lst[8][-1] == 1:
        inventory.append("icerod")     

    if grey_lst[9][-1] == 1:
        if len(normal_lst[9][0]) == normal_lst[9][1]:
            inventory.append("bombos")
        elif len(normal_lst[9][0]) == 2*(normal_lst[9][1])-1:
            inventory.append("bombos")      
            inventory.append("mm_medalion")     
        elif len(normal_lst[9][0]) == 2*(normal_lst[9][1])-2:
            inventory.append("bombos")      
            inventory.append("tr_medalion")  
        else:
            inventory.append("bombos")      
            inventory.append("mm_medalion")
            inventory.append("tr_medalion")   

    if grey_lst[10][-1] == 1:
        if len(normal_lst[10][0]) == normal_lst[10][1]:
            pass
        elif len(normal_lst[10][0]) == 2*(normal_lst[10][1])-1:    
            inventory.append("mm_medalion")     
        elif len(normal_lst[10][0]) == 2*(normal_lst[10][1])-2:    
            inventory.append("tr_medalion")  
        else:   
            inventory.append("mm_medalion")
            inventory.append("tr_medalion")  

    if grey_lst[11][-1] == 1:
        if len(normal_lst[11][0]) == normal_lst[11][1]:
            pass
        elif len(normal_lst[11][0]) == 2*(normal_lst[11][1])-1:    
            inventory.append("mm_medalion")     
        elif len(normal_lst[11][0]) == 2*(normal_lst[11][1])-2:    
            inventory.append("tr_medalion")  
        else:   
            inventory.append("mm_medalion")
            inventory.append("tr_medalion")  

    if grey_lst[13][-1] == 1:
        if len(normal_lst[13][0]) == normal_lst[13][1]:
            inventory.append("crystal")
        elif len(normal_lst[13][0]) == 2*(normal_lst[13][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[13][0]) == 2*(normal_lst[13][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[14][-1] == 1:
        inventory.append("lamp")

    if grey_lst[15][-1] == 1:
        inventory.append("hammer")

    if grey_lst[16][-1] == 1:
        inventory.append("flute")

    if grey_lst[18][-1] == 1:
        inventory.append("book")

    if grey_lst[19][-1] == 1:
        inventory.append("shovel")

    if grey_lst[20][-1] == 1:
        if len(normal_lst[20][0]) == normal_lst[20][1]:
            inventory.append("crystal")
        elif len(normal_lst[20][0]) == 2*(normal_lst[20][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[20][0]) == 2*(normal_lst[20][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[21][-1] == 1:
        inventory.append("bottle")

    if grey_lst[22][-1] == 1:
        inventory.append("redcane")

    if grey_lst[23][-1] == 1:
        inventory.append("bluecane")

    if grey_lst[24][-1] == 1:
        inventory.append("cape")

    if grey_lst[25][-1] == 1:
        inventory.append("mirror")

    if grey_lst[26][-1] == 1:
        inventory.append("moonpearl")

    if grey_lst[27][-1] == 1:
        inventory.append("aga")

    if grey_lst[28][-1] == 1:
        inventory.append("boots")
    
    if grey_lst[29][-1] == 1:
        if len(normal_lst[29][0]) == normal_lst[29][1]:
            inventory.append("glove1")
        else:   
            inventory.append("glove1")
            inventory.append("glove2")

    if grey_lst[30][-1] == 1:
        inventory.append("flippers")

    if grey_lst[31][-1] == 1:
        if len(normal_lst[31][0]) == normal_lst[31][1]:
            inventory.append("sword1")
        else:   
            inventory.append("sword1")
            inventory.append("sword2")

    if grey_lst[35][-1] == 1:
        if len(normal_lst[35][0]) == normal_lst[35][1]:
            inventory.append("crystal")
        elif len(normal_lst[35][0]) == 2*(normal_lst[35][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[35][0]) == 2*(normal_lst[35][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[36][-1] == 1:
        if len(normal_lst[36][0]) == normal_lst[36][1]:
            inventory.append("crystal")
        elif len(normal_lst[36][0]) == 2*(normal_lst[36][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[36][0]) == 2*(normal_lst[36][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[37][-1] == 1:
        if len(normal_lst[37][0]) == normal_lst[37][1]:
            inventory.append("crystal")
        elif len(normal_lst[37][0]) == 2*(normal_lst[37][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[37][0]) == 2*(normal_lst[37][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[38][-1] == 1:
        if len(normal_lst[38][0]) == normal_lst[38][1]:
            inventory.append("crystal")
        elif len(normal_lst[38][0]) == 2*(normal_lst[38][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[38][0]) == 2*(normal_lst[38][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[39][-1] == 1:
        if len(normal_lst[39][0]) == normal_lst[39][1]:
            inventory.append("crystal")
        elif len(normal_lst[39][0]) == 2*(normal_lst[39][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[39][0]) == 2*(normal_lst[39][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[40][-1] == 1:
        if len(normal_lst[40][0]) == normal_lst[40][1]:
            inventory.append("crystal")
        elif len(normal_lst[40][0]) == 2*(normal_lst[40][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[40][0]) == 2*(normal_lst[40][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    if grey_lst[41][-1] == 1:
        if len(normal_lst[41][0]) == normal_lst[41][1]:
            inventory.append("crystal")
        elif len(normal_lst[41][0]) == 2*(normal_lst[41][1])-1:
            inventory.append("good_crystal")        
        elif len(normal_lst[41][0]) == 2*(normal_lst[41][1])-2:
            inventory.append("r_or_b_pendant")
        else:
            inventory.append("g_pendant")

    crystal_count = 0
    good_c_count = 0
    pendant_count = 0
    for x in inventory:
        if x == "crystal" or x == "good_crystal":
            crystal_count+=1
        if x == "good_crystal":
            good_c_count+=1
        if x == "r_or_b_pendant":
            pendant_count+=1

    if crystal_count == 7:
        inventory.append("all_crystals")
    if good_c_count == 2:
        inventory.append("good_crystals")
    if pendant_count == 2:
        inventory.append("r&b_pendant")

def gui():
    global inventory
    inventory = ["None"]

    inventory_calc()

    global loc_lst
    loc_lst = []

    global main
    main = Frame(root)
    main.pack()

    # Lager en ScrolledFrame widget som er en enkel løsning jeg fant på et scrollbar settup
    sf = ScrolledFrame(main,height=300)
    sf.pack(side="top", expand=1, fill="both")

    # binder scrollhjul og piltaster til scroll funskjonaliteten
    sf.bind_arrow_keys(main)
    sf.bind_scroll_wheel(main)

    global loc_list_frame
    loc_list_frame = sf.display_widget(Frame)
    locations()
    sort_loc()
    #lager det visuelle ut fra elementer i loc_lst
    for x in loc_lst:
        if x[-1]==1:
            btn_frame = Frame(loc_list_frame)
            btn_frame.pack(anchor=NW)
            l = Label(btn_frame, text=x[0]+"\nitems: "+ str(x[1]), font='Helvetica 14',  fg="green", width=12)
            l.grid(row=0, column=0)
            done_btn = Button(btn_frame, command=lambda var=x: done(var), text="DONE", highlightthickness = 0, bd = 0, font='Helvetica 16 bold', fg="purple")
            done_btn.grid(row=0, column=1)
        else:
            btn_frame = Frame(loc_list_frame)
            btn_frame.pack(anchor=NW)
            l = Label(btn_frame, text=x[0]+"\nitems: "+ str(x[1]), font='Helvetica 14', fg="grey", width=12)
            l.grid(row=0, column=0)
            done_btn = Button(btn_frame, command=lambda var=x: done(var), text="DONE", highlightthickness = 0, bd = 0, font='Helvetica 16 bold', fg="purple", state=DISABLED)
            done_btn.grid(row=0, column=1)


    global item_ui_frame
    item_ui_frame = Frame(main,)
    item_ui_frame.pack()

#lager inventory settupet
    nr = 1                
    for y in range(6):
        for x in range(7):
            img(nr, x, y)
            nr+=1
    

root = Tk() 
root.title("alttpr tracker")
root.geometry("240x530")

gui()

mainloop()
