import time
import os
import uiautomator2 as u2
import easyocr
import multiprocessing
from PIL import Image


PAGE_INDICATOR = {
    "模拟炒股": "com.hexin.plat.android:id/tab_mn",
    "返回": "com.hexin.plat.android:id/title_bar_img",
    "股票多选": "com.hexin.plat.android:id/stockname_tv",
    "关闭按钮1": "com.hexin.plat.android:id/close_btn",
    "确定按钮": "com.hexin.plat.android:id/ok_btn",
}

MAX_COUNT = 1000   # 最大可显示持仓数目，调试用

class THSTrader:
    def __init__(self, serial="emulator-5554") -> None:
        
        self.d =  u2.connect_usb(serial)
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.__back_to_moni_page()

    
    def get_balance(self):
        """ 获取资产 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_holdings_image").click()
        time.sleep(1)
        self.d.swipe(340, 600, 340, 1000)
        time.sleep(1)
        return {
            "总资产": float(self.d(resourceId="com.hexin.plat.android:id/totalasset_value").get_text().replace(",", "")),
            "可用余额": float(self.d(resourceId="com.hexin.plat.android:id/canuse_value").get_text().replace(",", "")),
            "股票市值": float(self.d(resourceId="com.hexin.plat.android:id/totalworth_value").get_text().replace(",", "")),
        }
    
    def get_position(self):
        """ 获取当前持有股票 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_holdings_image").click()
        time.sleep(1)
        i = 0
        first = True
        while True:
#             print(i)
            if i > MAX_COUNT:
                break
            try:
                self.d.xpath(f'//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)  # 滑动后还是找不到才退出
                    first = False
                else:
                    break
        
        count = i
        holdings = []
        for i in range(count):
            holdings.append(self.__ocr_parse_holding(f"tmp{i}.png"))
        
        return holdings
    
    
   
    
    def get_avail_withdrawals(self):
        """ 获取可以撤单的列表 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").click()
        time.sleep(1)
        
        i = 0
        first=True
        while True:
#             print(i)
            if i > MAX_COUNT:
                break
            try:
                self.d.xpath(f'//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)  # 滑动后还是找不到才退出
                    first = False
                else:
                    break
        count = i
        withdrawals = []
        for i in range(count):
            withdrawals.append(self.__ocr_parse_withdrawal(f"tmp{i}.png"))
        
        return withdrawals
    
    
    def withdraw(self, stock_name, t, amount, price):
        """ 撤单 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").click()
        time.sleep(1)
        success = False
        i = 0
        first = True
        while True:
#             print(i)
            if i > MAX_COUNT:
                break
            try:
                self.d.xpath(f'//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                info = self.__ocr_parse_withdrawal(f"tmp{i}.png")
                if (stock_name == info["股票名称"]) and int(amount) == int(info["委托数量"]) \
                        and (abs(float(price) -  float(info["委托价格"])) < 0.01) and (t == info["委托类型"]):
                            self.d.xpath(f'//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i+1}]').click()
                            time.sleep(1)
                            self.d(resourceId="com.hexin.plat.android:id/option_chedan").click()
                            time.sleep(1)
                            success = True
                            break
                
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)  # 滑动后还是找不到才退出
                    first = False
                else:
                    break
        return {
            "success": success
        }

    def buy(self, stock_no, amount, price):
        return self.__imeaction(stock_no, amount, price, "menu_buy_image")
        
    def sell(self, stock_no, amount, price):
        return self.__imeaction(stock_no, amount, price, "menu_sale_image")

    def __imeaction(self, stock_no, amount, price, open_tag):
        """ 买入或者卖出通用 """
        stock_no = str(stock_no)
        amount = str(amount)
        price = str(price)
        success = False
        msg = ""
        stock_name = ""
        while True:
            self.__back_to_moni_page()
            self.d(resourceId=f"com.hexin.plat.android:id/{open_tag}").click()
            self.__input_stock_no(stock_no)
            self.__input_stock_price(price)
            self.__input_stock_buy_count(amount)
            self.d.xpath('//*[@resource-id="com.hexin.plat.android:id/transaction_layout"]/android.widget.LinearLayout[1]').click()
            time.sleep(1)
            if self.__entrust_doubel_check(stock_no, amount, price):
                try:
                    stock_name = self.d(resourceId="com.hexin.plat.android:id/stock_name_value").get_text()
                    self.d(resourceId="com.hexin.plat.android:id/ok_btn").click()
                    time.sleep(1)
                    self.d(resourceId="com.hexin.plat.android:id/content_scroll").screenshot().save(f"tmp.png")
                    msg = self.__ocr_get_full_text()
                    self.d(resourceId="com.hexin.plat.android:id/ok_btn").click()
                    success = True
                    break
                except: 
                    raise
            else:
                self.d(resourceId="com.hexin.plat.android:id/cancel_btn").click()
                time.sleep(2)
                
        if open_tag == "menu_buy_image":
            t = "买入"
        else:
            t = "卖出"
        return {
            "success": success,
            "msg": msg,
            "stock_name": stock_name.replace(" ", ""),
            "amount": amount,
            "price": price,
            "type": t
        }

    def __entrust_doubel_check(self, stock_no, amount, price):
        time.sleep(1)
        if self.d(resourceId="com.hexin.plat.android:id/stock_code_value").get_text().replace(" ", "") != stock_no:
            return False
        
        if self.d(resourceId="com.hexin.plat.android:id/number_value").get_text().replace(" ", "").replace(",", "") != amount:
            return False
        
        price = float(price)
        pnow = float(self.d(resourceId="com.hexin.plat.android:id/price_value").get_text())
        if abs(price - pnow) > 0.01:
            return False
        
        return True

    def __back_to_moni_page(self):
        self.__util_close_other()
        self.d.app_start("com.hexin.plat.android")
        self.d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()
        if self.__util_check_app_page(PAGE_INDICATOR["返回"]):
            try:
                self.d(resourceId="com.hexin.plat.android:id/title_bar_img").click()
            except: pass 

        self.d(resourceId="com.hexin.plat.android:id/tab_mn").click()

           
    
    def __input_stock_no(self, stock_no):
        """ 输入股票ID """
        self.__util_close_other()
        self.d(resourceId="com.hexin.plat.android:id/content_stock").click()
        time.sleep(2)
        self.__util_input_text(stock_no)
        time.sleep(2)
        if self.__util_check_app_page(PAGE_INDICATOR["股票多选"]):
            try:
                self.d.xpath('//*[@resource-id="com.hexin.plat.android:id/recyclerView"]/android.widget.RelativeLayout[1]').click()
            except: pass

    def __input_stock_price(self, price):
        """ 输入股票价格 """
        self.__util_close_other()
        self.d(resourceId="com.hexin.plat.android:id/stockprice").click()
        time.sleep(2)
        self.__util_input_text(price)

    def __input_stock_buy_count(self, buy_count):
        """ 输入股票购买量 """
        self.__util_close_other()
        self.d(resourceId="com.hexin.plat.android:id/stockvolume").click()
        time.sleep(2)
        self.__util_input_text(buy_count)

    def __util_close_other(self):
        time.sleep(1)
        if self.__util_check_app_page(PAGE_INDICATOR["关闭按钮1"]):
            try:
                self.d(resourceId=PAGE_INDICATOR["关闭按钮1"]).click()
            except: pass
        
        if self.__util_check_app_page(PAGE_INDICATOR["确定按钮"]):
            try:
                self.d(resourceId=PAGE_INDICATOR["确定按钮"]).click()
            except: pass

    def __util_input_text(self, text):
        """ 输入工具，uiautomator2的clear_text和send_keys速度好像有点儿慢，所以用了这种方法 """
        self.d.shell("input keyevent 123")
        for _ in range(20):
            self.d.shell("input keyevent 67")
        self.d.shell(f"input text {text}")

    def __util_check_app_page(self, indicator):
        """ 工具，检查页面是否包含某特征 """
        hierachy = self.d.dump_hierarchy()
        if indicator in hierachy:
            return True
        return False
    
    def __ocr_get_full_text(self):
        result = self.reader.readtext("tmp.png")
        text = ""
        for line in result:
            text += line[1]
        return text

    
    def __ocr_parse_holding(self, path):
        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_name = result[0][1]
        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_count = result[0][1]
        Image.open(path).crop((419, 60, 548, 102)).save("tmp.png")
        
        result = self.reader.readtext(f'tmp.png')
        try:
            stock_available = result[0][1]
        except:
            stock_available = "0"
        return {
            "股票名称": stock_name.replace(" ", ""),
            "股票余额": int(stock_count.replace(",", "")),
            "可用余额": int(stock_available.replace(",", ""))
        }
    
    def __ocr_parse_withdrawal(self, path):
        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_name = result[0][1]
        Image.open(path).crop((219, 11, 390, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_price = result[0][1]
        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_count = result[0][1]
        Image.open(path).crop((589, 11, 704, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        t = result[0][1]
        return {
            "股票名称": stock_name.replace(" ", ""),
            "委托价格": float(stock_price.replace(",", "")),
            "委托数量": int(stock_count.replace(",", "")),
            "委托类型": t.replace(" ", "")
        }