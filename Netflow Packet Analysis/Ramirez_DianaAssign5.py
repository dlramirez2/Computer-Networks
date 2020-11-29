import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def average_pktSize():
    sum_pkts = df['dpkts'].sum()
    sum_bytes = df['doctets'].sum()
    return sum_bytes/sum_pkts


def linear_flowGraph(df, type, column1, column2):
    index = 0
    temp_arr = []
    x = []
    y = []
    while index < df.shape[0]:
        value1 = df._get_value(index, column1)
        value2 = df._get_value(index, column2)
        index = index + 1
        if(column1 == 'dpkts'):
            mean = value2/value1
            temp_arr.append(mean)
        else:
            diff = value2 - value1
            temp_arr.append(diff)

    min_dur = min(temp_arr)
    max_dur = max(temp_arr)
    points = np.arange(min_dur, max_dur, 300)
    for p in points:
        x.append(p)
        n = 0
        for d in temp_arr:
            if d >= p:
                n = n + 1
        fx = n/len(temp_arr)
        y.append(fx)

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(type + ' Linear graph')
    plt.show()


def log_flowGraph(df, type, column1, column2):
    index = 0
    temp_arr = []
    x = []
    y = []

    while index < df.shape[0]:
        value1 = df._get_value(index, column1)
        value2 = df._get_value(index, column2)
        index = index + 1
        if(column1 == 'dpkts'):
            mean = value2/value1
            temp_arr.append(mean)
        else:
            diff = value2 - value1
            temp_arr.append(diff)

    min_val = min(temp_arr)
    max_val = max(temp_arr)
    points = np.arange(min_val, max_val, 300)
    for p in points:
        if(p > 0):
            x.append(math.log(p))
        else:
            x.append(0)
        n = 0
        for d in temp_arr:
            if d >= p:
                n = n + 1
        fx = n/len(temp_arr)
        y.append(fx)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('log(x)')
    plt.title(type + ' Logarithmic graph')
    plt.show()


def top10_traffic(portColumn, sum_bytes):
    grouped = df.groupby([portColumn], as_index=False)['doctets'].sum()
    grouped = grouped.sort_values(['doctets'], ascending=False)
    group_arr = grouped.head(10).to_numpy()
    i = 0
    prct_arr = []
    while i < 10:
        # Calculating the percentage of total traffic
        prct_arr.append((group_arr[i][1]/sum_bytes)*100)
        i = i+1

    print('Src--Total_Bytes-----Percent')
    i = 0
    for x in group_arr:
        for c in x:
            print(c, "   ", end=" ")
        print("{:.2f}".format(prct_arr[i]), "%")
        i = i+1
        print()


def traffic_fromIP(df, percent, columnName, sum_bytes):
    prct = percent / 100
    ips = df[columnName].value_counts()
    total_occurrences = ips.size
    num_to_show = round(prct * total_occurrences)
    ips = df.groupby([columnName])['doctets'].agg(
        ['sum']).sort_values(by=['sum'], ascending=False)
    ips = ips.head(num_to_show)
    print(ips)
    traffic_sum = (ips.sum()/sum_bytes)*100
    print('Percent of traffic', traffic_sum)


def maskZero_traffic():
    mask_zero = df.groupby('src_mask')['doctets'].agg(
        ['sum']).sort_values(by=['sum'], ascending=False)
    bytes_1 = mask_zero.to_numpy()
    percent = (bytes_1[0]/df['doctets'].sum())*100
    return percent


def maskNonZero_traffic(df, percent, columnName):
    df1 = df[df.src_mask != 0]
    traffic_fromIP(df1, percent, columnName, df['doctets'].sum())


def instituteA_addrBlock(df, columnName):
    df1 = df[df[columnName].astype(str).str.startswith('128.112')]
    sum_pkts = df['dpkts'].sum()
    sum_bytes = df['doctets'].sum()
    instA_pkts = df1['dpkts'].sum()
    instA_bytes = df1['doctets'].sum()
    print('Fraction of packets:', instA_pkts/sum_pkts)
    print('Fraction of bytes:', instA_bytes/sum_bytes)


# Reading file
df = pd.read_csv('Netflow_dataset.csv')

# Task A
data = average_pktSize()
print('Average size of packets captured across all traffic: ', data)

# Task B
print('Flow durations linear graph:')
linear_flowGraph(df, 'Flow Durations', 'first', 'last')

print('Flow durations logarithmic graph:')
log_flowGraph(df, 'Flow Durations', 'first', 'last')

print('Flow sizes linear graph:')
linear_flowGraph(df, 'Flow Sizes', 'dpkts', 'doctets')
print('Flow sizes logarithmic graph:')
log_flowGraph(df, 'Flow Sizes', 'dpkts', 'doctets')

# Task C
print('Top 10 src ports:')
top10_traffic('srcport', df['doctets'].sum())
print('Top 10 dst ports:')
top10_traffic('dstport', df['doctets'].sum())

# Task D
print('Total traffic from 0.1% of ip prefixes')
traffic_fromIP(df, .1, 'srcaddr', df['doctets'].sum())
print('Total traffic from 1% of ip prefixes')
traffic_fromIP(df, 1, 'srcaddr', df['doctets'].sum())
print('Total traffic from 10% of ip prefixes')
traffic_fromIP(df, 10, 'srcaddr', df['doctets'].sum())
print('Traffic percent with source mask of 0:')
print(maskZero_traffic())

print('Traffic percent with source mask other than 0:')
print('Total traffic from 0.1%s')
maskNonZero_traffic(df, .1, 'srcaddr')
print('Total traffic from 1%s')
maskNonZero_traffic(df, 1, 'srcaddr')
print('Total traffic from 10%s')
maskNonZero_traffic(df, 10, 'srcaddr')

print('Institute A sent traffic')
instituteA_addrBlock(df, 'srcaddr')

print('Institute A received traffic')
instituteA_addrBlock(df, 'dstaddr')
