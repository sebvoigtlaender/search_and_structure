from typing import Dict

import arxiv
from tqdm import tqdm

from src.utils import convert_datetime_to_date_string, dict_to_df, parse_pubmed_to_arxiv_query, save_articles


def retrieve_and_save_arxiv_articles(user_config: Dict, queries: str):
    def single_query(user_config: Dict, query: str):
        articles = []
        arxiv_query = parse_pubmed_to_arxiv_query(query)
        search = arxiv.Search(
            query = f"{arxiv_query}",
            max_results = user_config["arxiv"]["n_results"],
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        results = client.results(search)

        for record in list(results):
            article = {}
            article["title"] = record.title if record.title else ""
            article["abstract"] = record.summary if record.summary else ""
            article["journal"] = record.journal_ref if record.journal_ref else ""
            article["date"] = convert_datetime_to_date_string(record.published) if record.published else ""
            article["authors"] = [record.authors[i].name for i in range(len(record.authors))] if record.authors else []
            article["affiliation"] = ""
            article["article_type"] = ""
            article["n_citations"] = ""
            article["doi"] = record.doi if record.doi else ""
            articles.append(article)
        return articles

    articles_dict = {}
    client = arxiv.Client()
    for query in tqdm(queries):
        articles = single_query(user_config, query)
        articles_dict[query.strip()] = articles
    save_articles(dict_to_df(articles_dict), f"{user_config['destination_path']}")
