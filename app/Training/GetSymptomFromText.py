## tiền xử lý một câu trong quá trình xử lý ngôn ngữ tự nhiên (NLP)
import pandas as pd
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os


intentShort = os.path.join("app/Data", 'intents_short.json')
with open(intentShort, 'r') as f:
    intents = json.load(f)

lemmatizer = WordNetLemmatizer()

stp=stopwords.words('english')
stp.remove('not')



def preprocess_sent(sent):
    sent=sent.replace("'t",' not')
    t=nltk.word_tokenize(sent) ## câu được chia thành các từ riêng lẻ (còn được gọi là "tokens")
    return ' '.join([lemmatizer.lemmatize(w.lower()) for w in t if (w not in stp and w.isalpha())])

sent=[]
app_tag=[]  ## tag của câu
for intent in intents['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        sent.append(preprocess_sent(pattern))
        app_tag.append(tag)

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(sent)
feature_names = vectorizer.get_feature_names_out()
dense = vectors.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
vocab=list(df.columns)

def bag_of_words(tokenized_sentence, all_words):
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag

def predictSym(sym,vocab,app_tag):
    sym=preprocess_sent(sym)
    print('test sym: ' + sym)
    bow=np.array(bag_of_words(sym,vocab))

    res=cosine_similarity(bow.reshape((1, -1)), df).reshape(-1)
    order=np.argsort(res)[::-1].tolist()
    possym=[]
    correctsym = []

    for i in order:
        if app_tag[i] not in correctsym:
            if app_tag[i].replace('_',' ') in sym:
                correctsym.append(app_tag[i])
            else :
                if app_tag[i] not in possym and res[i]!=0:
                    possym.append(app_tag[i])
    return correctsym, possym

df_tr=pd.read_csv(os.path.join("app/Data", 'Training.csv'))

def OHV(cl_sym, all_sym):
    l = np.zeros([1, len(all_sym)])
    for sym in cl_sym:
        if sym in all_sym:
            l[0, all_sym.index(sym)] = 1
    return pd.DataFrame(l, columns=all_sym)

def contains(small, big):
    a=True
    for i in small:
        if i not in big:
            a=False
    return a

def possible_diseases(l,disease):
    poss_dis=[]
    for dis in set(disease):
        if contains(l,symVONdisease(df_tr,dis)):
            poss_dis.append(dis)
    return poss_dis

def symVONdisease(df,disease):
    ddf=df[df.prognosis==disease]
    m2 = (ddf == 1).any()
    return m2.index[m2].tolist()

def clean_symp(sym):
    return sym.replace('_',' ').replace('.1','').replace('(typhos)','').replace('yellowish','yellow').replace('yellowing','yellow')

disease = df_tr.iloc[:,-1].to_list()
all_symp_col=list(df_tr.columns[:-1])
all_symp=[clean_symp(sym) for sym in (all_symp_col)]
print(len(all_symp_col))

def possible_diseases(l):
    poss_dis=[]
    for dis in set(disease):
        if contains(l,symVONdisease(df_tr,dis)):
            poss_dis.append(dis)
    return poss_dis

def get_symptoms(message):
    correctsym1, psym1 = predictSym(message,vocab,app_tag)
    return correctsym1, psym1

def main_sp(name, sym = None):
    if sym is None:
        print("Hi Mr/Ms "+name+", can you describe you main symptom ?  \n\t\t\t\t\t\t",end="=>")
        sym1 = input("")
        sym = sym1

    print("\ntest input : ", sym)

    correctsym1, psym1 = predictSym(sym,vocab,app_tag)
    print("test correctsym 1 : ")
    print(correctsym1)
    print("test psym1 : ")
    print(psym1)

    if len(psym1)==0 and len(correctsym1)==0:
        print("I am sorry, I am not able to understand your symptoms.")
        return None

    print('Based on the signs you provided, I want to ask you a few things to confirm the information.')
    i=0
    while True and i<len(psym1):
        print('Do you experience '+psym1[i].replace('_',' ')+ ' ?')
        rep=input("")
        if str(rep)=='yes':
            correctsym1.append(psym1[i])
        i=i+1


    checkinput2nd = False
    print("Do you have any other symptoms?")
    sym2=input("")
    if(sym2 != "no"):
        checkinput2nd = True
        correctsym2, psym2 = predictSym(sym2,vocab,app_tag)
        i=0
        while True and i<len(psym2):
            print('Do you experience '+psym2[i].replace('_',' '))
            rep=input("")
            if str(rep)=='yes':
                correctsym2.append(psym2[i])
        i=i+1

    print("\n\nThank you for providing me with this information.\n")

    #create patient symp list
    # all_sym=[sym1,sym2]
    if checkinput2nd == False:
        all_sym=correctsym1
    else:
        all_sym=correctsym1 + correctsym2
    print("test lists all_sym : ")
    print(all_sym)
    #predict possible diseases
    diseases=possible_diseases(all_sym)
    print("test lists disease : ")
    print(diseases)

    if len(diseases) != 0:
        stop = False
        # print("Are you experiencing any ")
        for dis in diseases:
            if stop==False:
                for sym in symVONdisease(df_tr,dis):
                    if sym not in all_sym:
                        print("Are you experiencing any " + clean_symp(sym)+' ?')
                        while True:
                            inp=input("")
                            if(inp=="yes" or inp=="no"):
                                print("user input")
                                print(inp)
                                break
                            else:
                                print("provide proper answers i.e. (yes/no) : ",end="")

                        if inp=="yes":
                            all_sym.append(sym)
                            print("TEST all_sym 2 : ")
                            print(all_sym)

                            dise=possible_diseases(all_sym)
                            print("TEST possible diseases : ")
                            print(dise)
                            if len(dise)==1:
                                stop=True
                                break
                        else:
                            continue

    return predict_disease(all_sym)