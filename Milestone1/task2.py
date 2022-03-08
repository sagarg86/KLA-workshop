import yaml
from yaml.loader import SafeLoader

from datetime import datetime
import time
import threading



with open('Milestone1B.yaml') as fh:

    read_data = yaml.load(fh, Loader=yaml.FullLoader)

temp=open("logfile2.txt","w")
threads=[]

def flow(work, execution, activities):
    now=datetime.now()
    temp.write(f"{now};{work} Entry\n")
    if execution == "Sequential":
        for act in activities:
            if activities[act]['Type']=="Flow":
                newwork=work + '.' + act
                flow(newwork,activities[act]['Execution'],activities[act]['Activities'])
            elif activities[act]['Type']=="Task":
                newwork=work + '.' + act
                task(newwork,activities[act]['Function'],activities[act]['Inputs'])
    elif execution == "Concurrent":
        for act in activities:
            if activities[act]['Type']=="Flow":
                newwork=work+ '.' +act
                thread=threading.Thread(target=flow,args=[newwork,activities[act]['Execution'], activities[act]['Activities']])
                thread.start()
                threads.append({thread,newwork})
            elif activities[act]['Type']=="Task":
                newwork=work+ '.' +act
                thread=threading.Thread(target=task,args=[newwork,activities[act]['Function'], activities[act]['Inputs']])
                thread.start()
                threads.append({thread,newwork})    
            now=datetime.now()
            for thread in threads:
                thread.join()
            temp.write(f"{now};{work}.{act} Exit \n")

def task(work,function,inputs):
    if function =='TimeFunction':
        fun_input=inputs['FunctionInput']
        exc_time=inputs['ExecutionTime']
        now= datetime.now()
        temp.write(f"{now};{work} Entry \n")
        temp.write(f"{now};{work} Executing {function} ({fun_input}, {exc_time})\n")
        time.sleep(int(exc_time))
        now= datetime.now()
        temp.write(f"{now};{work} Exit \n")


for work in read_data:
    if read_data[work]['Type']=="Flow":
        flow(work,read_data[work]['Execution'],read_data[work]['Activities'])
    elif read_data[work]['Type']=="Task":
        task(work,read_data[work]['Function'],read_data[work]['Inputs'])
  
