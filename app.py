import pandas as pd 
from nltk.tokenize import word_tokenize
#from nltk.downloader import download, download_shell
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
import streamlit as st
import sqlite3




ps = PorterStemmer()
STOPWORDS = stopwords.words('english')
new_word = ["having","feel",'symptoms','symptoms','experiencing','experienced','feeling']
STOPWORDS.extend(new_word)

df = pd.read_csv('NAFDAC-DRUGS.csv',usecols = ['NAME_OF_PRODUCT','USE_OF_DRUG','IMAGE'])
df_dict = df.set_index('NAME_OF_PRODUCT').T.to_dict('list')
list_drug_symptoms = [i[0] for i in list(df_dict.values())]
list_drug_images = [i[1] for i in list(df_dict.values())]


tab1, tab2= st.tabs(["Drug Recommender", "WordCloud ☁️"])

with tab1:
    st.title('Drug Recommender :pill:')
    st.subheader('Please do consult your doctor before taking any of the recommended drugs')

    text = st.text_area(label ='Enter the KEYWORDS of the symptoms you are experiencing.',
                        placeholder = 'Enter the keywords of the symptoms are you experiencing e.g headache, stomach pain, diarrhea, body pain,fever\
,infection,cold,catarrh,diabetes,hypertension,diarrhea,cough,vagina infections,body odour e.t.c'
                        ,height = 100)

    field_names = ['having','feel','symptoms','symptoms','experience','experiencing']



    empty = []
    token_length = []
    def similarity(my_word):
        my_word = my_word.lower()
        my_word = re.sub(r'[^\w\s]', ' ',my_word)
        my_word = word_tokenize(my_word)
        my_word_tokens = [ps.stem(word1) for word1 in my_word if word1 not in STOPWORDS]

        for i in list_drug_symptoms:
            drug_symptom = i.lower()
            drug_symptom = re.sub(r'[^\w\s]', ' ',drug_symptom)
            drug_symptom = word_tokenize(drug_symptom)
            drugs_symptom_tokens = [ps.stem(word) for word in drug_symptom if word not in STOPWORDS]
            a_token_len = len(drugs_symptom_tokens)
            my_set = set.intersection(set(my_word_tokens),set(drugs_symptom_tokens))
            set_len = len(my_set)
            empty.append(set_len)
            token_length.append(a_token_len)
        return (empty,token_length) # returns a tuple

    if st.button('Recommend'):
        my_ratios = similarity(text)
        freq = my_ratios[0]
        token_len = my_ratios[1]
        my_drug_names = list(df_dict.keys())
        my_drug_images = list_drug_images
        my_result = [my_drug_names,freq,token_len,my_drug_images]
        my_result_df = pd.DataFrame(my_result).T
        my_result_df.columns = ['Drug_Names','Freqtokens','drug_t_len','drug_images']
        sorted_result_df= my_result_df.sort_values(by=['Freqtokens','drug_t_len'],ascending=[False, True])
        top5 = sorted_result_df.head(5)

        while text:
            if sorted_result_df['Freqtokens'].sum() == 0:
                st.subheader('There are no drugs to recommend you at this time.')
                result = 'There are no drugs to recommend you at this time.'
                break
        
            else: 
                st.write('**Here are the recommended drugs for the symptoms you are experiencing**')
                result = ','.join(top5['Drug_Names'].tolist())
            
            drug1,drug2,drug3,drug4,drug5 = st.columns(5)

            #IMAGES
            with drug1:
                st.write(top5.iloc[0,0])
                st.image(top5.iloc[0,3])
            
            with drug2:
                st.write(top5.iloc[1,0])
                st.image(top5.iloc[1,3])

            with drug3:
                st.write(top5.iloc[2,0])
                st.image(top5.iloc[2,3])

            with drug4:
                st.write(top5.iloc[3,0])
                st.image(top5.iloc[3,3])

            with drug5:
                st.write(top5.iloc[4,0])
                st.image(top5.iloc[4,3])
                break
        else:
            st.subheader('Please Enter a valid response!')
            result = 'Please Enter a valid response!'


        def database():
            conn = sqlite3.connect('mydata1.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS users_symptom(symptoms TEXT,recommendations TEXT)""")
            c.execute("INSERT INTO users_symptom VALUES(?,?)",(text,result))
            conn.commit()
            #conn.close()

        database()

with tab2:
    st.subheader('Word Cloud showing the common symptoms this Webapp will recommend drugs for')
    st.image('wordcloud.png')



   