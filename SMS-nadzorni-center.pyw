# -*- coding: cp1250 -*-
# SMS-nadzorni-center.pyw

import wx
import wx.grid as gridlib
import time
from time import strftime
import MySQLdb as mdb
import sys
import string
import glob
import logging
import logging.handlers
from logging import Formatter
import msvcrt
import ZgodovinaBazena

class SmsGUI(wx.Frame):

    bazeni=["ZB-ZL", "ZB-E", "ZB-L", "ZB-R", "ZB-D", "ZB-F", "ZB-M", "ZB-G"]
    bazeniDB=["zl", "e", "l", "r", "d", "f", "m", "g"]
    crpalkNaBazen=[2,2,2,2,3,2,3,4]


    
    def __init__(self, *args, **kwargs):
        super(SmsGUI, self).__init__(*args, **kwargs)
        self.x=0
        self.InitUI()
        self.Maximize()

    def InitUI(self):
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

##  orodna vrstica        
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.SUNKEN_BORDER)
        self.toolbar.AddLabelTool(1, '', wx.Bitmap('zb-zl.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(2, '', wx.Bitmap('zb-e.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(3, '', wx.Bitmap('zb-l.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(4, '', wx.Bitmap('zb-r.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(5, '', wx.Bitmap('zb-d.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(6, '', wx.Bitmap('zb-f.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(7, '', wx.Bitmap('zb-m.png'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(8, '', wx.Bitmap('zb-g.png'))        
        self.toolbar.Realize()


##  shema in gumbi na shemi
        self.bitmap=wx.StaticBitmap(self.panel,10,wx.Bitmap('shema-1.png'), pos=(5,5))
        
        self.zbzlIMG=wx.BitmapButton(self.bitmap,12,wx.Bitmap('zb-zls.png'), pos=(292,133), style=wx.NO_BORDER)
        self.kookaburraIMG=wx.StaticBitmap(self.bitmap,11,wx.Bitmap('kookaburra.png'), pos=(300,635), style=wx.NO_BORDER)
        self.KomLogoIMG=wx.StaticBitmap(self.bitmap,11,wx.Bitmap('KOM_logo.jpg'), pos=(10,15), style=wx.NO_BORDER)
        self.zbzdIMG=wx.StaticBitmap(self.bitmap,13,wx.Bitmap('zb-zds.png'), pos=(160,85), style=wx.NO_BORDER)
        self.zbeIMG=wx.BitmapButton(self.bitmap,14,wx.Bitmap('zb-es.png'), pos=(300,253), style=wx.NO_BORDER)
        self.zbrIMG=wx.BitmapButton(self.bitmap,15,wx.Bitmap('zb-rs.png'), pos=(285,370), style=wx.NO_BORDER)
        self.zbtIMG=wx.StaticBitmap(self.bitmap,16,wx.Bitmap('zb-ts.png'), pos=(230,425), style=wx.NO_BORDER)
        self.zbfIMG=wx.BitmapButton(self.bitmap,17,wx.Bitmap('zb-fs.png'), pos=(230,510), style=wx.NO_BORDER)
        self.zbgIMG=wx.BitmapButton(self.bitmap,18,wx.Bitmap('zb-gs.png'), pos=(130,570), style=wx.NO_BORDER)
        self.zblIMG=wx.BitmapButton(self.bitmap,19,wx.Bitmap('zb-ls.png'), pos=(150,340), style=wx.NO_BORDER)
        self.zbdIMG=wx.BitmapButton(self.bitmap,20,wx.Bitmap('zb-ds.png'), pos=(105,435), style=wx.NO_BORDER)
        self.zbmIMG=wx.BitmapButton(self.bitmap,21,wx.Bitmap('zb-ms.png'), pos=(60,520), style=wx.NO_BORDER)

##  Risanje črt v seznamu črpalk
        self.lnh = wx.StaticLine(self.panel, -1, pos=(425,85))
        self.lnh.SetSize((290,2))

        self.lnv = wx.StaticLine(self.panel, -1, pos=(520,60))
        self.lnv.SetSize((2,460))


##  nalepke
        self.naslovBazena = wx.StaticText(self.panel, label='Stanje črpalk po bazenih', pos=(420,15), style=wx.BOLD)
        self.naslovBazena.SetFont(wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD))
        self.naslovZgodovine = wx.StaticText(self.panel, label='Zgodovina vseh sms-ov', pos=(750,15), style=wx.BOLD)
        self.naslovZgodovine.SetFont(wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD))
        maxStCrpalk=4
        self.C=[]
        for i in range(0,(maxStCrpalk)):
            self.C.append(wx.StaticText(self.panel, label='Č'+str((i+1)), pos=((550+(i*45)),60)))
            self.C[i].SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.NORMAL))


####  Prikažem črpalke z določenimi stanji (glej funkcijo za definicijo
        idCrpalk=21
        i=0
        razmikX=45
        razmikY=55
        self.arrayCrpalk=[]
        self.itemNalepka=[]
        self.zbIMG=[]
        for item in self.bazeni:
            self.bitmapCrpalka=[]
            posY=90+(i*razmikY)
            self.zbIMG.append(wx.BitmapButton(self.panel,(100+self.bazeni.index(item)),wx.Bitmap('zb.png'), pos=(425,(posY+5)), style=wx.NO_BORDER))
            self.itemNalepka.append(wx.StaticText(self.panel, label=str(item), pos=(450,(posY+5))))
            self.itemNalepka[i].SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
            i+=1
            for j in range(0,self.crpalkNaBazen[self.bazeni.index(item)]):
                idCrpalk+=1
                posX=540+(j*razmikX)
                self.bitmapCrpalka.append(wx.StaticBitmap(self.panel,idCrpalk,wx.Bitmap('crp2-n.png'), pos=(posX, posY)))
            self.arrayCrpalk.append([item, self.bitmapCrpalka])
        
        del posX, posY
        

        
##  Dodamo na v sizer
        vbox.Add(self.toolbar, 0, wx.EXPAND)
        vbox.Add(self.panel,1, wx.EXPAND|wx.ALL)

##  Pogledamo v bazo za spremembe
        self.TimerDB = wx.Timer(self, id=201)
        self.TimerDB.Start(5000)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.TimerDB)

##  Bind Events
        self.Bind(wx.EVT_TOOL, lambda evt, temp=0: self.PokaziZgodovinoBazena(evt, temp), id=1)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=1: self.PokaziZgodovinoBazena(evt, temp), id=2)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=2: self.PokaziZgodovinoBazena(evt, temp), id=3)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=3: self.PokaziZgodovinoBazena(evt, temp), id=4)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=4: self.PokaziZgodovinoBazena(evt, temp), id=5)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=5: self.PokaziZgodovinoBazena(evt, temp), id=6)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=6: self.PokaziZgodovinoBazena(evt, temp), id=7)
        self.Bind(wx.EVT_TOOL, lambda evt, temp=7: self.PokaziZgodovinoBazena(evt, temp), id=8)

        
        self.SetTitle('Komunala Trbovlje - SMS nadzorni center')
        self.SetSizer(vbox)
        self.Show(True)

        
    def PokaziZgodovinoBazena(self,e, id_bazena):
        ZgodovinaBazena.ZgodovinaBazena1(None,id_bazena)
  
        
    def PreglejBazo(self, e):
        db1=None
        while db1==None:
            try:
                db1 = mdb.connect('localhost', 'root', '', 'smsc')
            except mdb.Error, e:
                time.sleep(10)
                continue
        
        cursor=db1.cursor()
        try:
            self.prviZagon
            poglej_v_bazo="SELECT * FROM  `objekti` WHERE  `sprememba` =1"
        except:
            poglej_v_bazo="SELECT * FROM  `objekti`"
            self.prviZagon=''
            
        try:
            cursor.execute(poglej_v_bazo)
            db1.commit()
        except:
            db1.rollback()
            db1.close()

        vrstice=cursor.fetchall()
        if vrstice!=():
            self.PrikaziZgodovino()
        for vrsta in vrstice:
            obdelujemBazen=vrsta[1]
            kateriBazen=self.bazeniDB.index(obdelujemBazen)
            crpalk=self.crpalkNaBazen[kateriBazen]
            sestevekStanj=vrsta[5]+vrsta[6]+vrsta[7]+vrsta[8]
            self.UtripajBazen(sestevekStanj, kateriBazen)
            for i in range(0,crpalk):
                razdelek=5+i
                self.ZamenjajCrpalke(kateriBazen, i, vrsta[razdelek])
            posodobi_stanje_bazena="UPDATE  `smsc`.`objekti` SET  `sprememba` =  '0' WHERE  `objekti`.`bazen` ='%s'" % (obdelujemBazen)
            try:
                cursor.execute(posodobi_stanje_bazena)
                db1.commit()
            except:
                db1.rollback()
                db1.close()
        db1.close()

        
    def PoglejZgodovino(self):
        db2=None
        while db2==None:
            try:
                db2 = mdb.connect('localhost', 'root', '', 'smsc')
            except mdb.Error, e:
                time.sleep(10)
                continue
        
        cursor=db2.cursor()
        poglej_v_bazo2="SELECT * FROM  `sms` ORDER BY  `sms`.`datum` DESC LIMIT 0 , 500"
        try:
            cursor.execute(poglej_v_bazo2)
            db2.commit()
        except:
            db2.rollback()
            db2.close()
            
        vrstice2=cursor.fetchall()
        db2.close()
        return vrstice2

       
    def PrikaziZgodovino(self):
        ##  Tabela sms-ov
        while True:
            try:
                self.myGrid
                vrstice2=self.PoglejZgodovino()
                i=0
                for vrsta2 in vrstice2:
                    datum=vrsta2[1].strftime('%d.%m.%Y %H:%M:%S')
                    self.myGrid.SetCellValue(i,0, datum)
                    self.myGrid.SetCellValue(i,1, str(vrsta2[2]).upper())
                    self.myGrid.SetCellValue(i,2, str(vrsta2[6]))
                    self.myGrid.SetCellValue(i,3, str(vrsta2[4]))
                    if vrsta2[5]==1:
                        stanje='OK'
                    else:
                        stanje='Napaka'
                    self.myGrid.SetCellValue(i,4, stanje)
                    self.myGrid.SetCellValue(i,5, str(vrsta2[0]))
                    i+=1
                break
            except:
                self.myGrid = gridlib.Grid(self.panel, pos=(750,50))
                self.myGrid.CreateGrid(500, 6)
                self.myGrid.SetSize((510,600))
                self.myGrid.SetColLabelSize(20)
                self.myGrid.SetRowLabelSize(70)
##                self.myGrid.SetDefaultCellBackgroundColour(self.panel.GetBackgroundColour())
                self.myGrid.SetDefaultCellBackgroundColour('white')
                self.myGrid.EnableDragGridSize(False)
                self.myGrid.EnableDragColSize(False)
                self.myGrid.EnableDragRowSize(False)
                self.myGrid.EnableEditing(False)
                self.myGrid.EnableCellEditControl(True)
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
        
        
            
    def ZamenjajCrpalke(self, bazen, crpalka, stanje):
        self.arrayCrpalk[bazen][1][crpalka].SetBitmap(wx.Bitmap('crp'+str(stanje)+'-n.png'))

    def UtripajBazen(self, sestevek, bazen):
        self.ikona=self.bazeni[bazen].lower()
        while True:
            try:
                self.utripBazenov
                if sestevek<4:
                    if bazen not in self.utripBazenov:
                        self.utripBazenov.append(bazen)
                    self.toolbar.SetToolNormalBitmap(bazen+1, wx.Bitmap(self.ikona+'n.png'))
                    self.Timer1 = wx.Timer(self, id=202)
                    self.Timer1.Start(500)
                    self.Bind(wx.EVT_TIMER, self.OnTimer1, self.Timer1)
                else:
                    if bazen in self.utripBazenov:
                        self.utripBazenov.remove(bazen)
                    self.toolbar.SetToolNormalBitmap(bazen+1, wx.Bitmap(self.ikona+'.png'))
                    try:
                        if self.utripBazenov==[]:
                            self.Timer1.Stop()
                    except:
                        pass
                    spremenljivka=self.ikona.replace('-','')+'IMG'
                    eval("self."+spremenljivka+".SetBitmapLabel(wx.Bitmap(self.ikona+'s.png'))")
                break
            except:
                self.utripBazenov=[]

    def OnQuit(self, e):
        self.Close()

    def OnTimer(self,e):
        if e.GetEventObject() == self.TimerDB:
            self.PreglejBazo(e)

    def OnTimer1(self,e):
        for bazen in self.utripBazenov:
            ikona=self.bazeni[bazen].lower()
            spremenljivka=ikona.replace('-','')+'IMG'
            try:
                getattr(self,'y'+str(bazen))
                eval("self."+spremenljivka+".SetBitmapLabel(wx.Bitmap(ikona+'sn.png'))")
                delattr(self,'y'+str(bazen))
            except:
                eval("self."+spremenljivka+".SetBitmapLabel(wx.Bitmap(ikona+'s.png'))")
                setattr(self,'y'+str(bazen),'')
            

def main():
    app=wx.App()
    SmsGUI(None)
    app.MainLoop()

if __name__=='__main__':
    main()
