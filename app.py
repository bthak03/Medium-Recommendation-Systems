import streamlit as st 
import numpy as np
from PIL import Image
import pandas as pd
from elasticsearch import Elasticsearch, RequestsHttpConnection
host = '52.90.189.105'
region = 'us-east-1'
st.set_page_config(layout="wide")

def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': host, 'port': 9200}])
    if es.ping():
        print('Yupiee  Connected ')
    else:
        print('Awww it could not connect!')
    return es
es = connect_elasticsearch()

def query_func(userinput):
    articles = []
    results = es.search(index = 'mediumarticle', doc_type= 'doc', body = { 'size':5,'query':{'match':{"title": userinput}}})
    hits = results['hits']['hits']
    
        
    for i in range(len(hits)):
        articles.append(hits[i]['_source']['_soucre'])
       
    return articles


# Streamlit layout
image = Image.open('sidebarimage.jpg')
st.sidebar.image(image)
st.title('Medium Article Recommendation System')



my_expander = st.beta_expander('About App', expanded= False)

with my_expander:
    text = open('files/aboutapp.txt', 'r')
    st.write(text.read())

# elasticsearch query
with st.beta_container():
    search, select,article = st.beta_columns((.5,.3, .2))
    userText = search.text_input("Write your search here", "Python Data Science")
    add_selectbox = select.selectbox('Select Search then Recommend', ('search', 'recommend'))
    output = query_func(userinput= userText)
    a = article.selectbox('Article', range(len(output)))

#query = es.search(index = 'mediumarticle', doc_type= 'doc', body = { 'size':5,'query':{'match':{"title": userText}}})
#query = query['hits']['hits']




if add_selectbox == 'search':
    f,s,t = st.beta_columns(3)
    first = [f,s,t]
    fo, f, six = st.beta_columns(3)
    second = [fo,f,six]
    j = 0 
    for i in first:
        with i:
            st.header(output[j]['title'])
            st.subheader(output[j]['subtitle'])
            st.write(output[j]['article_url'])
            #st.markdown(    )
        j += 1
    j = 3
    for i in second:
        if j < 5:
            with i:
                st.header(output[j]['title'])
                st.subheader(output[j]['subtitle'])
                st.write(output[j]['article_url'])
        else:
            st.header('')
            st.subheader('')
            st.write('')
        j += 1

        
       
elif add_selectbox == 'recommend':
    st.write(str(output[a]))
#query_func(userinput= userText)




