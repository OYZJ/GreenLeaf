"""
CS578 Course Project Dongdong Ma

"""
path = 'C:\personal files\programming\Python\CS501\project\Project_Code\Project_Code'

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as p

def warn(*args, **kwargs): pass
import warnings
warnings.warn = warn

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
train = pd.read_csv(path+'/train.csv')

def encode(train):
    le = LabelEncoder().fit(train.species) 
    labels = le.transform(train.species)           # encode species strings
    classes = list(le.classes_)                    # save column names for submission                            # save test ids for submission
    
    train = train.drop(['species', 'id'], axis=1)  
    
    return train, labels, classes

train, labels, classes = encode(train)
#train.head(1)




#split the original dataset into two parts 80% for training, and 20% for validation 
sss = StratifiedShuffleSplit(labels, 10, test_size=0.2, random_state=23)

for train_index, test_index in sss:
    X_train, X_test = train.values[train_index], train.values[test_index]
    y_train, y_test = labels[train_index], labels[test_index]
    






#Extra pixel level Features

from PIL import Image
import glob
import numpy
image_list = []

#sort the images based on the number in the name
import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

##image folder 1
image_list = []
image_list_2 = [] 
for filename in sorted(glob.glob('C:/Users/Dong/OneDrive - purdue.edu/2017 Fall/CS578/Course_Project/images/image1/*.jpg'),key=numericalSort):
    im=Image.open(filename)
    image_list.append(im)
image_list_2 = []
for imagename in image_list:
    im_2=imagename
    B=im_2.resize([2500, 1], resample=0)
    image_list_2.append(B)
 # from astropy.table import Table, Column   
for imagename in image_list_2:
    l= len(image_list_2)
    a=0
    table1 = numpy.zeros(shape=(l,2500))
    while a<len(image_list_2):
        table1[a]= image_list_2[a]
        a+=1
im.close()
    
##image folder 2   
image_list = []
image_list_2 = []  
for filename in sorted(glob.glob('C:/Users/Dong/OneDrive - purdue.edu/2017 Fall/CS578/Course_Project/images/image2/*.jpg'),key=numericalSort): 
    im=Image.open(filename)
    image_list.append(im)
  #  im.close()
image_list_2 = []
for imagename in image_list:
    im_2=imagename
    B=im_2.resize([2500, 1], resample=0)
    image_list_2.append(B)
for imagename in image_list_2:
    l= len(image_list_2)
    a=0
    table2 = numpy.zeros(shape=(l,2500))
    while a<len(image_list_2):
        table2[a]= image_list_2[a]
        a+=1   
im.close()    
    
##image folder 3
image_list = []
image_list_2 = []  
for filename in sorted(glob.glob('C:/Users/Dong/OneDrive - purdue.edu/2017 Fall/CS578/Course_Project/images/image3/*.jpg'),key=numericalSort): 
    im=Image.open(filename)
    image_list.append(im)
  #  im.close()
image_list_2 = []
for imagename in image_list:
    im_2=imagename
    B=im_2.resize([2500, 1], resample=0)
    image_list_2.append(B)

for imagename in image_list_2:

    l= len(image_list_2)
    a=0
    table3 = numpy.zeros(shape=(l,2500))
    while a<len(image_list_2):
        table3[a]= image_list_2[a]
        a+=1   
im.close() 

##image folder 4
image_list = []
image_list_2 = []  
for filename in sorted(glob.glob('C:/Users/Dong/OneDrive - purdue.edu/2017 Fall/CS578/Course_Project/images/image4/*.jpg'),key=numericalSort): 
    im=Image.open(filename)
    image_list.append(im)
  #  im.close()
image_list_2 = []
for imagename in image_list:
    im_2=imagename
    B=im_2.resize([2500, 1], resample=0)
    image_list_2.append(B)

for imagename in image_list_2:

    l= len(image_list_2)
    a=0
    table4 = numpy.zeros(shape=(l,2500))
    while a<len(image_list_2):
        table4[a]= image_list_2[a]
        a+=1   
im.close()  
 
table=numpy.concatenate((table1,table2,table3,table4),axis=0)

  

#Feature selection & dimensionality reduction   

##PCA
#determine the number of PCA components by using SVD method 
import math
from numpy.linalg import inv
F=20
numtable=len(table[1,:])
meantable = np.mean(table, 1);
tables = table - np.transpose(np.matlib.repmat(meantable, numtable,1 ));
U, s, V = np.linalg.svd(tables, full_matrices=True)
D = np.diag(s)
E = D[:F, :F]
W = V[:, :F]
Z = math.sqrt(numtable)*np.dot(W,inv(E))
table_val = Z[test_index]
table_train = Z[train_index]


plt.plot(s[:100], linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_')
plt.show()



X_trainf = numpy.concatenate((X_train,table_train),axis=1)
X_valf = numpy.concatenate((X_test,table_val),axis=1)


from sklearn import preprocessing
X_trainf = preprocessing.scale(X_trainf)
X_valf = preprocessing.scale(X_valf)







 #Classification Method select the suiable classifier for next step  
 
from sklearn import linear_model, datasets   
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis



classifiers = [
    KNeighborsClassifier(3),
    linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=100),
    SVC(kernel="rbf", C=0.025, probability=True),
    NuSVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis()]

# Logging for Visual Comparison
log_cols=["Classifier", "Accuracy", "Log Loss"]
log = pd.DataFrame(columns=log_cols)
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
for clf in classifiers:
    ##cross validation
 #   kkkk= SVC(kernel="linear")
 #   rfecv = RFECV(clf, step=10, cv=StratifiedKFold(2),scoring='accuracy')
    clf.fit(X_trainf, y_train)
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    train_predictions = clf.predict(X_valf)
    acc = accuracy_score(y_test, train_predictions)
    print("Accuracy: {:.4%}".format(acc))
    
    train_predictions = clf.predict_proba(X_valf)
    ll = log_loss(y_test, train_predictions)
    print("Log Loss: {}".format(ll))
    
    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
    
print("="*30)

sns.set_color_codes("muted")
sns.barplot(x='Accuracy', y='Classifier', data=log, color="b")

plt.xlabel('Accuracy %')
plt.title('Classifier Accuracy')
plt.show()

sns.set_color_codes("muted")
sns.barplot(x='Log Loss', y='Classifier', data=log, color="g")

plt.xlabel('Log Loss')
plt.title('Classifier Log Loss')
plt.show()



#parameter tunning for LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
K_range=[1,10,100,500,800, 1000,2000,3000,4000,5000,6000,7000,10000]
K_scores=[]
log_Loss=[]
for K in K_range:
#    log_reg = LogisticRegression(solver='lbfgs', multi_class='multinomial'
    clf = linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=K)
    rfecv = RFECV(clf, step=10,scoring='accuracy')
    rfecv.fit(X_trainf, y_train)
    train_predictions = rfecv.predict(X_valf)
    acc = accuracy_score(y_test, train_predictions)
    K_scores.append(acc)    
    
   
    
    train_predictions = rfecv.predict_proba(X_valf) 
    ll = log_loss(y_test, train_predictions)
    log_Loss.append(ll)


plt.figure(1)
plt.subplot(211)
plt.plot(K_range, K_scores)
plt.ylim([0.97, 1])
#plt.xlabel('Value of C')
plt.ylabel('Accuracy') 


plt.subplot(212)
plt.plot(K_range, log_Loss)
plt.xlabel('Value of C')
plt.ylabel('log_loss')
plt.show()





#Cross validation
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


import math
n=len(X_trainf[:,1])
k=11
cvacc=[]
for i in range(1, k):
    A1=math.floor(n*(i-1)/k)+1
    A2=math.floor(n*i/k)
    T = np.arange(A1,A2, dtype=np.int)
    All=np.arange(1,n)
    sizeT = len(T)    
    S = diff(All, T)
    cvtrainX=X_trainf[S]
    cvtrainy=y_train[S]
    cvvalidationX=X_trainf[T]
    cvvalidationy=y_train[T]    
    rfecv = RFECV( linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=4000), step=10,scoring='accuracy')
    rfecv.fit(cvtrainX, cvtrainy)
    cvvalidationX_predictions = rfecv.predict(cvvalidationX)
    acc1 = accuracy_score(cvvalidationy, cvvalidationX_predictions)
    cvacc.append(acc1)    






#Test on the validation dataset
classifiers = [
    linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=4000)]
# Logging for Visual Comparison
log_cols=["Classifier", "Accuracy", "Log Loss"]
log = pd.DataFrame(columns=log_cols)

for clf in classifiers:
    ##cross validation
    rfecv = RFECV(clf, step=10,scoring='accuracy')
    rfecv.fit(X_trainf, y_train)
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    train_predictions = rfecv.predict(X_valf)
    acc = accuracy_score(y_test, train_predictions)
    print("Accuracy: {:.4%}".format(acc))
    
    train_predictions = rfecv.predict_proba(X_valf)
    ll = log_loss(y_test, train_predictions)
    print("Log Loss: {}".format(ll))
    
    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
    
print("="*30)




#test the number of training samples versus accuracy 

y_train1=y_train
x_train1=X_trainf
ratio=[0.7,0.6,0.5,0.4,0.3, 0.2]
samplenumber=[]
Samplenumer_accuracy=[]
Samplenumer_log_Loss=[]
for J in ratio:
    aaa = StratifiedShuffleSplit(y_train1, 10, test_size=J, random_state=23)
    for train_index_a, test_index_a in aaa:
        X_train_a = x_train1[train_index_a]
        y_train_a = y_train1[train_index_a]
        X_trainf_a=X_train_a
    
    classifiers = [
    linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=4000)]
    
    for clf in classifiers:
        rfecv = RFECV(clf, step=10,scoring='accuracy')
        rfecv.fit(X_trainf_a, y_train_a)
        train_predictions = rfecv.predict(X_valf)
        acc = accuracy_score(y_test, train_predictions)        
        train_predictions = rfecv.predict_proba(X_valf)
        ll = log_loss(y_test, train_predictions) 
    Samplenumer_accuracy.append(acc)    
    Samplenumer_log_Loss.append(ll)
    samplenumber.append(round(792*(1-J)))


plt.figure(1)
plt.subplot(211)
plt.plot(samplenumber, Samplenumer_accuracy,'r')
plt.ylim([0.90, 1])
#plt.xlabel('Value of C')
plt.ylabel('Accuracy') 


plt.subplot(212)
plt.plot(samplenumber, Samplenumer_log_Loss,'r')
plt.xlabel('number of training samples')
plt.ylabel('log_loss')
plt.show()
















