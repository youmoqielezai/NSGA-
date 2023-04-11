import numpy as np
import random


class ga_m():
	def __init__(self,generation,popsize,parm_ga,go,to,data_m):
		self.generation=generation          #迭代次数
		self.popsize = popsize  # 种群规模
		self.p1 = parm_ga[0]   # 交叉概率
		self.p2 = parm_ga[1]   # 变异概率
		self.go=go             # 多目标模块
		self.to=to             # 解码模块
		self.cent,self.customers=data_m[0],data_m[1]  # 回收中心，所有节点数
# data_m=[10,customers]                #10是配送中心数，customers是所有点个数
	def road_cross(self,chrom_L1,chrom_L2):		#路径编码的pox交叉
		index=np.random.randint(1,self.customers+1,1)[0] # 随机生成一个1-80的值
		C1,C2=np.zeros((1,chrom_L1.shape[0]),dtype=np.int)-1,np.zeros((1,chrom_L1.shape[0]),dtype=np.int)-1
		sig,svg=[],[]
		for i in range(chrom_L1.shape[0]):#固定位置的路径编码不变
			if(chrom_L1[i]<=index):
				C1[0,i]=chrom_L1[i]
			else:
				sig.append(chrom_L1[i])
			if(chrom_L2[i]<=index):
				C2[0,i]=chrom_L2[i]
			else:
				svg.append(chrom_L2[i])
		signal1,signal2=0,0				#为0的地方按顺序添加路径编码
		for i in range(chrom_L1.shape[0]):
			if(C1[0,i]==-1):
				C1[0,i]=svg[signal1]
				signal1+=1
			if(C2[0,i]==-1):
				C2[0,i]=sig[signal2]
				signal2+=1
		return C1[0],C2[0]
	def Job_vara(self,W1,W2):       #工序的逆序变异
		W1,W2=np.array([W1]),np.array([W2])
		index1=random.sample(range(self.customers),2)
		index2=random.sample(range(self.customers),2)
		index1.sort(),index2.sort();
		L1=W1[:,index1[0]:index1[1]+1]
		L2=W2[:,index2[0]:index2[1]+1]
		W_all=np.zeros((2,W1.shape[1]),dtype=np.int)
		W_all[0],W_all[1]=W1[0],W2[0]
		for i in range(L1.shape[1]):
			W_all[0,index1[0]+i]=L1[0,L1.shape[1]-1-i]  #反向读取工序编码
		for i in range(L2.shape[1]):
			W_all[1,index2[0]+i]=L2[0,L2.shape[1]-1-i]  #反向读取工序编码
		return W_all[0],W_all[1]
	def nsga(self):
		Total_road=np.zeros((self.popsize,self.customers-self.cent),dtype=np.int)  # popsize行 回收点列全为0
		Total_road1=np.zeros((self.popsize,self.customers-self.cent),dtype=np.int) 
		Total_center=np.zeros((self.popsize,self.cent),dtype=np.int)
		Total_center1=np.zeros((self.popsize,self.cent),dtype=np.int)

		answer=[]
		fit_every=[[],[],[],[]]
		for gen in range(self.generation):     # 遍历迭代次数
			if(gen<1):
				for i in range(self.popsize):   # 遍历种群
					center=np.arange(self.cent)  # 生成回收中心0-9集合
					road=np.arange(self.cent,self.customers,1) # 生成废物生产节点10-79集合
					np.random.shuffle(center)    # 打乱回收中心集合顺序
					np.random.shuffle(road)      # 打乱废物生产节点集合顺序
# 					road1=[97,67,9,94,43,8,81,18,59,87,92,53,88,58,66,37,23,56,69,86,21,16,57,36,80,89,19,31,30,39,40,61,65,54,78,29,17,15,60,7,50,93,91,5,71,82,49,62,63,46,32,11,48,38,34,90,73,52,72,10,47,42,35,45,84,41,20,77,14,51,68,95,22,44,27,98,24,99,83,13,6,12,79,70,28,64,85,55,96,76,25,75,26,33,74]
# 					road=np.array(road1)
# 					center1=[1,3,0,4,2]
# 					center=np.array(center1)
					Total_road[i]=road           # 将产生的每个个体放入
					Total_center[i]=center
					risk,cost=self.to.decode_tall(road,center)
					answer.append([risk,cost])  # 生成100个种群规模大小的answer[[risk1,cost1],[risk2,cost2],...]
				
				front,crowd,crowder=self.go.dis(answer)    #计算分层，拥挤度，种群排序结果
				signal=front[0]   # 第一梯队索引值
				pareto=np.array(answer)[signal].tolist()   # 第一梯队目标值
				pareto_center,pareto_road=Total_center[signal],Total_road[signal]  # 第一梯队对应的中心集合和回收点集合
				x=[pareto[i][0] for i in range(len(pareto))]   # 第一梯队风险值
				y=[pareto[i][1] for i in range(len(pareto))]   # 第一梯度成本值
				fit_every[3].append(gen)   #  迭代次数
				fit_every[0].append([min(x),sum(x)/len(x),max(x)])
				fit_every[1].append([min(y),sum(y)/len(y),max(y)])
			index_sort=crowder
            # 选取种群排序结果对应个体的回收中心和需求点集合
			Total_center,Total_road=Total_center[index_sort][0:self.popsize],Total_road[index_sort][0:self.popsize]
			answer=np.array(answer)[index_sort][0:self.popsize].tolist()
			answer1=[]
			for i in range(0,self.popsize,2):
				chrom_L1=Total_road[i]    # 偶数需求点个体
				chrom_L2=Total_road[i+1]  # 奇数需求点个体
				L1,L2=Total_center[i],Total_center[i+1]  # 偶数/奇数回收中心
				if np.random.rand()<self.p1:   # 小于交叉概率
					C1,C2=self.road_cross(chrom_L1,chrom_L2)
					C3,C4=self.road_cross(L1,L2)
				else:
					C1,C2=chrom_L1,chrom_L2
					C3,C4=L1,L2
				if np.random.rand()<self.p2:  
					road1,road2=self.Job_vara(C1,C2)
					center1,center2=self.Job_vara(C3,C4)
				else:
					road1,road2=C1,C2
					center1,center2=C3,C4
				Total_road1[i]=road1
				Total_road1[i+1]=road2
				Total_center1[i]=center1
				Total_center1[i+1]=center2

				risk,cost=self.to.decode_tall(road1,center1)
				answer1.append([risk,cost])
				risk,cost=self.to.decode_tall(road2,center2)
				answer1.append([risk,cost])

			Total_road=np.vstack((Total_road,Total_road1)) #合并父代和子代
			Total_center=np.vstack((Total_center,Total_center1))
			answer=answer+answer1
			front,crowd,crowder=self.go.dis(answer)    #计算分层，拥挤度，种群排序结果
			signal=front[0]
			pareto=np.array(answer)[signal].tolist()
			pareto_center,pareto_road=Total_center[signal],Total_road[signal]
			x=[pareto[i][0] for i in range(len(pareto))]
			y=[pareto[i][1] for i in range(len(pareto))]
			fit_every[3].append(gen)
			fit_every[0].append([min(x),sum(x)/len(x),max(x)])
			fit_every[1].append([min(y),sum(y)/len(y),max(y)])
			print('算法迭代到第 %.0f 次'%(gen+1))
			
		return pareto,pareto_center,pareto_road,fit_every  #返回pareto解及其编码
	