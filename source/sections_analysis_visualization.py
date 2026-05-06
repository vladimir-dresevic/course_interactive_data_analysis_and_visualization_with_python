import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from books_data_prep import prepare_data

df = pd.read_csv('data/books.csv')

df = prepare_data(df)

inventory_gap = df.groupby('section').agg({
    'title': 'count',
    'times_borrowed': 'sum'
})

inventory_gap['titles_to_borrow_ratio'] = inventory_gap['times_borrowed'] / inventory_gap['title']

inventory_gap = inventory_gap.sort_values(by=['titles_to_borrow_ratio'], ascending=False).reset_index()

sns.barplot(
    data=inventory_gap,
    x="section",
    y="titles_to_borrow_ratio",
    order=inventory_gap['section']
)

plt.title("Borrows per book by library section")
plt.xlabel("Section")
plt.ylabel("Borrows per book")

plt.show()



#print(inventory_gap.sort_values(by=['titles_to_borrow_ratio'], ascending=False))


