from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import pandas as pd
import pickle

wrongsp = []
def savetofile():
    try:
        file = open(savefile.get(), "w")
        #amount_written = file.write(wrongsp)
        for ele in wrongsp:
            file.write(ele + '\n')
        #print(amount_written)
        file.close()
    except:
        print('exception')
        raise

def calculate(*args):
    try:
        feature_names = ['CP_CPU_SU','LOCK_LATCH','SUSPEND','LOCK_REQUEST_AVG','GETPAGES_AVG','SELECT_AVG']

        #loading model
        filename = modelfile.get()#'finalized_model.sav'
        model = pickle.load(open(filename, 'rb'))

        #print predection value,'./SP_DETAIL_PRE2.csv'
        df_pridict = pd.read_csv(datasetfile.get(),index_col='SPNAME')
        X_pridict = df_pridict[feature_names]
        y_pred_pridict = model.predict(X_pridict)

        i = 0
        while (i < y_pred_pridict.size):
            if (y_pred_pridict[i] == 0):
                #listboxSP.insert('end', str(X_pridict.index[i]) + '      ' + str(X_pridict['OCCUR'].values[i]) + '      ' + str(
                    #y_pred_pridict[i]))
                #textarea.insert(INSERT, str(X_pridict.index[i]) + '      ' + str(X_pridict['OCCUR'].values[i]) + '      ' + str(
                    #y_pred_pridict[i])+'\n')
                #textarea.insert(INSERT,'{0},{2},{1}'.format(str(X_pridict.index[i]),str(X_pridict['OCCUR'].values[i]),str(
                    #y_pred_pridict[i]) )+ '\n')
                tv.insert('', 'end', text=str(X_pridict.index[i]), values=(str(X_pridict['CP_CPU_SU'].values[i]), str(y_pred_pridict[i])))
                wrongsp.append('{0},{2},{1}'.format(str(X_pridict.index[i]),str(X_pridict['CP_CPU_SU'].values[i]),str(
                    y_pred_pridict[i]) ))
            i += 1
    except:
        print('exception')
        raise

#form design
root = Tk()

root.title("SP Prediction")
mainframe = ttk.Frame(root, padding = "3 3 12 12", width=200, height= 200)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

modelfile = StringVar()
modelfile.set('finalized_model.sav')
datasetfile = StringVar()
datasetfile.set('SP_DETAIL_PRE2.csv')
savefile = StringVar()
savefile.set('C:/Users/hajiBolouri/Desktop/testfiel.csv')

labelInputModel = ttk.Label(mainframe, text='Model Destination:').grid(column=0, row=0, sticky=W)
textModel = ttk.Entry(mainframe, width=20, textvariable=modelfile).grid(column=0, row=1 ,  sticky=W)
labelInputDataset = ttk.Label(mainframe, text='Dataset Destination:').grid(column=0, row=2, sticky=W)
textInputDataset = ttk.Entry(mainframe, width=20, textvariable=datasetfile).grid(column=0, row=3, sticky=W)
#fake Label to add more space between two space
#fakeLabel2 = Label(mainframe,width=15).grid(column=0,row=4)
#fakeLabel3 = Label(mainframe,width=5).grid(column=0,row=4)
#
buttonClick = ttk.Button(mainframe,text='Calculate',command=calculate).grid(column=0, row=6,  sticky=W)
labelList = ttk.Label(mainframe, text='Bad SP List:').grid(column=2, row=0,  sticky=N)
#List box,which is in future replace with Text
#listboxSP = Listbox(mainframe, width=50, height=10)
#listboxSP.grid(column=2, row=1, rowspan=5, sticky=(N,W,E,S))
#s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=listboxSP.yview)
#s.grid(column=2, row=1, rowspan=5, sticky=(N,S,E))
#listboxSP['yscrollcommand'] = s.set
#ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))

#textarea = Text(mainframe,width=50, height=10)
#textarea.grid(column=2, row=1, rowspan=5, sticky=(N,W,E,S))
#s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=textarea.yview)
#s.grid(column=2, row=1, rowspan=5, sticky=(N,S,E))
#textarea['yscrollcommand'] = s.set
#ttk.Sizegrip().grid(column=1,row=1,sticky=(S,E))

#fake Label to add more space between two space
fakeLabel = Label(mainframe,width=5).grid(column=1,row=1)

tv = Treeview(mainframe, height=10,  selectmode='extended')#height=10,
tv.grid(column=2, row=1, rowspan=8, sticky=(N,W,E,S))
#-add scroll bar
s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=tv.yview)
s.grid(column=2, row=1, rowspan=8, sticky=(N,S,E))
tv['yscrollcommand'] = s.set
ttk.Sizegrip().grid(column=1,row=1,sticky=(S,E))
#-
tv['columns'] = ('Call','Error')
tv.heading("#0",text='SP Name')
tv.heading('Call',text='CPU Usage')
tv.heading('Error',text = 'SP Validation')
#tv.insert('','end',text='first',values=('5','39'))

textSave = ttk.Entry(mainframe, width=20, textvariable=savefile).grid(column=2, row=9 ,  sticky=W)
buttonSave = ttk.Button(mainframe,text='Save Result',command=savetofile).grid(column=2, row=10 , sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
#