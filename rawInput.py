#! /usr/bin/env python

"this is raw input test example by howard huang"

if __name__ == '__main__':
    value = raw_input('''please input your select as below \n (1) sum 1~5 number \n (2) averege 1~5 number \n (X) exit\n''')
    while(value != 'X'):
        if value == 'X':
            break
        if value == '1':
            print 'sum is %d' % (1+2+3+4+5)
        if value == '2':
            print 'sum is %d' % ((1+2+3+4+5)/5)
    
        value = raw_input('''please input your select as below \n (1) sum 1~5 number \n (2) averege 1~5 number \n (X) exit\n''')