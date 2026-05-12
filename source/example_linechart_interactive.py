import matplotlib.pyplot as plt
import pandas as pd
from books_data_prep import prepare_data
import plotly.express as px

df = pd.read_csv("data/books.csv")
df = prepare_data(df)

borrowed_by_year = df.groupby("year_published")["times_borrowed"].sum().reset_index()

fig = px.line(borrowed_by_year, x="year_published", y="times_borrowed", labels={
    "year_published": "Year Published",
    "times_borrowed": "Times Borrowed"
},
markers=True
)

fig.update_xaxes(
    rangeslider_visible=True
)

fig.show()
