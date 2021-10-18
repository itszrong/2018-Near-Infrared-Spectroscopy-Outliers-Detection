import csv

#load data from filename into storage, return number of data points read
def load(filename, storage):

    size = 0
    with open(filename) as csvfile:
        reader1 = csv.reader(csvfile)
        for  row in reader1:
            if size > 0:
                storage.append(float(row[0]))
            size +=1

    return size

#newton's difference quotient
def derivativeNDQ(y, x, der):
    for i in range(len(y)-1):
        der.append((y[i+1]-y[i])/(x[i+1]-x[i]))

#Symmetric difference quotient
def derivativeSDQ(y, x, der):
    firstLine = True
    for i in range(len(y)-1):
        if firstLine == True:
            der.append(0)
            firstLine = False
        else:
            der.append((y[i+1]-y[i-1])/2*(x[i+1]-x[i]))

#Five Point Stencil
def derivativeFPS(y, x, der):
    firstLine = 0
    for i in range(len(y)-2):
        if firstLine <2:
            der.append(0)
            firstLine +=1
        else:
            der.append((-y[i+2]+8*y[i+1]-8*y[i-1]+y[i-2])/12*(x[i+1]-x[i]))

def difference(clean, dirty, dif):
    for i in range(len(clean)):
        dif.append(abs(dirty[i]-clean[i]))

def outliers(dif, outliers, x):
    for i in range(len(dif)):
        if dif[i] > 0.0001:
            outliers.append(x[i])

def shift(dif, clean_y, dirty_y, baselineValues):
    for i in range(len(dif)):
        if abs(dif[i]) < 0.0001:
            baselineValues.append(abs((clean_y[i]-dirty_y[i])))

    baselineMean = sum(baselineValues) / len(baselineValues)
    return(baselineMean)

def waterTest(x, difference):
    for i in range (len(x)):
        if x[i] == 1450 and difference[i]>0.0001:
            print("The difference in the second derivative at 1450nm is", difference[i], "so water is present.")
        if x[i] == 1950 and difference[i]>0.0001:
            print("The difference in the second derivative at 1950nm is", difference[i], "so water is present.")

"""
# file handling
def fileWrite(x, clean, dirty):
    # create the file
    f = open("SDQ-D1-dex-nn.csv", "w+")# overwrite any existing data
    f.write("wavelength, clean y derivative, dirty y derivative\n")
    for i in range(len(clean)):
        f.write("%6.10f," % (x[i]))
        f.write("%6.10f," % (clean[i]))
        f.write("%6.10f\n" % (dirty[i]))
    f.close()

# read the contents back
    f = open("WriteNIRS.txt", "r")
    if f.mode == 'r': # in case file has not opened
        fileContents=f.readlines()
        for line in fileContents:
             print(line,end ='') # each line already includes CR
    f.close()
"""


def main():
    clean_data_x=[]
    size_x = load("clean_data_x.csv", clean_data_x)

    print("The", len(clean_data_x), " wavelengths(nm) tested are", clean_data_x)

#load all the clean data

    data_y_clean1= []
    sizeClean1 = load("data_y_clean1.csv", data_y_clean1)
    print("There are", sizeClean1, "absorption values in the clean mixture, D1-xxx-1, are", data_y_clean1)

#load all the dirty data

    data_y_dirty1 = []
    sizeDirty1 = load("data_y_dirty1.csv", data_y_dirty1)
    print("There are", sizeDirty1,"absorption values in the dirty mixture, D1-dex-nn, are", data_y_dirty1)

#calculate first and second derivatives

    firstDerClean1 = []
    derivativeFPS(data_y_clean1, clean_data_x, firstDerClean1)
    print("The first derivatives of the clean mixture, D1-xxx-1, are", firstDerClean1)

    secondDerClean1 = []
    derivativeFPS(firstDerClean1, clean_data_x, secondDerClean1)
    print("The second derivatives of the clean mixture, D1-xxx-1, are", secondDerClean1)

    firstDerDirty1 = []
    derivativeFPS(data_y_dirty1, clean_data_x, firstDerDirty1)
    print("The first derivatives of the dirty mixture, D1-dex-nn, are", firstDerDirty1)

    secondDerDirty1 = []
    derivativeFPS(firstDerDirty1, clean_data_x, secondDerDirty1)
    print("The second derivatives of the dirty mixture, D1-dex-nn, are", secondDerDirty1)
"""
#find the difference and the outliers

    dif1 = []
    difference(secondDerClean1, secondDerDirty1, dif1)
    print("The difference in the second derivatives are", dif1)

#find the outliers

    outliers1 = []
    outliers(dif1, outliers1, clean_data_x)
    print("There are", len(outliers1), "outliers :", outliers1)
    print("The percentage purity is", 1-(len(outliers1)/len(data_y_dirty1)))

#find the baseline shift

    baselineValues1 = []
    baselineMean1 = shift(dif1, data_y_clean1, data_y_dirty1, baselineValues1)
    print("The mean baseline shift (excluding outliers) is", baselineMean1, "the difference in y values is", baselineValues1)
    print("The greateast baseline shift is", max(baselineValues1))

#test for water at 1450nm and 1950nm
    waterTest(clean_data_x, dif1)

#write second derivatives to file
#    fileWrite(clean_data_x, secondDerClean1, secondDerDirty1)
"""
if __name__ == "__main__":
    main()

