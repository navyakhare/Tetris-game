def level(score):
    if score>=1000:
        return 5
    elif score>=500:
        return 4
    elif score>=250:
        return 3
    elif score>=100:
        return 2
    elif score<=100:
        return 1

def time(l):
    if l==1:
        return 800
    elif l==2:
        return 600
    elif l==3:
        return 400
    elif l==4:
        return 300
    elif l==5:
        return 200


