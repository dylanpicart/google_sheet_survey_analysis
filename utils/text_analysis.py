# utils/text_analysis.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud(text_series):
    text = " ".join(text_series.dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig
