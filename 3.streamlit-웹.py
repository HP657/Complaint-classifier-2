import streamlit as st
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pickle
import requests

@st.cache_data()
def load_data():
    df = pd.read_csv('data\output2.csv', encoding='euc-kr', sep='\t')
    return df

@st.cache_data()
def preprocess_data(df):
    okt = Okt()
    df['tokens'] = df['민원 내용'].apply(lambda x: ' '.join(okt.morphs(x)))
    return df

@st.cache_data()
def load_model():
    with open('model\model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def predict_department(complaint, vectorizer, encoder, model):
    complaint_vec = vectorizer.transform([complaint])
    prediction = model.predict(complaint_vec)
    return encoder.inverse_transform(prediction)[0]

def besok(text):
    url = 'https://api.matgim.ai/54edkvw2hn/api-keyword-slang'
    headers = {
        'content-type': 'application/json',
        'x-auth-token': '5ea265fc-0070-4e8b-a0e3-f0ca42451ea4'
    }
    data = {
        'document': f'{text}'
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    response_data = result.get('result', {}).get('data', [])
    return response_data

def main():
    st.set_page_config(
        page_title="민원 분류기",
        page_icon=r"photo\icon.png",
        initial_sidebar_state="expanded"
    )

    img_url = r"photo\banner.png"
    st.image(img_url, width=300)
    text = st.text_area('민원 내용을 작성해주세요.')
    btn = st.button('클릭하기')

    if btn:
        response_data = besok(text)
        if response_data:
            vulgar_words = [item['text'] for item in response_data if item['category'] == 'vulgarism']
            if vulgar_words:
                vulgar_words_str = ", ".join([f"{word}" for word in vulgar_words])
                st.markdown(f"<span style='color:red;'> 비속어: \"{vulgar_words_str}\"가 포함되어 있습니다. 수정 후 다시 제출해주세요.</span>", unsafe_allow_html=True)
        else:
            df = load_data()
            df = preprocess_data(df)

            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(df['tokens'])

            encoder = LabelEncoder()
            y = encoder.fit_transform(df['담당부서'])

            model = load_model()

            result = predict_department(text, vectorizer, encoder, model)
            st.write(f'{result} 부서에 전달되었습니다.')

if __name__ == "__main__":
    main()
