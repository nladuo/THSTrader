# THSTrader
量化交易。通用版同花顺客户端的python API。

## 为什么有这个项目
本来看到了这个[easytrader](https://github.com/shidenggui/easytrader)这个项目，不过不知道为什么跑着老崩。于是乎，自己看了一遍easytrader的源码，写了一个自己的版本。


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
### 说明
首先登陆同花顺客户端，然后打开下单程序。

**注意：使用过程中请保证下单程序处于可视状态，不要最小化同花顺客户端。**

### 示例代码
``` python
from THSTrader.THSTrader import THSTrader



if __name__ == "__main__":
    trader = THSTrader(r"C:\同花顺软件\同花顺\xiadan.exe")    # 连接客户端

    print(trader.get_balance())                            # 获取当前可用资金

    print(trader.get_position())                           # 获取当前持有的股票

    print(trader.sell(stock_no="162411", amount=100, price=0.62))   # 卖出股票

    result = trader.buy(stock_no="162411", amount=100, price=0.541) # 买入股票
    print(result)

    if result["success"] == True:	 # 如果买入下单成功，尝试撤单
        print("撤单测试--->", end="")
        print(trader.cancel_entrust(entrust_no=result["entrust_no"]))
```

### 获取当前可用资金
``` python
trader.get_balance()
```
返回：
``` 
{
	'资金余额': 198577.0,
	'可用金额': 197264.69,
	'可取金额': 0.0,
	'股票市值': 2869.4,
	'总资产': 200134.09
}
```
### 获取当前持有的股票
``` python
trader.get_balance()
```
返回：
``` 
[{
	'证券代码': 2024,
	'证券名称': '苏宁易购',
	'股票余额': 100,
	'可用余额': 0,
	'冻结数量': 100,
	'盈亏': -0.31,
	'成本价': 13.123,
	'盈亏比例(%)': -0.02,
	'市价': 13.12,
	'市值': 1312.0,
	'交易市场': '深圳Ａ股',
	'股东帐户': 101106569,
	'实际数量': 100,
	'可申赎数量': 100
}, {
	'证券代码': 162411,
	'证券名称': '华宝油气',
	'股票余额': 2600,
	'可用余额': 2600,
	'冻结数量': 0,
	'盈亏': 134.4,
	'成本价': 0.547,
	'盈亏比例(%)': 9.44,
	'市价': 0.6,
	'市值': 1557.4,
	'交易市场': '深圳Ａ股',
	'股东帐户': 101106569,
	'实际数量': 2600,
	'可申赎数量': 2600
}]
```

### 买入股票
``` python
trader.buy(stock_no="162411", amount=100, price=0.541)
```
返回：
``` 
{
	'success': True,
	'msg': '您的买入委托已成功提交，合同编号：873674677。',
	'entrust_no': '873674677'
}
```

### 卖出股票
``` python
trader.sell(stock_no="162411", amount=100, price=0.62)
```
返回：
``` 
{
	'success': True,
	'msg': '您的卖出委托已成功提交，合同编号：873679996。',
	'entrust_no': '873679996'
}
```


### 买卖撤单
``` python
trader.cancel_entrust(entrust_no="873674677")
```
返回：
``` 
{
	'success': True,
	'msg': '您的撤单委托已成功提交，合同编号：873674677。',
	'entrust_no': '873674677'
}
```

## LICENSE
GPL-3.0
