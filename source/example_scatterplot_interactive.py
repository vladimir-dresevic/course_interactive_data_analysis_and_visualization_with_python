import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from books_data_prep import prepare_data
import plotly.express as px

df = pd.read_csv("data/books.csv")
df = prepare_data(df)

fig = px.scatter(data_frame=df,
                 x="ratings_count",
                 y="rating",
                 hover_name="title",
                 hover_data=["author", "genre", "ratings_count", "year_published", "page_count", "price", "language"],
                 trendline="ols")

fig.show()
