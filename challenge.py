import os

max_value = 200
inc = 5
count = 0
for i in range(inc):
    lines = os.popen( 'vmstat').readlines()
    dct = dict( zip( lines[-2].split(), lines[-1].split()))
    if int(dct['free']) > max_value:
        count = count + 1
if count == inc:
    #print (dct['free'])
    print('yeah we did it', count)
