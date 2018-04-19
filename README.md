# THSTrader
通用版同花顺量化交易python API。

## 为什么有这个项目
本来看到了这个[easytrader]()这个项目，不过不知道为什么跑着老崩。于是乎，自己看了一遍easytrader的源码，写了一个自己的版本，懒得提PR给easytrader了，就创建了这个项目。


## 同花顺客户端
### v8.60.64_20170215
#### 说明
代码在master分支。

#### 客户端链接
链接: https://pan.baidu.com/s/1hFLmLljhR6wOCKbTtcoDbw 密码: ng8q

### v8.70.32_20180202
#### 说明
代码在v8.70.32_20180202分支，这个版本的同花顺在复制数据时要输入验证码，这里用K最近邻算法进行识别，稳定性有待测量。
#### 客户端链接
链接: https://pan.baidu.com/s/1wNLOqxQ1CYbl9X3nSsYGTw 密码: h2v3


## 操作接口（API）

首先登陆同花顺客户端，然后打开下单程序。

```
from THSTrader.THSTrader import THSTrader


if __name__ == "__main__":
    trader = THSTrader(r"C:\同花顺软件\同花顺\xiadan.exe")    # 连接客户端

    print(trader.get_balance())                            # 获取当前可用资金

    print(trader.get_position())                           # 获取当前持有的股票

    print(trader.sell("162411", amount=100, price=0.541))  # 卖出股票

    result = trader.buy("162411", amount=100, price=0.541) # 买入股票
    print(result)

    if result["success"] == True:						   # 如果买入下单成功，尝试撤单
        print("撤单测试--->", end="")
        print(trader.cancel_entrust(result["entrust_no"]))
```