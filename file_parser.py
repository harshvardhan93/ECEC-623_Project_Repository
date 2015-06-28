import os
import sys
import csv

file_names = []

for file in os.listdir("./files"):
    file_names.append(file)

print file_names
print "\n"

def sentences(file_name):
    with open(file_name) as f:
       for line in f:
           yield [sentence for sentence in line.strip().split()] 

#all_data = []

for files in file_names:
    if files == '.DS_Store':
        continue
    file_name=files+".csv"
    fptr=open(file_name,'w')    
    data = []
    temp_line=[]
    temp= []
    temp_line1=[]
    temp_line2=[]
    sum_comp=0
    sum_self=0
    sum_local_uq=0
    for line in sentences("./files/" + files):
        if 'Trimming' in line:
            break
        if 'std::' in line:
            continue
        if len(line)==0:
            continue
        if 'Function' in line:
            temp_line.append('')
            temp_line.append('')
            temp_line1.append('')
            temp_line1.append(line[2])
            temp_line2.append(line[14]+line[15])
            temp_line2.append(line[16]+line[17])
            temp_line2.append(line[18]+line[19]+line[20])
            temp_line2.append(line[21]+line[22]+line[23])
            temp_line2.append('')
            temp_line2.append('')
            temp_line2.append('')
            temp_line2.append('')
            temp_line2.append('')
            temp_line2.append('')
            temp.append('Computation')
            temp.append('uqSive')
            temp.append('selfCnt')            
            temp.append('Param_1')
            temp.append('Param 2 uq_local/2^12')
            temp.append('Norm_Computation')
            temp.append("Local_Uq_Norm")
            temp.append('Performance_node')
            temp.append('Application_cpu_cycles')
            temp.append('Local/BW')
            temp.append('CPU Execution Time(ns)')
            temp.append("Acc Execution Time(ns)")
            temp.append("Excess Exec Time")
            temp.append("OBJFCT")
            temp_line.append(line[0] + " " + line[1])
            line = temp_line + temp_line1 + line[3:13] + temp_line2 + temp
        else:
            print files
            comp = int(line[6]) + int(line[7])
            sum_comp = sum_comp + comp
            uq = int(line[10])/4096.0
            if (int(line[13])!=0):
                self = float(line[10])/float(line[13])
            else:
                self = -1000
            if(self!=-1000):
                sum_self=sum_self+self
            sum_local_uq=sum_local_uq+ float(line[10])
            line.append(comp)
            line.append(uq)
            line.append(self)
        data.append(line)

    for each in data:
        if each[25] == "Computation":
            continue
        else: 
            if(each[10] == '0'):
                ans = 0
                each.append(ans)
            else:
                t_comp = (float(each[25])/float(sum_comp))
                ans = ((t_comp/float(each[10])))
                each.append(ans)
            local_uq_norm=(float(each[10])/float(sum_local_uq))        
            temp_ans = ((float(each[10])/float(sum_local_uq))/2**12)
            norm_comp = (float(each[25])/float(sum_comp))
            performance_node=(float(each[0])+10*(float(each[4])+float(each[5])+float(each[6]))+100*(float(each[7])+float(each[8])+float(each[9]))+10*(float(each[11])+float(each[13])))
            app_cpu_cycles=float((performance_node*3)/2.0)
            local_bw=(float(each[13])/21.3)
            cpu_exec_time=(float(local_bw)+float(each[25]))
            acc_exec_time=(float(local_bw)+(float(each[25])*3/2.0))
            excess_exec_time=(float(acc_exec_time)-float(cpu_exec_time))
            objfct=((100*(float(excess_exec_time)/float(cpu_exec_time)))**2)
            each.append(temp_ans)    
            each.append(norm_comp) 
            each.append(local_uq_norm)
            each.append(performance_node)
            each.append(app_cpu_cycles)
            each.append(local_bw)
            each.append(cpu_exec_time)
            each.append(acc_exec_time)
            if excess_exec_time<0:               
                each.append('0')
            else:
                each.append(excess_exec_time)
            each.append(objfct)   
    file_writer = csv.writer(fptr)
    file_writer.writerows(data)
    fptr.close()
