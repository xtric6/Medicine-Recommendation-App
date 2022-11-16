import pandas as pd 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
import streamlit as st



ps = PorterStemmer()
STOPWORDS = stopwords.words('english')
new_word = ["having","feel",'symptoms','symptoms']
STOPWORDS.extend(new_word)

df = pd.read_csv('small_drug7.csv')
drug_use_dict = dict(zip(df['NAME_OF_PRODUCT'],df['USE_OF_DRUG']))


st.title('Drug Recommender :pill:')
st.subheader('Please do consult your doctor before taking any of the recommended drugs')
text = st.text_area(label = 'What symptoms are you experiencing', placeholder = 'Enter your symptoms here:')



#result = []
empty = []
token_length = []

#if st.text_area(label = 'What symptoms are you experiencing', placeholder = 'Enter your symptoms here:'):
def similarity(my_word):
    my_word = my_word.lower()
    my_word = word_tokenize(my_word)
    my_word_tokens = [ps.stem(word1) for word1 in my_word if word1 not in STOPWORDS]
    #my_word = " ".join(my_word_tokens)
    for i in list(drug_use_dict.values()):
        lemmed_words = i.lower()
        lemmed_words = word_tokenize(i)
        lemmed_tokens = [ps.stem(word) for word in lemmed_words if word not in STOPWORDS]
        a_token_len = len(lemmed_tokens)
        #lemmed_words = " ".join(lemmed_tokens)
        #match_word= sm(None,my_word,lemmed_words).ratio()
        my_set = set.intersection(set(my_word_tokens),set(lemmed_tokens))
        set_len = len(my_set)
        empty.append(set_len)
        token_length.append(a_token_len)
    return (empty,token_length) # returns a tuple

#text = st.text_area(label = 'What symptoms are you experiencing', placeholder = 'Enter your symptoms here:')
#def recommender():
    #text = st.text_area(label = 'What symptoms are you experiencing', placeholder = 'Enter your symptoms here:')
if st.button('Recommend'):
    #my_word = text
    my_ratios = similarity(text)
    freq = my_ratios[0]
    token_len = my_ratios[1]
    my_drug_names = list(drug_use_dict.keys())
    my_result = [my_drug_names,freq,token_len]
    my_result_df = pd.DataFrame(my_result).T
    my_result_df.columns = ['Drug_Names','Freqtokens','drug_t_len']
    #my_result_df = pd.Series(my_result).to_frame(['frequency']).sort_values(ascending=False,by='frequency')[:20]
    #print(my_ratios)
    #print(len(my_ratios))
    sorted_result_df= my_result_df.sort_values(by=['Freqtokens','drug_t_len'],ascending=[False, True])
        
    if sorted_result_df['Freqtokens'].sum() == 0:
        st.write('No drugs to recommend')
    
    else: 
        st.write('Here are the recommended drugs for the symptoms you are experiencing')
        st.markdown('**PLEASE DO CONSULT YOUR DOCTOR BEFORE TAKING ANY OF THE LISTED DRUGS**')
        st.dataframe(sorted_result_df.head(10))
    


#st.button('Recommend', on_click = recommender)