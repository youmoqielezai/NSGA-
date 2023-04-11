import numpy as np
import pandas as pd

# file=('./算例.xlsx')
# Data1=pd.read_excel(file,0,index_col=0) # 读取excel表中的第一个工作表中的所有数据
# w=np.array(Data1)[:,:2] # 读取节点坐标
# demand=np.array(Data1)[:,2:4] # 所有节点的各废物类型的回收量

file=('C:\\Users\\幽默且叻仔\\Desktop\\实际案例.xlsx')
Data1=pd.read_excel(file,0,index_col=0) # 读取excel表中的第一个工作表中的所有数据
w=np.array(Data1)[:,:2].tolist() # 读取节点坐标
demand=np.array(Data1)[:,2:3].tolist() # 所有节点的各废物类型的回收量
volume=np.array(Data1)[:,3:4].tolist()
print(T1)


distance=np.array(pd.read_excel(file,2,index_col=0)).tolist()  # 读取第3个工作表中除去第1行第1列的各点之间的人口数量
T1=np.array(pd.read_excel(file,8,index_col=0)).tolist()     # 读取第4个工作表中除去第1行第1列的各点之间的速度
jtraffic=np.array(pd.read_excel(file,4,index_col=0)).tolist()# 读取第5个工作表中除去第1行第1列的各点之间的事故概率
car_L=np.array(pd.read_excel(file,6,index_col=0)).tolist() # 读取第6个工作表中除去第1行第1列的各点之间的车流量
trans_C=np.array(pd.read_excel(file,6,index_col=0))# 读取第7个工作表中除去第1行第1列的各点之间的通行能力
center=np.array(pd.read_excel(file,1,index_col=0))# 读取第2个工作表中除去第1行第1列的所有数据

print(distance)
center_loadr=center[:,2:4].tolist()   # 回收中心回收各废物类型的容量限制
center_RFC=center[:,3].tolist()       # 回收中心的建设成本
print(center_loadr)
print(center_RFC)


# print(people_M.shape,V_all.shape,error_P.shape,car_L.shape,trans_C.shape)(80*80，80*80，。。。。)
# # print(w.tolist())
# # print(demand.tolist())
# # print()
# # print(w.shape) # （80*2）
# # Distance=np.zeros((w.shape[0],w.shape[0]))  #生成（80*80的全为0的数组）
# # for i in range(w.shape[0]-1):
# # 	for j in range(i+1,w.shape[0],1):
# # 			dis=np.sqrt((w[j][0]-w[i][0])**2+(w[j][1]-w[i][1])**2)
# # 			Distance[i,j]=dis
# # 			Distance[j,i]=dis
# # print(Distance.tolist())     # 生成距离数组
# filename=('./text5.txt')
# def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
#     file = open(filename,'a')
#     s = str(data)
#     file.write(s)
#     file.close()
# text_save(filename,trans_C.tolist())