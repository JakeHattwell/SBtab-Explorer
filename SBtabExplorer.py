import os
import time
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import webbrowser
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from resources.sbtabpy import modelSystem
import settings

#from tkinter import ttk


class MainApplication():
    def __init__(self,master):
        #configuring master
        config = {"title":"SBtab Explorer", "version":"[Version: 0.1.0]"}
        self.master = master
        self.tkcss = [
            #light
            {  
                "BASE":"gray80",
                "DARK":"gray90",
                "DARKER":"gray95",
                "LIGHT":"gray75",
                "LIGHTER":"gray35",
                "CURSOR":"black"
            },
            #dark
            {
                "BASE":"gray25",
                "DARK":"gray15",
                "DARKER":"gray10",
                "LIGHT":"gray35",
                "LIGHTER":"gray50",
                "CURSOR":"white"
            }
            ]

        self.cs = self.tkcss[settings.DARK_THEME]
        self.font = ("systemfixed",10)
        self.master.title(config["title"] + " " +config["version"])
        self.master.state("zoomed")
        self.master.update()
        self.info = {} #dictionary to hold the label and button displays
        self.size = {} #dictionary holding sizes of the datasets
        self.displayFields = {} #dict for fields in notebook pages
        self.pages = {} #Dict to hold notebook pages
        self.temp_id = 0 #Temp ID assigned to new entries in tables

        #create menus
        self.menubar = tk.Menu(self.master)
        file_menu = tk.Menu(self.menubar,tearoff=0)
        open_menu = tk.Menu(file_menu,tearoff=0)
        open_menu.add_command(label="Open TSV", command=lambda x = "tsv":self.open_folder(x))
        open_menu.add_command(label="Open XLSX", command=lambda x = "xlsx":self.open_folder(x))
        file_menu.add_cascade(label="Open",menu=open_menu)
        save_menu = tk.Menu(file_menu,tearoff=0)
        save_menu.add_command(label="Save TSV", command= lambda x=False,mode="tsv": self.memory_dump(x,mode))
        save_menu.add_command(label="Save XLSX", command= lambda x=False: self.memory_dump(x))
        file_menu.add_cascade(label="Save",menu=save_menu)
        saveas_menu = tk.Menu(file_menu,tearoff=0)
        saveas_menu.add_command(label="Save As TSV", command= lambda x=True,mode="tsv": self.memory_dump(x,mode))
        saveas_menu.add_command(label="Save As XLSX", command= lambda x=True: self.memory_dump(x))
        file_menu.add_cascade(label="Save As",menu=saveas_menu)
        if settings.EMAIL_SUBMISSION_ENABLED:
            file_menu.add_command(label="Submit",command=self.email_form)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        help_menu = tk.Menu(self.menubar,tearoff=0)
        
        text="""
  Version 1
-----------------------
Created by Jake Hattwell
University of Queensland
"""
        help_menu.add_command(label="About", command=lambda title=" ",msg=text : messagebox.showinfo(title=title,message=msg))
        help_menu.add_command(label="GitHub (opens browser)",command=lambda url="https://github.com/jakehattwell/SBtab-explorer": webbrowser.open_new_tab(url))
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        self.menubar.add_cascade(label="Help",menu=help_menu)
        self.master.config(menu=self.menubar)

        #create notebook layout
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH,expand=True)
        #main display window
        self.window_frame = tk.Frame(self.notebook,bd=2, relief=tk.SUNKEN,bg=self.cs["BASE"])
        self.window_frame.pack(fill=tk.BOTH,expand=True)
        self.window_frame.columnconfigure(0, weight = 3)
        self.window_frame.columnconfigure(1, weight = 1)
        self.window_frame.rowconfigure(0, weight = 1)
        self.window_frame.rowconfigure(1, weight = 1)
        self.notebook.add(self.window_frame,text="Home")
        #main UI window
        self.ui_frame= tk.Frame(self.window_frame, bd=1, relief=tk.SOLID,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"])
        self.ui_frame.grid(row=0,column=0,sticky = "nesw",rowspan=2)

        self.ui_frame.columnconfigure(0,weight=1)
        self.ui_frame.columnconfigure(1,weight=0)
        self.ui_frame.rowconfigure(0,weight=0)
        self.ui_frame.rowconfigure(1,weight=1)

        self.load_prompt = tk.Label(self.ui_frame, text="Use the file menu to load a SBtab folder.",bg=self.cs["LIGHT"],fg=self.cs["CURSOR"])
        self.load_prompt.grid(row=0,column=0, sticky=tk.NE+tk.SW,columnspan=2)

        self.wscrollbar = tk.Scrollbar(self.ui_frame)
        self.wscrollbar.grid(row=1,column=1,sticky="ns")

        self.work_canvas = tk.Canvas(self.ui_frame,bd=2, relief=tk.SUNKEN,yscrollcommand=self.wscrollbar.set,background=self.cs["DARK"],highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"])
        self.work_canvas.config(width=self.ui_frame.winfo_width()-self.wscrollbar.winfo_width(),bg=self.cs["DARK"])
        self.wscrollbar.config(command=self.work_canvas.yview,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],bg=self.cs["LIGHT"],troughcolor=self.cs["DARK"])
        self.work_canvas.configure(scrollregion=self.work_canvas.bbox("all"))
        self.work_canvas.grid(row=1,column=0,sticky = "nesw")
        self.work_frame = tk.Frame(self.work_canvas,bg=self.cs["DARK"])
        self.work_frame.columnconfigure(0,weight=1)
        self.work_canvas.create_window((0,0),window=self.work_frame,anchor='nw')
        self.work_frame.bind("<Configure>", self.on_frame_configure)
        self.work_canvas.bind("<MouseWheel>", lambda event: self.work_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
        self.work_frame.bind("<MouseWheel>", lambda event: self.work_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
        self.tool_frame = tk.Frame(self.window_frame,bd=2,relief=tk.SUNKEN,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],bg=self.cs["BASE"])
        self.tool_frame.grid(row=0,column=1,sticky="nesw")

        self.text_frame = tk.Frame(self.window_frame,bd=2,relief=tk.SUNKEN,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],bg=self.cs["BASE"])
        self.text_frame.grid(row=1,column=1,sticky="nesw")
        self.text_box = tk.Text(self.text_frame,width=20,padx=10,wrap=tk.WORD,bg=self.cs["BASE"],fg=self.cs["CURSOR"],font=self.font)
        self.text_box.grid(row=0,column=0,sticky="nesw")
        self.text_frame.columnconfigure(0, weight = 1)
        self.text_frame.rowconfigure(0, weight = 1)
        self.footer = tk.Frame(self.master,bg=self.cs["LIGHT"],width=0,height=16)
        self.footer.pack(side=tk.LEFT)
        self.placeholder=tk.Frame(self.master,bg=self.cs["LIGHT"],width=self.master.winfo_width(),height=16)
        self.placeholder.pack(side=tk.RIGHT)
        
        

    def open_folder(self,filetype):
        """Opens a folder of SBtab files

        type specified by filetype (tsv/xslx)
        Creates a workspace, and redraws the layout of the program
            """
        self.workspace = modelSystem(self)
        self.folder = tk.filedialog.askdirectory()
        success = self.workspace.load_folder(self.folder,filetype)
        if success:
            self.load_prompt.destroy()
            self.search_frame = tk.Frame(self.ui_frame,bd=2,relief=tk.SUNKEN,highlightcolor=self.cs["DARKER"],bg=self.cs["LIGHT"])
            search_var = tk.StringVar()
            self.search_box = tk.Entry(self.search_frame,textvariable=search_var,bg=self.cs["DARK"],fg=self.cs["CURSOR"],insertbackground=self.cs["CURSOR"])
            search_var.set("Search Text")
            self.search_box.bind('<FocusIn>', self.on_entry_click)
            self.search_box.bind('<FocusOut>', self.on_focusout)
            self.search_box.bind('<Return>', self.search_model_data)
            self.search_box.grid(row = 0,column=1,sticky = "nesw")
            self.search_label = tk.Label(self.search_frame,text="Type and press enter to search",bg=self.cs["LIGHT"],fg=self.cs["CURSOR"])
            self.search_label.grid(row=0,column=2,sticky="nesw")
            
            self.tools_button = tk.Menubutton(self.search_frame,text="Tools",bg=self.cs["BASE"],fg=self.cs["CURSOR"],relief="raised")
            self.tools_menu = tk.Menu(self.tools_button,tearoff=0)
            self.new_menu = tk.Menu(self.tools_menu,tearoff=0)

            for i in self.workspace.tables:
                self.new_menu.add_cascade(label=i,command=lambda x = i:self.new_entry(x))

            self.tools_menu.add_cascade(label="New",menu=self.new_menu)
            self.tools_button.config(menu=self.tools_menu)
            self.tools_button.grid(row=0,column=0,sticky="nesw")

            self.search_frame.columnconfigure(0,weight=0)
            self.search_frame.columnconfigure(1,weight=3)
            self.search_frame.columnconfigure(2,weight=1)
            self.search_frame.grid(row=0,sticky="nesw",columnspan=2)
            self.ui_frame.rowconfigure(0,weight=0)
            self.size = self.workspace.size
            self.size_text = "\n".join([str(key)+": "+str(val)+" entries" for key,val in self.size.items()])
            self.size_text = "\n".join(["Dataset has been loaded!",self.size_text])
            messagebox.showinfo(" ",self.size_text)
            self.footer.config(width=0,bg=self.cs["LIGHT"])
            self.placeholder.config(bg=self.cs["LIGHT"],width=self.master.winfo_width(),height=16)
            
            self.master.focus_set()

    def print_out(self,text):
        self.text_box.config(state=tk.NORMAL)
        if self.text_box.get("1.0",tk.END) != "":
            self.text_box.insert(tk.END,"\n")
        self.text_box.insert(tk.END,text)
        self.text_box.see(tk.END)
        self.text_box.config(state=tk.DISABLED)
        self.master.update()

    def on_entry_click(self,event):
        if self.search_box.get() == "Search Text":
            self.search_box.delete(0, "end") # delete all the text in the entry
            self.search_box.insert(0, '') #Insert blank for user input      
            self.search_box.config(fg = self.cs["CURSOR"])      

    def on_focusout(self,event):
        if self.search_box.get() == '':
            self.search_box.insert(0, 'Search Text')
        if settings.DARK_THEME:
            self.search_box.config(fg = self.cs["BASE"])
        else:
            self.search_box.config(fg = self.cs["LIGHTER"])

    def search_model_data(self,event=None):

        if self.search_box.get() != '':
            query = self.search_box.get()
            results = self.workspace.searchModel(query)
            self.work_frame.columnconfigure(0,weight=0)
            self.work_frame.columnconfigure(1,weight=1)
            row = 0
            
            for key,value in self.info.items():
                try:
                    value.destroy()
                except:
                    key = key
                    pass
            self.info = {}

            for key,result in results.items():
                text = self.workspace.prettyPrint([result[0],result[1]])
                self.info["key"+str(row)+"L"] = tk.Label(self.work_frame,font=self.font,text=text,bd=2,relief="raised", justify="left",anchor="w",bg=self.cs["DARK"],fg=self.cs["CURSOR"],padx=10,pady=5)
                self.info["key"+str(row)+"L"].grid(row = row,column = 1,sticky="nesw",columnspan=1)
                self.info["key"+str(row)+"L"].bind("<MouseWheel>", lambda event: self.work_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                self.info["key"+str(row)+"B"] = tk.Button(self.work_frame,font=self.font,padx=10,text = "Open",justify="center",bd=2,relief="raised",anchor="e",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = lambda result=result:self.display_data(result)) #
                self.info["key"+str(row)+"B"].grid(row = row,column = 0,sticky="nesw")
                self.info["key"+str(row)+"B"].bind("<MouseWheel>", lambda event: self.work_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                self.info["key"+str(row)+"D"] = result[5]
                row += 1

        self.master.update()

    def new_entry(self,entry_type): ###JUMP TEXT
        temp_id = "["+str(self.temp_id)+"] New " + entry_type
        table = entry_type
        self.pages[temp_id] = tk.Frame(self.notebook)
        self.pages[temp_id].config(bg=self.cs["DARK"])
        headers = self.workspace.tables[table].headers
        window_text=temp_id
        self.pages[temp_id].columnconfigure(0,weight=3)
        self.pages[temp_id].headers = headers
        self.pages[temp_id].rowconfigure(0,weight=3)
        self.pages[temp_id].columnconfigure(1,weight=2)
        self.displayFields[window_text]={}
        self.notebook.add(self.pages[temp_id],text=window_text,sticky="nesw")
        row=0
        info_frame = tk.Frame(self.pages[temp_id],bg=self.cs["DARK"])
        info_frame.grid(row=0,column=0,sticky="NESW")
        info_frame.columnconfigure(1,weight=1)

        row += 1

        row += 1
        # create fields
        for header in headers:
            fieldLabel = tk.Label(info_frame,text=header,justify="left",bg=self.cs["BASE"],fg=self.cs["CURSOR"],padx=5)
            fieldLabel.grid(row=row,column=0,sticky="NESW")
            text = tk.StringVar()
            self.displayFields[window_text][header] = tk.Entry(info_frame,textvariable=text,bg=self.cs["DARK"],fg=self.cs["CURSOR"],disabledbackground=self.cs["DARK"],insertbackground=self.cs["CURSOR"])
            text.set("")
            self.displayFields[window_text][header].grid(row=row,column=1,sticky="NESW")
            
            row += 1
        info_frame.rowconfigure(row,weight=10)
        btn1 = tk.Button(info_frame,text="Save and Continue",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = lambda new=True,table=table:self.save_data(new=new,table=table)) #Buttons at top of window
        btn1.grid(row=0,column=0,sticky="nesw",columnspan=2)
        btn2 = tk.Button(info_frame,text="Exit",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = self.delete_tab)
        btn2.grid(row=1,column=0,sticky="nesw",columnspan=2)
        row += 1
        print("Created new",entry_type) #traceback for sanity check
        self.temp_id += 1
        self.notebook.select(self.notebook.index("end")-1)
        #results["-".join([table,ID])] = [table,ID,key,str(val),str(row),entry]
        
 
    def display_data(self,data,jump=False):
        #check if tab already open
        if data[1] in self.pages:
            q = messagebox.askquestion(" ","Entry already open! Did you want to jump to the tab?",icon = 'warning')
            if q == 'yes':    
                for i in self.notebook.tabs():
                    if self.notebook.tab(i,"text")==data[1]:
                        selection = i
                self.notebook.select(selection)
        else:
            self.pages[data[1]] = tk.Frame(self.notebook)
            self.pages[data[1]].config(bg=self.cs["DARK"])
            self.pages[data[1]].data=data
            window_text=data[1]
            self.pages[data[1]].columnconfigure(0,weight=3)
            self.pages[data[1]].rowconfigure(0,weight=3)
            self.pages[data[1]].columnconfigure(1,weight=2)
            self.displayFields[window_text]={}
            self.notebook.add(self.pages[data[1]],text=window_text,sticky="nesw")
            row=0
            info_frame = tk.Frame(self.pages[data[1]],bg=self.cs["DARK"])
            info_frame.grid(row=0,column=0,sticky="NESW")
            info_frame.columnconfigure(1,weight=1)
            btn1 = tk.Button(info_frame,text="Save and Continue",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = self.save_data) #
            btn1.grid(row=row,column=0,sticky="nesw",columnspan=2)
            row += 1
            # btn2 = tk.Button(window,text="Save and Close") #,command = self.saveAndClose
            # btn2.grid(row=row,column=0,sticky="nesw")
            # row += 1
            btn2 = tk.Button(info_frame,text="Exit",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = self.delete_tab)
            btn2.grid(row=row,column=0,sticky="nesw",columnspan=2)
            row += 1
            for key,val in data[5].items():
                if key != None:
                    title = key.capitalize()
                fieldLabel = tk.Label(info_frame,text=title,justify="left",bg=self.cs["BASE"],fg=self.cs["CURSOR"],padx=5)
                fieldLabel.grid(row=row,column=0,sticky="NESW")
                text = tk.StringVar()
                self.displayFields[window_text][key] = tk.Entry(info_frame,textvariable=text,bg=self.cs["DARK"],fg=self.cs["CURSOR"],disabledbackground=self.cs["DARK"],insertbackground=self.cs["CURSOR"])
                text.set(val)
                if title == "!id":
                    self.displayFields[window_text][key].config(state='disabled')
                self.displayFields[window_text][key].grid(row=row,column=1,sticky="NESW")
                
                row += 1
            info_frame.rowconfigure(row,weight=10)
            row += 1
            
            
            linker_frame = tk.Frame(self.pages[data[1]])
            linker_frame.grid(row=0,column=1,sticky="NESW",rowspan = len(data[5])+3) #rowspan makes it match the buttons
            self.pages[data[1]].rowconfigure(len(data[5])+3,weight=1)
            linker_frame.columnconfigure(0,weight=1)
            linker_frame.rowconfigure(0,weight=1)


            tempwscrollbar = tk.Scrollbar(linker_frame)
            tempwscrollbar.grid(row=0,column=1,sticky="ns")
            tempwscrollbarx = tk.Scrollbar(linker_frame,orient="horizontal")
            tempwscrollbarx.grid(row=1,column=0,sticky="ew")
        #
            tempwork_canvas = tk.Canvas(linker_frame,bd=2, relief=tk.SUNKEN,background=self.cs["DARK"],highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],yscrollcommand=tempwscrollbar.set,xscrollcommand=tempwscrollbarx.set)
            tempwork_canvas.config(width=linker_frame.winfo_width()-tempwscrollbar.winfo_width(),height=linker_frame.winfo_height()-tempwscrollbar.winfo_height(),bg=self.cs["DARK"])

            tempwscrollbar.config(command=tempwork_canvas.yview,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],bg=self.cs["LIGHT"],troughcolor=self.cs["DARK"])
            tempwscrollbarx.config(command=tempwork_canvas.xview,highlightbackground=self.cs["LIGHT"],highlightcolor=self.cs["DARKER"],bg=self.cs["LIGHT"],troughcolor=self.cs["DARK"])
            
            tempwork_canvas.grid(row=0,column=0,sticky = "nesw")
            tempwork_frame = tk.Frame(tempwork_canvas,bg=self.cs["DARK"])
            tempwork_frame.columnconfigure(0,weight=1)
            tempwork_frame.rowconfigure(0,weight=1)
            tempwork_canvas.create_window((0,0),window=tempwork_frame,anchor='nw')
            tempwork_canvas.bind("<MouseWheel>", lambda event: tempwork_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
            tempwork_canvas.bind("<Configure>",lambda event: tempwork_canvas.configure(scrollregion=tempwork_canvas.bbox("all")))

            query = data[1]
            if len(query) > 1:
                results = self.workspace.searchModel(query)
                row = 0
                self.pages[data[1]+"data"] = {}
                for key,result in results.items():
                    text = self.workspace.prettyPrint([result[0],result[1]])
                    self.pages[data[1]+"data"]["key"+str(row)+"L"] = tk.Label(tempwork_frame,font=self.font,text=text,bd=2,relief="raised", justify="left",anchor="w",bg=self.cs["DARK"],fg=self.cs["CURSOR"],padx=10,pady=5)
                    self.pages[data[1]+"data"]["key"+str(row)+"L"].grid(row = row,column = 1,sticky="nesw",columnspan=1)
                    self.pages[data[1]+"data"]["key"+str(row)+"L"].bind("<MouseWheel>", lambda event: tempwork_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                    self.pages[data[1]+"data"]["key"+str(row)+"B"] = tk.Button(tempwork_frame,font=self.font,padx=10,text = "Open",justify="center",bd=2,relief="raised",anchor="e",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = lambda result=result:self.display_data(result)) #
                    self.pages[data[1]+"data"]["key"+str(row)+"B"].grid(row = row,column = 0,sticky="nesw")
                    self.pages[data[1]+"data"]["key"+str(row)+"B"].bind("<MouseWheel>", lambda event: tempwork_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                    self.pages[data[1]+"data"]["key"+str(row)+"D"] = result[5]
                    row += 1
                if data[0] == "Reaction":
                    rxn  = data[5]["!ReactionFormula"]
                    for i in ["+","<","=",">"]:
                        rxn = rxn.replace(i,"")
                    rxn = rxn.split(" ")
                    while "" in rxn:
                        rxn.remove("")
                    for i in rxn:
                        try:
                            results = self.workspace.tables["Compound"].data[i]
                            result = ["Compound",i,"","","",results]
                            if results["!ID"] == i and "key"+results["!ID"]+"D" not in self.pages[data[1]+"data"]:
                                text = self.workspace.prettyPrint(["Compound",results["!ID"]])
                                self.pages[data[1]+"data"]["key"+str(row)+"mL"] = tk.Label(tempwork_frame,font=self.font,text=text,bd=2,relief="raised", justify="left",anchor="w",bg=self.cs["DARK"],fg=self.cs["CURSOR"],padx=10,pady=5)
                                self.pages[data[1]+"data"]["key"+str(row)+"mL"].grid(row = row,column = 1,sticky="nesw",columnspan=1)
                                self.pages[data[1]+"data"]["key"+str(row)+"mL"].bind("<MouseWheel>", lambda event: tempwork_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                                self.pages[data[1]+"data"]["key"+str(row)+"mB"] = tk.Button(tempwork_frame,font=self.font,padx=10,text = "Open",justify="center",bd=2,relief="raised",anchor="e",fg=self.cs["CURSOR"],bg=self.cs["LIGHT"],command = lambda result=result:self.display_data(result)) #
                                self.pages[data[1]+"data"]["key"+str(row)+"mB"].grid(row = row,column = 0,sticky="nesw")
                                self.pages[data[1]+"data"]["key"+str(row)+"mB"].bind("<MouseWheel>", lambda event: tempwork_canvas.yview_scroll(int(-1*(event.delta/90)), "units"))
                                self.pages[data[1]+"data"]["key"+str(row)+"mD"] = result[5]
                                row += 1
                        except:
                            pass
            if jump:
                self.delete_tab()
            self.master.update()
            
            self.notebook.select(self.notebook.index("end")-1)
            

    def save_data(self,new=False,table=False): ###JUMP TEXT
        if new:
            headers = self.pages[self.notebook.tab(self.notebook.select(),"text")].headers
            idkey = self.displayFields[self.notebook.tab(self.notebook.select(),"text")][headers[0]].get()
            if idkey not in self.workspace.tables[table].data:
                self.workspace.tables[table].data[idkey] = {}
                for header in headers:
                    self.workspace.tables[table].data[idkey][header] = self.displayFields[self.notebook.tab(self.notebook.select(),"text")][header].get()
                package = [table,idkey,0,0,0,self.workspace.tables[table].data[idkey]]
                self.display_data(package,jump=True)
                self.notebook.select(self.notebook.index("end")-1)
                messagebox.showinfo(" ","Saved!\nMake sure you save using the File Menu as well.")
            else:
                messagebox.showinfo(" ","ID already exists. Please use another.")
        else:
            for key in self.pages[self.notebook.tab(self.notebook.select(),"text")].data[5]:
                # don't ask.
                self.workspace.tables[self.pages[self.notebook.tab(self.notebook.select(),"text")].data[0]].data[self.pages[self.notebook.tab(self.notebook.select(),"text")].data[1]][key] = self.displayFields[self.pages[self.notebook.tab(self.notebook.select(),"text")].data[1]][key].get()
            messagebox.showinfo(" ","Saved!\nMake sure you save using the File Menu as well.")

        
    def delete_tab(self):
        name=self.notebook.tab(self.notebook.select(),"text")
        for child in self.pages[self.notebook.tab(self.notebook.select(),"text")].winfo_children():
            child.destroy()
        self.notebook.forget(self.notebook.select())
        self.pages.pop(name)
    
    def email_form(self):
        def _submit():
            responses = [objects[i+"E"].get(1.0,tk.END) for i in attribs]
            recipient = settings.EMAIL_SUBMISSION_ADDRESS
            subject = '[Curation Submission]'

            body = """Please attach the files to this email\n----------------------------------------------------"""

            text = "".join([attribs[i]+": " + responses[i] for i in range(len(responses))])
            body = body + "\n\n" + text

            body = body.replace(' ', '%20').replace("\n","%0D%0A")

            webbrowser.open('mailto:' + recipient + '&subject=' + subject + '&body=' + body, new=1)

        def focusNext(widget):
            widget.tk_focusNext().focus_set()
            return 'break'
            
        config = {"title":" ", "version":"[Version: 0.1.0]"}
        popup = tk.Toplevel()
        popup.title(config["title"] + " " +config["version"])
        popup.focus_set()
        data_frame = tk.Frame(popup,bg=self.cs["DARK"])
        data_frame.pack(fill=tk.BOTH,expand=True)
        data_frame.columnconfigure(0,weight=1)
        data_frame.columnconfigure(1,weight=3)
        info_label = tk.Label(data_frame,bg=self.cs["DARK"],fg=self.cs["CURSOR"],text="Enter your details")
        info_label.grid(row=0,column=0,columnspan=2)
        
        objects = {}
        attribs = ["Name","Institution","Curator ID","Email Address","Summary of changes"]
        row=1
        for i in attribs:
            objects[i+"L"] = tk.Label(data_frame,text=i,bg=self.cs["BASE"],fg=self.cs["CURSOR"],font=self.font)
            objects[i+"L"].grid(column=0,row=row,sticky="nesw")
            if i == "Summary of changes":
                objects[i+"E"] = ScrolledText(data_frame,bg=self.cs["BASE"],fg=self.cs["CURSOR"],height=10,font=self.font,insertbackground=self.cs["CURSOR"])
            else:
                objects[i+"E"] = tk.Text(data_frame,bg=self.cs["BASE"],fg=self.cs["CURSOR"],height=1,font=self.font,insertbackground=self.cs["CURSOR"])
            
            objects[i+"E"].grid(column=1,row=row,sticky="nesw")
            objects[i+"E"].bind('<Tab>', lambda e, t=objects[i+"E"]: focusNext(t))        
            row += 1
        submit_button = tk.Button(data_frame,text="Submit",bg=self.cs["LIGHT"],fg=self.cs["CURSOR"],font=self.font,command=_submit)
        submit_button.grid(column=0,row=row,columnspan=2,sticky="nesw")



    def memory_dump(self,saveAs = False,mode="xlsx"):
        if saveAs:
            try:
                self.folder = tk.filedialog.askdirectory()
            except:
                pass

        files = len(self.workspace.tables)
        count = 1
        
        for tablename,val in self.workspace.tables.items():
            if mode == "xlsx":
                val.save_to_excel(self.folder + "\\"+tablename)
            elif mode == "tsv":
                val.save_to_tsv(self.folder + "\\"+tablename)
            self.footer.config(width=self.master.winfo_width()*count/files,bg="green2")
            self.placeholder.config(width=self.master.winfo_width()*(files-count)/files)
            self.master.update()
            self.master.update_idletasks()
            time.sleep(0.05)
            count+=1
        messagebox.showinfo(" ","Saved!")
        self.footer.config(width=0,bg=self.cs["LIGHT"])
        self.placeholder.config(bg=self.cs["LIGHT"],width=self.master.winfo_width(),height=16)
        self.print_out("------------------------")
        text = "Saved to " + self.folder + " in ." + mode + " format"
        self.print_out(text)

    def _on_mousewheel(self, event):
        self.work_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.work_canvas.configure(scrollregion=self.work_canvas.bbox("all"))

root = tk.Tk()
myApp = MainApplication(root)
root.mainloop()
