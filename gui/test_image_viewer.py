import os
import wx
import MySQLdb as mdb

class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Thumbnail Detail View')
 
        self.panel = wx.Panel(self.frame)
 
 #       self.PhotoMaxSize = 240
 
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        img = wx.EmptyImage(460,215)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        self.gnameLbl = wx.StaticText(self.panel, label='Game Name:')
        self.gnameTxt = wx.TextCtrl(self.panel, size=(200,-1), style=wx.TE_READONLY)
        self.taskIDLbl = wx.StaticText(self.panel, label='TaskID:')
        self.taskIDTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
        self.fdateLbl = wx.StaticText(self.panel, label='Finished Date:')
        self.fdateTxt = wx.TextCtrl(self.panel, size=(160,-1), style=wx.TE_READONLY)
        self.rdateLbl = wx.StaticText(self.panel, label='Release Date:')
        self.rdateTxt = wx.TextCtrl(self.panel, size=(160,-1), style=wx.TE_READONLY)
        self.imgWLbl = wx.StaticText(self.panel, label='Width (460px):')
        self.imgWTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
        self.imgHLbl = wx.StaticText(self.panel, label='Height (215px):')
        self.imgHTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
        self.imgAspectLbl = wx.StaticText(self.panel, label='Aspect Ratio W/H (2.14):')
        self.imgAspectTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
        self.pathLbl = wx.StaticText(self.panel, label='Local Path:')
        self.pathTxt = wx.TextCtrl(self.panel, size=(500,-1), style=wx.TE_READONLY)
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        approveBtn = wx.Button(self.panel, label='Approve')
        approveBtn.Bind(wx.EVT_BUTTON, self.onApprove)
        rejectBtn = wx.Button(self.panel, label='Reject')
        rejectBtn.Bind(wx.EVT_BUTTON, self.onReject)
        cancelBtn = wx.Button(self.panel, label='Cancel')
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
        addCommentBtn = wx.Button(self.panel, label="Add Comment")
        addCommentBtn.Bind(wx.EVT_BUTTON, self.onAddComment)
        self.commentLbl = wx.StaticText(self.panel, label='Comments:')
        self.commentTxt = wx.TextCtrl(self.panel, size=(500,250), style=wx.TE_MULTILINE|wx.TE_READONLY)


        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.head1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.head2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.head3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.head4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cntrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.commentSizer = wx.BoxSizer(wx.VERTICAL)
        self.footerSizer = wx.BoxSizer(wx.VERTICAL)


        self.head1Sizer.Add(self.gnameLbl, 0, wx.ALL, 5)
        self.head1Sizer.Add(self.gnameTxt, 0, wx.ALL, 5)
        self.head1Sizer.Add(self.taskIDLbl, 0, wx.ALL, 5)
        self.head1Sizer.Add(self.taskIDTxt, 0, wx.ALL, 5)
        self.head2Sizer.Add(self.fdateLbl, 0, wx.ALL, 5)
        self.head2Sizer.Add(self.fdateTxt, 0, wx.ALL, 5)
        self.head2Sizer.Add(self.rdateLbl, 0, wx.ALL, 5)
        self.head2Sizer.Add(self.rdateTxt, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgWLbl, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgWTxt, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgHLbl, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgHTxt, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgAspectLbl, 0, wx.ALL, 5)
        self.head3Sizer.Add(self.imgAspectTxt, 0, wx.ALL, 5)

        self.imgSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        self.footerSizer.Add(self.pathLbl, 0, wx.ALL, 5)
        self.footerSizer.Add(self.pathTxt, 0, wx.ALL, 5)
        
        self.cntrlSizer.Add(approveBtn, 0, wx.ALL, 5)
        self.cntrlSizer.Add(rejectBtn, 0, wx.ALL, 5)
        self.cntrlSizer.Add(cancelBtn, 0, wx.ALL, 5)
        self.cntrlSizer.Add(addCommentBtn, 0, wx.ALL, 5)
        self.cntrlSizer.Add(browseBtn, 0, wx.ALL, 5)

        self.commentSizer.Add(self.commentLbl, 0, wx.ALL, 5)
        self.commentSizer.Add(self.commentTxt, 0, wx.ALL, 5)

        self.mainSizer.Add(self.head1Sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.head2Sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.head3Sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.head4Sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.imgSizer, 0, wx.ALL, 5)   
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.footerSizer, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.cntrlSizer, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)        
        self.mainSizer.Add(self.commentSizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onBrowse(self, event):
        self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
        self.cursor = self.conbe.cursor()
        self.taskid = 6852
        self.env = 'Dev'
        sql = 'SELECT DISTINCT tbltitles.name, tbltitles.finisheddate, tbltitles.releasedate, tbltitles.rank, tbltitles.thmb_vis_verified, tbltitles.comment FROM tbltitles \
                WHERE tbltitles.gameID=%s \
                ORDER by tbltitles.titleID DESC'
        args = ([self.taskid]) 
        self.cursor.execute(sql,args)
        row = self.cursor.fetchone()
        gname = row[0]
        fdate = row[1]
        rdate = row[2]
        if gname.find(':') or gname.find('/'):
            for ch in [':','/']:
                if ch in gname:
                    gname = gname.replace(ch,"")
        thmbpath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + self.env + '\\' + gname + '\\RTM\\' + str(self.taskid) + '\\thumbnail\\' + str(self.taskid) + '.jpg'
 
        if gname:
            self.gnameTxt.SetValue(gname)
            self.gnameTxt.SetBackgroundColour((0,255,0))
        else:
            self.gnameTxt.SetValue('Missing Value')
            self.gnameTxt.SetBackgroundColour((255,0,0))
        if self.taskid:
            self.taskIDTxt.SetValue(str(self.taskid))
            self.taskIDTxt.SetBackgroundColour((0,255,0))
        else:
            self.taskIDTxt.SetValue('Missing Value')
            self.taskIDTxt.SetBackgroundColour((255,0,0))
        if fdate:
            self.fdateTxt.SetValue(fdate)
            self.fdateTxt.SetBackgroundColour((0,255,0))
        else:
            self.fdateTxt.SetValue('Mising Value')
            self.fdateTxt.SetBackgroundColour((255,255,0))
        if rdate:
            self.rdateTxt.SetValue(rdate)
            self.rdateTxt.SetBackgroundColour((0,255,0))
        else:
            self.rdateTxt.SetValue('Missing Value')
            self.rdateTxt.SetBackgroundColour((255,0,0))
        if thmbpath:    
            self.pathTxt.SetValue(thmbpath)
            self.pathTxt.SetBackgroundColour((0,255,0))
        else:
            self.pathTxt.SetValue('Missing Path')
            self.pathTxt.SetBackgroundColour((255,0,0))
        self.renderImage()

    def onApprove(self, event):
        sql = 'UPDATE tbltitles SET thmb_vis_verified = 1 WHERE gameID=%s'
        args = (self.taskid)
        try:
            self.cursor.execute(sql, [args])
            self.conbe.commit()
        except mdb.Error, e:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    def onReject(self, event):
        sql = 'UPDATE tbltitles SET thmb_vis_verified = 0 WHERE gameID=%s'
        args = (self.taskid)
        try:
            self.cursor.execute(sql, [args])
            self.conbe.commit()
        except mdb.Error, e:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    def onCancel(self, event):
        pass

    def onAddComment(self, event):
        pass
 
    def renderImage(self):
        filepath = self.pathTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        AR = W/float(H)
        AR = '%.2f'%round(AR,2)
        self.imgHTxt.SetValue(str(H))
        self.imgWTxt.SetValue(str(W))
        self.imgAspectTxt.SetValue(str(AR))
        if W == 460:
            self.imgWTxt.SetBackgroundColour((0,255,0))
        else:
            self.imgWTxt.SetBackgroundColour((255,255,0))
        if H == 215:
            self.imgHTxt.SetBackgroundColour((0,255,0))
        else:
            self.imgHTxt.SetBackgroundColour((255,255,0))
        if AR == 2.14:
            self.imgAspectTxt.SetBackgroundColour((0,255,0))
        else:
            self.imgAspectTxt.SetBackgroundColour((255,255,0))
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
