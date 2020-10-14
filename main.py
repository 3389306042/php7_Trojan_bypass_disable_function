
'''
1.程序必须写大部分注释，一些基本语法除外
2.命名使用易理解拼音，eg:shu_ru_kuang

'''

import wx   #导入GUI库，wx是一个写界面比较好的库

class zhu_chuang_kou(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,title="PHP蚊子1.0.0",size=(1000,600))
        self.Center()   #将窗口居中
        panel=wx.Panel(self)    #创建画板
        #创建标题
        #title = wx.StaticText(panel,label='你好',pos=(200,1),size=(-1,-1))
        font = wx.Font(16,wx.DEFAULT,wx.FONTSTYLE_NORMAL, wx.NORMAL)
        #title.SetFont(font)

        #目标文字和输入框
        self.mu_biao = wx.StaticText(parent=panel,label=" 目标 ",pos=(0,3),style=wx.TE_CENTER)
        self.mu_biao.SetFont(font)

        self.mu_biao_shu_ru_kuang=wx.TextCtrl(parent=panel,pos=(70,-1),style=wx.TE_CENTER,value="http://192.168.1.1/",size=(500,-1))
        self.mu_biao_shu_ru_kuang.SetFont(font)

        huo_qu_shell=wx.Button(parent=panel,pos=(800,3),label="获取shell",size=(120,-1))
        huo_qu_shell.SetFont(font)

        '''shui_ping_box = wx.BoxSizer(wx.HORIZONTAL)  # 水平布局
        shui_ping_box.Add(self.mu_biao,proportion=1)
        shui_ping_box.Add(self.mu_biao_shu_ru_kuang,proportion=1,boder=1)
        
        self.panel.SetSizer(    shui_ping_box)

        self.bmps=[
            wx.Bitmap('temp.jpg',wx.BITMAP_TYPE_PNG),
            wx.Bitmap('temp.jpg',BITMA)
        ]'''

def main():
    app = wx.App()
    frame = zhu_chuang_kou(parent=None, id=-1)  # 创建chuang_kou类对象
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()