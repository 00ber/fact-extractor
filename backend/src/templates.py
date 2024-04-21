# Template to extract a list of facts from a single document
fact_extraction_template = """Given a question, answer the question by extracting facts that are relevant to the question from the given set of logs.
Here are the rules that you MUST follow:
- REMEMBER THAT THE ORDER OF THE LOGS IS VERY IMPORTANT. If two facts from the logs contradict ALWAYS choose the fact from the latest log (in our case, the logs that appears later in the list).
- Respond with just the facts separated by newlines. Do not include any additional context.
- Two log blocks are separated by a blank line and Each log has the following format: 
    doc_number\n timestamp\nlog text 
    Some examples: 

00:01:11,430 --> 00:01:40,520
John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.

00:01:41,450 --> 00:01:49,190
Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.

Here is an example:
QUESTION: What product design decisions did the team make?
LOGS:
00:01:11,430 --> 00:01:44,520
Alex: Let's choose our app's color scheme today.

00:01:45,450 --> 00:01:48,190
Jordan: I suggest blue for a calm feel.

00:01:49,40 --> 00:01:55,10
Casey: We need to make sure it's accessible to all users.

FACTS:
The team will use blue for the color scheme of the app.
The team will make the app accessible to all users.


Based on the rules mentioned before, generate facts for the given question and set of logs:

QUESTION: {question}
LOGS:
{logs}
FACTS:"""

# Template used to refine a list of facts from all documents 
refinement_template = """
Your job is to produce a final set of facts given a list of extracted facts.
The extracted facts have an order and the order represents the recency of the facts, meaning that the latest fact (the one with a larger number) is the truth

Here are the steps to do the refinement:
First, check each fact from the list of extracted facts and make sure that the information does not contradict any other fact.
Next, if there are two or more facts that contradict each other, ONLY keep the latest (the one that appears later in the list) among the contradicting facts.
For example, let's look at the following logs:
1. John loves to cook.
2. Brenda is in Morocco right now.
3. John hates cooking.

Here we can see that facts 1 and 3 are contradictory. Thus the final facts will be:
Brenda is in Morocco right now.
John hates cooking


IMPORTANT: 
- Recursively do the refinement using the newly refined facts for upto 2 times.
- Do not include the line numbers in the final refined facts.
- Only output facts separated by newlines in the final answer. Do not include any extra context.

Here is the ordered list of facts: 
EXTRACTED FACTS:
{extracted_facts}

Given the ordered list of extracted facts, create a list of refined facts
REFINED FACTS:
"""
