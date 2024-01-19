# Search and Structure

This small python package is intended to help users to automate the retrieval and analysis process when surveying scientific literature on PubMed and ArXiv.

## Installation

Clone the repository and run `conda env create -f environment.yaml` to create a conda environment. Activate the environment with `conda activate search`

## Usage

1. Add a `.env` file to the `search_and_structure` folder with the following variables:

```
BASE_PATH=<absolute path to the search_and_structure folder>
OPENAI_API_KEY=<your OpenAI API key>
EMAIL=<your e-mail address (needed for retrieving articles from PubMed)>
```

After adding a `.env` file with these variables you can start a test run! To customize the search, follow these steps:

2. Add a `.txt` file in the `queries` folder with PubMed/MEDLINE-formatted search strings. You don't need to change the syntax for an ArXiv search, as the PubMed-style search strings are automatically translated to ArXiv-style search strings (you can find example queries in `queries`)
3. The `retrieve_config` requires a `queries_path` pointing to a `.txt` file containing search queries and a `destination_path` pointing to the retrieved articles (see `retrieve_config.yaml`). The `destination_path` must have the format `data/<articles filename>.csv`.
4. The `structure_config` requires a `source_path` pointing to a `.csv` file containing retrieved articles and a `destination_path` pointing to the LLM-structured articles (see `structure_config.yaml`). The `destination_path` must have the format `data/<structured articles filename>.csv`. You need a paid OpenAI API subscription to use this script.
5. Execute the `retrieve` (and `structure`) scripts to retrieve the search results (and analyze them by using the OpenAI GPT-4 API).

Advanced users can modify the `p_structure_article` function in `src/openai_api_wrapper` to change the prompt and the types of information that are saved in the `structured_articles` file.