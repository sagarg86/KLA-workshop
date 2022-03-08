import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import time



with open('Milestone1A.yaml') as fh:

    read_data = yaml.load(fh, Loader=yaml.FullLoader)

temp=open("logfile1.txt","w")

def flow(work, execution, activities):
    if execution == "Sequential":
        for act in activities:
            now=datetime.now()
            temp.write(f"{now};{work}.{act} Entry\n")
            if activities[act]['Type']=="Flow":
                newwork=work + '.' + act
                flow(newwork,activities[act]['Execution'], activities[act]['Activities'])
            elif activities[act]['Type']=="Task":
                newwork=work + '.' + act
                task(newwork,activities[act]['Function'], activities[act]['Inputs'])
            now=datetime.now()
            temp.write(f"{now};{work}.{act} Exit \n")

def task(work,function,inputs):
    if function =='TimeFunction':
        fun_input=inputs['FunctionInput']
        exc_time=inputs['ExecutionTime']
        now= datetime.now()
        temp.write(f"{now};{work} Executing{function} ({fun_input},{exc_time})\n")
        time.sleep(int(exc_time))

for work in read_data:
    now=datetime.now()
    temp.write(f"{now};{work} Entry\n")
    if read_data[work]['Type']=="Flow":
        flow(work,read_data[work]['Execution'],read_data[work]['Activities'])
    elif read_data[work]['Type']=="Task":
        task(work,read_data[work]['Function'],read_data[work]['Inputs'])
    now=datetime.now()
    temp.write(f"{now};{work} Exit")



