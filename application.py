#!/usr/bin/env python
""" A stupid fucking program to make sure shit gets out """

import wx

class MainWindow(wx.Frame):
    # pylint: disable=R0904
    # pylint: disable=C0103
    """
    Prop that frame up with a turd of a status bar, and put in a
    stupid fuckin' menu, too.
    """


    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        box = wx.BoxSizer(wx.VERTICAL)


        box.Add(panel1, 2, wx.EXPAND)
        box.Add(panel2, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def OnClear(self, event):
        print "poops"
        pass

    def OnChange(self, event):
        pass

    def OnKeyPress(self, event):
        pass


def main():
    """docstring for """

    app = wx.App(False)
    frame = MainWindow(parent=None, title="Order List")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
