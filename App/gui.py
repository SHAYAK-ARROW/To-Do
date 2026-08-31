import tkinter as tk

# ei vari able amder state  dhore rakhbe  windo na tori kore print scanf call jate na hoy kono bhabei 
#class use na korar jono eta 
window = None
output_box = None
input_box = None
import threading as th

terminal_ready = th.Event()# event  obj ana holo  eta duto th e conction korer  but ki bhabe kaj kore bujhte parchi na
# eta bojha ki  joruri ? na hoyto amra keno lagbe janleo kaj hobe but amat ache clear noi 

def creat_fake_terminal():
    global window, output_box, input_box
    # change korte hobe to tai global 

    window = tk.Tk() # windo bano hoche 
    window.title("ARROW TO-DO MANAGER")# app windo er anme deoya hoche 




# monitor  er size janna hoche 
    scren_w=window.winfo_screenwidth()
    scren_h=window.winfo_screenheight()


# monitor er 70 % size er  windo ana hoche 
    w=int(scren_w*0.7)
    h=int(scren_h*0.7)
    window.geometry(f"{w}x{h}")


# terminal print er jono ekta text area use krochi ar , inpot er jono entryu 
    input_box = tk.Entry(window, bg="black", fg="white", insertbackground="white",font=("Consolas",16))
    # 16 holo size ar fonmt ke tupple dite hoy 
    # box ta  kalo , lkeha ar cursor sada
    # entry shudhu banaei hjoi na oi obj ke bosate hoy windo te 
    # entry wiget take am ekdom niche boa npr adesh dilam ar bolam x axis boro bor choriye dite but y borabor norm,al i tha 
    input_box.pack(side="bottom", fill="x")


# eta hobe text wiget eta scrol eable hote hobe ekhan amra out pout dekhabo
    output_box = tk.Text(window, bg="black", fg="white",font=("Consolas",18))
    # etapo same case  backgrond kalo  lekha sada but eta chage krote chai  noi to clasic terrminal i lagbe 
    output_box.pack(fill="both", expand=True)
    # ekhane order dilam jeno eta ke windo te bosay same case ekhane shudhu bosano holio
    # bole dilam dui dikei jot paro expand kor ar  expand true dilam jate  windo maximize kroleo chirye jay \


# input neoyar function add kora holo
    def enter(event):# vent add koraholo noi to error aschilo
        # text box theke input tana hoche 
        user_text = input_box.get()
        # output box e  print kora hoche kothay print kora hobe na ekdom ses  e tai cursor ke order deoya hoche  end e jete ar tar pore ki print hobe set adicchi
        output_box.insert("end", f"input: {user_text}\n")
        #user er input  ta niyer por clear krolam entry bosx ta 
        
        # ekhane dekho je ahge  output box auo o scrol hochilo na ekho n hobe karon bole c=hci last ta dekhao 
        output_box.see("end")          

        input_box.delete(0, "end")


# enter box er sathe  enter function lin holo
    input_box.bind("<Return>", enter)
    # acha bojha gelo eta holo binf der function return bolte enter key ernam  ota chaple  eter namer function call hobe  ok
    # retuen asole enter key er name 

    terminal_ready.set()
#  eta  event ke embeed kora holo windo te jate jana jay  windo chalu hpolo ki na 
    # winod chau kora holo

    window.mainloop()


creat_fake_terminal()