#!/usr/bin/env python
# coding: utf-8

# ## MFQ 스케줄링 기법 구현
# ### 3개의 RQ를 갖는 MFQ 스케줄링 기법 구현
# 
# - Q0: Time quantum 2인 RR 스케줄링 기법 사용
# 
# - Q1: Time quantum 2인 RR 스케줄링 기법 사용 
# 
# - Q2: FCFS 스케줄링 기법 사용

# ### Import library 

# In[130]:


import numpy as np
import pandas as pd


# ### Process class 정의

# - 각 프로세스는 id, arrive_time, burst_time, tt, wt, priority를 속성으로 가짐 

# In[131]:


class Process:
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.tt = 0  ## turn around time 작업이 끝나는 시간
        self.wt = 0  ## waiting time 기다린 시간
        self.priority = 0
        
    def __repr__(self):
        return('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))


# ### Input data를 불러오는 함수 정의 

# - txt를 파일을 불러와 각각의 object를 Project class로 변환 후 리스트에 저장

# In[132]:


def read_input(input_file):
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    
    return result


# ### Example
# - 8개의 프로세스이며 각각의 프로세스는 arrive_time과 burst_time을 속성으로 갖는다
# - 또한, process 클래스에서 각 프로세스의 초기 tt와 wt와 priority는 0으로 설정하였다

# In[133]:


read_input("input1.txt")


# ### Queue class를 정의

# - 일반적인 Queue class를 정의하되 추가적으로 time quantum을 속성으로 갖도록 설정함

# In[134]:


class Queue():
    def __init__(self, quantum):
        self.items = []
        self.quantum = quantum

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()


# ### Simulate 함수 정의 (MFQ Scheduling)

# 함수의 구현 과정은 다음과 같다
# 
# 1) current_time(현재시간)을 설정하고 초기 input data 중 arrival time이 currenet_time과 같은 프로세스를 꺼내서 Q0에 넣는다.(Q0에 넣은 프로세스는 input data에서 삭제한다) 단, 해당되는 process가 존재하지 않으면 current_time을 +1 한다.
# 
# 2) Q0, Q1, Q2에 들어있는 프로세스를 처리하는 경우에는 Q0을 먼저 확인하고 Q0에 존재하는 프로세스를 작업한다. Q0이 비어있으면 Q1을 확인하고 Q1에 존재하는 프로세스를 작업하고 Q1 역시 비어있으면 Q2에 존재하는 프로세스의 작업을 진행한다.
# 
# 3) 또한, Q0에서 진행된 작업은 처리 후 Q1으로 보내고, Q1에서 진행된 작업은 처리 후 Q2로 보낸다
# 
# 4) 최종적으로 input data, Q0, Q1, Q2 모두가 빈 상태가 될 때까지 이 과정을 반복한다. 그리고 각 프로세스에 대해서 waiting time을 계속해서 수정하고 최종적으로 프로세스가 마무리되는 시기에 turn around time을 설정한다.

# In[136]:


def simulate():
    schedule = []  ## schedule 리스트에 프로세스의 id, 작업이 시작되는 시간과 끝나는 시간, 작업이 진행되는 큐의 위치(Q0인지, Q1인지, Q2인지)에 대한 정보를 저장한다. 
    current_time = 0
    process_result = []  ## input data가 Q0로 들어갈 경우 이를 input data에서 삭제하는 방식을 이용하였기에 해당 프로세스에 대한 정보를 새로운 리스트에 저장

    while(not ((len(process_list) == 0) & (Q0.isEmpty()) & (Q1.isEmpty()) & (Q2.isEmpty()))):
        ## input data와 Q0, Q1, Q2 모두가 비어있는 상태가 될 때까지 작업을 반복
        
        temp = []
        
        ## current time과 arrive_time을 비교해서 해당되는 프로세스를 Q0에 입력
        
        for process in process_list:
            if(process.arrive_time <= current_time):
                process.wt = process.wt + current_time - process.arrive_time
                
                Q0.enqueue(process)
                temp.append(process)
        
        ## 다음과 같은 방식으로 해당 요소를 삭제한 이유는 위의 과정에서 Q0에 입력된 프로세스를 바로 삭제하는 경우 리스트의 순서가 바뀌어서 옳지 못한 결과값이 산출되는 문제가 발생하였고 이를 해결하기 위해 아래와 같은 방식으로 제거
        for tp in temp:
            process_list.remove(tp)
        
        
        
        ## 먼저 Q0를 살펴본 후 그 안에 프로세스가 존재하면 이 프로세스 처리 먼저 진행한다.
        if(Q0.isEmpty() != True):    
            processing = Q0.dequeue()
            
            ## time quantum이 2이고, burst_time이 1인 경우 작업은 1만큼만 진행되는 반면 time quantum이 2이고, burst_time이 3인 경우에는 작업이 2만큼 진행된다. 즉, 이와 같이 두 가지 경우를 나눠 진행
            if(processing.burst_time > Q0.quantum):
                schedule.append((processing.id, current_time, current_time + Q0.quantum, "Q0"))
                
                processing.burst_time = processing.burst_time - Q0.quantum
                current_time = current_time + Q0.quantum
                
                ## 기다리는 process의 waiting time 수정
                for process in Q0.items:
                    process.wt = process.wt + Q0.quantum
                for process in Q1.items:
                    process.wt = process.wt + Q0.quantum
                for process in Q2.items:
                    process.wt = process.wt + Q0.quantum
                
                Q1.enqueue(processing)
                
            else:
                schedule.append((processing.id, current_time, current_time + processing.burst_time, "Q0"))
                
                
                ## 기다리는 process의 waiting time 수정
                for process in Q0.items:
                    process.wt = process.wt + processing.burst_time
                for process in Q1.items:
                    process.wt = process.wt + processing.burst_time
                for process in Q2.items:
                    process.wt = process.wt + processing.burst_time
                
                ## 작업 중인 process 처리
                current_time = current_time + processing.burst_time
                processing.burst_time = 0
                
                processing.tt = current_time
                process_result.append(processing)
                

        ## Q0에 존재하는 프로세스가 모두 처리되면 Q1을 처리한다.
        elif(Q1.isEmpty() != True):
            processing = Q1.dequeue()
            
            if(processing.burst_time > Q1.quantum):
                schedule.append((processing.id, current_time, current_time + Q1.quantum, "Q1"))
                
                processing.burst_time = processing.burst_time - Q1.quantum
                current_time = current_time + Q1.quantum
                
                ## 기다리는 process의 waiting time 수정
                for process in Q1.items:
                    process.wt = process.wt + Q1.quantum
                for process in Q2.items:
                    process.wt = process.wt + Q1.quantum
                    
                Q2.enqueue(processing)
            else:
                schedule.append((processing.id, current_time, current_time + processing.burst_time, "Q1"))
                
                
                ## 기다리는 process의 waiting time 수정
                for process in Q1.items:
                    process.wt = process.wt + processing.burst_time
                for process in Q2.items:
                    process.wt = process.wt + processing.burst_time
                
                
                ## 작업 중인 process 처리
                current_time = current_time + processing.burst_time
                processing.burst_time = 0
                
                processing.tt = current_time
                process_result.append(processing)

        ## Q0과 Q1 모두 처리되면 Q2를 처리한다.
        elif(Q2.isEmpty() != True):
            processing = Q2.dequeue()
                
            schedule.append((processing.id, current_time, current_time+processing.burst_time, "Q2"))
            
            ## 기다리는 process의 waiting time 수정
            for process in Q2.items:
                process.wt = process.wt + processing.burst_time
            
            ## 작업 중인 process 처리
            current_time = current_time + processing.burst_time
            processing.burst_time = 0
            
            processing.tt = current_time
            process_result.append(processing)
        else:
            current_time = current_time + 1
            
    return(schedule, process_result)


# ### Simulation & Result

# - 다양한 입력에 대한 실행 결과를 제시한다

# ### 1) simulation1

# In[137]:


Q0 = Queue(2)
Q1 = Queue(4)

## Q2의 경우 어차피 time quantum을 뒤의 과정에서 사용하지 않으므로 time quantum에 임의의 수 설정
Q2 = Queue(0)

process_list = read_input("input1.txt")
process_list


# In[138]:


schedule, process_result = simulate()


# In[139]:


pd.DataFrame(schedule, columns=["process_id","current_time","end_time","where?"])


# 위의 결과를 해석해보면 process1이 current_time이 0일 때 Q0에서 current_time이 2가 될 때까지 진행됨을 의미한다.
# 그 다음으로 process2가 2부터 4까지 Q0에서 진행되고 다음에 prcoess3가 4에서 6까지 Q0에서 작업된다. 그 뒤 과정 역시 동일하다.

# In[140]:


for process in process_result:
    print("Process_id:",process.id, "Process_tt:", process.tt, "Process_wt:", process.wt)


# 각 프로세스에 대한 turn around time과 waiting time은 위와 같다

# In[141]:


turn_around = []
waiting_time = []

for process in process_result:
    turn_around.append(process.tt)
    waiting_time.append(process.wt)
    
print("average Turnaround time::",np.mean(turn_around))
print("average Waiting time:",np.mean(waiting_time))


# 전체 프로세스의 평균 TT 및 평균 WT는 위와 같다

# ### 2) simulation2

# In[142]:


Q0 = Queue(2)
Q1 = Queue(4)
Q2 = Queue(0)

process_list = read_input("input2.txt")
process_list


# In[143]:


schedule, process_result = simulate()
pd.DataFrame(schedule, columns=["process_id","current_time","end_time","where?"])


# In[144]:


for process in process_result:
    print("Process_id:",process.id, "Process_tt:", process.tt, "Process_wt:", process.wt)


# In[145]:


turn_around = []
waiting_time = []

for process in process_result:
    turn_around.append(process.tt)
    waiting_time.append(process.wt)
    
print("average Turnaround time::",np.mean(turn_around))
print("average Waiting time:",np.mean(waiting_time))


# ### 3) simulation3

# In[146]:


Q0 = Queue(2)
Q1 = Queue(4)
Q2 = Queue(0)

process_list = read_input("input3.txt")
process_list


# In[147]:


schedule, process_result = simulate()
pd.DataFrame(schedule, columns=["process_id","current_time","end_time","where?"])


# In[148]:


turn_around = []
waiting_time = []

for process in process_result:
    turn_around.append(process.tt)
    waiting_time.append(process.wt)
    
print("average Turnaround time::",np.mean(turn_around))
print("average Waiting time:",np.mean(waiting_time))


# ### 4) simulation4

# In[149]:


Q0 = Queue(2)
Q1 = Queue(4)
Q2 = Queue(0)

process_list = read_input("input4.txt")
process_list


# In[150]:


schedule, process_result = simulate()
pd.DataFrame(schedule, columns=["process_id","current_time","end_time","where?"])


# In[151]:


turn_around = []
waiting_time = []

for process in process_result:
    turn_around.append(process.tt)
    waiting_time.append(process.wt)
    
print("average Turnaround time::",np.mean(turn_around))
print("average Waiting time:",np.mean(waiting_time))


# ### 5) simulation5

# In[152]:


Q0 = Queue(2)
Q1 = Queue(4)
Q2 = Queue(0)

process_list = read_input("input5.txt")
process_list


# In[153]:


schedule, process_result = simulate()
pd.DataFrame(schedule, columns=["process_id","current_time","end_time","where?"])


# In[154]:


turn_around = []
waiting_time = []

for process in process_result:
    turn_around.append(process.tt)
    waiting_time.append(process.wt)
    
print("average Turnaround time::",np.mean(turn_around))
print("average Waiting time:",np.mean(waiting_time))

