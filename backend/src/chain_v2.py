
import requests
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from templates import refinement_template

from logger import logger

fact_extraction_template = """"You are provided with a specific QUESTION, a list of CURRENT FACTS (which may be empty) and a list of NEW LOGS.
Your task is to analyze the NEW LOGS to extract new facts relevant to the QUESTION and update the list of CURRENT FACTS based on this new information. 
Ensure that your extractions are accurate and relevant.


Task Instructions:
------------------
Step 1. Fact Extraction:
Review each log entry carefully. 
Identify and extract any new and relevant information that directly addresses the question posed. 
Remember that the logs are ordered. So, the logs that come later are more recent.
Focus on extracting clear and concise facts that are pertinent to the question. 
The extracte facts must sound like facts, rather than answer to the question directly.

Step 2. Fact Integration:
Add New Facts: Evaluate the extracted facts and add them to the list of current facts if they provide new insights or additional details not previously covered.
Modify Existing Facts: If any new information contradicts or updates an existing fact, modify the existing entry to reflect the most accurate and up-to-date information.
Confirm Existing Facts: Where new data supports (confirms) existing facts without adding new information, do not change the existing facts.

Step 3. Output:
Your output must STRICTLY be the list of updated facts only, without any prefix or additional context. Each fact must be separated by a newline.

Examples:
------------------
QUESTION: 
What are the team decisions?

CURRENT FACTS:
The team is going to use Haskell to code the backend.
The team is meeting on Friday to discuss the next week's goals.

LOGS:
Log Entry 1: John: I don't think we should use Haskell for the backend. Since none of us are proficient in it, the learning cost is too steep.
Log Entry 2: Alex: I agree. We should stick to using Python for now.
Log Entry 3: John: Yeah, let's do that. For the frontend, are we all OK with using Angular?
Log Entry 4: Alex: Yes!

UPDATED FACTS:
The team is going to use Python to code the backend.
The team is meeting on Friday to discuss the next week's goals.
The team has decided to use Angular for the frontend.

Based on the aforementioned instructions, perform the task for the following set of QUESTION, CURRENT FACTS and NEW LOGS.

QUESTION:
{question}

CURRENT FACTS:
{current_facts}

NEW LOGS:
{logs}

UPDATED FACTS:
"""

def generate_log_entry(index, log_block):
    log_lines = log_block.split("\n")[:3]
    log = log_lines[-1]
    return f"Log Entry {index}: {log}"

def retrieve_logs(document_url):
    try:
        error = None
        response = requests.get(document_url)
        if response.status_code != 200:
            error = f"Got status {response.status_code} in request to {document_url}."
            logger.error(error)
            return [], error
        content = response.text
        log_blocks = content.split("\n\n")
        logs = [generate_log_entry(i, block) for i, block in enumerate(log_blocks)]
        return logs, error
    except requests.exceptions.RequestException as e:
        error = f"Request to {document_url} failed"
        return [], error
    
def get_fact_extraction_chain():
    fact_extraction_prompt = PromptTemplate.from_template(fact_extraction_template)
    extract_facts_chain = (
        {
                "question": lambda x: x["question"],
                "current_facts": lambda x: x["current_facts"],
                "logs": lambda x: x["logs"],
        }
        | fact_extraction_prompt
        | ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    )

    return extract_facts_chain

async def get_facts(question, document_urls):
    current_facts = []
    logger.info(document_urls)
    errors = []
    for i, document_url in enumerate(document_urls):
        logs, error = retrieve_logs(document_url)
        if error is not None:
            errors.append(error)
            continue
        fact_extraction_chain = get_fact_extraction_chain()
        inputs = { "question": question, "logs": logs, "current_facts": current_facts }
        extraction_results = await fact_extraction_chain.ainvoke(inputs)
        current_facts = extraction_results.content.split("\n")
        logger.info(f"Document Number: {i}")
        logger.info(f"Inputs: {inputs}")
        logger.info(f"Updated Facts: {current_facts}")
        logger.info("-" * 80)
    return {"question": question, "facts": current_facts, "errors": errors}
