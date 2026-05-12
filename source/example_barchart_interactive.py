import matplotlib.pyplot as plt
import pandas as pd
from books_data_prep import prepare_data
import plotly.express as px

df = pd.read_csv("data/books.csv")
df = prepare_data(df)

genre_counts = df["genre"].value_counts().reset_index()

fig = px.bar(genre_counts, x="genre", y="count", color="genre")
fig.show()