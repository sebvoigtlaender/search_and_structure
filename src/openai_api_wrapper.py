import os

import openai
import pandas as pd
from tqdm import tqdm

from src.utils import call_chat_api, deserialize_dict

openai.api_key = os.environ["OPENAI_API_KEY"]


def p_structure_article(title: str, abstract: str):
    p_sys = "You are an AI assistant for producing a structured representation of given unstructured text. Follow instructions precisely and to the letter; refrain from inventing content that is not in the text."
    p_user = f'''You will be given the title and the abstract of an academic paper, marked by TITLE: and ABSTRACT: .
From the title and abstract, extract information on the motivation/rationale for the study, the data used, the machine learning method, and the results (with numbers!).
Return the information in the specified format, as seen below. If there is no information in the title or abstract on some of these keys, entry 'no information' into the corresponding field.


TITLE:
"""
{title}
"""
ABSTRACT: 
"""
{abstract}
""" 

Specified format: {{"motivation": <unstructured text>, "data": <unstructured text>, "model": <unstructured text>, "results": <unstructured text>}}

Your response: '''

    return [{"role": "system", "content": p_sys}, {"role": "user", "content": p_user}]


def structure_articles(articles: pd.DataFrame):
    structured_articles = []
    responses = []
    for i in tqdm(range(len(articles))):
        p = p_structure_article(articles.iloc[i]["title"], articles.iloc[i]["abstract"])
        response = call_chat_api(p)["choices"][0]["message"]["content"]
        responses.append(
            {
                "key": articles.iloc[i]["key"] if "key" in articles.keys() else "",
                "title": articles.iloc[i]["title"],
                "response": response,
            }
        )
        try:
            response_dict = deserialize_dict(response)
            structured_articles.append(
                {
                    "key": articles.iloc[i]["key"] if "key" in articles.keys() else "",
                    "title": articles.iloc[i]["title"],
                    "abstract": articles.iloc[i]["abstract"],
                    "doi": articles.iloc[i]["doi"] if "doi" in articles.keys() else "",
                    "motivation": response_dict["motivation"],
                    "data": response_dict["data"],
                    "model": response_dict["model"],
                    "results": response_dict["results"],
                }
            )
        except:
            print(
                f"\nAn error occured while structuring article {articles.iloc[i]['title']}. Skipping this article..."
            )
    structured_articles, responses = pd.DataFrame(structured_articles), pd.DataFrame(
        responses
    )
    return structured_articles, responses
