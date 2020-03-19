# -*- coding: utf-8 -*-

from THS.THSTrader import THSTrader
import time

if __name__ == "__main__":
    trader = THSTrader(r"C:\同花顺软件\同花顺免费模拟炒股软件\weituo\模拟炒股\xiadan.exe")    # 连接客户端

    print(trader.get_balance())                            # 获取当前可用资金

    print(trader.get_position())                           # 获取当前持有的股票

    print(trader.sell(stock_no="162411", amount=100, price=0.238))  # 卖出股票

    result = trader.buy(stock_no="162411", amount=100, price=0.218)  # 买入股票
    print(result)
    time.sleep(5)
    if result["success"] == True:						   # 如果买入下单成功，尝试撤单
        print("撤单测试--->", end="")
        print(trader.cancel_entrust(entrust_no=result["entrust_no"]))

