from http import cookies
import easytrader
from scrapy import getData
from send import send_message

def ranking(df,condition1='premium_rt'):
    NUM = 10
    df = df.sort_values(by=condition1,ascending=True)[:NUM]
    return df

def fa(x):
  if x.startswith('110') or x.startswith('113'):
    return 'SH' + x
  if x.startswith('123') or x.startswith('127') or x.startswith('128'):
    return 'SZ' + x

def getName(data):
  result = map(fa,data)
  result = list(result)
  return result

def is_not_empty(s):
    return s and len(s.strip()) > 0
    
# 指定雪球
user = easytrader.use('xq')
# 初始化信息
user.prepare(
  cookies='device_id=bcffa4f5bde5109e6bd563dbee92085b; s=dg15btnbrl; bid=2a430e784436d90c894fa77e3fed0d71_l6emd53p; __utmz=1.1659592402.1.1.utmcsr=ww2.ezhai.net.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=1; __utma=1.877784686.1659592402.1660297801.1660551276.4; acw_tc=276077a016624538471903731e5b0bf14fa94af503b617af33e3abee7ecdab; Hm_lvt_1db88642e346389874251b5a1eded6e3=1660274508; xq_a_token=d2637d30668603f25aafbfbb74621fc107ff35a9; xqat=d2637d30668603f25aafbfbb74621fc107ff35a9; xq_r_token=d1bf8df154985532e6a2eedbd66a9b58ff7e9a8b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjg2NzQ2MDE2MDYsImlzcyI6InVjIiwiZXhwIjoxNjY1MDQ1ODY2LCJjdG0iOjE2NjI0NTM4NjY0MDIsImNpZCI6ImQ5ZDBuNEFadXAifQ.e3OApPbN3O1uKfyAJYuMqmqx3QHi62wKA01vix89IfAH_M1y9vlyWBp76dUimaDfuO-C4WQWWTbVx5husSf3QW1wEYWh0ZOxsunVX2uqE41pTedjaWUJd9lz6-RSZp0_ueQ77X9jj8lmt5TE7cmWVV21bIVwyh-fyJSKxz0yVZY0EGylQJmxViMzCPA_s97S1Yt9kaaFGkGmfAZsliD5EdYdH03hDJ4WIOhryP9lvyMij9gALka6911rFSuvQKz8QsMP6EDbllE6uXQBhKpmwDm2rrtx2uxzKDj0gPklVfgx8R6_eErsmDt2GRbkrGZSWe7QJargXfg40NobLLZRcg; xq_is_login=1; u=8674601606; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1662453882',
  portfolio_code='ZH2476354',  
  portfolio_market='cn'
)
# 打印账户
# print(user.balance)
# print(user.position,'position')
currentData = list(map(lambda x:x['stock_code'],user.position))
# 打印持仓
# print(user.position)
df = getData()
df = ranking(df)
dfName = list(df['bond_nm'])
df = list(filter(is_not_empty,getName(list(df['bond_id']))))

removeData = list(set(currentData).difference(set(df)))
buyData =  list(set(df).difference(set(currentData)))
 
for x in removeData:
  user.adjust_weight(x, 0)
for x in df:
  user.adjust_weight(x, 10)

userId = ['SuWei','DanErShenYang','BaoChiBengGan','MaoXiaoMao','life']

text1 = " 组合收益率: %.2f%% \n 组合雪球链接 %s \n 今日卖出: %s \n 今日买进: %s \n 当前持仓: %s" % (user.balance[0]['asset_balance'] / 10000,'https://xueqiu.com/P/ZH2476354',','.join(removeData),','.join(buyData),','.join(dfName))
for item in userId:
  send_message(text1,item)



