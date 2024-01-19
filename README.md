# Search and Structure

This small python package is intended to help users to automate the retrieval and analysis process when surveying scientific literature on PubMed and ArXiv.

## Installation

Clone the repository and run `conda env create -f environment.yaml` to create a conda environment. Activate the environment with `conda activate search`

## Usage

1. Add a .env file to `search_and_structure` as follows:
```
BASE_PATH=<absolute path to the current folder>
OPENAI_API_KEY=<your OpenAI API key>
EMAIL=<your e-mail address that allows you to retrieve articles from pubmed via the pubmed API>
```

2. Add a .txt file in the `queries` folder with PubMed/MEDLINE-formatted search strings. You do not need to change the syntax for an ArXiv search, as the PubMed-style search strings are automatically translated to ArXiv-style search strings.
3. Modify the `retrieve_config`: add a `queries_path` pointing to a `.txt` file containing queries and a `destination_path` pointing to the retrieved articles. The `destination_path` must have the format `data/<ARTICLES_FILENAME>.csv`.
4. Modify the `structure_config`: add a `source_path` pointing to a `.csv` file containing retrieved articles and a `destination_path` pointing to the LLM-structured articles. The `destination_path` must have the format `data/<STRUCTURED_ARTICLES_FILENAME>.csv`. You need a paid OpenAI API subscription to use this script.
5. Execute the `retrieve` (and `structure`) scripts to retrieve the search results (and analyze them by using the OpenAI GPT-4 API).

Advanced users can modify the `p_structure_article` function in `src/openai_api_wrapper` to change the prompt and the types of information that are saved in the `structured_articles` file.