
## Compound interest calculator

from Tkinter import *


def calFutureValue(PV,factorNum,intyear):
    FV = PV
    for i in range(intyear):
        FV *= factorNum
    ## print 'Future Value = %d ' % FV
    return FV

def calculateFV():
    FV = calFutureValue(int(presentValue.get()), float(factor.get()), int(year.get()))
    FV = int(FV)
    futureValue.set(str(FV))
    futureValue1.set(str(FV//10000))
    addValue.set(str(FV-int(presentValue.get()))) 
    addValue1.set(str((FV-int(presentValue.get()))//10000))
    addValueByMonth.set(str((FV-int(presentValue.get()))/12/int(year.get())))      
       
if __name__ == '__main__':     
    root = Tk()
    root.title('Compound interest calculator')
    root.geometry('450x300+0+0')
    presentValue = StringVar()
    factor = StringVar()
    year = StringVar()
    futureValue = StringVar()
    futureValue1 = StringVar()
    addValue = StringVar()
    addValue1 = StringVar()
    addValueByMonth = StringVar()
    presentValue.set('1000000')
    factor.set('1.041')
    year.set('5')
    
    Label(root, text='Present Value:').place(x=10,y=25)
    Entry(root, width=10,textvariable=presentValue).place(x=120,y=25)
    
    Label(root, text='Factor:').place(x=10,y=50)
    Entry(root, width=10,textvariable=factor).place(x=120,y=50)
    
    Label(root, text='Year:').place(x=10,y=75)
    Entry(root, width=10,textvariable=year).place(x=120,y=75)
    
    Button(root, text="Calculate", command=calculateFV).place(x=350,y=60)
    
    Label(root, text='Future Value:').place(x=10,y=100)
    Entry(root, width=40,textvariable=futureValue).place(x=120,y=100)
    Label(root, text='RMB(wang):').place(x=10,y=125)
    Entry(root, width=40,textvariable=futureValue1).place(x=120,y=125)
    Label(root, text='add RMB:').place(x=10,y=150)
    Entry(root, width=40,textvariable=addValue).place(x=120,y=150)
    Label(root, text='add RMB(wang):').place(x=10,y=175)
    Entry(root, width=40,textvariable=addValue1).place(x=120,y=175)
    Label(root, text='add RMB/Month:').place(x=10,y=200)
    Entry(root, width=40,textvariable=addValueByMonth).place(x=120,y=200)
    
    root.mainloop()