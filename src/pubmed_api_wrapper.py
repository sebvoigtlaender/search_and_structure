import time
from http.client import IncompleteRead, RemoteDisconnected
from typing import Dict, List
from urllib.error import HTTPError

from Bio import Entrez, Medline
from tqdm import tqdm

from src.utils import convert_to_dates_pubmed, dict_to_df, save_articles


def retrieve_and_save_pubmed_articles(user_config: Dict, queries: List, retries: int = 5) -> Dict:

    def get_n_citations(record_citations: List) -> int:
        link_set = record_citations[0]["LinkSetDb"]
        if link_set:
            return len(link_set[0]["Link"])
        return None

    Entrez.email = user_config["email"]
    articles_dict = {}

    start_date, end_date = convert_to_dates_pubmed(user_config["pubmed"]["date_range"])
    n_art = 0

    for query in queries:
        search_query = f"{query.strip()}"
        for retry in range(retries):
            try:
                handle = Entrez.esearch(
                    db="pubmed",
                    term=search_query,
                    sort=user_config["pubmed"]["sort_by"],
                    retmax=user_config["pubmed"]["n_results"],
                    mindate=start_date,
                    maxdate=end_date,
                )
                record = Entrez.read(handle)
                n_art += int(record["Count"])
                break
            except (IncompleteRead, ValueError, HTTPError, RemoteDisconnected) as e:
                wait_time = 2**retry
                print(
                    f"{e.__class__.__name__} occurred. Waiting for {wait_time} seconds."
                )
                time.sleep(wait_time)
            if retry == retries - 1:
                print("Max retries reached. Skipping this query...")
                continue

        print(f"\rtotal articles retrieved: {n_art}", end="", flush=True)
        
        pmid_list = record["IdList"]
        articles = []

        for pmid in tqdm(pmid_list):
            for retry in range(retries):
                try:
                    handle = Entrez.efetch(
                        db="pubmed", id=pmid, rettype="medline", retmode="text"
                    )
                    record = Medline.read(handle)
                    break
                except (IncompleteRead, HTTPError, RemoteDisconnected) as e:
                    wait_time = 2**retry
                    print(
                        f"{e.__class__.__name__} occurred. Waiting for {wait_time} seconds."
                    )
                    time.sleep(wait_time)
                if retry == retries - 1:
                    print("Max retries reached. Skipping this article...")
                    continue
                
            handle_citations = Entrez.elink(
                dbfrom="pubmed", id=pmid, linkname="pubmed_pubmed_citedin"
            )
            record_citations = Entrez.read(handle_citations)
            n_citations = get_n_citations(record_citations)

            article = {}
            article["title"] = record.get("TI", "")
            article["abstract"] = record.get("AB", "")
            article["journal"] = record.get("JT", "")
            article["date"] = record.get("DP", "") if record.get("DP", "") else ""
            article["authors"] = record.get("AU", "")
            article["affiliation"] = record.get("AD", "")
            article["article_type"] = record.get("PT", "")
            article["n_citations"] = n_citations

            if "AID" in record:
                for aid in record["AID"]:
                    if aid.endswith("[doi]"):
                        article["doi"] = aid.rstrip("[doi]")
                        break
                else:
                    article["doi"] = ""
            else:
                article["doi"] = ""

            articles.append(article)
        articles_dict[query.strip()] = articles
        save_articles(dict_to_df(articles_dict), f"{user_config['destination_path']}")
