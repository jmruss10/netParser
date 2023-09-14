#Process NetConfig and pull information. 
import re, argparse

count = 0
def check_line(line):

    global proCheck
    if re.search(r'^prologue', line): proCheck = 1
    if re.search(r'^end_prologue', line):
        proCheck = 0
        return False

    if proCheck == 1: return False
    global count
    firstWord = line.split(' ', 1)[0]
    if firstWord == "process" or firstWord == "protocol":
        if count != 0:
            print("New Data Set with Mismatched Braces")
            return False
        else:
            count += 1
            return True
    else:
        chars = [*line]
        for char in chars:
            if char == "{":
                count += 1
            elif char == "}":
                count -= 1
        return True

def add_to_dict(setting, data, key):
  
    global dataDict

    if setting == "process" or setting == "protocol":
        key = setting + "-" + data
        dataDict[key] = {}
        #print("new Key: " + key)
        return key
    else:
        if key == "NONE": return "ERROR"
        #print("key: " + key + "Settings: " + setting, data)
        dataDict[key][setting] = data

    return key


def get_info(line):
    count=1
    words = line.strip().split(' ')
    setting, data = "",""
    for word in words:
        if word == "{}" and count == 2:
            data == ""
        elif word != "{" and word != "}":
            if count == 1:
                setting = word
                count += 1
            else:
                data = word

    if setting == "": setting = "NONE"
    if data == "": data = "NONE"
    return setting, data


def create_dict():
    workDir = "/home/russjmc/Playground/Python/netconfig"
    workFile = workDir + "/NetConfig"

    fileData = open(workFile)

    #print(fileData)
    global dataDict
    proCheck=0
    key = "NONE"

    with fileData:
        for line in fileData.readlines():
            if check_line(line):
                setting, data = get_info(line)
                if setting == "NONE" and data == "NONE": continue
                #print("setting: " + setting + " data: " + data)
                key = add_to_dict(setting, data, key)


def data_display(dataDict):

    thdList = []
    for key in dataDict.keys():
       if re.search(r'^protocol', key):
            thread = key.split('-')[1]
            thDir = key.split('_')[-1]
            if "FTPPORT" in dataDict[key]:
                typ = "FTP"
                data = dataDict[key]["OBFILESETTEMPLATE"] if thDir == "o" else dataDict[key]["IBFILEMASK"]
                #print(key.split('-')[1] + " " + dataDict[key]["OBFILESETTEMPLATE"])
            elif "PORT" in dataDict[key]:
                typ = "TCP"
                data = dataDict[key]["PORT"]
                #print(key.split('-')[1] + " tcp " + dataDict[key]["PORT"])
            else:
                typ = "NDF"
                data = "Not Defined"

            #thdLine=print(thread.ljust(25, ' ') + thDir.ljust(2, ' ') + typ.ljust(4, ' ') + data)
            thdLine = ((thread.ljust(25, ' ')), (thDir.ljust(2, ' ')), (typ.ljust(4, ' ')), (data))
            thdList.append(thdLine)

    #sorts=args.sort

    thdList=(sorted(thdList, key = lambda x: x[args.sort]))
    for line in thdList: print(line[0],line[1], line[2], line[3])

def main():

    parser = argparse.ArgumentParser(description = "NetConfig Display module")
    parser.add_argument("-s", "--sort", help="Sort by column.", default=1, required=False)
    parser.parse_args()
    args = parser.parse_args()
    print(args.sort)
    sort = args.sort
    print("sort after args: " + str(sort))

    create_dict()
    #print(dataDict)
    data_display(dataDict)

dataDict = {}
sort = 0
#args = lambda: None

main()
