import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().replace(' ', '_').replace('-', '_')
                  for col in df.columns]
    return df


def convert_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df[['times_borrowed', 'page_count']] = df[[
        'times_borrowed', 'page_count']].astype('Int16')
    df['total_copies'] = pd.to_numeric(df['total_copies'], errors='coerce')
    df['total_copies'] = df['total_copies'].astype('Int16')

    df['year_published'] = pd.to_numeric(df['year_published'], errors='coerce')
    df['year_published'] = df['year_published'].astype('Int16')
    return df


def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df['last_borrowed_date'] = pd.to_datetime(
        df['last_borrowed_date'], errors='coerce', format='%d_%b_%y')
    return df


def convert_to_category(df: pd.DataFrame) -> pd.DataFrame:
    df['genre'] = df['genre'].astype('category')
    df['section'] = df['section'].astype('category')
    df['language'] = df['language'].astype('category')
    return df


def parse_ratings(df: pd.DataFrame) -> pd.DataFrame:

    def parse_rating(text):
        if pd.isna(text) or str(text).strip().lower() == "no rating available":
            return None

        parts = str(text).split()

        try:
            return float(parts[0])
        except (ValueError, IndexError):
            return None

    df['rating'] = df['rating'].apply(parse_rating)

    return df


def parse_ratings_count(df: pd.DataFrame) -> pd.DataFrame:

    def parse_rating_count(text):
        if pd.isna(text) or str(text).strip().lower() == "no reviews":
            return None

        parts = str(text).replace(',', '').split()

        try:
            return int(parts[0])
        except (ValueError, IndexError):
            return None

    df['ratings_count'] = df['ratings_count'].apply(parse_rating_count)

    return df


def parse_prices(df: pd.DataFrame) -> pd.DataFrame:

    def parse_price(text):

        if pd.isna(text) or str(text).strip().lower() == "price not available":
            return None

        try:
            price_str = str(text).replace(',', '').replace('$', '').strip()
            return float(price_str)
        except ValueError:
            return None

    df['price'] = df['price'].apply(parse_price)

    return df


def split_dimensions_to_separate_columns(df: pd.DataFrame) -> pd.DataFrame:
    df[['dimensions_width', 'dimensions_depth', 'dimensions_height']] = df['dimensions'].str.replace(
        "inches", "").str.replace(" ", "").str.split('x', expand=True).astype(float)

    df.drop('dimensions', axis=1, inplace=True)

    return df


def split_catalog_position_to_separate_columns(df: pd.DataFrame) -> pd.DataFrame:
    df[['catalog_shelf', 'catalog_row', 'catalog_row_number']
       ] = df['catalog_position'].str.split('-', expand=True)

    return df


def remove_na(df: pd.DataFrame) -> pd.DataFrame:
    del df['isbn']
    del df['thumbnail']

    df.dropna(axis=0, thresh=12, inplace=True)

    df.dropna(subset=['catalog_position', 'title',
              'author'], how="all", inplace=True)

    df['title'] = df['title'].fillna("Unknown title")
    df['author'] = df['author'].fillna("Unknown author")
    df['genre'] = df['genre'].astype(object).fillna(
        "Unknown genre").astype('category')
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    df.drop_duplicates(subset=['catalog_position'], keep='first', inplace=True)
    return df


def standardize_languages(df: pd.DataFrame) -> pd.DataFrame:

    mapping = {
        'eng': 'en',
        'En': 'en',
        'pt-BR': 'pt',
        'zh-CN': 'cn'
    }

    df['language'] = df['language'].astype(
        object).replace(mapping).astype('category')

    return df


def standardize_sections(df: pd.DataFrame) -> pd.DataFrame:

    mapping = {
        'Young Adult (YA)': 'Young Adult',
        "Children's": "Children",
        "Children's Fiction": "Children"
    }

    df['section'] = df['section'].astype(
        object).replace(mapping).astype("category")

    return df


def standardize_authors(df: pd.DataFrame) -> pd.DataFrame:

    mapping = {
        'Lev Tolstoy': 'Leo Tolstoy',
        'Winston S. Churchill': 'Winston Churchill',
        'Plato': 'Platon',
        'Will Shakespeare': 'William Shakespeare'
    }

    df['author'] = df['author'].replace(mapping)
    return df


def standardize_genres(df: pd.DataFrame) -> pd.DataFrame:

    mapping = {
        'Classic': 'Classics',
        'Classic Literature': 'Classics',
        'Novel': 'Novels',
        "Religion, Spirituality": "Religion & Spirituality",
        "Spirituality": "Religion & Spirituality",
        "Historical": "History",
        "Religious Fiction": "Religion & Spirituality",
        "Religion": "Religion & Spirituality",
        "Utopian Fiction": "Utopian",
        "Utopian Literature": "Utopian",
        "Natural History": "History",
        "Children's Stories": "Children's Fiction",
        "Children's Literature": "Children's Fiction",
        "Music/Songbooks": "Music",
        "Epic Poetry": "Poetry"
    }

    df['genre'] = df['genre'].astype(
        object).replace(mapping).astype('category')

    return df


def remove_future_books(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['year_published'] <= pd.Timestamp.today().year]


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.pipe(standardize_column_names).pipe(convert_to_numeric).pipe(convert_to_datetime).pipe(convert_to_category).pipe(parse_ratings).pipe(parse_ratings_count).pipe(parse_prices).pipe(split_dimensions_to_separate_columns).pipe(split_catalog_position_to_separate_columns).pipe(remove_na).pipe(remove_duplicates).pipe(standardize_languages).pipe(standardize_sections).pipe(standardize_authors).pipe(standardize_genres).pipe(remove_future_books)
