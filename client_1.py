import sys
import time
import tkinter
from socket import *
from threading import Thread
from colorama import Fore

from RSA import RSA


# Maneja el recibimiento de mensajes
def receive():
    msg_list.insert(tkinter.END, "Usuario: %s " % NAME)
    msg_list.insert(tkinter.END, "Conexion exitosa")
    while True:
        try:
            messageR = CLIENT.recv(BUFFER_SIZE).decode("utf8")
            messageR = RSA.deEncrypt(messageR, private_key_1)
            print(Fore.YELLOW, end='')
            print(">" + messageR)
            msg_list.insert(tkinter.END, messageR)
        except OSError:
            break


# Maneja el mandar mensajes
def send():
    messageS = my_msg.get()
    my_msg.set("")
    messageS = NAME + ": " + messageS
    print(Fore.BLUE, end='')
    print(messageS)
    msg_list.insert(tkinter.END, messageS)
    messageS = RSA.encrypt(messageS, public_key_2)
    CLIENT.send(messageS.encode("utf8"))


def on_closing():
    print(Fore.RED + 'Cerrando conexion...')
    time.sleep(1)
    CLIENT.close()
    root.quit()
    sys.exit()


# ----tkinter GUI----
root = tkinter.Tk()
root.title("RSA Chat")
root.resizable(False, False)
root.geometry("450x350+500+180")

messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
msg_list.pack(ipadx=30, ipady=6)
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=my_msg, width=70, bd=3)
entry_field.bind("<Return>", send)
entry_field.pack(ipadx=1, ipady=6, pady=10)
send_button = tkinter.Button(root, text="Send", command=send, width=15, relief="groove")
send_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

# ----SOCKET Part----
HOST = "127.0.0.1"
PORT = 1234
NAME = input('Enter your name: ')
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDRESS)
print(Fore.GREEN + 'Conexion establecida...')

public_key_1, private_key_1 = RSA.generateKeys()
msg = str(public_key_1[0]) + '*' + str(public_key_1[1])
CLIENT.send(bytes(msg, "utf8"))
m = CLIENT.recv(BUFFER_SIZE).decode('utf8')
public_key_2 = [int(x) for x in m.split('*')]

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
