

import numpy as np
from PIL import Image
import warnings
from sklearn.preprocessing import LabelEncoder
import re
from sklearn import preprocessing
from sklearn import linear_model
import pandas as pd
from sklearn.decomposition import PCA

def warn(*args, **kwargs): pass

warnings.warn = warn


def encode(train, test):
    le = LabelEncoder().fit(train.species) 
    labels = le.transform(train.species)           # encode species strings
    classes = list(le.classes_)                    # save column names for submission
    test_ids = test.id                             # save test ids for submission
    train_ids=train.id
    
    train = train.drop(['species', 'id'], axis=1)  
    test = test.drop(['id'], axis=1)
    
    return train, labels, test,train_ids, test_ids, classes

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def make_square(img, size=1300, fill_color=(0)):
    x, y = img.size
    new_im = Image.new('L', (size, size), fill_color)
    new_im.paste(img)
    return new_im



def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]






train = pd.read_csv('C:\personal files\programming\Python\CS501\project\Project_Code\Project_Code\GreenLeaf/train_newfeatures_Demo.csv')
test = pd.read_csv('C:/personal files/programming/Python/CS501/project/Project_Code/Project_Code/GreenLeaf/train_newfeatures_Demo.csv')

global trainf
global labels
global classes
train, labels, test,train_ids, test_ids, classes = encode(train, test)
trainf=preprocessing.scale(train)



def Class_prediction(testID):
    train_ids1=train_ids.values
    itemindex = np.where(train_ids1==testID)
    testID=itemindex[0][0]
    pca = PCA(n_components=50)
    pca.fit(trainf)
    Z = pca.transform(trainf)
    TestLeaf=pd.DataFrame(Z)
    TestLeaf_X=TestLeaf.iloc[[0,testID],:]
    TestLeaf_Y=labels[testID]
    classifier =linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=100)
    classifier.fit(Z, labels)
    Y_prediction = classifier.predict(TestLeaf_X)
    AA=classifier.predict_proba(TestLeaf_X)

    AA=AA[1]
    AA_index=list(AA.argsort()[-3:][::-1])

    id1=AA_index[0]
    id2=AA_index[1]
    id3=AA_index[2]
    AA_spec=[classes[id1],classes[id2],classes[id3]]
    AA_prob=AA[np.argsort(AA)[-3:]][::-1]

    Pred_ID=Y_prediction[1]
    RealID=TestLeaf_Y
    return classes[Pred_ID], classes[RealID],AA_spec, AA_prob



'''
##PCA
#determine the number of PCA components by using SVD method 
X_modelf = preprocessing.scale(train)
F=20
table=X_modelf
U, s, V = np.linalg.svd(table.T, full_matrices=True)
D = np.diag(s)
E = D[:F,:F];
W = V[:, :F];
Z = np.dot(W,inv(E))
table_val=Z[test_index]
table_train=Z[train_index] 


plt.plot(s[:100], linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_')


#X_trainf=numpy.concatenate((X_train,table_train),axis=1)
#X_valf=numpy.concatenate((X_test,table_val),axis=1)    
#X_testf=numpy.concatenate((test,table_test),axis=1)    

#X_modelf=np.concatenate((X_train,X_test),axis=0)


from sklearn.decomposition import PCA
pca = PCA(n_components=50)
pca.fit(X_modelf)
Z = pca.transform(X_modelf)
table_test=Z[test_index]
table_train=Z[train_index] 
X_trainf=table_train
X_testf=table_test



testID=5 #import of prediction 
trainf=preprocessing.scale(train)
def Class_prediction(trainf,labels,testID):
    TestLeaf=pd.DataFrame(X_testf)
    TestLeaf_X=TestLeaf.iloc[[0,testID],:]
    TestLeaf_Y=y_test[testID]
    classifier =linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=100)      
    classifier.fit(Z, labels)
    Y_prediction = classifier.predict(TestLeaf_X)
    return Y_prediction[1], TestLeaf_Y


Pred_ID,RealID=Class_prediction(trainf,labels,testID)
print("The predicton is",Pred_ID,"the real plant ID is",RealID)

'''














'''

classifiers = [
    KNeighborsClassifier(3),
    linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=100),
    SVC(kernel="rbf", C=0.025, probability=True),
    NuSVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
#    GradientBoostingClassifier(),
#    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis()]

# Logging for Visual Comparison
log_cols=["Classifier", "Accuracy", "Log Loss"]
log = pd.DataFrame(columns=log_cols)
import matplotlib.pyplot as plt
from sklearn.svm import SVC
#from sklearn.model_selection import StratifiedKFold
#from sklearn.feature_selection import RFECV
#from sklearn.datasets import make_classification
for clf in classifiers:
    ##cross validation
 #   kkkk= SVC(kernel="linear")
 #   rfecv = RFECV(clf, step=10, cv=StratifiedKFold(2),scoring='accuracy')
    clf.fit(X_trainf, y_train)
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    test_predictions = clf.predict(X_trainf)
    acc = accuracy_score(y_train, test_predictions)
    print("Accuracy: {:.4%}".format(acc))
    
    test_predictions = clf.predict_proba(X_trainf)
    ll = log_loss(y_train, test_predictions)
    print("Log Loss: {}".format(ll))
    
    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
    
print("="*30)


for clf in classifiers:
    ##cross validation
 #   kkkk= SVC(kernel="linear")
 #   rfecv = RFECV(clf, step=10, cv=StratifiedKFold(2),scoring='accuracy')
    clf.fit(X_trainf, y_train)
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    test_predictions = clf.predict(X_testf)
    acc = accuracy_score(y_test, test_predictions)
    print("Accuracy: {:.4%}".format(acc))
    
    test_predictions = clf.predict_proba(X_testf)
    ll = log_loss(y_test, test_predictions)
    print("Log Loss: {}".format(ll))
    
    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
    
print("="*30)




































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
    train_predictions = rfecv.predict(X_testf)
    acc = accuracy_score(y_test, train_predictions)
    K_scores.append(acc)    
    
   
    
    train_predictions = rfecv.predict_proba(X_testf) 
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
 





#Cross validation


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
    train_predictions = rfecv.predict(X_testf)
    acc = accuracy_score(y_test, train_predictions)
    print("Accuracy: {:.4%}".format(acc))
    
    train_predictions = rfecv.predict_proba(X_testf)
    ll = log_loss(y_test, train_predictions)
    print("Log Loss: {}".format(ll))
    
    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
    
print("="*30)


"""
from sklearn.metrics import roc_curve, auc
clf = linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=1000)
rfecv = RFECV(clf, step=10, cv=StratifiedKFold(2),scoring='accuracy')
y_score1 = rfecv.fit(X_trainf, y_train).decision_function(X_valf)
y_score =np.argmax(y_score1, axis=1)
#y_score = y_score1.idxmax(axis=1)
fpr, tpr, _ = roc_curve(y_test, y_score)
roc_auc = auc(fpr, tpr)
from sklearn.multiclass import OneVsRestClassifier
classifier = OneVsRestClassifier(linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial',C=1000))
y_score = rfecv.fit(X_trainf, y_train).decision_function(X_valf)
"""




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


'''

