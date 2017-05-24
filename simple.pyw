# -*- coding: cp1250 -*-
# simple.pyw

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


class MyPopupMenu(wx.Menu):
    
    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()
        
        
##        self.parent = parent

##        cmi = wx.MenuItem(self, wx.NewId(), 'Zapri program')
##        self.AppendItem(cmi)
##        self.Bind(wx.EVT_MENU, self.OnClose, cmi)


##    def OnMinimize(self, e):
##        self.parent.Iconize()

##    def OnClose(self, e):
##        self.parent.Close()
        
##class MyImageRenderer(wx.grid.PyGridCellRenderer):
##    def __init__(self, img):
##        wx.grid.PyGridCellRenderer.__init__(self)
##        self.img = img
##    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
##        image = wx.MemoryDC()
##        image.SelectObject(self.img)
##        dc.SetBackgroundMode(wx.SOLID)
##        if isSelected:
##            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
##            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
##        else:
##            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
##            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
##        dc.DrawRectangleRect(rect)
##        width, height = self.img.GetWidth(), self.img.GetHeight()
##        if width > rect.width-2:
##            width = rect.width-2
##        if height > rect.height-2:
##            height = rect.height-2
##        dc.Blit(rect.x+1, rect.y+1, width, height, image, 0, 0, wx.COPY, True)


class SmsGUI(wx.Frame):

    bazeni=["ZB-ZL", "ZB-E", "ZB-R", "ZB-D", "ZB-F", "ZB-G", "ZB-L", "ZB-M"]
    crpalkNaBazen=[3,3,2,2,3,4,3,4]


    
    def __init__(self, *args, **kwargs):
        super(SmsGUI, self).__init__(*args, **kwargs)
        self.x=0
        self.InitUI()
        self.Maximize()

    def InitUI(self):
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

##  orodna vrstica        
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
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
        self.bitmap=wx.StaticBitmap(self.panel,10,wx.Bitmap('shema.png'), pos=(5,5))
        self.zbzlIMG=wx.BitmapButton(self.bitmap,12,wx.Bitmap('zb-zls.png'), pos=(292,133), style=wx.NO_BORDER)
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
        self.lnh = wx.StaticLine(self.panel, -1, pos=(415,75))
        self.lnh.SetSize((290,1))

        self.lnv = wx.StaticLine(self.panel, -1, pos=(510,50))
        self.lnv.SetSize((1,460))

### establish the painting surface
##        dc = wx.PaintDC(self.panel)
##        dc.SetPen(wx.Pen('black', 4))
##        # draw a blue line (thickness = 4)
##        dc.DrawLine(450, 70, 450, 70)
##  nalepke
##        self.nalepka1 = wx.StaticText(self.panel, label='Nalepka', pos=(600,20))
        self.naslovBazena = wx.StaticText(self.panel, label='Stanje črpalk po bazenih', pos=(420,15), style=wx.BOLD)
        self.naslovBazena.SetFont(wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD))
        maxStCrpalk=4
        self.C=[]
        for i in range(0,(maxStCrpalk)):
            self.C.append(wx.StaticText(self.panel, label='Č'+str((i+1)), pos=((530+(i*45)),50)))
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
            posY=80+(i*razmikY)
            self.zbIMG.append(wx.BitmapButton(self.panel,(100+self.bazeni.index(item)),wx.Bitmap('zb.png'), pos=(415,(posY+5)), style=wx.NO_BORDER))
            self.itemNalepka.append(wx.StaticText(self.panel, label=str(item), pos=(450,(posY+5))))
            self.itemNalepka[i].SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
            i+=1
            for j in range(0,self.crpalkNaBazen[self.bazeni.index(item)]):
                idCrpalk+=1
                posX=520+(j*razmikX)
                self.bitmapCrpalka.append(wx.StaticBitmap(self.panel,idCrpalk,wx.Bitmap('crp1-n.png'), pos=(posX, posY)))
            self.arrayCrpalk.append([item, self.bitmapCrpalka])
##        print self.itemNalepka[1]
        
        del posX, posY
        
        
##  Tabela stanja objektov in črpalk
##
##        self.myGrid = gridlib.Grid(self.panel, pos=(415,70))
##        self.myGrid.CreateGrid(8, 6)
##        self.myGrid.SetSize((500,600))
##        self.myGrid.SetColLabelSize(20)
##        self.myGrid.SetRowLabelSize(70)
##        self.myGrid.SetDefaultCellBackgroundColour(self.panel.GetBackgroundColour())
##        self.myGrid.EnableDragGridSize(False)
##        self.myGrid.EnableDragColSize(False)
##        self.myGrid.EnableDragRowSize(False)
##        self.myGrid.EnableEditing(False)
##        self.myGrid.SetDefaultCellFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.NORMAL))
##        self.myGrid.SetLabelFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
##
##        img=wx.Bitmap('crp1-u.png', wx.BITMAP_TYPE_PNG)
##        imageRenderer = MyImageRenderer(img)
##        
##        
##        for i in range(2,6):
##            for j in range(0,8):
##                self.myGrid.SetCellRenderer(j,i,imageRenderer)
##                self.myGrid.SetRowSize(j, 70)
####                self.myGrid.SetCellBackgroundColour(j,i,'DARK GREEN')
##
##
##            
##            
##        self.myGrid.SetColSize(0, 50)
##        self.myGrid.SetColLabelValue(0, "Objekt")
##        
##        self.myGrid.SetColSize(1, 100)
##        self.myGrid.SetColLabelValue(1, "Opis")
##
##        self.myGrid.SetColSize(2, 55)
##        self.myGrid.SetColLabelValue(2, "Č1")
##
##        self.myGrid.SetColSize(3, 55)
##        self.myGrid.SetColLabelValue(3, "Č2")
##
##        self.myGrid.SetColSize(4, 55)
##        self.myGrid.SetColLabelValue(4, "Č3")
##
##        self.myGrid.SetColSize(5, 55)
##        self.myGrid.SetColLabelValue(5, "Č4")
##        
##        self.myGrid.SetCellValue(0,0, "ZB-ZL")
##        self.myGrid.SetCellValue(1,0, "ZB-E")
##        self.myGrid.SetCellValue(2,0, "ZB-R")
##        self.myGrid.SetCellValue(3,0, "ZB-D")
##        self.myGrid.SetCellValue(4,0, "ZB-F")
##        self.myGrid.SetCellValue(5,0, "ZB-G")
##        self.myGrid.SetCellValue(6,0, "ZB-L")
##        self.myGrid.SetCellValue(7,0, "ZB-M")
##
##        self.myGrid.SetCellValue(0,1, "Klečka")
##        self.myGrid.SetCellValue(1,1, "Občina")
##        self.myGrid.SetCellValue(2,1, "Kamnikar")
##        self.myGrid.SetCellValue(3,1, "Njiva")
##        self.myGrid.SetCellValue(4,1, "Tržnica")
##        self.myGrid.SetCellValue(5,1, "RTH")
##        self.myGrid.SetCellValue(6,1, "Kešetovo")
##        self.myGrid.SetCellValue(7,1, "Rondo")
        
##  Gumbi
##        wx.Button(self.bitmap, 11, 'Alarm', (50, 130))

##  Dodamo na v sizer
        vbox.Add(self.toolbar, 0, wx.EXPAND)
        vbox.Add(self.panel,1, wx.EXPAND|wx.ALL)
##        self.panel.SetSizer(gs)

    
        
##        self.statusbar = self.CreateStatusBar()

        self.Bind(wx.EVT_TOOL, self.OnQuit, id=2)
        self.Bind(wx.EVT_TOOL, self.ZamenjajIkono, id=1)
##        self.Bind(wx.EVT_BUTTON, self.ZamenjajIkono, id=11)
        self.Bind(wx.EVT_BUTTON, self.ZamenjajIkono, id=12)
##        self.panel.Bind(wx.EVT_MOTION, self.OnRightDown)

        
        self.SetTitle('Komunala Trbovlje - SMS nadzorni center')
        self.SetSizer(vbox)
        self.Show(True)

##    def PrikaziCrpalke(self, bazen, prva, druga, tretja, cetrta):
        ##  Slike črpalk 1, 2, 3, 4
        ##  Stanja: ne obstaja->0, nevtralno->1, napaka->2, OK->3
##        self.bitmapCrpalka1.SetBitmap(wx.Bitmap('crp'+str(prva)+'-u.png'))
##        self.bitmapCrpalka2.SetBitmap(wx.Bitmap('crp'+str(druga)+'-u.png'))
##        self.bitmapCrpalka3.SetBitmap(wx.Bitmap('crp'+str(tretja)+'-u.png'))
##        self.bitmapCrpalka4.SetBitmap(wx.Bitmap('crp'+str(cetrta)+'-u.png'))
        

##    def OnRightDown(self, e):
####        self.PopupMenu(MyPopupMenu(self), e.GetPosition())
##        self.nalepka1.SetLabel(str(e.GetPosition()))

        
    def ZamenjajIkono(self,e):
##        self.toolbar.DeleteTool(1)
##        self.toolbar.EnableTool(3,False)
##        x=self.toolbar.GetToolNormalBitmap(8, wx.Bitmap('zb-gn.png'))
        try:
##            self.naslovBazena.SetLabel('ZB-ZL - Klečka')
##            self.myGrid.SetCellBackgroundColour(0,2,'RED')
            self.arrayCrpalk[0][1][2].SetBitmap(wx.Bitmap('crp2-n.png'))
##            self.PrikaziCrpalke(1,2,3,3,0)
            self.x
            self.toolbar.SetToolNormalBitmap(1, wx.Bitmap('zb-zln.png'))
            self.Timer = wx.Timer(self, wx.ID_OK)
            self.Timer.Start(500)
            self.Bind(wx.EVT_TIMER, self.OnTimer, self.Timer)
            del self.x
        except:
##            self.naslovBazena.SetLabel('Vsi bazeni')
##            self.myGrid.SetCellBackgroundColour(0,2,'DARK GREEN')
            self.arrayCrpalk[0][1][2].SetBitmap(wx.Bitmap('crp1-n.png'))
##            self.PrikaziCrpalke(1,0,0,0,0)
            self.toolbar.SetToolNormalBitmap(1, wx.Bitmap('zb-zl.png'))
            self.Timer.Stop()
            self.zbzlIMG.SetBitmapLabel(wx.Bitmap('zb-zls.png'))
            self.x=''
##        self.myGrid.Refresh()
            
    def OnQuit(self, e):
        self.Close()

    def OnTimer(self,e):
        try:
            self.y
            self.zbzlIMG.SetBitmapLabel(wx.Bitmap('zb-zlsn.png'))
            del self.y
        except:
            self.zbzlIMG.SetBitmapLabel(wx.Bitmap('zb-zls.png'))
            self.y=''
            

def main():
    app=wx.App()
    SmsGUI(None)
    app.MainLoop()

if __name__=='__main__':
    main()

                                     
##app=wx.App()
##window=wx.Frame(None, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE)
##window.Show(True)
##app.MainLoop()
