#!/usr/bin/env python
# -*- coding: utf-8 -*-
from orders import Orders
import Tkinter as tk

ORDERS = Orders()

def passable():
    pass

class Application(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.create_menu()
        self.build_list()
        self.open()

    def create_menu(self):
        self.menubar = tk.Menu(self)
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_command(label="Update", command=self.update)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=self.menubar)

    def build_list(self):
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.listbox.pack(fill=tk.BOTH, side=tk.LEFT)

        scrollbar.config(command=self.listbox.yview)

    def build_viewer(self):
        self.viewbox = tk.Frame(self)
        self.viewbox.pack(fill=tk.BOTH)
        labler = tk.Label(self.viewbox, text="test")
        labler.grid(column=2)

    def update(self):
        pass

    def open(self):
        orderlist = ORDERS.read_recent(limit=30)
        if orderlist.Status == "Success":
            orderlist = orderlist.OrderList
            for order in orderlist:
                fmt_dict = dict()
                fmt_dict['status'] = order.Status.Name
                fmt_dict['first_name'] = order.Customer.BillingAddress.FirstName
                fmt_dict['last_name'] = order.Customer.BillingAddress.LastName
                fmt_dict['order_number'] = order._OrderNumber
                line = """\
{status} - {order_number} - {first_name} {last_name}"""
                self.listbox.insert(tk.END, line.format(
                    **fmt_dict))

def main():
    app = Application()
    app.title('nsCommerce Order Import')
    app.mainloop()

if __name__ == '__main__':
    main()
