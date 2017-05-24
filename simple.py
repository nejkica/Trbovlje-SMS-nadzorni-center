#!/usr/bin/python
# -*- coding: utf-8 -*-
# simple.pyw

import wx

class SmsGUI(wx.Frame):
    def __init__(self, parent, title):
        super(SmsGUI, self).__init__(parent, -1, title, size=(250, 200))
        self.Maximize()

        self.InitUI()

if __name__=='__main__':
    app=wx.App()
    SmsGUI(None, title='Velikost')
    app.MainLoop()

                                     
##app=wx.App()
##window=wx.Frame(None, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE)
##window.Show(True)
##app.MainLoop()
