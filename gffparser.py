import matplotlib.pyplot as plt
import logomaker
import numpy as np
import pandas as pd
import os



def lineParser(line):
    line = line.strip()
    line = line.split("\t")
    a = line[-1]
    a = a.split(";")
    tracts = int(a[1].split("=")[1])
    sequence = a[-1].split("=")[1]
    return (tracts, sequence)
    

def fileParser(file, result):
    for line in file.readlines():
        line = line.strip()
        if line[0] == "#":
            continue
        a = lineParser(line)
        length = len(a[1])
        if length in result.keys():
            result[length].add(a)
        else:
            result[length] = {a}
    return result
# get distribution calculates how many at
def getDistribution(array, length):
    result = {'a': [], 'c': [], 't': [], 'g': []}
    array_len = len(array)
    for i in range(length):
        result['a'].append(0)
        result['c'].append(0)
        result['t'].append(0)
        result['g'].append(0)
        for j in range(array_len):
            val = list(array)[j][1][i]
            result[val][i] += 1
    val1 = pd.Series(result['a'])
    val2 = pd.Series(result['c'])
    val3 = pd.Series(result['t'])
    val4 = pd.Series(result['g'])

    result = {'a': val1, 'c': val2, 't': val3, 'g': val4, "p": pd.Series([ i for i in range(length)])}
    df = pd.DataFrame(result)
    print(df)
    return df
        

def generateBarPlots(dic):
    for key in dic.keys():
        df = getDistribution(dic[key], key)
        df.plot(kind="bar", x="p", y=["a", "t"])
        plt.savefig("length-%d-at.png"%key)
        plt.close()
        df.plot(kind="bar", x="p", y=["c", "g"])
        plt.savefig("length-%d-cg.png"%key)
        plt.close()


def printLenghts(dict):
    size = 0
    for key in dict.keys():
        size += 1
        print("Length %d has %d sequence."% (key,len(dict[key])))
    print("There is total of %d different lengths of repeats"%size)


def createLengthDistribution(dictionary):
    result = {}
    count = 0
    for x, y in dictionary.items():
        size = len(y)
        print(size)
        if size < 7000:
            name = "Other lengths"
        else:
            name = "Length of %d"% x
        if name not in result.keys():
            result[name] = size
        else:
            result[name] += size   
    return (result.keys(), result.values())


if __name__ == '__main__':
    result = {}
    
    f = open("/home/jaroslav/Bioinformatics-thesis/anotations-hg38/all_together.gff", "r")
    result = fileParser(f, result)
    printLenghts(result)
    #printLenghts(g)
    #print(g)
    histogram_data = createLengthDistribution(result)
    plt.pie(histogram_data[1], labels=histogram_data[0], startangle=90, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()
    #getDistribution(g[51], 51 )
    
    #generateBarPlots(g)
    #df = getDistribution(g[37], 37)
    #df.plot(kind="bar", x="p", y=["a", "t"])
    #df.plot(kind="bar", x="p", y=["c", "g"])
    #df.groupby(['p',['a', "t"]]).size().unstack().plot(kind='bar',stacked=True)
    f.close()
    