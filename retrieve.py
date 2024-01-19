from typing import Dict
import os
import hydra

from src import base_config
from src.arxiv_api_wrapper import retrieve_and_save_arxiv_articles
from src.pubmed_api_wrapper import retrieve_and_save_pubmed_articles
from src.utils import load_queries


@hydra.main(
    version_base = None,
    config_path = "config/",
    config_name = "retrieve_config",
)
def execute_search(user_config: Dict):
    os.makedirs(os.path.join(base_config["base_path"], "data"), exist_ok=True)
    queries_path = os.path.join(base_config["base_path"], user_config["queries_path"])
    destination_path = os.path.join(base_config["base_path"], user_config["destination_path"])
    assert os.path.exists(queries_path), "The path to the queries does not exist"
    assert not os.path.exists(destination_path), f"There's a already a file at {destination_path}. Change the destination path in the retrieve config or delete the file!"
    
    user_config["destination_path"] = destination_path
    user_config["email"] = base_config["email"]

    queries = load_queries(queries_path)
    if user_config["source"] == "pubmed":
        retrieve_and_save_pubmed_articles(user_config, queries)
    elif user_config["source"] == "arxiv":
        retrieve_and_save_arxiv_articles(user_config, queries)
    else:
        print(f"\nSource '{user_config['source']}' not supported. Please use 'pubmed' or 'arxiv'.")

if __name__ == "__main__":
    execute_search()
