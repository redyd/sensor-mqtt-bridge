def Average(l):
    sum=0
    for i in range(0,len(l)):
        sum+=l[i]
    return sum/len(l)


def MovingAverage(list, latest, size):
    if len(list) == size:
        list.pop(0)
    list.append(latest)
    return Average(list)