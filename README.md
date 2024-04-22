# AI-based Fact Extractor
A web application that processes and extracts facts from a set of call logs using an LLM.

## Approach:

### Framework/Libraries/Tools

- **Frontend:**
  - Angular
  - Tailwind
- **Backend:**
  - FastAPI
  - Langchain
- **Misc:**
  - Docker
  - Nginx

### API Backend Setup

I setup a basic server using FastAPI that has the following 2 endpoints:

**1. POST /submit_question_and_documents**
- The payload validation is handled automatically by FastAPI (using Pydantic behind the scenes). 
- Whenever a request arrives, a job id (set as a constant for this demo) is generated and an asyncio task to extract facts is created with that job id. The job id is also added as key to a `jobs` dictionary, which keeps track of the facts extraction job (there may be better options for this, I chose to use a dictionary just for simplicity).
- Once the task is created, a HTTP 200 response is immediately sent back with the job id in the body.
- When the fact extraction task completes (asynchronously), the coroutine running the task updates the `jobs` dictionary with the facts and any errors when done.

**2. GET /get_question_and_documents**
- When a request arrives, the job details is retrieved from the `jobs` dictionary using the request id (which is a constant for this demo's purpose).
- A response with the following payload is sent back as response:
```json
{
    "question": "...",   // The original question of the submitted request
    "facts": [           // Final list of facts, empty if the request is still being processed
        .....
    ],
    "errors": [         // Any errors that occured while extracting the facts, empty if the request is still being processed
        ....
    ],
    "status": "..."     // "done" if the facts extraction is complete, "processing" if the request is still being processed
}
``` 

### Prompting and iterative fact updates
Here is the main flow for extracting facts pertaining to the given question from a given set of documents:

1. Initialize an empty list of current facts.
2. For each document:
   1. Fetch the logs
   2. Parse the logs.
   3. Passing the target question, parsed logs of the current document and the current list of facts (empty for the first iteration) as the input variables to the LLM, prompt the LLM to 
      1. First extract facts pertaining to the question from the logs of the current document.
      2. Then, update the provided set of current facts with the facts extracted from the logs of the current document.
   4. Parse the output of the LLM and replace the set of current facts with the parsed output from the LLM.
3. Return the current facts.

<details>
  <summary><strong>Here is the prompt used for this:</strong></summary>
<pre>You are provided with a specific QUESTION, a list of CURRENT FACTS (which may be empty) and a list of NEW LOGS.
Your task is to analyze the NEW LOGS to extract new facts relevant to the QUESTION and update the list of CURRENT FACTS based on this new information. 
Ensure that your extractions are accurate and relevant.<br>

Task Instructions:
\------------------
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
\------------------
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
</pre></details>

### Usage

**Requires:** Docker, Docker Compose

If `make` command is available
```bash
make up-dev
```

If `make` command is not available
```
$ docker build -f ./backend/Dockerfile -t fact-extractor-backend ./backend
$ docker build -f ./frontend/Dockerfile -t fact-extractor-frontend ./frontend
$ docker compose up
```

Docker services:
- **fact-extractor-backend**: FastAPI backend
- **fact-extractor-frontend**: Angular frontend
- **test-fileserver**: Serves a few example text files for testing
