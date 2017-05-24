# -*- coding: cp1250 -*-
# TiskajZgodovino.pyw

import wx
import time
import MySQLdb as mdb
from time import strftime

import wx.calendar
from wx.html import HtmlEasyPrinting 

class TiskajZgodovino(wx.Frame):
    title='Tiskanje Zgodovine'
    odCasSpr=time.strftime('%m/%d/%y %H:%M:%S')
    doCasSpr=time.strftime('%m/%d/%y %H:%M:%S')
    izbraniBazen='vsi'
    
    
    def __init__(self, *args, **kwargs):
        super(TiskajZgodovino, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        self.name = "OknoTiskanjaZgodovine-%s"%wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Eno okno že imaš odprto, najprej ga zapri.", "ERROR")
            self.Destroy()
            return False

        
    
        self.panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)



##  nalepke
        self.naslovTZ = wx.StaticText(self.panel, label='Tiskaj zgodovino bazena ', pos=(15,15), style=wx.BOLD)
        self.naslovTZ.SetFont(wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD))

## izbira bazena
        self.bazeni=["ZL", "E", "L", "R", "D", "F", "M", "G", "Vsi"]
        self.naslovTZ = wx.StaticText(self.panel, label='Izberi bazen ', pos=(25,50))
        self.cb=wx.ComboBox(self.panel, -1, 'vsi', pos=(150,50), size=(50,50), choices=self.bazeni)

## koledarja
        cal1 = wx.calendar.CalendarCtrl(self.panel, -1, wx.DateTime_Now(), pos = (25, 80),
                                       style=wx.calendar.CAL_SUNDAY_FIRST |
                                       wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.cal1 = cal1

        cal2 = wx.calendar.CalendarCtrl(self.panel, -1, wx.DateTime_Now(), pos = (225, 80),
                                       style=wx.calendar.CAL_SUNDAY_FIRST |
                                       wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.cal2 = cal2
        

## čas
        self.nalCasod = wx.StaticText(self.panel, label='Čas', pos=(25,223))
        self.uraOd = wx.TextCtrl(self.panel, -1, "00", pos=(50, 220), size=wx.Size(25,20))
        self.dvopicje1 = wx.StaticText(self.panel, label=':', pos=(77,220))
        self.minOd = wx.TextCtrl(self.panel, -1, "00", pos=(81, 220), size=wx.Size(25,20))
        self.dvopicje2 = wx.StaticText(self.panel, label=':', pos=(108,220))
        self.sekOd = wx.TextCtrl(self.panel, -1, "00", pos=(112, 220), size=wx.Size(25,20))
        
        self.nalCasdo = wx.StaticText(self.panel, label='Čas', pos=(225,223))
        self.uraDo = wx.TextCtrl(self.panel, -1, "00", pos=(250, 220), size=wx.Size(25,20))
        self.dvopicje3 = wx.StaticText(self.panel, label=':', pos=(277,220))
        self.minDo = wx.TextCtrl(self.panel, -1, "00", pos=(281, 220), size=wx.Size(25,20))
        self.dvopicje4 = wx.StaticText(self.panel, label=':', pos=(308,220))
        self.sekDo = wx.TextCtrl(self.panel, -1, "00", pos=(312, 220), size=wx.Size(25,20))
        
## gumb

        btnTiskaj = wx.Button(self.panel, label='Tiskaj', pos=(50,250), id=300)



##  Dodamo na v sizer
        vbox.Add(self.panel,1, wx.EXPAND|wx.ALL)


        self.SetTitle('Komunala Trbovlje - Tiskanje Zgodovine')
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        self.CenterOnScreen()
        self.SetSize(wx.Size(550, 600))
        self.Refresh()
        self.SetSizer(vbox)

##  Bind Events
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.TiskajZgodovino1(evt), id=300)
        self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged, cal1)
        self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged, cal2)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
                            
       
        self.Show(True)
        return True

    def OnSelect(self, evt):
        item=evt.GetSelection()
        self.izbraniBazen=self.bazeni[item].lower()
        
    def OnCalSelChanged(self, evt):
        self.odCasSpr=self.cal1.GetDate()
        self.doCasSpr=self.cal2.GetDate()

        
    def TiskajZgodovinoSQL(self):
        db4=None
        while db4==None:
            try:
                db4 = mdb.connect('localhost', 'root', '', 'smsc')
            except mdb.Error, e:
                time.sleep(10)
                continue
        
        cursor=db4.cursor()
        if self.izbraniBazen!="vsi":
            poglej_v_bazo4="SELECT * FROM `sms` WHERE `vrsta_objekta`='%s' AND `datum`>'%s' AND `datum`<'%s' ORDER BY `sms`.`datum` DESC" % (self.izbraniBazen, self.odCas, self.doCas)
        else:
            poglej_v_bazo4="SELECT * FROM `sms` WHERE `datum`>'%s' AND `datum`<'%s' ORDER BY `sms`.`datum` DESC" % (self.odCas, self.doCas)

        try:
            cursor.execute(poglej_v_bazo4)
            db4.commit()
        except:
            db4.rollback()
            db4.close()
            
        vrstice4=cursor.fetchall()
        stVrstic4=len(vrstice4)
        db4.close()
        return vrstice4, stVrstic4

       
    def TiskajZgodovino1(self, evt):
        datumOd=time.strftime('%Y-%m-%d',time.strptime(str(self.odCasSpr),'%m/%d/%y %H:%M:%S'))
        datumDo=time.strftime('%Y-%m-%d',time.strptime(str(self.doCasSpr),'%m/%d/%y %H:%M:%S'))
        self.odCas=datumOd+' '+self.uraOd.GetValue()+':'+self.minOd.GetValue()+':'+self.sekOd.GetValue()
        self.doCas=datumDo+' '+self.uraDo.GetValue()+':'+self.minDo.GetValue()+':'+self.sekDo.GetValue()


        vsebinaZaTisk=self.TiskajZgodovinoSQL()
        vrstice=vsebinaZaTisk[0]
        stVrstic=vsebinaZaTisk[1]

        vsebinaZaNaTiskalnik='<table border="1" cellspacing="0" BORDERCOLOR="BLACK"><tr><td><font size="1" face="arial">ZŠ</font></td><td><font size="1" face="arial">Datum in Čas</font></td><td><font size="1" face="arial">PBMV</font></td><td><font size="1" face="arial">Opis</font></td><td><font size="1" face="arial">Črp</font></td><td><font size="1" face="arial">Stanje</font></td><td><font size="1" face="arial">Telefonska</font></td></tr>'
        i=0
        for vrsta in vrstice:
            i+=1
            datum=vrsta[1].strftime('%d.%m.%Y %H:%M:%S')
            if vrsta[5]==1:
                stanje='OK'
            else:
                stanje='Napaka'
                
            vsebinaZaNaTiskalnik+='<tr><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td><td><font size="1" face="arial">%s</font></td></tr>'% (str(i),datum,str(vrsta[2]).upper(),str(vrsta[6]),str(vrsta[4]), stanje, str(vrsta[0]))
        vsebinaZaNaTiskalnik+='</table>'
        vsebinaZaNaTiskalnik+="<p><font size='1' face='arial'>Bazen: %s; Od: %s; Do: %s</font></p>" % (str(self.izbraniBazen), str(self.odCas), str(self.doCas))
                                                                                                                             

        p = Printer()
        p.Print(vsebinaZaNaTiskalnik, "Zgodovina")
        
        

    def onCloseWindow(self, e):
        self.Destroy()

        return 0


class Printer(HtmlEasyPrinting):

    def GetHtmlText(self,text):
        html_text = text.replace('\n\n','<P>')
        html_text = text.replace('\n', '<BR>')
        return html_text

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PrintText(self.GetHtmlText(text),doc_name)

    def PreviewText(self, text, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetHtmlText(text))

