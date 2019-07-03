from textblob import TextBlob


def sentiment_analyse(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity * blob.sentiment.subjectivity


if __name__ == "__main__":
    sentiment_analyse(
        """
Real-time data connectivity on the blockchain, real world applications being built on a platform that is backed by an existing company to whom is also partnered with the likes of #AWS, #ORACLE and #MICROSOFT.
How can one not feel bullish about this super GEM?
        """
    )
