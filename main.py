import numpy as np
import pandas as pd
from data import data_m
from decode import tool
from nsga2 import ga_m
from multi_opt import mul_op

import time
start =time.perf_counter()
#中间写上代码块


go=mul_op()                          #多目标模块
da=data_m()							     #数据模块
information=da.get_information()     # 数据信息

location_xy=information[0]           #加上配送中心的全部坐标
customers=len(location_xy)
data_m=[5,customers]                #5是配送中心数，customers是所有点个数

data_car=[9.5,241,17,38.5]   #单位运送成本，固定成本，载重,容积
to=tool(data_car,information)       #解码模块
parm_ga=[0.8,0.2]                    #交叉概率，变异概率

ho=ga_m(3,100,parm_ga,go,to,data_m)            #50,100是迭代次数、种群规模，其余上面已经介绍
pareto,pareto_center,pareto_road,fit_every=ho.nsga()   #nsga2的结果

print('pareto：\n',pareto)                   #输出pareto解
index=1
center,road=pareto_center[index],pareto_road[index]   #index等于0是pareto第一个解，其余依次类推
risk,cost=to.decode_tall(road,center)          #计算一下，和pareto对比
print(risk,cost)


car_road,re,aa,RISK,RFC,KFC,KCW,chengben,d_c_center,total_dispose,Total_distance,TC,set1,set2=to.decode(road,center)#解码第一类垃圾的选址、路径等信息
to.print_road(center,car_road,re,aa,RISK,RFC,KFC,KCW,chengben,total_dispose,Total_distance,TC,set1,set2)   #输出结果
to.draw(center,car_road,aa,RISK,RFC,KFC,KCW,re,chengben,d_c_center,Total_distance,TC,set1,set2)            #画路径图，


go.draw_change(fit_every)          #画pareto解的两个目标随迭代次数的变化

go.draw_change2(pareto)

end = time.perf_counter()
print('Running time: %s Seconds'%(end-start))
0
