import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from books_data_prep import prepare_data
import plotly.express as px

df = pd.read_csv("data/books.csv")
df = prepare_data(df)

fig = px.histogram(data_frame=df,
                   x="rating",
                   color="section",
                   marginal="box",
                   hover_data=["title", "author", "rating", "ratings_count"])

fig.update_layout(
    xaxis_title="Rating",
    yaxis_title="Number of Books"
)

fig.show()
