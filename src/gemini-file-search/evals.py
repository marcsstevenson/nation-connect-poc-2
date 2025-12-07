"""
Evaluation script for testing file search RAG system performance.
Reads questions from CSV, generates answers, scores them with LLM, and exports results to Markdown.
"""

from google import genai
from google.genai import types
import time
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

# Initialize the Gemini API client
client = genai.Client()

# Read evaluation dataset from CSV file (questions and expected answers)
eval_data = []
with open('evals.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        if row and len(row) >= 2:  # Validate row has both question and answer
            eval_data.append({'question': row[0], 'expected_answer': row[1]})

# Create output CSV file for results
with open('eval-results.csv', 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['question', 'generated_answer', 'expected_answer', 'response_time_seconds', 'score', 'reasoning']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Process each evaluation question
    for item in eval_data:
        question = item['question']
        expected_answer = item['expected_answer']

        # Generate answer using file search RAG and measure response time
        start_time = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )
        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        generated_answer = response.text

        # Use LLM to score the generated answer against expected answer
        scoring_prompt = f"""You are an expert evaluator. Compare the generated answer with the expected answer and score it on a scale of 1-10 where:
- 1-3: Poor - Incorrect or missing key information
- 4-6: Fair - Partially correct but missing important details
- 7-8: Good - Mostly correct with minor omissions
- 9-10: Excellent - Accurate and comprehensive

Question: {question}

Expected Answer: {expected_answer}

Generated Answer: {generated_answer}

Provide your response in the following format:
Score: [number]
Reasoning: [brief explanation]"""

        scoring_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=scoring_prompt
        )

        # Parse score and reasoning from LLM response
        scoring_text = scoring_response.text
        score = None
        reasoning = ""

        for line in scoring_text.split('\n'):
            if line.startswith('Score:'):
                score = line.replace('Score:', '').strip()
            elif line.startswith('Reasoning:'):
                reasoning = line.replace('Reasoning:', '').strip()

        # Write evaluation results to CSV
        writer.writerow({
            'question': question,
            'generated_answer': generated_answer,
            'expected_answer': expected_answer,
            'response_time_seconds': response_time,
            'score': score,
            'reasoning': reasoning
        })

        # Display progress
        print(f"Q: {question[:100]}...")
        print(f"Response time: {response_time}s")
        print(f"Score: {score}")
        print(f"Reasoning: {reasoning[:100]}...")
        print("-----")

print(f"\nEvaluation complete. Results saved to eval-results.csv")



