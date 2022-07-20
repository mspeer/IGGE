import wx
from wx.lib.pubsub import pub 
 
########################################################################
class OtherFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Secondary Frame")
        panel = wx.Panel(self)

        pub.subscribe(self.myListener, "panelListener")
 
           #----------------------------------------------------------------------
    def myListener(self, message, arg2=None):
        """
        Listener function
        """
        print "OtherFrame: Received the following message: " + message
        if arg2:
            print "OtherFrame: Received another arguments: " + str(arg2)
 
   
########################################################################
class MyPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
     
        btn = wx.Button(self, label="Open Frame")
        btn.Bind(wx.EVT_BUTTON, self.onOpenFrame)

    #----------------------------------------------------------------------
    def onOpenFrame(self, event):
        """
        Opens secondary frame
       """
        frame = OtherFrame()
        frame.Show()
 
#        msg = self.msgTxt.GetValue()
        msg = 'MyPanel: This is my message to pass to new form'
        pub.sendMessage("panelListener", message=msg)
        pub.sendMessage("panelListener", message="test2", arg2="2nd argument!")
        self.Close()

     
 
########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="New PubSub API Tutorial")
        panel = MyPanel(self)
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
