# a web service needs to report its state to a target url or IP
import requests
from sys import argv
from os.path import exists
from time import sleep

states = ("Running", "Starting", "Rebooting", "Offline")

def report_status(target, state):
    uri = ""
    s = ""
    dbgmsg = ""
    for c in target:
        # make sure uri is string
        uri += str(c)

    for j in state:
        # make sure state is string
        s += str(j)
    
    if s == "":
        # if state is not initalized earlier, set to starting
        s = "Starting"
    elif s not in states:
        # if state is not in list of known valid states, report the invalid state
        s = "Invalid"
    else:
        pass
    
    if uri != "":
        try:
            p = requests.post(uri, data={"state":s})
            print(p.status_code, s)
        except requests.exceptions.ConnectionError as e:
            dbgmsg = f"host url could not be reached: {uri}"
            print(dbgmsg)
            #print("logging state to file") # Debug
        except requests.exceptions.MissingSchema as m:
            print(f"host url may not have been formatted correctly, please include a valid url ie http://your-url-here : {uri}")

        with open("statelog.txt", 'a+') as f:
            info = str(uri + " " + s + " " + dbgmsg + '\n')
            f.write(info)
        
    return s


if __name__ == "__main__":
    reporting_target = ""
    state = "beenis"
    uri = ""
    if len(argv) < 2:
        print("no host set for reporting, please include target url or IP for reporting in order to recieve monitoring reports.")
    elif len(argv) >= 2:
        uri = str(argv[1])
        reporting_target = uri
    
    while True:
        state = report_status(reporting_target, state)

        if state == "Starting":
            state = "Running"
        elif state == "Invalid":
            state = "Rebooting"
        elif state == "Rebooting":
            state = "Starting"
        elif state == "Running":
            state = "Running"
        else:
            pass

        sleep(3)
    #print(uri, reporting_target, state, "#Debug") #Debug

