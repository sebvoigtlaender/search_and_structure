import datetime, json, re, time
from typing import Dict, List

import openai
import pandas as pd
from IPython.display import HTML, display
from openai.error import (
    APIConnectionError,
    APIError,
    RateLimitError,
    ServiceUnavailableError,
    Timeout,
)


display_full_df = lambda df: display(HTML(df.to_html()))

def call_chat_api(messages: List[str], retries: int = 5, model: str = "gpt-4"):
    assert openai.api_key
    for retry in range(retries):
        try:
            return openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
        except (RateLimitError, Timeout, APIError, ServiceUnavailableError) as e:
            wait_time = 2 * retry
            print(
                f"\n{e.__class__.__name__} occurred. Waiting for {wait_time} seconds."
            )
            time.sleep(wait_time)
        except APIConnectionError as e:
            print(f"\nFailed to connect to OpenAI API: {e}")


def confirm_structure():
    try:
        return input(f"\nWARNING: The next step will structure articles using OpenAI GPT-4. This may incur considerable costs, depending on the number of articles. Do you want to continue? (y/n): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped structuring articles.")


def deserialize_dict(string: str):
    try:
        dictionary = json.loads(string)
        return dictionary
    except json.JSONDecodeError:
        return None


def convert_to_dates_pubmed(date_string: str):
    start_date = date_string.split(", ")[0].replace("-", "/")
    end_date = date_string.split(", ")[1].replace("-", "/")
    return start_date, end_date


def dict_to_df(df_dict: Dict):
    list_df = []
    for key, df in df_dict.items():
        df_temp = pd.DataFrame({"key": [key] * len(df)})
        df_temp = pd.concat([df_temp, pd.DataFrame(df)], axis=1)
        list_df.append(df_temp)

    df_final = pd.concat(list_df, ignore_index=True)
    return df_final


def load_queries(queries_path: str):
    with open(queries_path, "r") as f:
        queries = f.read().split("\n")
    return queries


def parse_pubmed_to_arxiv_query(query: str) -> str:
    def format_title_terms(match):
        terms = match.group(1).split()
        return '(' + ' AND '.join(f'ti:{term}' for term in terms) + ')'
    arxiv_query = re.sub(r'\"([^\"]+)\"\[Title\]', format_title_terms, query)
    arxiv_query = arxiv_query.replace(' AND ', ' AND ').replace(' OR ', ' OR ')
    return arxiv_query


def parse_pubmed_to_google_scholar_query(query: str) -> str:
    def format_title_terms(match):
        term = match.group(1)
        return f'intitle:"{term}"'
    google_scholar_query = re.sub(r'\"([^\"]+)\"\[Title\]', format_title_terms, query)
    return google_scholar_query


def convert_datetime_to_date_string(dt: datetime.datetime) -> str:
    return dt.strftime("%Y %B %d")


def save_articles(articles_dict: Dict, path: str):
    articles_dict.to_csv(path, index=False)


def open_articles(path: str):
    return pd.read_csv(path)


def select_articles(articles: pd.DataFrame, key: str, query: str, sort: str = None, regex: bool = True, neg: bool = False):
    if not neg:
        x = articles[articles[key].astype(str).str.contains(query, na=False, case=False, regex=regex)]
    else:
        x = articles[~articles[key].astype(str).str.contains(query, na=False, case=False, regex=regex)]
    if sort:
        x = x.sort_values(by=sort, ascending=False)
    return x


def sort_articles(articles: pd.DataFrame, sort: str, ascending: bool = False):
    return articles.sort_values(by=sort, ascending=ascending)


def select_cols(articles: pd.DataFrame, *cols: str) -> pd.DataFrame:
    return articles[list(cols)]


def articles_to_csv(articles: pd.DataFrame, path: str):
    articles.to_csv(path, index=False)
