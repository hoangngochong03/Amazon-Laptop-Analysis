from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
import emoji

def remove_emoji(text):
    if pd.isna(text):
        return text
    text = emoji.replace_emoji(text, replace='')
    return text

def sentiment(title,review):
    ratetitle=0.2
    ratereview=0.8
    if pd.isna(review):
        ratetitle=1
        ratereview=0
        review=''
    elif pd.isna(title):
        ratetitle=0
        ratereview=1
        title=''
    elif pd.isna(review) and pd.isna(title):
        return 0        
    title = str(title)
    review = str(review)
    tokens1 = tokenizer.encode(title, return_tensors='pt',max_length=512)
    tokens2 = tokenizer.encode(review, return_tensors='pt',max_length=512)
    result1 = model(tokens1)
    result2 = model(tokens2)
    score1=int(torch.argmax(result1.logits))+1
    score2=int(torch.argmax(result2.logits))+1
    score=score1*ratetitle + score2*ratereview
    return score

def classify_score(score):
    if score < 2.8:
        return 'Negative'
    elif 2.8 <= score <= 3.4:
        return 'Neutral'
    else:
        return 'Positive'
    
    
#Link huggingface: https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

data=pd.read_csv(r"data\reviews.csv")

data["Title"]=data["Title"].astype("string")
data["Review"]=data["Review"].astype("string")


data['Title'] = data['Title'].apply(remove_emoji)
data['Review'] = data['Review'].apply(remove_emoji)
    

data['Score'] = data.apply(lambda row: sentiment(row['Title'], row['Review']), axis=1)

data["Label"]=data["Score"].apply(classify_score)

data.to_csv("../data/Reviews_sentiment.csv",index=False)

data.to_excel("../tmp/reviews_sentiment.xlsx",index=False)