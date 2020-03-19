import pywinauto
from pywinauto import clipboard
from pywinauto import keyboard
# from .captcha_recognize import captcha_recognize
import pandas as pd
import io
import time


class THSTrader:

    def __init__(self, exe_path=r"C:\同花顺软件\同花顺\xiadan.exe"): 
        print("正在连接客户端:", exe_path, "......")
        self.app = pywinauto.Application().connect(path=exe_path, timeout=10)
        print("连接成功!!!")
        self.main_wnd = self.app.top_window()

    def buy(self, stock_no, price, amount):
        """ 买入 """
        time.sleep(1)
        self.__select_menu(['买入[F1]'])
        return self.__trade(stock_no, price, amount)

    def sell(self, stock_no, price, amount):
        """ 卖出 """
        time.sleep(1)
        self.__select_menu(['卖出[F2]'])
        return self.__trade(stock_no, price, amount)

    def cancel_entrust(self, entrust_no):
        """ 撤单 """
        time.sleep(1)
        self.__select_menu([1])
        self.__select_switch_tab("r")

        cancelable_entrusts = self.__get_grid_data()  # 获取可以撤单的条目
        # print(cancelable_entrusts)

        for i, entrust in enumerate(cancelable_entrusts):
            if str(entrust["合同编号"]) == str(entrust_no):  # 对指定合同进行撤单
                return self.__cancel_by_double_click(i)
        return {"success": False, "msg": "没找到指定订单"}

    def get_balance(self):
        """ 获取资金情况 """
        time.sleep(0.5)
        self.__select_menu([4])
        result = {
            "可用余额": self.main_wnd .window(control_id=0x40E, class_name='Static').window_text()
        }
        time.sleep(0.5)
        self.__select_menu([0])
        self.__select_switch_tab("w")
        df = self.__get_grid_data(is_records=False)
        result["股票市值"] = df["市值"].sum()
        return result
    
    def check_trade_finished(self, entrust_no):
        """ 判断订单是否完成 """
        time.sleep(0.5)
        self.__select_menu(['卖出[F2]'])
        time.sleep(0.5)
        self.__select_menu(['撤单[F3]'])
        cancelable_entrusts = self.__get_grid_data(is_entrust=True)
#        print(cancelable_entrusts)
        for i, entrust in enumerate(cancelable_entrusts):
            if str(entrust["合同编号"]) == str(entrust_no):  # 如果订单未完成，就意味着可以撤单
                if entrust["成交数量"] == 0:
                    return False
        return True

    def get_position(self):
        """ 获取持仓 """
        time.sleep(0.5)
        self.__select_menu([0])
        self.__select_switch_tab("w")
        return self.__get_grid_data()

    def get_today_entrusts(self):
        """ 获取当日委托 """
        time.sleep(0.5)
        self.__select_menu([0])
        self.__select_switch_tab("r")
        return self.__get_grid_data()

    def get_today_trades(self):
        """ 获取当日成交"""
        time.sleep(0.5)
        self.__select_menu([0])
        self.__select_switch_tab("e")
        return self.__get_grid_data()

    def __trade(self, stock_no, price, amount):
        time.sleep(0.5)
        self.main_wnd.window(control_id=0x408, class_name="Edit").set_text(str(stock_no))  # 设置股票代码
        self.main_wnd.window(control_id=0x409, class_name="Edit").set_text(str(price))  # 设置价格
        self.main_wnd.window(control_id=0x40A, class_name="Edit").set_text(str(amount))  # 设置股数目
        time.sleep(0.5)
        self.main_wnd.window(control_id=0x3EE, class_name="Button").click()   # 点击卖出or买入

        time.sleep(0.5)
        self.app.top_window().set_focus()
        self.app.top_window().window(control_id=0x6, class_name='Button').click()  # 确定买入

        time.sleep(0.5)
        self.app.top_window().set_focus()
        result = self.app.top_window().window(control_id=0x3EC, class_name='Static').window_text()

        time.sleep(0.5)
        self.app.top_window().set_focus()
        try:
            self.app.top_window().window(control_id=0x2, class_name='Button').click()  # 确定
        except:
            pass
        return self.__parse_result(result)

    def __get_grid_data(self, is_records=True):
        """ 获取grid里面的数据 """
        self.__click_update_button()
        time.sleep(0.5)
        grid = self.main_wnd.window(control_id=0x417, class_name='CVirtualGridCtrl')
        grid.set_focus()
        time.sleep(0.5)
        pywinauto.keyboard.SendKeys('^c')
        data = clipboard.GetData()
        df = pd.read_csv(io.StringIO(data), delimiter='\t', na_filter=False)
        if is_records:
            return df.to_dict('records')
        else:
            return df

    def __select_switch_tab(self, key):
        self.main_wnd.set_focus()
        time.sleep(0.5)
        pywinauto.keyboard.SendKeys(f'+{key}')
        time.sleep(0.5)

    def __select_menu(self, path):
        """ 点击左边菜单 """
        if r"网上股票" not in self.app.top_window().window_text():
            self.app.top_window().set_focus()
            pywinauto.keyboard.SendKeys("{ENTER}")  
        self.__get_left_menus_handle().get_item(path).click()

    def __get_left_menus_handle(self):
        while True:
            try:
                handle = self.main_wnd.window(control_id=129, class_name='SysTreeView32')
                handle.wait('ready', 2)  # sometime can't find handle ready, must retry
                return handle
            except Exception as ex:
                print(ex)
                pass

    def __click_update_button(self):
        self.app.top_window().window(control_id=0x8016, class_name='Button').click()

    def __cancel_by_double_click(self, row):
        """ 通过双击撤单 """
        x = 50
        y = 50 + 20 * row
        self.app.top_window().window(control_id=0x417, class_name='CVirtualGridCtrl').double_click(coords=(x, y))
        self.app.top_window().window(control_id=0x6, class_name='Button').click()  # 确定撤单
        time.sleep(0.1)
        if "网上股票交易系统5.0" not in self.app.top_window().window_text():
            result = self.app.top_window().window(control_id=0x3EC, class_name='Static').window_text()
            self.app.top_window().window(control_id=0x2, class_name='Button').click()  # 确定撤单
            return self.__parse_result(result)
        else:
            return {
                "success": True
            }

    @staticmethod
    def __parse_result(result):
        """ 解析买入卖出的结果 """
        
        # "您的买入委托已成功提交，合同编号：865912566。"
        # "您的卖出委托已成功提交，合同编号：865967836。"
        # "您的撤单委托已成功提交，合同编号：865967836。"
        # "系统正在清算中，请稍后重试！ "
        
        if r"已成功提交，合同编号：" in result:
            return {
                "success": True,
                "msg": result,
                "entrust_no": result.split("合同编号：")[1].split("。")[0]
            }
        else:
            return {
                "success": False,
                "msg": result
            }

