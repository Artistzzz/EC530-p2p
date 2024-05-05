import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from cryptography.fernet import Fernet
import chatDB
from chatDB import User, Message, init_db
import html

class ChatClient:
    def __init__(self, master, engine):
        self.engine = engine
        self.master = master
        master.title("Secure P2P Chat")

        self.text_area = scrolledtext.ScrolledText(master, state='disabled', height=10, width=50)
        self.text_area.grid(row=0, column=0, padx=10, pady=10)

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=0, padx=10, pady=10)

        self.cipher = Fernet(Fernet.generate_key())

        self.setup_network()

    def setup_network(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 8000
        self.s.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        msg = self.msg_entry.get()
        sanitized_msg = html.escape(msg)  # Sanitize input to avoid any injection or XSS
        encrypted_msg = self.cipher.encrypt(sanitized_msg.encode())
        self.s.send(encrypted_msg)
        self.msg_entry.delete(0, tk.END)
        self.display_message("You: " + sanitized_msg)

    def receive_messages(self):
        while True:
            msg = self.s.recv(1024)
            if msg:
                decrypted_msg = self.cipher.decrypt(msg).decode()
                self.display_message("Friend: " + decrypted_msg)

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

def main():
    engine = init_db()
    root = tk.Tk()
    app = ChatClient(root, engine)
    root.mainloop()

if __name__ == "__main__":
    main()