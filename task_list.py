from tkinter import *
import tkinter.messagebox
import tkinter as tk
import sqlite3


class Main:

    def __init__(self):

        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()

        self.tasks = []

        self.create_table()
        self.createFrame()
        self.createWidget()

    # Create the database table.
    def create_table(self):

        self.c.execute("CREATE TABLE IF NOT EXISTS Tasks1(Unfin_task TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS Tasks2(Fin_task TEXT)")
        self.conn.commit()

    def createFrame(self):

        # Create the frames.
        self.topFrame = Frame(root, bg='#b70101')
        self.topFrame.grid(row=0, column=0, sticky=EW)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.ctrlFrame = Frame(root, bg='#d13434')
        self.ctrlFrame.grid(row=1, column=0, sticky=NSEW)

        self.ctrl_left = Frame(self.ctrlFrame)
        self.ctrl_left.grid(row=0, column=0, sticky=N)
        self.ctrl_right = Frame(self.ctrlFrame)
        self.ctrl_right.grid(row=0, column=1)

        self.ctrl_right.grid_columnconfigure(0, weight=1)
        self.ctrl_right.grid_rowconfigure(0, weight=1)

    def createWidget(self):

        # Top widget information.
        self.title = Label(self.topFrame, text="To-do List", font='Times 25 bold', bg='#b70101', fg='#fff')
        self.title.grid(row=0, column=0, columnspan=2, sticky=W)

        self.btn_addTask = tk.Button(self.topFrame, text="Add Task", width=10, fg='#000', background='#015fb7', highlightbackground='#b70101', command=self.add_task)
        self.btn_addTask.grid(row=1, column=0, sticky=W)

        self.txt_input = Entry(self.topFrame, width=25, bg='white', highlightbackground='#b70101')
        self.txt_input.grid(row=1, column=1)
        self.txt_input.bind('<Return>', self.enter)
        self.txt_input.focus()

        # Center widget left frame information.
        self.btn_delAll = tk.Button(self.ctrl_left, text="Delete", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=self.del_one)
        self.btn_delAll.grid(row=0, column=0)

        self.btn_del_one = tk.Button(self.ctrl_left, text="Delete All", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=self.del_all)
        self.btn_del_one.grid(row=1, column=0)

        self.btn_taskDone = tk.Button(self.ctrl_left, text="Complete", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=self.move_done)
        self.btn_taskDone.grid(row=2, column=0)

        self.btn_showtask = tk.Button(self.ctrl_left, text="Show Finish", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=Complete)
        self.btn_showtask.grid(row=3, column=0)

        self.btn_exit = tk.Button(self.ctrl_left, text="Exit", fg='#000', bg='red', width=10, highlightbackground='#d13434', command=self.endProgam)
        self.btn_exit.grid(row=4, column=0)

        # Center widget right frame information.
        self.lb_tasks = Listbox(self.ctrl_right, width=25, height=10, bg='#FFF', bd=0, highlightbackground='#d13434', selectmode=EXTENDED)
        self.lb_tasks.grid(row=0, column=0, rowspan=10, padx=3)

        # Create the scrollbar.
        self.yscroll = Scrollbar(self.ctrl_right, command=self.lb_tasks.yview, orient=VERTICAL)
        self.yscroll.grid(row=0, column=1, sticky=NS)
        self.lb_tasks.configure(yscrollcommand=self.yscroll.set)
        self.xscroll = Scrollbar(self.ctrl_right, command=self.lb_tasks.xview, orient=HORIZONTAL)
        self.xscroll.grid(row=2, column=0, sticky=EW)
        self.lb_tasks.configure(xscrollcommand=self.xscroll.set)

        self.update_listbox()

    # Create an event for the keyboard's enter button.
    def enter(self, event=None):

        self.add_task()

    # Insert task in to the first table.
    def data_entry(self, task):

        self.c.execute("INSERT INTO Tasks1 VALUES(?)",(task,))
        self.conn.commit()

    # Update the listbox with the task.
    def update_listbox(self):
        self.c.execute('SELECT * FROM Tasks1')
        data = self.c.fetchall()
        self.clear_listbox()
        for A in data:
            self.lb_tasks.insert("end", A)

    # Clear the task from the listbox to enter the list in the table.
    def clear_listbox(self):
        self.lb_tasks.delete(0, "end")

    # Add the task to the listbox.
    def add_task(self):
        self.create_table()
        task = self.txt_input.get()
        if task != "":
            self.tasks.append(task)
            self.data_entry(task)
            self.update_listbox()
        else:
            tkinter.messagebox.showwarning("Warning", "You need to enter a task.")
        self.txt_input.delete(0, "end")

    # Delete all tasks from the database table and the listbox.
    def del_all(self):
        confirmed = tkinter.messagebox.askyesno("Please Confirm", "Do you really want to delete all?")
        if confirmed == True:
            self.c.execute("DELETE FROM Tasks1")
            self.update_listbox()
            self.conn.commit()

    # Delete the selected task from the database table and update the listbox.
    def del_one(self):
        task = self.lb_tasks.get("active")
        self.c.execute("Delete from Tasks1 where Unfin_task = ?",(task))
        self.update_listbox()
        self.conn.commit()

    # Delete completed task from table 1 and insert in table 2.
    def move_done(self):
        task = self.lb_tasks.get("active")
        self.c.execute("Delete from Tasks1 where Unfin_task = ?", (task))
        self.c.execute("INSERT INTO Tasks2 VALUES(?)", (task))
        self.update_listbox()
        self.conn.commit()

    # Exit the application.
    def endProgam(self):
        root.destroy()


class Complete(Main):

    def __init__(self):
        Main.__init__(self)

        self.createWidget()

    def createWidget(self):

        # Top widget information.
        self.title = Label(self.topFrame, text="To-do List", font='Times 25 bold', bg='#b70101', fg='#fff')
        self.title.grid(row=0, column=0, columnspan=2, sticky=W)

        self.btn_addTask = tk.Button(self.topFrame, text="Add Task", width=10, fg='#000', background='#015fb7', highlightbackground='#b70101', state=DISABLED)
        self.btn_addTask.grid(row=1, column=0)

        self.lbl_done = Label(self.topFrame, text="Completed Tasks", font='Times 20 bold', width=20, fg='#fff', background='#b70101', highlightbackground='#b70101')
        self.lbl_done.grid(row=1, column=1)

        # Center widget left frame information.
        self.btn_delAll = tk.Button(self.ctrl_left, text="Delete", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=self.del_two)
        self.btn_delAll.grid(row=0, column=0)

        self.btn_del_one = tk.Button(self.ctrl_left, text="Delete All", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=self.del_all_two)
        self.btn_del_one.grid(row=1, column=0)

        self.btn_taskDone = tk.Button(self.ctrl_left, text="Complete", width=10, fg='#000', background='#b70101', highlightbackground='#b70101', state=DISABLED)
        self.btn_taskDone.grid(row=2, column=0)

        self.btn_showtask = tk.Button(self.ctrl_left, text="Show List", fg='#000', bg='blue', width=10, highlightbackground='#d13434', command=Main)
        self.btn_showtask.grid(row=3, column=0)

        self.btn_exit = tk.Button(self.ctrl_left, text="Exit", fg='#000', bg='red', width=10, highlightbackground='#d13434', command=self.endProgam)
        self.btn_exit.grid(row=4, column=0)

        # Center widget right frame information.
        self.lb_tasks_d = Listbox(self.ctrl_right, width=25, height=10, bg='#FFF', bd=0, highlightbackground='#d13434', selectmode=EXTENDED)
        self.lb_tasks_d.grid(row=0, column=0, rowspan=10, padx=3)

        self.update_listbox2()

    # Update the listbox with the task.
    def update_listbox2(self):
        self.c.execute('SELECT * FROM Tasks2')
        data2 = self.c.fetchall()
        self.clear_listbox2()
        for B in data2:
            self.lb_tasks_d.insert("end", B)
        self.conn.commit()

    # Clear the task from the listbox to enter the list in the table.
    def clear_listbox2(self):
        self.lb_tasks_d.delete(0, "end")

    # Delete the selected task from the database table and update the listbox.
    def del_two(self):
        task = self.lb_tasks_d.get("active")
        self.c.execute("Delete from Tasks2 where Fin_task = ?",(task))
        self.update_listbox2()
        self.conn.commit()

    # Delete all tasks from the database table and the listbox.
    def del_all_two(self):
        confirmed = tkinter.messagebox.askyesno("Please Confirm", "Do you really want to delete all?")
        if confirmed == True:
            self.c.execute("DELETE FROM Tasks2")
            self.update_listbox2()
            self.conn.commit()


if __name__ == '__main__':
    root = Tk()
    root.title("To-do List")
    root.geometry('400x350+0+0')
    root.configure(bg="white")
    Main()
    root.mainloop()
