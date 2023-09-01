from transformers import pipeline
import pandas as pd

def _category_predictor(text, classifier):
    '''
    Returns category and score for each text
    '''
    pred = pd.DataFrame(classifier(text, top_k=1))
    classifier.call_count = 0
    cats = pred['label'][0]
    probs = pred['score'].round(3)[0]
    return [cats, probs]

def classify_text(df_texts:pd.DataFrame):
    '''
    Classifies texts of social network messages as relatable to greenery and not relatable to greenery.
    Returns a dataframe with the categories and probabilities.
    '''
    REP_ID = "Sandrro/greenery_finder_model_v3"
    classifier = pipeline("text-classification", model=REP_ID, tokenizer='cointegrated/rubert-tiny2', max_length=2048, truncation=True, device=0, use_auth_token=True)
    df_texts = df_texts.dropna(subset='text')
    df_texts.loc[df_texts['text'].map(type) == list, 'text'] = df_texts[df_texts['text'].map(type) == list]['text'].map(lambda x: ', '.join(x))
    df_texts[['cats','probs']] = pd.DataFrame(df_texts['text'].map(lambda x: _category_predictor(x, classifier)).to_list())

    return df_texts