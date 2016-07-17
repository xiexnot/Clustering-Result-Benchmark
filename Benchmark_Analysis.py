import os
import sys
from collections import Counter

#input_helper
def input_helper():
	try:
		if sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == '--help' or sys.argv[1] == '-help':
			return False
	except:
		return False
	try:
		global label_filename
		global clustering_filename
		global Output_Feature
		label_filename = sys.argv[1]
		clustering_filename = sys.argv[2]
		Output_Feature = sys.argv[3]
		return True
	except:
		return False

def Print_Related_Information():
	print "Format: python [python's filename] [label's filename] [clustering result's filename] [Output's Feature(just for printing)]"
	print "label's filde: the label "
	#print "clustering result's file: the first line indicates the components we selected(e.g. [0], [0,1,2])"
	return 0

def Read_Files():
	global label_filename
	global Label
	print "Reading Label File..."
	label_input = open(label_filename,'rU')
	Label = label_input.read()
	if Label[len(Label)-1]=="\n":
		Label = Label[:-1]
	Label = Label.split('\n')
	print "len of Label = ",len(Label)
	print "label[len(label)-1] = ",Label[len(Label)-1]
	label_input.close()
	print "done..."
	global clustering_filename
	global Cluster
	cluster_input = open(clustering_filename,'rU')
	Cluster = cluster_input.read()
	Cluster = Cluster.split('\n')
	if Cluster[0][0] == '[':
		Cluster = Cluster[1:]
	if Cluster[len(Cluster)-1] == "":
		Cluster = Cluster[:-1]
	for i in range(len(Cluster)):
		try:
			Cluster[i] = int(Cluster[i])
		except:
			print "ERROR=",i," ",Cluster[i]
			while True:
				pass
	cluster_input.close()
	print "len of Cluster = ",len(Cluster)
	
def FindinList(item,totalList):
	for i in range(len(totalList)):
		if str(item) == str(totalList[i]):
			#print item," = ", totalList[i]
			return i
	return -1

def FindMaxPosition(x):
	target = 0
	for i in range(len(x)):
		if x[i] > x[target]:
			target = i
	return target
	
def Calculating_Average(x):
	sum = 0.0
	for i in range(len(x)):
		sum += float(x[i])
	return sum/float(len(x))

def Calculating_Precision(BM, BM_Flag):
	Precision = []
	TP = []
	FP = []
	for i in range(len(BM[0])):
		Precision.append(0.0)
		TP.append(0)
		FP.append(0)
	for j in range(len(BM[0])):
		TP[j] = 0
		FP[j] = 0
		for i in range(len(BM)):
			if BM_Flag[i][j]==True:
				TP[j] += BM[i][j]
			else:
				FP[j] += BM[i][j]
		Precision[j] = float(TP[j])/(float(TP[j])+float(FP[j]))			
	return Precision
	
def Calculating_Recall(BM, BM_Flag):
	Recall = []
	TP = []
	FN = []
	for i in range(len(BM)):
		TP.append(0)
		FN.append(0)
		Recall.append(0)
	for i in range(len(BM)):
		TP[i] = 0
		FN[i] = 0
		for j in range(len(BM[i])):
			if BM_Flag[i][j] == True:
				TP[i] += BM[i][j]
			else:
				FN[i] += BM[i][j]
		Recall[i] = float(TP[i]) / (float(TP[i])+float(FN[i]))
	return Recall

def Calculating_Accuracy(BM, BM_Flag):
	Accuracy = 0
	Sum = 0
	for i in range(len(BM)):
		for j in range(len(BM[i])):
			if BM_Flag[i][j] == True:
				Accuracy += BM[i][j]
			Sum += BM[i][j]
	Accuracy = float(Accuracy) / float(Sum)
	return Accuracy

def Calculating_Benchmark():
	global Cluster, Cluster_List
	global Label, Label_List
	global BM, BM_Flag
	global Precision, Recall
	global Recall_ave, F1_Score_ave, Precision_ave, Accuracy_ave
	
	# BM = Benchmark
	# BM[i][j] ith clustering result and jth label
	#in andy's program :
	#	x = Counter(feature[n])
	#	xx = sorted(list(x))
	Label_Count = Counter(Label)
	Cluster_Count = Counter(Cluster)
	print "label's counting = ",Label_Count
	Label_List = sorted(list(Label_Count))
	#print "label's list = ",Label_List
	Cluster_List = list(Cluster_Count)
	print "Cluster's counting = ", Cluster_Count
	#print "Cluster's list = ",Cluster_List
	BM = []
	BM_Flag = []
	for i in range(len(Cluster_List)):
		BM_Line = []
		BM_Flag_Line = []
		for i in range(len(Label_List)):
			BM_Line.append(0)
			BM_Flag_Line.append(False)
		BM.append(BM_Line)
		BM_Flag.append(BM_Flag_Line)
	
	print "Calculating Appearance..."
	Pairs = []
	for i in range(len(Label)):
		target_cluster = FindinList(Cluster[i],Cluster_List)
		target_label = FindinList(Label[i],Label_List)
		BM[int(target_cluster)][int(target_label)] += 1
	print "Calculating Appearance...done..."
	
	print "Calculating Benchmark..."
	for i in range(len(Cluster_List)):
		BM_Flag[i][FindMaxPosition(BM[i])] = True
	Recall = Calculating_Recall(BM, BM_Flag)
	Precision = Calculating_Precision(BM, BM_Flag)
	Accuracy_ave = Calculating_Accuracy(BM, BM_Flag)
	Recall_ave = Calculating_Average(Recall)
	Precision_ave = Calculating_Average(Precision)
	F1_Score_ave = 2*Precision_ave*Recall_ave / (Precision_ave + Recall_ave)
	#print "Recall = ", Recall
	#print "Precision = ", Precision
	print "Ave of Recall = ", Recall_ave
	print "Ave of Precision = ", Precision_ave
	print "Ave of Accuracy = ",Accuracy_ave
	print "Ave of F1-Score = ", F1_Score_ave 
	print "Calculating Benchmark...done..."
	return 0

def Output_Result():
	global BM
	global Cluster_List, Label_List
	global Accuracy_ave, Precision_ave, F1_Score_ave, Recall_ave
	global Recall, Precision
	global Output_Feature
	Output_File = open("Benchmark_Analysis_"+Output_Feature,"w")
	Output_File.write("cluster\label")
	for i in range(len(Label_List)):
		Output_File.write("\t"+Label_List[i])
	Output_File.write("\t"+"Recall"+"\n")
	for i in range(len(BM)):
		Output_File.write(str(Cluster_List[i]))
		for j in range(len(BM[i])):
			Output_File.write('\t'+str(BM[i][j]))
		Output_File.write("\t"+str(Recall[i]))
		Output_File.write('\n')
	Output_File.write("Precision")	
	for i in range(len(Precision)):
		Output_File.write("\t"+str(Precision[i]))
	Output_File.write("\n")
	print >> Output_File,"*************************"
	print >> Output_File, "Ave of Recall = \t", Recall_ave
	print >> Output_File, "Ave of Precision = \t", Precision_ave
	print >> Output_File, "Ave of Accuracy = \t", Accuracy_ave
	print >> Output_File, "Ave of F1-Score = \t", F1_Score_ave 
	Output_File.close()
	return 0

#-------------------------main------------------------

if input_helper() == True:
	pass
else:
	Print_Related_Information()
	exit()
Read_Files()
Calculating_Benchmark()
Output_Result()
