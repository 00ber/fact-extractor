
import requests
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from templates import refinement_template, fact_extraction_template

import logging
logger = logging.getLogger("uvicorn")


def retrieve_document_contents(document_url):
    response = requests.get(document_url)
    return response.text

def get_refinement_chain():
    refinement_prompt = PromptTemplate.from_template(refinement_template)
    refine_facts_chain = (
        {
            "extracted_facts": lambda x: x["facts"],
        }
        | refinement_prompt
        | ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    )

    return refine_facts_chain

def get_fact_extraction_chain():
    fact_extraction_prompt = PromptTemplate.from_template(fact_extraction_template)
    extract_facts_chain = (
        {
                "question": lambda x: x["question"],
                "logs": lambda x: retrieve_document_contents(x["document_url"]),
        }
        | fact_extraction_prompt
        | ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    )

    return extract_facts_chain


async def get_facts(question, document_urls):
    fact_extraction_chain = get_fact_extraction_chain()
    inputs = [{ "question": question, "document_url" : d} for d in document_urls]
    logger.info(inputs)
    extraction_results = await fact_extraction_chain.abatch(inputs)
    facts = "\n".join([r.content for r in extraction_results]).split("\n")
    enumerated_facts = [f"{i}. {f}" for i, f in enumerate(facts, 1)]
    refinement_chain = get_refinement_chain()
    refined_results = await refinement_chain.ainvoke({ "question": question, "facts": "\n".join(enumerated_facts) })
    return {"question": question, "facts": refined_results.content.split("\n")}
