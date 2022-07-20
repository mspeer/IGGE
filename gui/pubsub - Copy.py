import wx
from wx.lib.pubsub import pub 
 
########################################################################
class thmbDetailFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Thumbnail Detail View")
        panel = wx.Panel(self)

        pub.subscribe(self.myListener, "panelListener")
 
           #----------------------------------------------------------------------
    def myListener(self, message, arg2=None):
        """
        Listener function
        """
        print "thmbDetailFrame: Received the following message: " + message
        if arg2:
            print "thmbDetailFrame: Received another arguments: " + str(arg2)
 
   
########################################################################
class thmbGridPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
     
        btn = wx.Button(self, label="Open Thumbnail Detail View")
        btn.Bind(wx.EVT_BUTTON, self.onOpenthmbDetailFrame)

    #----------------------------------------------------------------------
    def onOpenthmbDetailFrame(self, event):
        """
        Opens secondary frame
       """
        frame = thmbDetailFrame()
        frame.Show()
 
#        msg = self.msgTxt.GetValue()
        msg = 'taskID: 6896'
        pub.sendMessage("panelListener", message=msg)
        pub.sendMessage("panelListener", message="test2", arg2="2nd argument!")
        self.Close()

     
 
########################################################################
class thmbGridFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Thumbnail Grid View")
        panel = thmbGridPanel(self)
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = thmbGridFrame()
    app.MainLoop()
