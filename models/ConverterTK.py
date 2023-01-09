from tkinter import *
from tkinter import filedialog
from .FileConv import FileConv
import shutil
import os
from tkinter import messagebox

class TKConv():

    def __init__(self):  

        self.window = Tk()
        
        self.window.title('FileConverter') 
        self.window.geometry("500x500")
        self.window.configure(bg="black")
        self.window.minsize(800, 500) 
        self.window.maxsize(800, 500) 

        self.label_file_explorer = Label(self.window, font = ('Arial',30), text = "FileConverter", width = 100, bg='black', fg='white')
        self.button_explore = Button(self.window, text = "Selecionar arquivo", command = self.browseFiles, bg='green', fg='white', width=15)  
        self.button_exit = Button(self.window, text = "Sair", command = exit, bg='green', fg='white', width=15) 
        self.button_conv = Button(self.window, text = "Converter", command = self.start_conversion, bg='green', fg='white', width=15) 
        self.loading = Label(self.window, font = ('Arial',10), text = f"selecionando...", width = 100, fg='white', bg='black')

        self.otpt_label = Label(self.window ,text = "Saída:", fg='white', bg='black').place(relx=0.4, rely=0.40, anchor=CENTER)
        self.otpt = StringVar(self.window)
        self.otpt.set("Selecione...")
        otpt_options = ['xlsx', 'csv']

        self.output = OptionMenu(self.window, self.otpt, *otpt_options)
        
        self.sv_label = Label(self.window ,text = "Salvamento:", fg='white', bg='black').place(relx=0.4, rely=0.50, anchor=CENTER)
        
        self.sv = StringVar(self.window)
        self.sv.set("Selecione...")
        sv_options = ['Uma página', 'Várias páginas', 'Vários arquivos']
        self.save_md = OptionMenu(self.window, self.sv, *sv_options)

        self.rw_label = Label(self.window ,text = "Linhas por arquivo/página:", fg='white', bg='black').place(relx=0.38, rely=0.60, anchor=CENTER)
        self.rows_value = Entry(self.window)

        self.nm_label = Label(self.window ,text = "Nome do arquivo:", fg='white', bg='black').place(relx=0.4, rely=0.70, anchor=CENTER)
        self.nm_value = Entry(self.window)


    def save_file(self, filename):
        file = os.path.abspath(filename)
        dire = filedialog.askdirectory(initialdir = "/",title='Onde deseja salvar o arquivo?')
        shutil.move(file, dire)
        return filename.split('/')[-1]

    def place_start_window(self):  
        self.output.place(relx=0.6, rely=0.40, anchor=CENTER)
        self.save_md.place(relx=0.6, rely=0.50, anchor=CENTER)
        self.rows_value.place(relx=0.6, rely=0.60, anchor=CENTER)
        self.nm_value.place(relx=0.6, rely=0.70, anchor=CENTER)
        self.label_file_explorer.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.button_conv.place(relx=0.40, rely=0.80, anchor=CENTER)
        self.button_exit.place(relx=0.60, rely=0.80, anchor=CENTER)
        self.button_explore.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.window.mainloop() 
    
    def browseFiles(self): 
        self.loading.place(relx=0.5, rely=0.33, anchor=CENTER)

        self.filecontent = filedialog.askopenfile(initialdir = "/", title = "Selecione um arquivo", 
                                            filetypes = (("Arquivo Excel", "*.xlsx*"), 
                                                         ("Arquivo CSV", "*.csv*"),
                                                         ("Todos os arquivos", "*.*"))) 
        
        if self.filecontent == None:
            filename = "Nenhum arquivo"
        else:
            filename = self.filecontent.name

        self.loading.configure(text=f'{filename} selecionado.')
    
    def treat_exception(self, exception):

        if str(exception).startswith("stat: path should be"):
            exception = "Diretório inválido"

        elif str(exception).startswith("sorry, can't convert csv to many pages"):
            exception = "Desculpe, não é possível ter várias páginas em um CSV..."

        elif "row" in str(exception):
            exception = "Número de linhas inválido"

        return exception

    def start_conversion(self):

        self.loading.configure(text='aguarde...')
        self.window.update_idletasks()

        try:
            if self.filecontent != None:
                conv = FileConv(self.filecontent, self.otpt.get(), 'zip', self.nm_value.get(), self.sv.get(), self.rows_value.get())
                if conv != None:
                    
                    conv.remove_zip_dir()
                    conv.create_dataframe()
                    conv.generate_files()
                    response = conv.get_response()
                    sf = self.save_file(response) 
                    
                    if sf:
                        messagebox.showinfo(title="Sucesso!", message=f"O arquivo {sf} foi retornado!")

                    if response != None:         
                        self.loading.configure(text='selecionando...')
                        self.loading.place_forget()

                    else:
                        self.loading.configure(text='selecionando...')
                        self.loading.place_forget()

                else:
                    self.loading.configure(text='selecionando...')
                    self.loading.place_forget()
                    
            else:
                self.loading.configure(text='selecionando...')
                self.loading.place_forget()

        except Exception as ex:
            print(ex)
            ex = self.treat_exception(ex)
            messagebox.showerror("ERROR!", ex)
            self.loading.place_forget()