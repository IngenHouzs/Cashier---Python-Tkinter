
from configparser import SectionProxy
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Tcl 
from tkinter import messagebox
from typing import ItemsView

from matplotlib.pyplot import draw_if_interactive, fill, get, text
from mysql.connector.constants import TLS_CIPHER_SUITES 
from mysql.connector import Error
from mysql.connector.errors import InternalError
import database
from PIL import Image, ImageTk
import mysql.connector as mysql 
import weakref 
import database

import random
import re
import datetime


# Creating Login Menu
display_login = tk.Tk()
display_login.title('MyCashier - by IngenHouzs')
display_login.geometry('400x300')

width = display_login.winfo_screenwidth()
height = display_login.winfo_screenheight()   

transaction_code_listings = []

total_charge = 0 


def login_menu():
    # Functionality
    def login():
        if username_input.get() == database.admin["user_name"] and password_input.get() == database.admin['password']:
            login_rect.destroy()
            login_frame1.destroy()
            admin_dashboard()
        else:
            login_rect.create_text(
                230, 200, text='Incorrect username and / or password.', font=('Trebuchet', '9'), fill='red')

    # Initialize Stuffs
    login_frame1 = ttk.Frame(display_login)
    login_rect = tk.Canvas(login_frame1, height=300,
                           width=400, background='#c2c2c2')

    username_input = ttk.Entry()

    password_input = ttk.Entry(show='*')

    login_button = ttk.Button(login_rect, text='Log In', command=login)
    quit_button = ttk.Button(login_rect, text='Quit',
                             command=display_login.quit)

    # Layout Manager
    login_frame1.pack()

    login_rect.pack()

    login_rect.create_rectangle(400, 0, 400, 400, fill='white')

    login_rect.create_text(200, 30, text='ADMIN LOGIN',
                           font=('Trebuchet', '20'))

    login_rect.create_line(5, 60, 395, 60, fill='black')

    login_rect.create_text(70, 90, text='USERNAME :', font=('Trebuchet', '11'))
    login_rect.create_text(70, 160, text="PASSWORD :",
                           font=('Trebuchet', '11'))

    login_rect.create_window(
        250, 90, window=username_input, height=40, width=250)
    login_rect.create_window(
        250, 160, window=password_input, height=40, width=250)

    login_rect.create_window(
        340, 230, window=login_button, height=30, width=70)

    login_rect.create_window(250, 230, window=quit_button, height=30, width=70) 
    display_login.resizable(False, False)

    # Run the Login Menu
    display_login.mainloop()

def cancel_transaction():
    display_login.destroy()
    admin_dashboard()

def admin_dashboard(): 
    database.dtbs_cursor = database.dtbs.cursor()
    try:
        with open(r'Cashier SQL\GeneralTransaction Query.sql', 'r') as file_runner:
            general_transaction_sqlrunner = file_runner.read().split(';')
            for commands in general_transaction_sqlrunner:
                if str(commands) == '':
                    continue 
                database.dtbs_cursor.execute(str(commands))
    except:
        pass

    # Functionality
    def add_new_transaction():
        dashboard_frame.destroy()
        dashboard_rect.destroy()
        transaction()

    def view_database():
        pass 

    def logout():
        dashboard_frame.destroy()
        dashboard_rect.destroy() 
        login_menu()

    # Functionality

    # Initialize Stuffs
    dashboard_frame = ttk.Frame(display_login)
    dashboard_rect = tk.Canvas(
        dashboard_frame, height=300, width=400, background='#c2c2c2')

    plus_img = Image.open(r'plus.png')
    plus_img_resize = plus_img.resize((30, 30))
    database_img = Image.open(r'server.png')
    database_img_resize = database_img.resize((30, 30)) 

    plus_img_packer = ImageTk.PhotoImage(plus_img_resize)
    database_img_packer = ImageTk.PhotoImage(database_img_resize)

    add_transaction = tk.Button(dashboard_frame, text='New Transaction',
                                height=3, width=30, bd=3, command=add_new_transaction)
    db_view_button = tk.Button(
        dashboard_frame, text='View Database\nCOMING SOON!', height=3, width=30, bd=3, command=view_database)
    log_out_button = ttk.Button(
        dashboard_frame, text='Log Out', command=logout)

    # Layout Manager
    dashboard_frame.pack()
    dashboard_rect.pack()

    dashboard_rect.create_text(
        55, 20, text=f"USER : {database.admin['user_name']}")
    dashboard_rect.create_line(5, 30, 395, 30, fill='black')

    dashboard_rect.create_rectangle(20, 44, 70, 90, fill='#a6a6a6')
    dashboard_rect.create_rectangle(22, 45, 68, 88, fill='#c2c2c2')
    dashboard_rect.create_image(45, 66, image=plus_img_packer)
    dashboard_rect.create_rectangle(80, 40, 300, 90)
    dashboard_rect.create_window(190, 68, window=add_transaction)

    dashboard_rect.create_rectangle(20, 104, 70, 150, fill='#a6a6a6')
    dashboard_rect.create_rectangle(22, 105, 68, 148, fill='#c2c2c2')
    dashboard_rect.create_image(45, 126, image=database_img_packer)
    dashboard_rect.create_rectangle(80, 100, 300, 150)
    dashboard_rect.create_window(190, 128, window=db_view_button)

    dashboard_rect.create_window(300, 200, window=log_out_button)  
    display_login.resizable(False, False)

    display_login.mainloop()


def transaction():   
    global loopingfunc_status 
    global itemEdit     
    global transaction_code_listings 
    database.dtbs_cursor = database.dtbs.cursor()
    database.dtbs_cursor.execute('SELECT `TransactionCode` FROM `general transaction`;')
    transaction_code_listings = list(database.dtbs_cursor.fetchall())   
    display_login.geometry('%sx%s' % (width, height))
    display_login.resizable(True, True)  
    loopingfunc_status = 1  
    trans_code = 0 
    fixed_trans_code = None 
    len_tcode = 12

    while True:
        fixed_trans_code = ['0' for i in range(len_tcode - len(str(trans_code)))] 
        fixed_trans_code = ''.join(fixed_trans_code) + str(trans_code)
        try:
            if (str(fixed_trans_code)) in transaction_code_listings[trans_code]: 
                fixed_trans_code = '' 
                trans_code += 1
                continue  
        except IndexError:
            break
        break

    # OOP for Cart Edits 

    class itemEdit: 
        global total_price 
        global total_charge 
        first_fill = '#a7ba8f' 
        second_fill = '#d1d1d1' 
        color_lists  = [first_fill, second_fill]  

        green_status = 1  

        ystart_row = 0
        y_end_row = 50
 
        ystart_text = 25  

        item_instances = [] 
        color_change = 0 

        def __init__(self, item_name, item_code, item_price, quantity):     

            if itemEdit.green_status == 1:   
                self._background = scrollbar_canvas.create_rectangle(0, itemEdit.ystart_row, 800, itemEdit.y_end_row, fill=itemEdit.color_lists[0], outline='', tags='green') 
                self.cancel_item     = scrollbar_canvas.create_window(740, itemEdit.ystart_text, window=Button(scrollbar_canvas, image=cross_sign_packer, borderwidth=0, background=itemEdit.color_lists[0], command=lambda : self.cancel_cart_button()), tags='green')    
                self.next_color = itemEdit.color_lists[1]  
                itemEdit.ystart_row += 50 
                itemEdit.y_end_row += 50 
                itemEdit.green_status -= 1
            else:  
                self._background = scrollbar_canvas.create_rectangle(0, itemEdit.ystart_row, 800, itemEdit.y_end_row, fill=itemEdit.color_lists[1], outline='', tags='white')  
                self.cancel_item     = scrollbar_canvas.create_window(740, itemEdit.ystart_text, window=Button(scrollbar_canvas, image=cross_sign_packer, borderwidth=0, background=itemEdit.color_lists[1], command= lambda : self.cancel_cart_button()), tags='white')    
                self.next_color = itemEdit.color_lists[0]
                itemEdit.ystart_row += 50 
                itemEdit.y_end_row += 50 
                itemEdit.green_status += 1  
              
            itemEdit.ystart_text += 50 
            
            self.item_name = item_name 
            self.item_code = item_code 
            self.item_price = item_price
            self.quantity = quantity 
            self.subtotal = str(int(self.quantity) * int(self.item_price)) 

            self.detail_item     = scrollbar_canvas.create_text(88, itemEdit.ystart_text-50, text=str(self.item_name), font=('Helvetica', '8')) 
            self.detail_code     = scrollbar_canvas.create_text(202, itemEdit.ystart_text-50, text=str(self.item_code), font=('Helvetica', '8')) 
            self.detail_price    = scrollbar_canvas.create_text(330, itemEdit.ystart_text-50, text=str(self.item_price), font=('Helvetica', '8'))
            self.detail_quantity = scrollbar_canvas.create_text(477, itemEdit.ystart_text-50, text=str(self.quantity), font=('Helvetica', '8'))
            self.detail_subtotal = scrollbar_canvas.create_text(655, itemEdit.ystart_text-50, text=str(self.subtotal), font=('Helvetica', '8')) 

            self.plus_button     = scrollbar_canvas.create_window(510, itemEdit.ystart_text-50, window=Button(scrollbar_canvas, text='+', font=('Helvetica', '8', 'bold'), justify=CENTER, command=lambda : self.edit_cart('+')), height=20, width=25)
            self.minus_button    = scrollbar_canvas.create_window(445, itemEdit.ystart_text-50, window=Button(scrollbar_canvas, text='-', font=('Helvetica', '8', 'bold'), justify=CENTER, command=lambda : self.edit_cart('-')), height=20, width=25) 

            self.__class__.item_instances.append(weakref.proxy(self))  
        

        def cancel_cart_button(self): 
            global total_charge 
            for same_lines in itemEdit.item_instances: 
                if scrollbar_canvas.coords(same_lines.detail_item)[1] == scrollbar_canvas.coords(self.detail_item)[1]:  
                    itemEdit.item_instances.remove(same_lines) 
                    break    

            for lines in itemEdit.item_instances:
                if scrollbar_canvas.coords(lines.detail_item)[1] > scrollbar_canvas.coords(self.detail_item)[1]:  
                    scrollbar_canvas.coords(lines._background, 0, scrollbar_canvas.coords(lines._background)[1]-50, 800, scrollbar_canvas.coords(lines._background)[3]-50)
                    scrollbar_canvas.coords(lines.cancel_item, scrollbar_canvas.coords(lines.cancel_item)[0], scrollbar_canvas.coords(lines.cancel_item)[1]-50)  
                    scrollbar_canvas.coords(lines.detail_item, scrollbar_canvas.coords(lines.detail_item)[0], scrollbar_canvas.coords(lines.detail_item)[1]-50) 
                    scrollbar_canvas.coords(lines.detail_code, scrollbar_canvas.coords(lines.detail_code)[0], scrollbar_canvas.coords(lines.detail_code)[1]-50)
                    scrollbar_canvas.coords(lines.detail_price, scrollbar_canvas.coords(lines.detail_price)[0], scrollbar_canvas.coords(lines.detail_price)[1]-50)  
                    scrollbar_canvas.coords(lines.detail_quantity, scrollbar_canvas.coords(lines.detail_quantity)[0], scrollbar_canvas.coords(lines.detail_quantity)[1]-50)                     
                    scrollbar_canvas.coords(lines.detail_subtotal, scrollbar_canvas.coords(lines.detail_subtotal)[0], scrollbar_canvas.coords(lines.detail_subtotal)[1]-50)                     
                    scrollbar_canvas.coords(lines.plus_button, scrollbar_canvas.coords(lines.plus_button)[0], scrollbar_canvas.coords(lines.plus_button)[1]-50)                   
                    scrollbar_canvas.coords(lines.minus_button, scrollbar_canvas.coords(lines.minus_button)[0], scrollbar_canvas.coords(lines.minus_button)[1]-50)     
                    scrollbar_canvas.itemconfig(lines._background, fill=lines.next_color)      
                    if lines.next_color == itemEdit.color_lists[0]:
                        lines.next_color = itemEdit.color_lists[1]
                    else:
                        lines.next_color = itemEdit.color_lists[0] 
                if itemEdit.item_instances[-1]:
                    if lines.next_color == itemEdit.color_lists[0]:
                        itemEdit.green_status = 1 
                    else:
                        itemEdit.green_status = 0

            scrollbar_canvas.delete(self._background)
            scrollbar_canvas.delete(self.detail_item)
            scrollbar_canvas.delete(self.detail_code)
            scrollbar_canvas.delete(self.detail_price) 
            scrollbar_canvas.delete(self.detail_quantity) 
            scrollbar_canvas.delete(self.detail_subtotal) 
            scrollbar_canvas.delete(self.plus_button) 
            scrollbar_canvas.delete(self.minus_button)  
            scrollbar_canvas.delete(self.cancel_item)   
            
            total_charge -= int(self.subtotal)
            total_price['state'] = 'normal'  
            temp_price = total_price.get()
            total_price.delete(0, 'end') 
            total_price.insert(0, str(int(temp_price)-int(self.subtotal)))  
            total_price['state'] = DISABLED 

            itemEdit.ystart_text -= 50  
            itemEdit.ystart_row -= 50
            itemEdit.y_end_row -= 50  


        def edit_cart(self, operator):    
            global total_price_editor 
            global subtotal 
            global total_charge
            self.quantity = str(eval(str(self.quantity) + str(operator) + str('1')))    
            total_price_editor = str(eval(str(total_price.get()) + str(operator) + str(self.item_price))) 
            total_charge += int(self.item_price)
            self.subtotal = (int(self.quantity) * int(self.item_price))  
            total_price['state'] = 'normal' 
            total_price.delete(0, 'end')
            total_price.insert(0, total_price_editor) 
            total_price['state'] = DISABLED
            scrollbar_canvas.itemconfig(self.detail_quantity, text=str(self.quantity)) 
            scrollbar_canvas.itemconfig(self.detail_subtotal, text=str(self.subtotal)) 

        
    # Functions 
    def get_receipt_function(): 
        global admin_dashboard 
        global receipt_text 
        global cust_itempurchase_header 
        global customerPaid  
        global temp_saver 
        global general_transaction_sqlrunner
        temp_saver = []
        receipt_custlist = Toplevel() 
        receipt_custlist.resizable(False, True) 
        receipt_custlist.title('TRANSACTION DETAIL')  
        receipt_custlist.geometry('350x1000')
        receipt_frame = tk.Frame(receipt_custlist)
        receipt_canvas = tk.Canvas(receipt_frame, height=1000, width=500, background='#c2c2c2')  
        receipt_frame.pack()
        receipt_canvas.pack() 
        receipt_canvas.create_text(100, 50, text=receipt_text) 
        receipt_canvas.create_text(155, 120, text=cust_itempurchase_header, font=('Helvetica', '7', 'bold'))  
        receipt_canvas.create_line(12, 105, 335, 105, fill='black')
        receipt_yposition = 150  
        for parts in itemEdit.item_instances:
            receipt_canvas.create_text(15, receipt_yposition, text=parts.item_name, font=('Helvetica', '5'), anchor=W) 
            receipt_canvas.create_text(97, receipt_yposition, text=parts.item_code, font=('Helvetica', '5')) 
            receipt_canvas.create_text(165, receipt_yposition, text=parts.item_price, font=('Helvetica', '5')) 
            receipt_canvas.create_text(234, receipt_yposition, text=parts.quantity, font=('Helvetica', '5')) 
            receipt_canvas.create_text(305, receipt_yposition, text=parts.subtotal, font=('Helvetica', '5')) 
            receipt_yposition += 15     
        receipt_canvas.create_text(305, receipt_yposition+13, text=str(customerPaid), font=('Helvetica', '10')) 
        receipt_canvas.create_line(12, receipt_yposition+2, 335, receipt_yposition+2, fill='black')
        receipt_canvas.create_text(240, receipt_yposition+13, text='TOTAL :', font=('Helvetica', '10'))
        receipt_canvas.create_window(300, receipt_yposition+35, window=Button(receipt_canvas, text='OK', command=receipt_custlist.destroy, border=3, background='#c9c8c5'), height=20, width=40)   
        receipt_custlist.geometry(f'350x{receipt_yposition+50}')  
        return
            

    def decrease_qty():
        try:
            minusqty_box.configure(state='normal')
            charge_label.config(state='normal')
            var_qty = int(qty_box.get())
            charge_label.delete(0, 'end')
            qty_box.delete(0, 'end')
            var_qty -= 1
            qty_box.insert(0, var_qty)
            subtotal_value = int(database.local_item_list[2][database.local_item_list[0].index(
                items_dropbox.get().rstrip(re.findall('(-\d*)', items_dropbox.get())[0]))])
            charge_label.insert(0, int(var_qty)*subtotal_value)
            charge_label.config(state=DISABLED)
        except ValueError:
            charge_label.config(state='normal')
            charge_label.delete(0, 'end')
            charge_label.config(state=DISABLED)
        if qty_box.get() == '0':
            minusqty_box.configure(state=DISABLED)
            return 
        else:
            minusqty_box.configure(state=ACTIVE)

    def increase_qty():
        global var_qty
        global subtotal_value 
        try:
            charge_label.config(state='normal')
            var_qty = int(qty_box.get())
            charge_label.delete(0, 'end')
            qty_box.delete(0, 'end')
            var_qty += 1
            qty_box.insert(0, var_qty)
            subtotal_value = int(database.local_item_list[2][database.local_item_list[0].index(
                items_dropbox.get().rstrip(re.findall('(-\d*)', items_dropbox.get())[0]))])
            charge_label.insert(0, int(var_qty)*subtotal_value)
            charge_label.config(state=DISABLED)
        except ValueError:
            charge_label.config(state='normal')
            charge_label.delete(0, 'end')
            charge_label.config(state=DISABLED) 
        if qty_box.get() == '0':
            minusqty_box.configure(state=DISABLED)
        else:
            minusqty_box.configure(state=ACTIVE) 

    def qtybox_bind(*args):
        global var_qty
        global subtotal_value
        var_qty = str(qty_box.get())
        subtotal_value = str(charge_label.get())
        try:
            check_qtyvar = int(var_qty) 
        except ValueError:
            charge_label.config(state='normal')
            charge_label.delete(0, 'end')
            charge_label.config(state=DISABLED)
            display_login.after(100, qtybox_bind)
            return
        if int(var_qty) == 0 or var_qty == '':
            charge_label.config(state='normal')
            qty_box.delete(0, '0')
            charge_label.delete(0, 'end')
            charge_label.insert(0, '0')
            charge_label.config(state=DISABLED) 
            minusqty_box.configure(state=DISABLED)
            display_login.after(100, qtybox_bind)
        else:
            charge_label.config(state='normal')
            subtotal_value = int(database.local_item_list[2][database.local_item_list[0].index(
                items_dropbox.get().rstrip(re.findall('(-\d*)', items_dropbox.get())[0]))])
            charge_label.delete(0, 'end')
            charge_label.insert(0, int(var_qty)*int(subtotal_value))
            charge_label.config(state=DISABLED)
            display_login.after(100, qtybox_bind)

    def pick_an_item(*args):
        for items in database.dropbox_items:
            if items_dropbox.get() == items:
                charge_label.config(state='normal')
                qty_box.delete(0, 'end')
                charge_label.delete(0, 'end')
                charge_label.config(state=DISABLED)
                subprice = int(database.local_item_list[2][database.local_item_list[0].index(
                    items.rstrip(re.findall('(-\d*)', items)[0]))])
                quantity = IntVar()
                quantity.set(1)
                qty_box.insert(0, quantity.get())
                charge_label.config(state='normal')
                charge_label.insert(0, str(subprice*quantity.get()))
                charge_label.config(state=DISABLED)
                break

    def cart_add_command():   
        global green_status
        global ystart_row 
        global y_end_row 
        global ystart_text 
        global total_charge  
        global edit_cart 
        global total_price_editor 
        global subtotal
        if qty_box.get() == 0:
            return
        subitem = items_dropbox.get()
        code = database.local_item_list[1][database.dropbox_items.index(items_dropbox.get())]
        price = database.local_item_list[2][database.dropbox_items.index(items_dropbox.get())]
        quantity = qty_box.get()
        subtotal = charge_label.get() 
        for item_inline in itemEdit.item_instances:
            if str(subitem) == str(item_inline.item_name):  
                for _ in range(int(quantity)):
                    item_inline.quantity = str(eval(str(item_inline.quantity) + str('+') + str('1')))    
                    total_price_editor = str(eval(str(total_price.get()) + str('+') + str(item_inline.item_price))) 
                    item_inline.subtotal = (int(item_inline.quantity) * int(item_inline.item_price))  
                    total_charge += int(item_inline.item_price)
                    total_price['state'] = 'normal' 
                    total_price.delete(0, 'end')
                    total_price.insert(0, total_price_editor) 
                    total_price['state'] = DISABLED
                    scrollbar_canvas.itemconfig(item_inline.detail_quantity, text=str(item_inline.quantity)) 
                    scrollbar_canvas.itemconfig(item_inline.detail_subtotal, text=str(item_inline.subtotal)) 
                    item_inline.quantity = int(item_inline.quantity)  
                return
        itemEdit(str(subitem), str(code), str(price), str(quantity)) 
        total_charge += int(subtotal)  
        total_price.config(state='normal')
        total_price.delete(0, 'end') 
        if total_price.get() == '': 
            total_price.insert(0, str(int(total_charge)))  
        total_price.config(state=DISABLED)  
        qty_box.delete(0, 'end')
        charge_label.config(state='normal') 
        charge_label.delete(0, 'end')
        charge_label.config(state=DISABLED)
        cart_frame.bind('<Configure>', lambda e : scrollbar_canvas.configure(scrollregion=scrollbar_canvas.bbox('all'))) 


    def cursor_click(*args):
        if cust_name_box.get() == 'Enter Customer Name : ' or cust_name_box.get() == None:
            cust_name_box.config(foreground='black', state=ACTIVE)
            cust_name_box.delete(0, 'end')

    def cursor_out(*args):
        if cust_name_box.get() == '' or cust_name_box.get() == None:
            cust_name_box.delete(0, 'end')
            cust_name_box.insert(0, 'Enter Customer Name : ')
            cust_name_box.config(foreground='#8f8f8f', state=DISABLED)

    def insert_subpurchase(*args): 
        global loopingfunc_status
        try:
            if items_dropbox.get() == 'Choose Item' or qty_box.get() == '' or type(int(qty_box.get())) != int:
                transaction_rect.delete('addsubpurchase-on')
                transaction_rect.create_window(
                    1434, 233, window=insert_purchase, height=134, width=100, tags='addsubpurchase')
            else:
                transaction_rect.delete('addsubpurchase')
                transaction_rect.create_window(
                    1434, 233, window=insert_purchase_true, height=134, width=100, tags='addsubpurchase-on')
            if loopingfunc_status == 0:
                return
            display_login.after(100, insert_subpurchase)  
        except ValueError: 
            transaction_rect.delete('addsubpurchase-on')
            transaction_rect.create_window(
                1434, 233, window=insert_purchase, height=134, width=100, tags='addsubpurchase') 
            if loopingfunc_status == 0:
                return 
            display_login.after(100, insert_subpurchase)
            
    def confirm_paid_checker(*args):
        global loopingfunc_status
        try:
            if paid_price.get() == '' or type(int(paid_price.get())) != int:
                confirm_paid.configure(state=DISABLED)
            else:
                confirm_paid.configure(state=ACTIVE)
        except ValueError:
            confirm_paid.configure(state=DISABLED)
        if loopingfunc_status == 0:
            return
        display_login.after(100, confirm_paid_checker)

    def confirm_paid_totalcheck():  
        global loopingfunc_status
        try:
            if total_price.get() == '' or type(int(paid_price.get())) != int:
                paid_price.configure(state=DISABLED)
            else:
                paid_price.configure(state=ACTIVE) 
        except ValueError:
            paid_price.configure(state=ACTIVE)  
        if loopingfunc_status == 0:
            return
        display_login.after(100, confirm_paid_totalcheck) 

    def tick_command():
        if int(paid_price.get()) < int(total_price.get()):   
            messagebox.showwarning('WARNING', 'INSUFFICIENT PAID AMOUNT')  
        else:
            change_price.config(state='normal')
            change_price.delete(0, 'end') 
            change_price.insert(0, int(paid_price.get())-int(total_price.get()))
            change_price.config(state=DISABLED)
              

    def confirm_payment(*args): 
        global loopingfunc_status
        try:
            if cust_name_box.get() == '' or cust_name_box.get() == 'Enter Customer Name : ' or total_price.get() == '' or paid_price.get() == '' or type(int(paid_price.get())) != int or change_price.get() == '':
                transaction_rect.delete('tag_yes')
                transaction_rect.create_window(
                    1145, 560, window=payment_confirmation, height=70, width=400, tags='tag_confirmation')
            else:
                transaction_rect.delete('tag_confirmation')
                transaction_rect.create_window(
                    1145, 560, window=yes_button, height=70, width=400, tags='tag_yes')  
        except ValueError: 
                transaction_rect.delete('tag_yes')
                transaction_rect.create_window(
                    1145, 560, window=payment_confirmation, height=70, width=400, tags='tag_confirmation')
        if loopingfunc_status == 0:
            return
        display_login.after(100, confirm_payment)

    def final_trans_confirmation(*args): 
        global loopingfunc_status 
        global itemEdit 
        global customerPaid 
        global client_query
        confirmation_msgbox = messagebox.askyesno('FINAL CONFIRMATION', 
        '''
        MAKE SURE THESE THINGS :
        1. YOU HAVE RECEIVED THE PAYMENT FROM CUSTOMER 
        2. YOU HAVE GIVEN THE CHANGE 

        '''
        )   
        if confirmation_msgbox == 1:  
            global receipt_text 
            global cust_itempurchase_header  
            global general_transaction_sqlrunner
            customerName = cust_name_box.get() 
            customerPaid = total_price.get() 
            customerDate = datetime.datetime.now()
            customerTCode = fixed_trans_code   
            try:
                with open(r'Cashier SQL\GeneralTransaction Query.sql', 'a') as file:
                    file.write(f"INSERT INTO `general transaction` VALUES ('{customerTCode}',   '{customerName}', '{customerDate}', '{customerPaid}');")
            except:
                pass
            loopingfunc_status = 0
            cust_itempurchase = '' 
            receipt_text = f'''
            TRANSACTION NUMBER : {customerTCode}

            Name        : {customerName} 
            Date           : {customerDate}
            ''' 
            cust_itempurchase_header = '''
            ITEM                CODE              PRICE               QTY              SUBTOTAL
            '''  
            get_receipt_function()
            database.dtbs_cursor = database.dtbs.cursor()
            database.dtbs.reconnect()
            try:
                with open(r'Cashier SQL\GeneralTransaction Query.sql', 'r') as file_runner: 
                    general_transaction_sqlrunner = file_runner.read().split(';')
                    for commands in general_transaction_sqlrunner: 
                        if str(commands) == '' or commands is None:
                            continue
                        database.dtbs_cursor.execute(str(commands), multi=True)   
            except:
                pass                        
            
            client_query = f'''
                DROP TABLE IF EXISTS `{str(customerName)}`;

                CREATE TABLE `{str(customerName)}` (
                    `Item Name` varchar(255),
                    `Item Code` varchar(255), 
                    `Price` int(11),
                    `Quantity` int(11), 
                    `Subtotal` int(11)
                ); 
            '''
            try:
                with open(r'Cashier SQL\ClientSide Query.sql', 'a') as itemlister: 
                    itemlister.write(client_query)
                    for item_details in itemEdit.item_instances:
                        itemlister.write(f'''INSERT INTO `{str(customerName)}` VALUES ('{str(item_details.item_name)}', '{str(item_details.item_code)}', {int(item_details.item_price)}, {int(item_details.quantity)}, {int(item_details.subtotal)});''')
                
                with open(r'Cashier SQL\ClientSide Query.sql', 'r') as runningclientscript:
                    clienttable_script = runningclientscript.read().split(';')
                    for lines in clienttable_script: 
                        if str(lines) == '' or lines is None:
                            continue
                        try:
                            database.clientdtbs_cursor.execute(str(lines), multi=True) 
                        except InternalError:
                            pass
            except:
                pass                        
                     
            display_login.geometry('400x300') 
            transaction_frame.destroy() 
            transaction_rect.destroy() 
            admin_dashboard()
        return



    # Initialize Stuffs

    transaction_frame = tk.Frame(display_login)
    transaction_rect = tk.Canvas(
        transaction_frame, height=height, width=width, background='#c2c2c2')  

    dollar_sign = Image.open(r'dollar.png')
    dollar_sign_2 = dollar_sign.resize((40, 40))
    dollar_sign_packer = ImageTk.PhotoImage(dollar_sign_2) 

    tick_sign = Image.open(r'check.png')
    tick_sign_2 = tick_sign.resize((40,40))  
    tick_sign_packed = ImageTk.PhotoImage(tick_sign_2) 

    cross_sign = Image.open(r'cancelbutton.png') 
    cross_sign_2 = cross_sign.resize((30,30)) 
    cross_sign_packer = ImageTk.PhotoImage(cross_sign_2)

    transaction_frame.pack()
    transaction_rect.pack() 

    scrollbar_frame = ttk.Frame(transaction_rect)
    scrollbar_canvas = tk.Canvas(scrollbar_frame, background='#cacccf')
    cart_scrollbar = ttk.Scrollbar(scrollbar_frame, orient='vertical', command=scrollbar_canvas.yview)    
    cart_frame = ttk.Frame(scrollbar_canvas) 

    cart_frame.bind('<Configure>', lambda e : scrollbar_canvas.configure(scrollregion=scrollbar_canvas.bbox('all')))  
    scrollbar_canvas.create_window(382, 450, window=cart_frame, anchor='nw')     
    scrollbar_canvas.configure(yscrollcommand=cart_scrollbar.set)    

    transaction_rect.create_window(382 , 450, window=scrollbar_frame, height=700, width=778)  
    scrollbar_canvas.pack(side=LEFT, fill='both', expand=True)   
    cart_scrollbar.pack(side=RIGHT, fill='y')

    transaction_rect.create_rectangle(0, 0, 770, 1000, fill='white')

    transaction_rect.create_rectangle(
        0, 0, 770, 45, fill="#b7cbeb", outline='black')

    transaction_rect.create_text(
        130, 25, text='ITEM CART', font=('Helvetica', 35))

    transaction_rect.create_rectangle(
        0, 100, 770, 60, fill='#628559', outline='')
    transaction_rect.create_text(
        80, 80, text='ITEM', fill='#ffffff', font=('Helvetica', '20', 'bold'))
    transaction_rect.create_text(
        195, 80, text='CODE', fill='#ffffff', font=('Helvetica', '20', 'bold'))
    transaction_rect.create_text(
        325, 80, text='PRICE', fill='#ffffff', font=('Helvetica', '20', 'bold'))
    transaction_rect.create_text(
        470, 80, text='QUANTITY', fill='#ffffff', font=('Helvetica', '20', 'bold'))
    transaction_rect.create_text(
        650, 80, text='SUBTOTAL', fill='#ffffff', font=('Helvetica', '20', 'bold')) 
    transaction_rect.create_text(
        988, 25, text=('Transaction Code : #'+str(fixed_trans_code)), font=('Helvetica', '18'), fill='#707070'
    )

    # Inputs
    clicked = StringVar()
    clicked.set('Choose Item')

    cust_name_box = ttk.Entry(font=('Helvetica-80'), foreground='#8f8f8f')
    cust_name_box.insert(0, 'Enter Customer Name : ')
    cust_name_box.bind('<Button-1>', cursor_click)
    cust_name_box.bind('<Leave>', cursor_out)

    qty_box = ttk.Entry(transaction_frame, font=(
        'Helvetica-80'), justify=CENTER)
    qty_box.bind('<Key>', qtybox_bind) 

    minusqty_box = tk.Button(transaction_frame, text='-',
                             font=('Helvetica-70'), justify=CENTER, command=decrease_qty)
    plusqty_box = tk.Button(transaction_frame, text='+',
                            font=('Helvetica-70'), justify=CENTER, command=increase_qty)

    charge_label = ttk.Entry(transaction_frame, font=(
        'Helvetica-90'), justify=CENTER, state=DISABLED)

    total_price = ttk.Entry(transaction_frame, font=(
        "Helvetica-90"), state=DISABLED, justify=CENTER)

    change_price = ttk.Entry(
        transaction_frame, font=('Helvetica'), state=DISABLED)

    paid_price = ttk.Entry(transaction_frame, font=('Helvetica')) 
    paid_price.bind('<Key>', confirm_paid_checker) 

    confirm_paid = tk.Button(transaction_frame, image=tick_sign_packed, command=tick_command)

    insert_purchase = tk.Button(transaction_rect, text='''ADD\nTO\nCART ''', state=DISABLED, font=(
        'Helvetica-50'), justify=CENTER, background='#ffffff', command=cart_add_command)
    insert_purchase_true = tk.Button(transaction_rect, text='''ADD\nTO\nCART ''', font=(
        'Helvetica-50'), justify=CENTER,  background='#adadad', command=cart_add_command)

    payment_confirmation = tk.Button(transaction_rect, text='CONFIRM TRANSACTION', state=DISABLED, font=(
        'Helvetica-50'), background='#ffffff')
    yes_button = tk.Button(transaction_rect, text='CONFIRM TRANSACTION', font=(
        'Helvetica-50'), background='#7cc46a', foreground='#000000', command=final_trans_confirmation)

    cancel_transaction = tk.Button(transaction_frame, text='Cancel Transaction', font=(
        'Helvetica-50'), foreground='#ffffff', background='#cf3025', command=None)

    styling = ttk.Style()
    styling.theme_use('clam')
    styling.configure('TCombobox', fieldbackground='white', background='white')

    items_dropbox = ttk.Combobox(display_login, textvariable=clicked, font=(
        'Helvetica-90'), justify=CENTER, state='readonly')
    items_dropbox['values'] = database.dropbox_items
    items_dropbox.bind('<<ComboboxSelected>>', pick_an_item)

    transaction_rect.create_window(
        1100, 120, window=cust_name_box, height=80, width=550)
    transaction_rect.create_window(
        1100, 200, window=items_dropbox, height=70, width=550)
    transaction_rect.create_rectangle(825, 170, 1375, 240, fill='black')
    transaction_rect.create_text(
        880, 275, text='QUANTITY : ', font=('Helvetica-90'))
    transaction_rect.create_window(
        1040, 275, window=qty_box,  height=50, width=110)
    transaction_rect.create_window(
        965, 276, window=minusqty_box, height=50, width=40)
    transaction_rect.create_window(
        1115, 276, window=plusqty_box, height=50, width=40)
    transaction_rect.create_image(1158, 275, image=dollar_sign_packer)
    transaction_rect.create_window(
        1275, 275, window=charge_label, height=50, width=200)

    transaction_rect.create_text(
        930, 350, text='TOTAL', font=('Helvetica', '50', 'bold'))
    transaction_rect.create_window(
        1220, 350, window=total_price, height=70, width=310)
    transaction_rect.create_text(863, 430, text='PAID', font=('Helvetica'))
    transaction_rect.create_text(880, 470, text='CHANGE', font=('Helvetica'))
    transaction_rect.create_window(
        1100, 430, window=paid_price, height=40, width=310) 
    transaction_rect.create_window(
        1290, 430, window=confirm_paid, height=40, width=40)
    transaction_rect.create_window(
        1100, 470, window=change_price, height=40, width=310)
    transaction_rect.create_rectangle(
        800, 45, 1500, 510, fill='', outline='#8f8f8f')
    transaction_rect.create_window(
        1145, 630, window=cancel_transaction, height=70, width=400)
    transaction_rect.create_line(810, 308, 1490, 308, fill='#8f8f8f')  

    confirm_paid_totalcheck()
    confirm_paid_checker()
    confirm_payment()
    insert_subpurchase() 
    display_login.mainloop()