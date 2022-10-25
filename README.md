# A small sentiment analysis based on an amazon product reviews

I am really proud of this program

The objective was to get a sentiment plot of different reviews on a product listed.
Using vaderSentiment a python library, we can get a sentiment analysis of a given sentence ranging from -1 to 1 (good to bad)

So I had to build a scraper that will go throught each review get it's title, rating, reviewer id and save all this small information into a simple database.

After that, to get the sentiment score of the reviews, the code needed to loop through all the reviews in the database and for each review, break it down to sentences and have them analyze using vaderSentiment then get an average sentiment score by adding all the sentiment and dividing by the number of sentences.

Finally using matplotlib we created a violin plot based on the sentiment scores we have previously got and  this gives us this **beautiful** graph

![sentiment_analysis](https://user-images.githubusercontent.com/109516711/197863249-74539188-5b74-422a-855a-70d3ef7208a4.png)
