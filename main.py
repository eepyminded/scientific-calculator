from tkinter import *
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

master = Tk()
master.title("Kalkulator")
master.geometry("700x700")

equals = ""

def enter(value):
    global equals
    equals = str(equals) + str(value)
    editBoxMain.insert(len(equals),value)

def equalsTo():
    global equals
    equals = editBoxMain.get()

    if "sin(" in equals:
        startSin = equals.find("sin(") + 4
        endSin = equals.find(")", startSin)
        sinInside = equals[startSin:endSin]
        sinValue = float(sinInside)

        sinResult = math.sin(math.radians(sinValue))

        equals = equals.replace(f"sin({sinInside})", str(sinResult))

        drawFunction(sinValue,"sin")

    if "cos(" in equals:
        startCos = equals.find("cos(") + 4
        endCos = equals.find(")", startCos)
        cosInside = equals[startCos:endCos]
        cosValue = float(cosInside)

        cosResult = math.cos(math.radians(cosValue))

        equals = equals.replace(f"cos({cosInside})", str(cosResult))

        drawFunction(cosValue,"cos")

    if "tan(" in equals:
        startTan = equals.find("tan(") + 4
        endTan = equals.find(")", startTan)
        tanInside = equals[startTan:endTan]
        tanValue = float(tanInside)

        tanResult = round(math.tan(math.radians(tanValue)),3)
        if tanResult > 100:
            editBoxMain.delete(0,"end")
            editBoxMain.insert(0,"undefined")
            equals = ""
        else:
            equals = equals.replace(f"tan({tanInside})", str(tanResult))

            drawFunction(tanValue,"tan")

    if "cot(" in equals:
        startCtan = equals.find("cot(") + 4
        endCtan = equals.find(")", startCtan)
        ctanInside = equals[startCtan:endCtan]
        ctanValue = float(ctanInside)

        ctanResult = 1 / math.tan(math.radians(ctanValue))
        equals = equals.replace(f"cot({ctanInside})", str(ctanResult))

        #drawFunction(ctanValue,"cot")

    equals = eval(equals)
    editBoxMain.delete(0,"end")
    equals = round(equals, 2)
    editBoxMain.insert(0,equals)

def drawFunction(angleOf,funcType):

    figureObj, axisObj = plt.subplots(figsize=(4, 4))
    
    xValues = range(0, 360)

    if funcType == "sin":
        yValues = [math.sin(math.radians(x)) for x in xValues]
        yValueAtAngle = math.sin(math.radians(angleOf))
    elif funcType == "cos":
        yValues = [math.cos(math.radians(x)) for x in xValues]
        yValueAtAngle = math.cos(math.radians(angleOf))
    elif funcType == "tan":
        yValues = [math.tan(math.radians(x)) for x in xValues]
        yValueAtAngle = math.tan(math.radians(angleOf))
    
    axisObj.plot(xValues, yValues)
    axisObj.plot((angleOf, angleOf), (0, yValueAtAngle), color="blue", linestyle="--")
    axisObj.plot((0, angleOf), (yValueAtAngle, yValueAtAngle), color="red", linestyle="--")
    plt.scatter(angleOf,yValueAtAngle, color="green")
    axisObj.text(angleOf,yValueAtAngle,f"{angleOf,round(yValueAtAngle,2)}")

    plt.xlim(0,360)
    if funcType == "tan":
        plt.ylim(-10,10)
    else:
        plt.ylim(-1,1)

    plt.grid(True)
    
    figureDraw = FigureCanvasTkAgg(figureObj, master=master)
    figureDraw.get_tk_widget().place(x=250, y=0) 
    figureDraw.draw()

def parabolaCalcy(x,a,b,c):
    return a * x**2 + b * x + c

def quadraticEquals():
    aValue = float(buttonA.get())
    bValue = float(buttonB.get())
    cValue = float(buttonC.get())

    deltaValue = bValue**2 - 4*aValue*cValue
    if aValue != 0:
        if deltaValue > 0:
            global xCentre
            xCentre = -bValue / (2*aValue)
            x1Value = (-bValue + math.sqrt(deltaValue))/2*aValue
            x2Value = (-bValue - math.sqrt(deltaValue))/2*aValue

            if x1Value < x2Value:
                pass
            else:
                tempVal = x2Value
                x2Value = x1Value
                x1Value = tempVal
            
            buttonX1.config(text=f"x1 = {x1Value}")
            buttonX2.config(text=f"x2 = {x2Value}")

        elif deltaValue == 0:
            x1Value = -bValue/2*aValue
            buttonX1.config(text=f"x1 = {x1Value}")
            buttonX2.config(text=f"x2 = {x2Value}")
        else:
            buttonX1.config(text=f"Brak rozwiązań! delta < 0")

        buttonDelta.config(text=f"delta = {deltaValue}")
        xMin = xCentre - 20
        xMax = xCentre + 20

        xValues = []
        for i in range(100):
            xValues.append(xMin + (xMax - xMin) * i / 100)

        yValues = [parabolaCalcy(x, aValue, bValue, cValue) for x in xValues]

        figureObj, axisObj = plt.subplots(figsize=(4, 4))

        figureDraw = FigureCanvasTkAgg(figureObj, master=master)
        figureDraw.get_tk_widget().place(x=250, y=0) 
        figureDraw.draw()

        plt.plot(xValues,yValues)
        plt.grid(True)

        plt.scatter(x1Value, 0, color="green")
        plt.scatter(x2Value, 0, color="green")

        axisObj.text(x1Value, 5, f"x1 = {x1Value}", color="green")
        axisObj.text(x2Value, -20, f"x2 = {x2Value}", color="red")

    else:
        buttonDelta.config(text=f"a nie może być równe 0!")


def cleanScreen():
    global equals
    equals = ""
    plt.clf()
    editBoxMain.delete(0,"end")
    buttonX1.config(text=f"x1 =")
    buttonX2.config(text=f"x2 =")
    buttonA.delete(0,"end")
    buttonB.delete(0,"end")
    buttonC.delete(0,"end")
    buttonDelta.config(text="delta = ")


editBoxMain = ttk.Entry(master, width=24, textvariable=equals)
editBoxMain.place(x=0,y=0)

# numery, przecinek, (, )

buttonOne = ttk.Button(master, text="1",width=4, command=lambda : enter(1))
buttonOne.place(x=10,y=40)

buttonTwo = ttk.Button(master, text="2",width=4, command=lambda : enter(2))
buttonTwo.place(x=70,y=40)

buttonThree = ttk.Button(master, text="3",width=4, command=lambda : enter(3))
buttonThree.place(x=130,y=40)

buttonFour = ttk.Button(master, text="4",width=4, command=lambda : enter(4))
buttonFour.place(x=10,y=80)

buttonFive = ttk.Button(master, text="5",width=4, command=lambda : enter(5))
buttonFive.place(x=70,y=80)

buttonSix = ttk.Button(master, text="6",width=4, command=lambda : enter(6))
buttonSix.place(x=130,y=80)

buttonSeven = ttk.Button(master, text="7",width=4, command=lambda : enter(7))
buttonSeven.place(x=10,y=120)

buttonEight = ttk.Button(master, text="8",width=4, command=lambda : enter(8))
buttonEight.place(x=70,y=120)

buttonNine = ttk.Button(master, text="9",width=4, command=lambda : enter(9))
buttonNine.place(x=130,y=120)

buttonZero = ttk.Button(master, text="0",width=4, command=lambda : enter(0))
buttonZero.place(x=70,y=160)

buttonComma = ttk.Button(master, text=",",width=4, command=lambda : enter("."))
buttonComma.place(x=130,y=160)

buttonLeftb = ttk.Button(master, text="(", width=4, command=lambda : enter("("))
buttonLeftb.place(x=10,y=200)

buttonRightb = ttk.Button(master, text=")", width=4, command=lambda : enter(")"))
buttonRightb.place(x=70,y=200)

# przyciski funkcyjne

buttonAdding = ttk.Button(master, text="+",width=4, command=lambda : enter("+"))
buttonAdding.place(x=190,y=40)

buttonSubtracting = ttk.Button(master, text="-",width=4, command=lambda : enter("-"))
buttonSubtracting.place(x=190,y=80)

buttonMultiplying = ttk.Button(master, text="*", width=4,command=lambda : enter("*"))
buttonMultiplying.place(x=190,y=120)

buttonDividing = ttk.Button(master, text="/", width=4,command=lambda : enter("/"))
buttonDividing.place(x=190,y=160)

buttonClear = ttk.Button(master, text="Cln", width=4,command=cleanScreen)
buttonClear.place(x=190,y=200)

buttonEquals = ttk.Button(master, text="=", width=4, command=equalsTo)
buttonEquals.place(x=10,y=160)

# funkcje trygonometryczne

buttonSin = ttk.Button(master, text="Sin", width=4, command=lambda : enter("sin("))
buttonSin.place(x=10,y=240)

buttonCos = ttk.Button(master, text="Cos", width=4, command=lambda : enter("cos("))
buttonCos.place(x=70,y=240)

buttonTan = ttk.Button(master, text="Tan", width=4, command=lambda : enter("tan("))
buttonTan.place(x=130,y=240)

buttonCtan = ttk.Button(master, text="Cot", width=4, command=lambda : enter("cot("))
buttonCtan.place(x=190,y=240)

# równanie kwadratowe

buttonA = ttk.Entry(master, width=4)
buttonA.place(x=10,y=300)
buttonAx2 = ttk.Label(master, text="x²+", width=4)
buttonAx2.place(x=50,y=300)

buttonB = ttk.Entry(master, width=4)
buttonB.place(x=75,y=300)
buttonBx = ttk.Label(master, text="x+", width=4)
buttonBx.place(x=115,y=300)

buttonC = ttk.Entry(master, width=4)
buttonC.place(x=130,y=300)

buttonQuadequals = ttk.Button(master, text="Oblicz", width=18, command=quadraticEquals)
buttonQuadequals.place(x=10,y=330)

buttonX1 = ttk.Label(master, text="x1 = ", width=10)
buttonX1.place(x=10,y=370)

buttonX2 = ttk.Label(master, text="x2 = ", width=10)
buttonX2.place(x=80,y=370)

buttonDelta = ttk.Label(master, text="delta = ", width=20)
buttonDelta.place(x=10,y=390)

master.mainloop()