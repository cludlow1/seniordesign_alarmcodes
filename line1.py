import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

line1df = pd.read_csv('line1.csv')
line2df = pd.read_csv('line2.csv')
line4df = pd.read_csv('line4.csv')
listofdfs = [line1df, line2df, line4df]

def process(line1df):
    def secondspace(x):
        return x.index(' ',x.index(' ')+1)


    line1df['Date'] = pd.to_datetime(line1df['Date'])
    line1df = line1df.sort_values(by = 'Date',ascending = True)
    line1df['AlarmNumber'] = line1df.Code.apply(lambda x: x[:secondspace(x)])

    alarmnumbers = line1df['AlarmNumber'].value_counts().keys().to_list()
    counts = line1df['AlarmNumber'].value_counts().to_list()
    longcode = []
    for num in alarmnumbers:
        for row in line1df['Code']:
            if num in row:
                longcode.append(row[secondspace(row):])
                break

    sumdf = pd.DataFrame(list(zip(longcode,alarmnumbers,counts)),columns = ['longcode','alarmnumbers','counts'])
    return sumdf

numlist = [1,2,4]
j = 0
for i in listofdfs:
    sumdf = process(i)
    sumdf = sumdf.sort_values(by = 'counts',ascending = True)
    y_pos = np.arange(len(sumdf['longcode']))
    yeet = plt.barh(y_pos,sumdf['counts'],align = 'center', alpha = 0.5)
    plt.yticks(y_pos,sumdf['longcode'])
    plt.xlabel('Frequency')
    plt.title('Line ' + str(numlist[j]) + ' Alarm Codes and Frequencies')
    plt.tight_layout()

    #add values
    labels = sumdf['counts']
    for label, rect in zip(labels,yeet.patches):
        width  = rect.get_width()
        yloc = rect.get_y() + rect.get_height() / 2
        plt.annotate(label,xy = (width,yloc),xytext=(0,5),textcoords='offset points',ha = 'center',va = 'top')
    plt.savefig('line' + str(numlist[j]) + '.png')
    plt.clf()
    j+=1
