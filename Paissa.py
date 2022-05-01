import tkinter as tk
from Queryer import Queryer
import ttkbootstrap as ttkbs


# from ttkbootstrap.tableview import Tableview


# import webbrowser


class TopMenu(ttkbs.Frame):
    """
    顶部菜单栏
    """

    def __int__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

    def creat_menu(self):
        """
        服务器选择菜单
        :return: 服务器名称（str）
        """
        self.top_menu = ttkbs.Menu(self.master)
        self.area_server = ttkbs.Menu(master=self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label='服务器', menu=self.area_server)
        self.top_menu.add_command(label='查询历史')
        self.top_menu.add_command(label='关于')
        self.menu_server_niao = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_mao = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_zhu = ttkbs.Menu(self.area_server, tearoff=0)
        self.menu_server_gou = ttkbs.Menu(self.area_server, tearoff=0)
        self.area_server.add_command(label='国服（等待跨大区开放后支持）')
        self.area_server.add_cascade(label='陆行鸟', menu=self.menu_server_niao)
        self.area_server.add_cascade(label='猫小胖', menu=self.menu_server_mao)
        self.area_server.add_cascade(label='莫古力', menu=self.menu_server_zhu)
        self.area_server.add_cascade(label='豆豆柴', menu=self.menu_server_gou)
        self.menu_server_niao.add_command(label='陆行鸟(全区服)', command=lambda: set_server('陆行鸟'))
        self.menu_server_niao.add_command(label='红玉海', command=lambda: set_server('红玉海'))
        self.menu_server_niao.add_command(label='神意之地', command=lambda: set_server('神意之地'))
        self.menu_server_niao.add_command(label='拉诺西亚', command=lambda: set_server('拉诺西亚'))
        self.menu_server_niao.add_command(label='幻影群岛', command=lambda: set_server('幻影群岛'))
        self.menu_server_niao.add_command(label='萌芽池', command=lambda: set_server('萌芽池'))
        self.menu_server_niao.add_command(label='宇宙和音', command=lambda: set_server('宇宙和音'))
        self.menu_server_niao.add_command(label='沃仙曦染', command=lambda: set_server('沃仙曦染'))
        self.menu_server_niao.add_command(label='晨曦王座', command=lambda: set_server('晨曦王座'))
        self.menu_server_zhu.add_command(label='莫古力(全区服)', command=lambda: set_server('莫古力'))
        self.menu_server_zhu.add_command(label='白银乡', command=lambda: set_server('白银乡'))
        self.menu_server_zhu.add_command(label='白金幻象', command=lambda: set_server('白金幻象'))
        self.menu_server_zhu.add_command(label='神拳痕', command=lambda: set_server('神拳痕'))
        self.menu_server_zhu.add_command(label='潮风亭', command=lambda: set_server('潮风亭'))
        self.menu_server_zhu.add_command(label='旅人栈桥', command=lambda: set_server('旅人栈桥'))
        self.menu_server_zhu.add_command(label='拂晓之间', command=lambda: set_server('拂晓之间'))
        self.menu_server_zhu.add_command(label='龙巢神殿', command=lambda: set_server('龙巢神殿'))
        self.menu_server_zhu.add_command(label='梦羽宝境', command=lambda: set_server('梦羽宝境'))
        self.menu_server_mao.add_command(label='猫小胖(全区服)', command=lambda: set_server('猫小胖'))
        self.menu_server_mao.add_command(label='紫水栈桥', command=lambda: set_server('紫水栈桥'))
        self.menu_server_mao.add_command(label='延夏', command=lambda: set_server('延夏'))
        self.menu_server_mao.add_command(label='静语庄园', command=lambda: set_server('静语庄园'))
        self.menu_server_mao.add_command(label='摩杜纳', command=lambda: set_server('摩杜纳'))
        self.menu_server_mao.add_command(label='海猫茶屋', command=lambda: set_server('海猫茶屋'))
        self.menu_server_mao.add_command(label='柔风海湾', command=lambda: set_server('柔风海湾'))
        self.menu_server_mao.add_command(label='琥珀原', command=lambda: set_server('琥珀原'))
        self.menu_server_gou.add_command(label='豆豆柴(全区服)', command=lambda: set_server('豆豆柴'))
        self.menu_server_gou.add_command(label='水晶塔', command=lambda: set_server('水晶塔'))
        self.menu_server_gou.add_command(label='银泪湖', command=lambda: set_server('银泪湖'))
        self.menu_server_gou.add_command(label='太阳海岸', command=lambda: set_server('太阳海岸'))
        self.menu_server_gou.add_command(label='伊修加德', command=lambda: set_server('伊修加德'))
        self.menu_server_gou.add_command(label='红茶川', command=lambda: set_server('红茶川'))
        return self.top_menu


class ModuleLoadPage(ttkbs.Frame):
    def __int__(self, master=None):
        super().__init__(master)
        self.master = master
        self.frame.pack()

    def create_loading_page(self):
        self.frame = ttkbs.Frame(self.master)
        tk.Label(self.frame, text='Loading...', font=20).pack()


class ModuleItemQuery(ttkbs.Frame):
    """
    首页查询界面
    """

    def __int__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack(expand=True, fill="both")

        self.creat_query_box()

    def creat_query_box(self):
        """
        物品查询输入框和查询按钮的界面渲染
        :return: 物品名称（is variable, not str）
        """
        self.query_box = ttkbs.Frame(self)
        self.query_item_name = ttkbs.StringVar()
        self.label1 = ttkbs.Label(master=self.query_box, text='请输入要查询的物品名称：', font=20)
        self.label1.place(x=60, y=150)
        self.entry1 = ttkbs.Entry(master=self.query_box, textvariable=self.query_item_name, font=18)
        self.entry1.place(relx=0.1, y=180, relwidth=0.8, height=60)
        self.commit_botton = ttkbs.Button(master=self.query_box, bootstyle="outline-button", text='查询',
                                          command=self.query_item_id)
        self.commit_botton.place(relx=0.70, y=300)
        self.query_box.pack(expand=True, fill="both")
        return self.query_item_name

    def query_item_id(self):
        """
        绑定在查询按钮的方法，用来查询物品的ID
        物品ID（ [list] ）
        """
        global query_server
        global item_id
        global query_item
        # self.query_box.pack_forget()
        query_item = Queryer(self.query_item_name.get(), query_server)
        item_id = query_item.query_item_id()
        if len(item_id) == 1:
            pass
        else:
            self.create_item_list(item_id)

    def create_item_list(self, item_id):
        self.item_list = ttkbs.Frame(self.master)
        cul = ['item_name', 'item_id']
        self.label2 = ttkbs.Label(master=self.item_list, text='双击物品名称选择要查询的物品', font=20)
        self.label2.place(x=60, y=50)
        self.list_view = ttkbs.Treeview(master=self.item_list, show="headings", columns=cul, selectmode='browse')
        self.list_view.column('item_name', anchor='center')
        self.list_view.column('item_id', width=1, anchor='center')
        self.list_view.heading('item_name', text='物品名称')
        self.list_view.heading('item_id', text='物品ID')
        # coldata = ["物品名称"]
        # self.list_view = Tableview(master=self.master, coldata=coldata, rowdata=item_id, paginated=False,
        #                            searchable=False, )
        self.list_view.place(rely=0.15, relx=0.1, relwidth=0.8, relheight=0.7)
        for item in item_id:
            self.list_view.insert('', index=99999, values=(item['Name'], item['ID']))

    def select_item(self, event):
        pass
        # item = self.list_view.selection()
        # if item:
        #     txt = self.list_view(item[0], 'text')
        #     print(item, '  ', txt)
        # self.list_view.bind('<ButtonRelease-1>', all)


class ModuleHistoryQueryBoard(ttkbs.Frame):
    def __int__(self):
        pass


class ModuleItemDetial(ttkbs.Frame):
    def __int__(self):
        pass


class ModuleSaleList(ttkbs.Frame):
    def __int__(self):
        pass


class ModuleSaleHistory(ttkbs.Frame):
    def __int__(self):
        pass


class ModuleCraftCost(ttkbs.Frame):
    def __int__(self):
        pass


class ModuleRelativeArticles(ttkbs.Frame):
    def __int__(self):
        pass


def set_server(server):
    global status_bar
    global query_server
    query_server = server
    textbox.set('正在查询服务器： %s' % server)


"""
主窗体控制
"""
style = ttkbs.Style(theme="flatly")
root = style.master
root.geometry('1000x700+400+150')
root.minsize(600, 360)
root.title('猴面雀 - FF14市场查询小工具')
root.wm_iconbitmap("Images/ico.ico")

"""
定义公共数据
"""
query_server = '猫小胖'
item_id = []
query_item = None

"""
创建菜单栏，增加选择服务器的功能
"""
menu = TopMenu(master=root)
root.config(menu=menu.creat_menu())

load_page = ModuleLoadPage(master=root)
# load_page.create_loading_page()
ModuleItemQuery(master=root).creat_query_box()
# item_list.create_item_list(item_id)

"""
创建下方状态栏
"""
textbox = tk.StringVar()
textbox.set('正在查询服务器： %s' % query_server)
status_bar = tk.Label(root, textvariable=textbox, anchor='se')
status_bar.pack(side='bottom', fill='x')

root.mainloop()
