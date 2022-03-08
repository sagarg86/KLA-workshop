import yaml
import threading
import time
import datetime
import pandas as pd

configurationFile = "DataSet\Milestone2\Milestone2B.yaml"
logFile = "Milestone2B.txt"

Output = dict()

def TimeFunction(name, input):
    inp = input.get("FunctionInput")
    if inp[0] == "$":
        while not inp in Output.keys():
            time.sleep(0.2)
        inp = Output[inp]
    with open(logFile,"a") as log:
        log.write(str(datetime.datetime.now())+";"+name+" Entry\n"+str(datetime.datetime.now())+";"+name+" Executing TimeFunction ({},{})\n".format(inp,input.get("ExecutionTime")))
    time.sleep(int(input.get('ExecutionTime')))
    with open(logFile,"a") as log:
        log.write(str(datetime.datetime.now())+";"+name+" Exit\n")

def DataLoad(name,input):
    with open(logFile,"a") as log:
        log.write(str(datetime.datetime.now())+";"+name+" Entry\n"+str(datetime.datetime.now())+";"+name+" Executing DataLoad ({})\n".format(input.get("Filename"),input.get("ExecutionTime")))
    DataFrame = pd.read_csv("DataSet/Milestone2/"+input.get("Filename"))
    res = [DataFrame,len(DataFrame)]
    with open(logFile,"a") as log:
        log.write(str(datetime.datetime.now())+";"+name+" Exit\n")
    return res

def Task_Manager(name,description,Output):
    if description.get('Condition') is not None:
        statement,oper,val = description.get('Condition').split(' ')
        while not statement in Output.keys():
            time.sleep(0.2)
        if oper == ">":
            if not(Output[statement] > int(val)):
                with open(logFile,"a") as log:
                    log.write(str(datetime.datetime.now())+";"+name+" Entry\n"+str(datetime.datetime.now())+";"+name+" Skipped\n"+str(datetime.datetime.now())+";"+name+" Exit\n")
                return
        elif oper == "<":
            if not(Output[statement] < int(val)):
                with open(logFile,"a") as log:
                    log.write(str(datetime.datetime.now())+";"+name+" Entry\n"+str(datetime.datetime.now())+";"+name+" Skipped\n"+str(datetime.datetime.now())+";"+name+" Exit\n")
                return

    if description.get('Function') == "TimeFunction":
        TimeFunction(name,description.get('Inputs'))
    elif description.get('Function') == "DataLoad":
        res = DataLoad(name,description.get('Inputs'))
        Output["$("+name+".NoOfDefects)"] = res[1]
        print(Output)

def Flow_Manager(name,description):
    threadList = []
    if description.get('Type') == "Task":
        Task_Manager(name,description,Output)
    elif description.get('Type') == "Flow" and description.get('Execution') == "Sequential":
        with open(logFile,"a") as log:
            log.write(str(datetime.datetime.now())+";"+name+" Entry\n")
        for key,value in description['Activities'].items():
            Flow_Manager(name+"."+key,value)
        with open(logFile,"a") as log:
            log.write(str(datetime.datetime.now())+";"+name+" Exit\n")
    elif description.get('Type') == "Flow" and description.get('Execution') == "Concurrent":
        with open(logFile,"a") as log:
            log.write(str(datetime.datetime.now())+";"+name+" Entry\n")
        for key,value in description['Activities'].items():
            threadList.append(threading.Thread(target=Flow_Manager,args=(name+"."+key,value)))
        for t in threadList:
            t.start()
        for t in threadList:
            t.join()
        with open(logFile,"a") as log:
            log.write(str(datetime.datetime.now())+";"+name+" Exit\n")

if __name__ == "__main__":
    with open(configurationFile,"r") as conf:
        configuration = yaml.load(conf,Loader=yaml.Loader)
    for key,value in configuration.items():
        Flow_Manager(key,value)