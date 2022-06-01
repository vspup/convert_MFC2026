# convert xml to map for gi tools

import xml.etree.cElementTree as ET
from s_map import *

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from statistics import mean
from statistics import stdev

Field = []
Dev = []
N = []
fField = [] # float

#k = 1/42.5761721313*10000

k = 234.87465913612476

avgField = 0
valMin = 0
idxMin = 0
valMax = 0
idxMax = 0
ppm = 0
sdev = 0

# Root window
root = tk.Tk()
root.title('Convert XML  to MAP')



nameMAP = 0
nameXML = 0

# Log
text = tk.Text(root, height=12)
text.grid(column=0, row=0, sticky='nsew', columnspan=4)


# for mane map
seriesEntry = tk.Entry(root)
seriesEntry.grid(column=0, row=1, sticky='nsew')
seriesEntry.insert('end', 'HM')
numberEntry = tk.Entry(root)
numberEntry.grid(column=1, row=1, sticky='nsew')
numberEntry.insert('end', '4930')
viselEntry = tk.Entry(root)
viselEntry.grid(column=2, row=1, sticky='nsew')
viselEntry.insert('end', 'W')
cellEntry = tk.Entry(root)
cellEntry.grid(column=3, row=1, sticky='nsew')
cellEntry.insert('end', 'A')

def open_xml_file():
    global nameXML
    global valMin, idxMin, valMax, idxMax, ppm, sdev, avgField, k
    # file type
    filetypes = (
        ('xml files', '*.xml'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes, initialdir='./@xml/')
    nameXML = f.name
    text.insert('end', '--> Read : ')
    text.insert('end', f.name)
    text.insert('end', '\n')
    tree = ET.parse(nameXML)

    freqS = tree.findall("body/dataset/measurements/measurement/freq")
    for freqI in freqS:
        Field.append(freqI.text.split())
    print("Field [MHz] = ")
    text.insert('end', '--> Field [MHz]\n')
    for m in Field:
        for n in m:
            print(n, end=', ')
        print()

    devS = tree.findall("body/dataset/measurements/measurement/stdDev")
    for devI in devS:
        Dev.append(devI.text.split())
    text.insert('end', '--> Deviation\n')
    print("Deviation [] = ")
    for m in Dev:
        for n in m:
            print(n, end=', ')
        print()

    nvS = tree.findall("body/dataset/measurements/measurement/nbValid")
    for nvI in nvS:
        N.append(nvI.text.split())
    text.insert('end', '--> Number\n')
    print("Number [] = ")
    i = 0
    for m in N:
        print(i, end=' [')
        for n in m:
            print(n, end=', ')
        print(']')
        i = i + 1

    write_MAP_button['state'] = tk.NORMAL
    text.insert('end', '--> Can write\n')

    # statistick
    for i in range(len(Field)):
        for j in range(len(Field[i])-1):
            if Field[i][j] == 'nan':
                if Field[i][j] == Field[i][0]: # if first
                    fff = float("{0:.12f}".format(float(Field[i][1]) * 1))*2 - float("{0:.12f}".format(float(Field[i][2]) * 1))
                elif Field[i][j] == Field[i][-1]: # if lasst
                    fff = float("{0:.12f}".format(float(Field[i][-3]) * 1))*2 - float("{0:.12f}".format(float(Field[i][-4]) * 1))
                else: # midle
                    fff = (float("{0:.12f}".format(float(Field[i][j-1]) * 1)) + float("{0:.12f}".format(float(Field[i][j+1]) * 1)))/2
            else:
                fff = float("{0:.12f}".format(float(Field[i][j]) * 1))
            fField.append(fff)

    # k translate to Gaus



    avgField = mean(fField)
    valMin, idxMin = min((valMin, idxMin) for (idxMin, valMin) in enumerate(fField))
    valMax, idxMax = max((valMax, idxMax) for (idxMax, valMax) in enumerate(fField))
    ppm = (max(fField) - min(fField))/mean(fField) * 1000000
    sdev = stdev(fField)

    text.insert('end', '--> Statistics\n')
    text.insert('end', '--> ' + str(ppm) + ' PPM\n')
    text.insert('end', '--> ' + str(avgField * k) + ' Gauss - Average Field\n')
    text.insert('end', '--> ' + str(sdev * k) + ' Gauss - Standard Deviation\n')
    text.insert('end', '--> ' + str(valMin * k) + 'Gauss - Minimum Field at point ' + str(idxMin) + ' \n')
    text.insert('end', '--> ' + str(valMax * k) + 'Gauss - Maximum Field at point ' + str(idxMax) + ' \n')

    kav = 30011.09377829 / avgField
    kmax = 30011.58498117 / valMax
    kmin = 30010.62603492 / valMin
    text.insert('end', '--> k = \t\t' + str(k) + ' \n')
    text.insert('end', '--> k avg = \t' + str(kav) + ' \n')
    text.insert('end', '--> k max = \t' + str(kmax) + ' \n')
    text.insert('end', '--> k min = \t' + str(kmin) + ' \n')

    # vsp
    text.insert('end', '--> F = ' + str(("{0:.11g}".format(float(fField[0])))) + 'e+006\n')
    text.insert('end', '--> Fg = ' + str(("{0:.11g}".format(float(fField[0]) / 100))) + 'e+008\n')
    text.insert('end', '--> Ff = ' + str(("{0:.11f}".format(float(fField[0]) / 100))) + 'e+008\n')

    print("{0:.11g}".format(float(fField[0]) / 100))
    print("{0:.11f}".format(float(fField[0]) / 100))

# open XML file button
open_XML = ttk.Button(
    root,
    text='Open XML File',
    command=open_xml_file
)
open_XML.grid(column=0, row=2, sticky='w', padx=10, pady=10)


def write_map_file():
    global nameMAP
    global valMin, idxMin, valMax, idxMax, ppm, sdev, avgField, k

    # file type
    filetypes = (
        ('xml files', '*.map'),
        ('All files', '*.*')
    )
    # show the open file dialog
    def_name = seriesEntry.get()+numberEntry.get()+viselEntry.get()+'00000'+cellEntry.get()+'.map'
    f = fd.asksaveasfile(mode='w', defaultextension=".map", initialfile=def_name, initialdir='./@map/')
    nameMAP = f.name
    text.insert('end', '<<- Start write to : ')
    text.insert('end', f.name)
    text.insert('end', '\n')

    fmap = open(nameMAP, 'w')

    fmap.write(s_titel_W_CoronaCamera50dsv)
    fmap.write(s_type_W_CoronaCamera50dsv)
    fmap.write(s_fieled_ofset)
    fmap.write(s_statistics)
    fmap.write('# ' + str(ppm) + ppm_statistic)
    fmap.write('# ' + str(avgField*k) + avg_statistic)
    fmap.write('# ' + str(sdev*k) + dev_statistic)
    fmap.write('# ' + str(valMin*k) + min_statistic + str(idxMin) + '\n')
    fmap.write('# ' + str(valMax*k) + max_statistic + str(idxMax) + '\n')

    print('\n')
    fmap.write(s_field_values)

    for i in range(NN):
        SF = ''
        for j in range(MM):

            SF = SF + str(("{0:.11f}".format(float(fField[0]) / 100))) + 'e+008'
            if j < 31:
                SF = SF + ', '
        print(SF)
        SF = SF + '\n'
        fmap.write(str(SF))

    # standart deviation
    print('\n')
    fmap.write(s_standart_deviation)
    for i in range(NN):
        SD = ''
        for j in range(MM):
            if Dev[i][j] == 'nan':
                SD = SD + str(0.005)
            else:
                SD = SD + str(("{0:.4f}".format(float(Dev[i][j])*0.1)))
            if j < 31:
                SD = SD + ', '
        print(SD)
        SD = SD + '\n'
        fmap.write(str(SD))

    # point
    print('\n')
    fmap.write(s_point)
    for i in range(NN):
        SP = ''
        for j in range(MM):
            if N[i][j] == 'nan':
                SP = SP + str(int(0.1))
            else:
                SP = SP + str(int(N[i][j]))
            if j < 31:
                SP = SP + ', '
        print(SP)
        SP = SP + '\n'
        fmap.write(str(SP))

    # Timestamp
    fmap.write(s_timestamp)
    for j in range(24):
        ST = ''
        for i in range(32):
            ST = ST + '09:' + str(11 + j) + ':09_03/26/2021'
            if i < 31:
                ST = ST + ', '
        print(ST)
        ST = ST + '\n'
        fmap.write(str(ST))

    fmap.close()
    text.insert('end', '<<- Finish write to MAP \n')


# open file button
write_MAP_button = ttk.Button(
    root,
    text='Write to map file',
    command=write_map_file,
    state=tk.DISABLED
)


write_MAP_button.grid(column=1, row=2, sticky='w', padx=10, pady=10)


root.mainloop()

