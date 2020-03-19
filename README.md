# THSTrader
量化交易。同花顺免费模拟炒股软件客户端的python API。(Python3)

## 为什么有这个项目
本来看到了这个[easytrader](https://github.com/shidenggui/easytrader)这个项目，不过这个客户端已经过时了(被强制更新)。于是乎，自己看了一遍easytrader的源码，写了一个自己的版本。

## 安装说明
### 同花顺免费模拟炒股软件客户端安装
#### 下载链接
这个版本是模拟炒股软件，但是可以添加不同券商的委托下单程序，是2015年更新的。
版本号：v8.10.44_20151010.
链接：https://pan.baidu.com/s/1H2rIxWZwBx-LuiFlXzc5Jg 提取码：5b15

### python环境安装
``` bash
pip3 install -r requirements.txt
```

## 操作接口（API）
操作演示视频见：[https://www.bilibili.com/video/av46248487/](https://www.bilibili.com/video/av46248487/)

同花顺的安装使用方法：见视频的2p。

### 说明
首先登陆同花顺客户端下载委托程序，下载完退出同花顺客户端，只**打开下单程序**。

**注意：使用过程中请保证下单程序处于可视状态，不要最小化客户端。**

### 示例代码
``` python
from THS.THSTrader import THSTrader


if __name__ == "__main__":
    trader = THSTrader(r"C:\同花顺软件\weituo\模拟炒股\xiadan.exe")    # 连接客户端

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
	'可用余额': 197264.69,
	'股票市值': 2869.4,
}
```
> ** 注意：这里总资产并不是可用余额+股票市值，有一些资金可能代表未成交的金额。 **
### 获取当前持有的股票
``` python
trader.get_position()
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
