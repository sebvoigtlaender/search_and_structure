from typing import Dict
import os
import hydra
import pandas as pd

from src import base_config
from src.openai_api_wrapper import structure_articles
from src.utils import confirm_structure, save_articles


@hydra.main(
    version_base = None,
    config_path = "config/",
    config_name = "structure_config",
)
def structure_retrieved_articles(user_config: Dict):
    
    source_path = os.path.join(base_config["base_path"], user_config["source_path"])
    destination_path = os.path.join(base_config["base_path"], user_config["destination_path"])
    assert os.path.exists(source_path), "Please provide a valid source path."
    assert source_path.endswith(".csv"), "Please provide a valid source file. File type should be .csv."
    assert not os.path.exists(destination_path), f"There's a already a file at {destination_path}. Change the destination path in the structure config or delete the file!"
    
    try:
        if confirm_structure() == "y":
            articles = pd.read_csv(source_path)
            assert "title" in articles.keys() and "abstract" in articles.keys(), "Please provide a source file with 'title' and 'abstract' columns."
            structured_articles, _ = structure_articles(articles)
            print(f"\nSaving {len(structured_articles)} LLM-structured articles.")
            save_articles(structured_articles, user_config["destination_path"])
    except:
        print(f"\nAn error occured.")

if __name__ == "__main__":
    structure_retrieved_articles()
