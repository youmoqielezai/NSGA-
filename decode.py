import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

class tool():
	def __init__(self,data_car,information):
		self.data_car=data_car
		self.location_xy,self.demand,self.distance,self.jdistance,self.jtraffic=information[0],information[1],information[2],information[3],information[4]
		self.center_load,self.center_RFC,self.volume,self.time1,self.time2,self.time3,self.time4=information[5],information[6],information[7],information[8],information[9],information[10],information[11]
		self.center_DFC,self.pop=information[12],information[13]
# 		self.location_xy,self.demand,self.distance,self.people_M,self.building_M,self.error_P,=information[0],information[1],information[2],information[3],information[4],information[5]#导入数据
# 		self.center_load,self.center_RFC=information[6],information[7]
	def decode(self,road,center):
		car_road=[] #车辆路径编码
        
		center_signal,signal,load_signal=0,0,0#第二个为车辆（染色体）编号
		set1,set2=[],[]
		D=[]#节点距离
		zhixindu=0.85
		d_g_distance=[]
		g_g_distance=[]
		total_distance=[]
		max_load=[]
		c_center=[]#确定建设的候选中心集合
		d_c_center=[]
		total_dispose=[]
		chengben=[]
		RFC=[]
		load_center=[]
		total_demand=sum(self.demand)
		KFC,KCW,RISK,DC=[],[],[],[]  #R分别为车辆固定成本、车辆运输成本、风险
		for i in range(center.shape[0]):
			if (self.time1[center[i]][center[i]]<=30):
				c_center.append(center[i])#确定建设的中心集合
				d_c_center.append(center[i])#确定建设的中心集合
				total_load_c_center=sum(self.center_load[c_center[j]] for j in range(len(c_center)))
				if total_load_c_center>total_demand:
					break
		for i in range(len(c_center)):
			RFC.append(self.center_RFC[c_center[i]])#将建设中心的建设成本添加到成本列表中
			load_center.append(self.center_load[c_center[i]])#确定中心的处理能力
# 		center_dx=c_center[0] #按照顺序挑选中心
# 		load_center=self.center_load[center_dx] #选中编号中心的处理能力
# 		load_up=[load_center]  #load_up代表什么意思？容量上限？
# 		RFC=[self.center_RFC[center_dx]] #选中编号中心的固定建设成本
#		RISK.append(6*10**(-4)*2*3.14*0.8**3*self.jdistance[center_dx][center_dx]*(1+(self.jtraffic[center_dx][center_dx]/1800)**4)/180)#把处置中心的风险添加到其中
		car_load=self.data_car[2]#车辆载重
		car_volume=self.data_car[3] #把中心添加到车辆路径列表中
		KFC.append(self.data_car[1])
		rw,kc=0,0
		dd,aa=[[]],[0]#dd代表车的载重，aa代表车辆数
		total_customers=road.shape[0]
		road=road.tolist()
		road_over=0
		for ii in range(total_customers):   #从客户点集合列表中按顺序挑选添加到车辆路径表中
			if ii==0:
				loc_index=int(road[0])
				for j in range(len(c_center)):
					if self.time1[loc_index][c_center[j]]<=30:
						d_g_distance.append(self.distance[c_center[j]][loc_index])
# 				for j in range(len(c_center)):
# 					d_g_distance.append(self.distance[c_center[j]][loc_index])
				if d_g_distance==[]:
					car_road.append([c_center[0]])
				else:
					min_distance=min(d_g_distance)#确定距离最近的中心编
					d_g_distance=[]#更新距离列表
					for j in range(len(c_center)):
						if(self.distance[c_center[j]][loc_index]==min_distance):
							car_road.append([c_center[j]])
							break
			elif ii>0:
				for i in range(len(road)):
					if self.time1[loc_index][road[i]]<=30:
						g_g_distance.append(self.distance[loc_index][road[i]])
				if g_g_distance==[]:
					loc_index=road[0]
					road_over=1
				else:
					min_distance=min(g_g_distance)#确定距离最近的中心编号
					g_g_distance=[]#更新距离列表
# 					loc_index=self.distance[loc_index].index(min_distance)
					for i in range(len(road)):
						if(self.distance[loc_index][road[i]]==min_distance):
							loc_index=int(road[i])#染色体编号
							break
			if(self.demand[loc_index]>car_load)or(self.volume[loc_index]>car_volume)or(road_over==1):#判断编码的节点需求是否大于车辆剩余载重
				for j in range(len(c_center)):
					if (self.time1[c_center[j]][car_road[signal][-1]]<=30)and(load_center[j]>=self.data_car[2]-car_load):
						d_g_distance.append(self.distance[c_center[j]][car_road[signal][-1]])
				if d_g_distance==[]:
# 					cc.append(car_road[signal][-1])
					max_load=max(load_center)
					jj=load_center.index(max_load)
# 					for j in range(len(c_center)):
# 						if(load_center[j]==max_load):
# 							jj=j
# 							break
					car_road[signal].append(c_center[jj])#车辆回到距离最近的中心
					load=self.data_car[2]-car_load #车辆运往中心的总量
					load_center[jj]-=load #处置中心剩余容量（更新处置中心剩余容量）
# 					if(load_signal==1)or(load_center[0]<2):#如果处置中心剩余容量小于车辆载重，则将该中心移除
# 						total_dispose.append(c_center[0])
# 						total_dispose.append(self.center_load[c_center[0]]-load_center[0])
# 						del c_center[0]#将满容量的处置中心移除建设列表
# 						del load_center[0]
				else:
					min_distance=min(d_g_distance)#确定距离最近的中心编号
					d_g_distance=[]#更新距离列表
# 					j=self.distance[car_road[signal][-1]].index(min_distance)
					for j in range(len(c_center)):
						if(self.distance[c_center[j]][car_road[signal][-1]]==min_distance):
							car_road[signal].append(c_center[j])#车辆回到距离最近的中心
							load=self.data_car[2]-car_load #车辆运往中心的总量
							load_center[j]-=load #处置中心剩余容量（更新处置中心剩余容量）
# 							if(load_signal==1)or(load_center[j]<3):#如果处置中心剩余容量小于车辆载重，则将该中心移除
# 								total_dispose.append(c_center[j])
# 								total_dispose.append(self.center_load[c_center[j]]-load_center[j])
# 								del c_center[j]#将满容量的处置中心移除建设列表
# 								del load_center[j]
# 							break
#				car_road[signal].append(center[center_signal])#车辆回到中心，路径结束
				road_volume=0 #实际道路运输量
				for j in range(len(car_road[signal])-1):#计算风险
						#if road_volume==0:
								#break
						#else:                            
						sig=car_road[signal][j] #取路径表格的第signal个列表中的第i个编码
						svg=car_road[signal][j+1] #取路径表格的第signal个列表中的第i+1个编码
						D=self.distance[sig][svg] #获得节点之间的距离
						T1=self.time1[sig][svg]
						T2=self.time2[sig][svg]
						T3=self.time3[sig][svg]
						T4=self.time4[sig][svg]
						pop=self.pop[sig][svg]
						if(T1<=30):
							rw=road_volume*3.6*10**-7*D*pop*4*T1/(3.14*0.8)
#							rw=0.9*10**-7*3.14*0.8**2*D**2*(T1+T2+T3+T4)/4
							kc=self.data_car[0]*(0.1*road_volume/self.data_car[2]+0.11)*D+0.08*0.83*(0.1*road_volume/self.data_car[2]+0.11)*D
						else:
							set1.append(sig)
							set1.append(svg)
# 						else:
# 							cc.append(sig)
# 							cc.append(svg)
							rw=1000000000
							kc=1000000000
# 						if(0.95*T4+0.05*T3>=30):
# 							set2.append(sig)
# 							set2.append(svg)
						total_distance.append(D)
						RISK.append(rw)
						KCW.append(kc)
						road_volume=road_volume+self.demand[car_road[signal][j+1]]#下段的运量需要加上下一个编号的需求

				rw,kc=0,0
# 				load=self.data_car[2]-car_load #车辆运往中心的总量
# 				load_center-=load #处置中心剩余容量（更新处置中心剩余容量）
# 				if(load_signal==1)or(load_center<self.demand[loc_index]):#如果中心剩余容量小于节点需求
# 					car_road.append([center[center_signal+1]])#将下一个中心编号添加到路径列表中
# 				else:
# 					car_road.append([center[center_signal]])#否则将同样的中心编号添加到路径列表中
				road_over=0
# 				for i in range(len(road)):
# 					loc_index=int(road[i])
# 					for j in range(len(c_center)):
# 						if self.time4[loc_index][c_center[j]]*0.95+0.05*self.time3[loc_index][c_center[j]]<=30:
# 							d_g_distance.append(self.distance[c_center[j]][loc_index])
# 					if d_g_distance!=[]:
# 						break
				loc_index=int(road[0])
				for j in range(len(c_center)):
					if self.time1[loc_index][c_center[j]]<=30:
						d_g_distance.append(self.distance[c_center[j]][loc_index])
				if d_g_distance==[]:
					max_load=max(load_center)
					jj=load_center.index(max_load)
					car_road.append([c_center[jj]])
        # 						if(load_center[j]==max_load):
#         # 							jj=j
#         # 							break
				else:
					min_distance=min(d_g_distance)
					d_g_distance=[]#更新距离列表
					for j in range(len(c_center)):
						if(self.distance[c_center[j]][loc_index]==min_distance):
							car_road.append([c_center[j]])#车辆从最近的中心出发访问下一个开始节点
							break


# 				car_road.append([c_center[0]]) 
				KFC.append(self.data_car[1]) #增加多一辆车的固定成本
				signal+=1
				car_load=self.data_car[2]
				car_volume=self.data_car[3]
				dd.append([])
# 				if(load_signal==1)or(load_center<self.demand[loc_index]):#若中心剩余容量不满足下一个需求
# 					center_signal+=1 #中心编号加1
# 					center_dx=center[center_signal]#选择下一编号的中心
# 					RFC.append(self.center_RFC[center_dx])#并将该编号的中心建设成本添加到成本列表中
# 					#RISK.append(6*10**(-4)*2*3.14*0.8**3*self.jdistance[center_dx][center_dx]*(1+(self.jtraffic[center_dx][center_dx]/1800)**4)/180)#把处置中心的风险添加到其中
# 					load_center=self.center_load[center_dx]#中心剩余容量的赋值
# #					load_up.append(load_center)
# 					load_signal=0
# 					aa.append(signal) #表示每个中心使用的车辆数
# 				if(load_center<self.data_car[2])and(load_signal==0)and(load_center>=self.demand[loc_index]) :#如果处置中心的剩余容量小于车辆的载重，但大于节点需求时，将剩余容量赋给车辆剩余载重
# 					car_load=load_center#车辆载重等于中心剩余容量
# 					load_signal=1
			car_load-=self.demand[loc_index]	#计算车辆剩余载重
			car_volume-=self.volume[loc_index]
			car_road[signal].append(loc_index)#把编号添加到路径的第signal个列表中
			del road[road.index(loc_index)]
			dd[signal].append(self.demand[loc_index])#dd的作用还未知(记录每辆车的载重过程)

			if(ii==total_customers-1):#如果i为最后一个点
				for j in range(len(c_center)):
					if (self.time1[c_center[j]][car_road[signal][-1]]<=30)and(load_center[j]>=self.data_car[2]-car_load):
						d_g_distance.append(self.distance[c_center[j]][car_road[signal][-1]])
				if d_g_distance==[]:
					max_load=max(load_center)
					jj=load_center.index(max_load)
					car_road[signal].append(c_center[jj])#车辆回到距离最近的中心
					load=self.data_car[2]-car_load #车辆运往中心的总量
					load_center[jj]-=load #处置中心剩余容量（更新处置中心剩余容量）
				else:
					min_distance=min(d_g_distance)
					d_g_distance=[]#更新距离列表
					for j in range(len(c_center)):
						if(self.distance[c_center[j]][car_road[signal][-1]]==min_distance):
							car_road[signal].append(c_center[j])#车辆回到距离最近的中心
							load=self.data_car[2]-car_load #车辆运往中心的总量
							load_center[j]-=load #处置中心剩余容量（更新处置中心剩余容量）
							break
# 				min_distance=min(d_g_distance)
# 				d_g_distance=[]#更新距离列表
# 				for j in range(len(c_center)):
# 					if(self.distance[c_center[j]][car_road[signal][-1]]==min_distance):
# 						car_road[signal].append(c_center[j])#车辆回到距离最近的中心
# 						load=self.data_car[2]-car_load #车辆运往中心的总量
# 						load_center[j]-=load #处置中心剩余容量（更新处置中心剩余容量）
# 						break
				for j in range(len(c_center)):
					total_dispose.append(c_center[j])
					total_dispose.append(self.center_load[c_center[j]]-load_center[j])
#				aa.append(len(dd))
# 				car_road[signal].append(center[center_signal])#则将处置中心编号添加到路径列表中，完成初始解的生成
				road_volume=0#以下都是计算风险
				for j in range(len(car_road[signal])-1):#计算风险
						#if road_volume==0:
								#break
						#else:                            
						sig=car_road[signal][j] #取路径表格的第signal个列表中的第i个编码
						svg=car_road[signal][j+1] #取路径表格的第signal个列表中的第i+1个编码
						D=self.distance[sig][svg] #获得节点之间的距离
						T1=self.time1[sig][svg]
						T2=self.time2[sig][svg]
						T3=self.time3[sig][svg]
						T4=self.time4[sig][svg]
						pop=self.pop[sig][svg]
						if(T1<=30):
							rw=road_volume*3.6*10**-7*D*pop*4*T1/(3.14*0.8)
							kc=self.data_car[0]*(0.1*road_volume/self.data_car[2]+0.11)*D+2.3*0.3*(0.1*road_volume/self.data_car[2]+0.11)*D
						else:
							set1.append(sig)
							set1.append(svg)
# 						else:
# 							cc.append(sig)
# 							cc.append(svg)
							rw=1000000000
							kc=1000000000
# 						if(0.95*T4+0.05*T3>=30):
# 							set2.append(sig)
# 							set2.append(svg)
# 						else:
# 							rw=1000000000
# 							kc=1000000000
# 							cc.append(sig)
# 							cc.append(svg)
						RISK.append(rw)
						total_distance.append(D)
						KCW.append(kc)
						road_volume=road_volume+self.demand[car_road[signal][j+1]]#下段的运量需要加上下一个编号的需求
		i=0
		while i <len(total_dispose):
			sig=total_dispose[i]
			svg=total_dispose[i+1]
			T1=self.time1[sig][sig]
			T2=self.time2[sig][sig]
			T3=self.time3[sig][sig]
			T4=self.time4[sig][sig]
			pop=self.pop[sig][sig]
			rw=4*10**-6*pop*svg*T1*2/(0.8)
			dc=svg*self.center_DFC[sig]
			RISK.append(rw)
			DC.append(dc)
			i=i+2
		aa.append(len(dd))
		re=[sum(dd[i]) for i in range(len(dd))]#re为每辆车的处理量
#		re1=[i*0.525 for i in re]
		chengben=sum(KFC)+sum(KCW)+sum(RFC)+sum(DC)
		TC=sum(KCW)
		Total_distance=sum(total_distance)
# 		risk=sum(RISK)
		return car_road,re,aa,RISK,RFC,KFC,KCW,chengben,d_c_center,total_dispose,Total_distance,TC,set1,set2
	def print_road(self,d_c_center,car_road,re,aa,RISK,RFC,KFC,KCW,chengben,total_dispose,Total_distance,TC,set1,set2):
		print('\n医疗废物的选址、[风险、成本】：%s、[%s、%s]\n'%(d_c_center,sum(RISK),chengben))
		print('车辆路径是：%s'%(car_road))
		print('第回收中心的回收量：%s、'%(total_dispose))
		print('\n')
	def draw(self,cent,car_road,aa,RISK,RFC,KFC,KCW,re,chengben,d_c_center,Total_distance,TC,set1,set2):
		for k in range(len(self.location_xy)):
			plt.scatter(self.location_xy[k][0],self.location_xy[k][1],c="red")
			plt.annotate(k,xy=(self.location_xy[k][0],self.location_xy[k][1]),xytext=(self.location_xy[k][0]+0.0005,self.location_xy[k][1]-0.0005))
		for i in range(len(car_road)):
			x=[self.location_xy[j][0] for j in car_road[i]]
			y=[self.location_xy[j][1] for j in car_road[i]]
			plt.plot(x,y,c='blue',linewidth=0.3)
		center=d_c_center
		x=[self.location_xy[j][0] for j in center]
		y=[self.location_xy[j][1] for j in center]
		plt.scatter(x,y,c='blue',label='医疗废物的选址、风险、成本：%s、%.2f、%.2f'%(center,sum(RISK),chengben))		
		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("横坐标",font1)
		plt.title("医疗废物处置中心的最优选址及最优配送方案路线图"%font1)
		plt.ylabel("纵坐标",font1)
		plt.legend(prop={'family':['SimHei'],'size':12})#标签字体大小，可以修改
		plt.show()
	def decode_tall(self,road,center):
		car_road,re,aa,RISK,RFC,KFC,KCW,chengben,d_c_center,total_dispose,Total_distance,TC,set1,set2=self.decode(road,center)
		risk=sum(RISK)
		cost=chengben
		return risk,cost
