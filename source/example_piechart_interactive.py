import matplotlib.pyplot as plt
import pandas as pd
from books_data_prep import prepare_data
import plotly.express as px

df = pd.read_csv("data/books.csv")
df = prepare_data(df)

section_counts = df["section"].value_counts().reset_index()

fig = px.pie(section_counts, names="section", values="count")
fig.show()
