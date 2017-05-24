# -*- coding: cp1250 -*-
# ZgodovinaBazena.pyw


import wx
import wx.grid as gridlib
import time
import MySQLdb as mdb
##import time
##from time import strftime
##import MySQLdb as mdb
##import sys
##import string
##import glob
##import logging
##import logging.handlers
##from logging import Formatter
##import msvcrt

class ZgodovinaBazena1(wx.Frame):
    title='Zgodovina bazena'
    bazeni=["ZB-ZL", "ZB-E", "ZB-L", "ZB-R", "ZB-D", "ZB-F", "ZB-M", "ZB-G"]
    bazeniDB=["zl", "e", "l", "r", "d", "f", "m", "g"]
    
    def __init__(self, *args, **kwargs):
        super(ZgodovinaBazena1, self).__init__(*args, **kwargs)
        self.bazen=self.bazeni[int(args[1])]
        self.bazenDB=self.bazeniDB[int(args[1])]
        self.InitUI()

    def InitUI(self):
        self.name = "OknoZgodovine-%s"%wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Eno okno že imaš odprto, najprej ga zapri.", "ERROR")
            self.Destroy()
            return False

        
    
        self.panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)


##  nalepke
        self.naslovZgodovine = wx.StaticText(self.panel, label='Zgodovina bazena '+str(self.bazen), pos=(15,15), style=wx.BOLD)
        self.naslovZgodovine.SetFont(wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD))

##  Dodamo na v sizer
        vbox.Add(self.panel,1, wx.EXPAND|wx.ALL)


        self.SetTitle('Komunala Trbovlje - Zgodovina bazena')
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        self.CenterOnScreen()
        self.SetSize(wx.Size(550, 600))
        self.Refresh()
        self.SetSizer(vbox)

##  Bind Events
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        
        self.Show(True)
        self.PoglejZgodovino()
        
        return True
        
    def PoglejZgodovino(self):
        db3=None
        while db3==None:
            try:
                db3 = mdb.connect('localhost', 'root', '', 'smsc')
            except mdb.Error, e:
                time.sleep(10)
                continue
        
        cursor=db3.cursor()
        poglej_v_bazo3="SELECT * FROM  `sms` WHERE `sms`.`vrsta_objekta`='%s' ORDER BY `sms`.`datum` DESC" % (self.bazenDB)
        try:
            cursor.execute(poglej_v_bazo3)
            db3.commit()
        except:
            db3.rollback()
            db3.close()
            
        vrstice3=cursor.fetchall()
        stVrstic3=len(vrstice3)
        self.PrikaziZgodovino(vrstice3, stVrstic3)
        db3.close()

       
    def PrikaziZgodovino(self, vrstice3, st_vrstic):
        ##  Tabela sms-ov
        while True:
            try:
                self.myGrid
                i=0
                for vrsta3 in vrstice3:
                    datum=vrsta3[1].strftime('%d.%m.%Y %H:%M:%S')
                    self.myGrid.SetCellValue(i,0, datum)
                    self.myGrid.SetCellValue(i,1, str(vrsta3[2]).upper())
                    self.myGrid.SetCellValue(i,2, str(vrsta3[6]))
                    self.myGrid.SetCellValue(i,3, str(vrsta3[4]))
                    if vrsta3[5]==1:
                        stanje='OK'
                    else:
                        stanje='Napaka'
                    self.myGrid.SetCellValue(i,4, stanje)
                    self.myGrid.SetCellValue(i,5, str(vrsta3[0]))
                    i+=1
                break
            except:
                if st_vrstic==0:
                    break
                self.myGrid = gridlib.Grid(self.panel, pos=(15,50))
                self.myGrid.CreateGrid(st_vrstic, 6)
                visinaTabele=(st_vrstic+1)*20
                if visinaTabele>500:
                    visinaTabele=500
                self.myGrid.SetSize((510,visinaTabele))
                self.myGrid.SetColLabelSize(20)
                self.myGrid.SetRowLabelSize(70)
##                self.myGrid.SetDefaultCellBackgroundColour(self.panel.GetBackgroundColour())
                self.myGrid.SetDefaultCellBackgroundColour('white')
                
                self.myGrid.EnableDragGridSize(False)
                self.myGrid.EnableDragColSize(False)
                self.myGrid.EnableDragRowSize(False)
                self.myGrid.EnableEditing(False)
                self.myGrid.SetDefaultCellFont(wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL))
                self.myGrid.SetLabelFont(wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL))
                
                self.myGrid.SetColSize(0, 130)
                self.myGrid.SetColLabelValue(0, "Datum")
                
                self.myGrid.SetColSize(1, 40)
                self.myGrid.SetColLabelValue(1, "PBMV")

                self.myGrid.SetColSize(2, 60)
                self.myGrid.SetColLabelValue(2, "Opis")

                self.myGrid.SetColSize(3, 30)
                self.myGrid.SetColLabelValue(3, "Črp")

                self.myGrid.SetColSize(4, 55)
                self.myGrid.SetColLabelValue(4, "Stanje")

                self.myGrid.SetColSize(5, 100)
                self.myGrid.SetColLabelValue(5, "Telefonska")

                continue
        

    def onCloseWindow(self, e):
        self.Destroy()
        return 0
