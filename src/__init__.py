import os
from dotenv import load_dotenv

load_dotenv()
base_config = {"base_path": os.environ["BASE_PATH"],
       "openai_api_key": os.environ["OPENAI_API_KEY"],
       "email": os.environ["EMAIL"],
    }

__all__ = ['retrieve_and_save_arxiv_articles', 'retrieve_and_save_pubmed_articles', 'confirm_structure', 'load_queries', 'save_articles']

from .arxiv_api_wrapper import retrieve_and_save_arxiv_articles
from .pubmed_api_wrapper import retrieve_and_save_pubmed_articles
from .utils import confirm_structure, load_queries, save_articles
