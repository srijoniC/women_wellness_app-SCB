
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
# =============================================================================
# nlp packages
# =============================================================================
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
# nltk.download('averaged_perceptron_tagger')
import string

binary_sort_train = pd.read_csv('binary_sort_train_data.csv')
binary_sort_test= pd.read_csv('binary_sort_test_data.csv')
cols= binary_sort_train.columns
cols= cols[:-1]
x = binary_sort_train[cols]
y = binary_sort_train['prediction']



grouped_data = binary_sort_train.groupby(binary_sort_train['prediction']).max()

'''converting prediction variables into categorical data'''
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

'''Train Test split Test'''
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = binary_sort_test[cols]
testy    = binary_sort_test['prediction']  
testy    = le.transform(testy)

#Decision Tree 
clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
print("for Decision Tree: ",clf.score(x_train,y_train))


# =============================================================================
# model=SVC()
# model.fit(x_train,y_train)
# print("for svm: ")
# print(model.score(x_test,y_test))
# =============================================================================

#linear regression
clf2 = LinearRegression(normalize=True)
clf2.fit(x_train,y_train)
y_pred = clf2.predict(x_test)
print("for linear regression: ",r2_score(y_test,y_pred))
#Random forest 
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=20)
exp= rf.fit(x_train, y_train);

#Random forest
predicted = rf.predict(x_test)
accuracy = accuracy_score(y_test, predicted)
#print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'for random forest: {accuracy:.3}')

# Calculate feature importances
''' Feature importances refers to techniques that assigns a score to input features based on how 
useful they are at predicting the target'''
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols


symptom_severness=dict()
disease_description = dict()
precautions=dict()
symptoms_list = {}

for index, symptom in enumerate(x):
        symptom_severness[symptom] = index
      
''' Caluculating severness of symptoms'''       
def condition_calculation(exp,days):
    sum=0
    for item in exp:
         sum=sum+symptom_severness[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")

'''fetch and display description of given disease'''
def illness_description():
    global disease_description
    with open('disease_description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            disease_description.update(_description)



''' fetch symptom severness data for calculation of condition severity'''
def symptom_severity():
    global symptom_severness
    with open('symptom_severness.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                symptom_severness.update(_diction)
        except:
            pass

'''fetch and display precautionary measures to be taken '''
def precautionDict():
    global precautions
    with open('precautionary_measures.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautions.update(_prec)


def patientInfo():
    print("Please enter your name \n\t\t\t\t\t\t",end="->")
    name=input("")
    print("Hello ",name, ", Welcome to symptom prediction chatbot")

#match user input with syptoms present in database
def check_pattern(symptoms,inp):
    import re
    prediction_list=[]
    
    ptr=0
    
    stop = set(stopwords.words('english') + list(string.punctuation)) #remove stop words
    list_word=[i for i in word_tokenize(inp.lower()) if i not in stop]
    
    # print(list_word)
    
    for word in list_word:
        regexp = re.compile(word) #used for pattern matching 
        for item in symptoms: 
            if regexp.search(item):
                # print('found 1')
                prediction_list.append(item)
            
    if(len(prediction_list)>0):
        prediction_list = list(dict.fromkeys(prediction_list))
        return 1,prediction_list
    else:
        return ptr,item
    
#predict disease
def predict(symptoms_exp):
    df = pd.read_csv('binary_sort_train_data.csv')
    X = df.iloc[:, :-1]
    y = df['prediction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_list = {}

    for index, symptom in enumerate(X):
        symptoms_list[symptom] = index

    input_vector = np.zeros(len(symptoms_list))
    for item in symptoms_exp:
      input_vector[[symptoms_list[item]]] = 1


    return rf_clf.predict([input_vector])


def print_disease(node):
    #print(node)
    node = node[0]
    #print(len(node))
    val  = node.nonzero() 
    # print(val)
    disease = le.inverse_transform(val[0])
    return disease

def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
   
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    #print(chk_dis)
  
    symptoms_present = []



    while True:

        print("Enter the symptom you are experiencing  \n\t\t\t\t\t\t",end="->")
        symptom_input = input("")
        conf,cnf_dis=check_pattern(chk_dis,symptom_input)
        if conf==1:
            print("searches related to input: ")
            for num,it in enumerate(cnf_dis):
                print(num,")",it)
            if num!=0:
                print(f"Select the one you meant (0 - {num}):  ", end="")
                conf_inp = int(input(""))
            else:
                conf_inp=0

            symptom_input=cnf_dis[conf_inp]
            break
            
        else:
            print("Enter valid symptom.")

    while True:
        try:
            num_days=int(input("From how many days you have been experiancing this symptom? : "))
            break
        except:
            print("Enter number of days.")
    def recurse(node, depth):
        
        
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == symptom_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            
            red_cols = grouped_data.columns 
            symptoms_given = red_cols[grouped_data.loc[present_disease].values[0].nonzero()]
            
            print("Are you experiencing any ")
            symptoms_exp=[]
            for syms in list(symptoms_given):
                inp=""
                print(syms,"? : ",end='')
                while True:
                    inp=input("")
                    if(inp=="yes" or inp=="no"):
                        break
                    else:
                        print("provide proper answers i.e. (yes/no) : ",end="")
                if(inp=="yes"):
                    symptoms_exp.append(syms)

            second_prediction=predict(symptoms_exp)
            
            condition_calculation(symptoms_exp,num_days)
            if(present_disease[0]==second_prediction[0]):
                print("You may have ", present_disease[0])

                print(disease_description[present_disease[0]])

                


            else:
                print("You may have ", present_disease[0], "or ", second_prediction[0])
                print(disease_description[present_disease[0]])
                print(disease_description[second_prediction[0]])

           
            precution_list=precautions[present_disease[0]]
            print("Take following measures : ")
            for  i,j in enumerate(precution_list):
                print(i+1,")",j)

            

    recurse(0, 1)
symptom_severity()
illness_description()
precautionDict()
patientInfo()
tree_to_code(clf,cols)

