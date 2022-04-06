from tkinter import *
from tkinter.ttk import Separator
from chat_interface import get_response, bot_name

BG_SOFTBLUE = "#b3b4c4"
BG_COLOR = "#263056"
TEXT_COLOR = "#F8F8FF"

FONT = "Calibri 14"
BOLD_FONT = "Calibri 13 bold"
MINOR_FONT = "Calibri 12"

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        #Head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="** CHATBOT **", font=BOLD_FONT, pady=10)
        head_label.place(relwidth=1)

        # Divisor de fundos
        #line = Label(self.window, width=450, bg=BG_SOFTBLUE)
        #line.place(relwidth=1, rely=0.07, relheight=0.012)

        #Separador
        separator = Separator(self.window, orient="horizontal")
        separator.place(relwidth=1, rely=0.07, relheight=0.012)

        #Textos
        #Variavel de instancia 
        self.text_widget = Text(self.window,width=20, height=2, bg=BG_COLOR, 
                                fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.config(cursor="arrow", state=DISABLED)

        #Scroll
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.98)
        scrollbar.configure(command=self.text_widget.yview)

        #label de baixo
        bottom_label = Label(self.window, bg=BG_SOFTBLUE, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #cAIXA DE TEXTO
        self.msg_entry = Entry(bottom_label, bg="#f8f8ff", fg="black", font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        #Botão
        send_button = Button(bottom_label, text="Enviar", font=MINOR_FONT, width=20, bg=BG_SOFTBLUE,
                            command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    #Presionar tecla enter
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Você")

    def _insert_message(self, msg, sender):
        #Se dar o enter ou clicar no botão e nao tiver nada
        if not msg:
            return
        #Se tiver texto
        self.msg_entry.delete(0, END)
        msgbot = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msgbot)
        self.text_widget.configure(state=DISABLED)
        
        msguser = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msguser)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)

if __name__ == "__main__":
    app = ChatApplication()
    app.run()
