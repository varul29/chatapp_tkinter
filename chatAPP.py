import requests
from tkinter import *
from tkinter import ttk
import json
import os

firstclick = True
# API_ENDPOINT = " http://127.0.0.1:5001/fetch"

query_data = [
    {
     "query":[
            "teams not connecting",
            "teams asking for password",
            "teams password prompt not showing"
            ],
     "text":"Please wait while we check everything in your pc",
     "file":"teams_issue.ps1"
     },
    {
     "query":[
            "not able to send any email",
            "unable to download the mail",
            "unable to retrieve mail",
            "emails receiving issue",
            "some issue in outlook conecting",
            "mail id not connecting to exchange server",
            "outlook issue",
            "send receive error"
            ],
     "text":"Please wait while we check everything in your pc",
     "file":"outlook_issue.ps1"
     },
    {
     "query":[
            "wallpaper not appearing",
            "internet not working"
            ],
     "text":"Please wait while we check everything in your pc",
     "file":"gp_update.ps1"
     },
    {
    "query":[
        "issue in windows update",
        "issue in update"
        ],
    "text":"Please wait while we check everything in your pc",
    "file":"gp_update.exe"
    },
    {
     "query":[
            "my pc is slow",
            "my laptop is slow",
            "my desktop is slow",
            "my workstation is slow",
            "my system performance is very slow",
            "my PC performance is very slow",
            "my laptop performance is very slow",
            "my desktop performance is very slow",
            "my workstation performance is very slow",
            "my chrome is working slow", 
            "chrome browser hang",
            "site is not opening",
            "browser asking continous password" 
            "net working slow", 
            "internet not working"
            ],
     "text":"Please wait while we check everything in your pc",
     "file":"diskcleanup_temp.ps1"
     },
    {
     "query":["hi"],
     "text":"hey how can i hep you",
     "file":""
    },
    {
     "query":["how are you"],
     "text":"am good how are you, how can i help you",
     "file":""
    },
    {
     "query":["i am still not able to find out the solution"],
     "text":"sorry for it, will surely raise a tikcet so that you will be able to find the solution",
     "file":""
    }
]


def home(data):
    send = {}
    st_get  = data #request.get_json()
    try:
        for i in query_data:
            if st_get["final_chat"] in i["query"]:
                send_data = {"file": i["file"],"text": i["text"]}
        return send_data
    except Exception as e:
        print(e)
        send_data = {"file": "NA","text": "Sorry I am not getting you"}
        return send_data

def on_entry_click(event):
    """function that gets called whenever entry1 is clicked"""        
    global firstclick

    if firstclick: # if this is the first time they clicked it
        firstclick = False
        entry_field.delete(0, "end") # delete all the text in the entry


def receive(get_chat):
    """Handles receiving of messages."""
    # while True:
    try:
        final_chat = {"final_chat":get_chat}
        # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # r = requests.post(url = API_ENDPOINT, data = json.dumps(final_chat), headers= headers).json()
        r = home(final_chat)
        print(r)
        r_text = r['text']
        if r["file"] =='':
            pass
        else:
            r_file = r['file']
            run_file = os.path.join(os.sep,'new_folder',r_file)
            if os.path.isfile(run_file):
                print(True)
                genie_text = 'Genie: '+r_text
                msg_list.insert(END, genie_text)
                import subprocess
                shell_script = 'powershell.exe' + ' ' + run_file
                data = subprocess.call(shell_script, shell=True)
                r_text = r_file + " ran successfully"
            else:
                r_text = "Sorry Diagnostics Scripts are not available"

    except Exception as e:  # Possibly client has left the chat.
        # print(e)
        r_text = "I am afraid there is some issue while accessing to the data"
    return r_text


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    print("This is send: ",type(msg))
    if msg == "{quit}":
        root.quit()
    if msg == "Type your messages here." or msg == "" :
        pass
    else:
        final_msg = "You: " + msg
        msg_list.insert(END, final_msg)
        receive_msg = receive(msg.lower())
        rec_msg = "Genie: " + receive_msg
        msg_list.insert(END, rec_msg)
        my_msg.set("")
    

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

root = Tk()
root.title("Chatapp tkinter")
photo = PhotoImage(file = "Any image file")
root.resizable(0,0)
messages_frame = Frame(root,borderwidth = 5)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=20, width=75, yscrollcommand=scrollbar.set,font=('Arial', 12))
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()
# Create style Object
style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', width = 20, borderwidth=5, focusthickness=3, focuscolor='none')
style.map('TButton', background=[('active','red')])

entry_field = Entry(root, textvariable=my_msg, font=('Arial', 12))
entry_field.bind('<FocusIn>', on_entry_click)
entry_field.bind("<Return>", send)
entry_field.pack(side=LEFT,padx=7, pady=5,ipadx=195, ipady=20)
send_button = Button(root, text="Send", font=('Helvetica', '15'),command=send)
send_button.pack(side=RIGHT,padx=3, pady=5,ipadx=27, ipady=13)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
