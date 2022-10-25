from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize

analyzer = SentimentIntensityAnalyzer()

paragraph = """ 
    I'm really happy with my purchase.
    I've been using the product for two weeks now.
    It does exactly as described in the product description.
    The only problem is that it takes a long time to charge.
    However, since I recharge during nights, this is something I can
live with."""

cumulative_sentiment = 0.0
sentence_list = tokenize.sent_tokenize(paragraph)
for sentence in sentence_list:
    vs = analyzer.polarity_scores(sentence)
    cumulative_sentiment += vs["compound"]
    print(sentence,": ", vs["compound"] )

average_sentiment = cumulative_sentiment / len(sentence_list)
print("Average score: ", average_sentiment)