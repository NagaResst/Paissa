import tkinter as tk

import ttkbootstrap as ttkbs


class TopMenu(tk.Frame):
    def __int__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

    def creat_menu(self):
        self.top_menu = ttkbs.Menu(self.master)
        self.area_server = ttkbs.Menu(master=self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label='服务器', menu=self.area_server)
        self.top_menu.add_command(label='查询历史')
        self.top_menu.add_command(label='关于')
        self.menu_server_niao = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_mao = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_zhu = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_gou = ttkbs.Menu(self.area_server, tearoff=0)
        self.area_server.add_cascade(label='陆行鸟', menu=self.menu_server_niao)
        self.area_server.add_cascade(label='猫小胖', menu=self.menu_server_mao)
        self.area_server.add_cascade(label='莫古力', menu=self.menu_server_zhu)
        self.area_server.add_cascade(label='豆豆柴', menu=self.menu_server_gou)
        self.menu_server_niao.add_command(label='陆行鸟', command=lambda: set_server('陆行鸟'))
        self.menu_server_niao.add_command(label='红玉海', command=lambda: set_server('红玉海'))
        self.menu_server_niao.add_command(label='神意之地', command=lambda: set_server('神意之地'))
        self.menu_server_niao.add_command(label='拉诺西亚', command=lambda: set_server('拉诺西亚'))
        self.menu_server_niao.add_command(label='幻影群岛', command=lambda: set_server('幻影群岛'))
        self.menu_server_niao.add_command(label='萌芽池', command=lambda: set_server('萌芽池'))
        self.menu_server_niao.add_command(label='宇宙和音', command=lambda: set_server('宇宙和音'))
        self.menu_server_niao.add_command(label='沃仙曦染', command=lambda: set_server('沃仙曦染'))
        self.menu_server_niao.add_command(label='晨曦王座', command=lambda: set_server('晨曦王座'))
        self.menu_server_zhu.add_command(label='莫古力', command=lambda: set_server('莫古力'))
        self.menu_server_zhu.add_command(label='白银乡', command=lambda: set_server('白银乡'))
        self.menu_server_zhu.add_command(label='白金幻象', command=lambda: set_server('白金幻象'))
        self.menu_server_zhu.add_command(label='神拳痕', command=lambda: set_server('神拳痕'))
        self.menu_server_zhu.add_command(label='潮风亭', command=lambda: set_server('潮风亭'))
        self.menu_server_zhu.add_command(label='旅人栈桥', command=lambda: set_server('旅人栈桥'))
        self.menu_server_zhu.add_command(label='拂晓之间', command=lambda: set_server('拂晓之间'))
        self.menu_server_zhu.add_command(label='龙巢神殿', command=lambda: set_server('龙巢神殿'))
        self.menu_server_zhu.add_command(label='梦羽宝境', command=lambda: set_server('梦羽宝境'))
        self.menu_server_mao.add_command(label='猫小胖', command=lambda: set_server('猫小胖'))
        self.menu_server_mao.add_command(label='紫水栈桥', command=lambda: set_server('紫水栈桥'))
        self.menu_server_mao.add_command(label='延夏', command=lambda: set_server('延夏'))
        self.menu_server_mao.add_command(label='静语庄园', command=lambda: set_server('静语庄园'))
        self.menu_server_mao.add_command(label='摩杜纳', command=lambda: set_server('摩杜纳'))
        self.menu_server_mao.add_command(label='海猫茶屋', command=lambda: set_server('海猫茶屋'))
        self.menu_server_mao.add_command(label='柔风海湾', command=lambda: set_server('柔风海湾'))
        self.menu_server_mao.add_command(label='琥珀原', command=lambda: set_server('琥珀原'))
        self.menu_server_gou.add_command(label='豆豆柴', command=lambda: set_server('豆豆柴'))
        self.menu_server_gou.add_command(label='水晶塔', command=lambda: set_server('水晶塔'))
        self.menu_server_gou.add_command(label='银泪湖', command=lambda: set_server('银泪湖'))
        self.menu_server_gou.add_command(label='太阳海岸', command=lambda: set_server('太阳海岸'))
        self.menu_server_gou.add_command(label='伊修加德', command=lambda: set_server('伊修加德'))
        self.menu_server_gou.add_command(label='红茶川', command=lambda: set_server('红茶川'))
        return self.top_menu


class ModuleLoadPage(tk.Frame):
    def __int__(self):
        pass


class ModuleIndex(tk.Frame):
    def __int__(self):
        return None


class ModuleItemList(tk.Frame):
    def __int__(self):
        pass


class ModuleItemDetial(tk.Frame):
    def __int__(self):
        pass


class ModuleSaleList(tk.Frame):
    def __int__(self):
        pass


class ModuleSaleHistory(tk.Frame):
    def __int__(self):
        pass


class ModuleCraftCost(tk.Frame):
    def __int__(self):
        pass


class ModuleRelativeArticles(tk.Frame):
    def __int__(self):
        pass


def set_server(server):
    global query_server
    query_server.set(server)


style = ttkbs.Style(theme="flatly")
root = style.master
root.geometry('1400x800+200+150')
root.title('猴面雀 - FF14市场查询小工具')
query_server = tk.StringVar()
query_server.set('猫小胖')
menu = TopMenu(master=root)
root.config(menu=menu.creat_menu())
select_server = ttkbs.Label(root, textvariable=query_server)
select_server.pack()
root.mainloop()
print(query_server)
