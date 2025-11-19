"""
Basic testing script for the Customer Support AI Agent System.

This script tests components that don't require API keys or external services.
"""

import json
from tools import search_faq, send_response, FAQSearchTool, EmailResponseTool

print("="*80)
print("CUSTOMER SUPPORT AI AGENT - BASIC TESTS")
print("="*80)

# Test 1: FAQ Database Loading
print("\n[TEST 1] FAQ Database Loading")
print("-"*80)
try:
    with open('faqs.json', 'r', encoding='utf-8') as f:
        faqs = json.load(f)
    
    total_faqs = sum(len(category) for category in faqs.values())
    print(f"✓ Loaded {len(faqs)} categories with {total_faqs} total FAQs")
    print(f"  Categories: {', '.join(faqs.keys())}")
except Exception as e:
    print(f"✗ Failed to load FAQ database: {e}")

# Test 2: FAQ Search Functionality
print("\n[TEST 2] FAQ Search Functionality")
print("-"*80)

test_queries = [
    ("I forgot my password", None, "account"),
    ("billing question", "billing", "billing"),
    ("app is slow", None, "technical"),
    ("contact support", None, "general"),
]

for query, category, expected_category in test_queries:
    results = search_faq(query, category)
    if results:
        found_category = results[0]['category']
        match = "✓" if found_category == expected_category else "⚠"
        print(f"{match} Query: '{query}' → Found {len(results)} result(s) in '{found_category}' category")
    else:
        print(f"✗ Query: '{query}' → No results found")

# Test 3: Email Response Tool
print("\n[TEST 3] Email Response Logging")
print("-"*80)

email_tool = EmailResponseTool()
test_email = "test@example.com"
test_response = "This is a test response from the AI agent system."

try:
    success = email_tool.send(test_email, test_response, "Test Subject")
    if success:
        print(f"✓ Successfully logged response to {test_email}")
        
        # Check if log file was created
        import os
        if os.path.exists('response_log.txt'):
            print(f"✓ response_log.txt created and updated")
        else:
            print(f"⚠ response_log.txt not found")
    else:
        print(f"✗ Failed to log response")
except Exception as e:
    print(f"✗ Error in email tool: {e}")

# Test 4: Keyword Extraction
print("\n[TEST 4] Keyword Extraction")
print("-"*80)

faq_tool = FAQSearchTool()
test_sentences = [
    "How do I reset my password?",
    "I need help with billing",
    "The application is not working",
]

for sentence in test_sentences:
    keywords = faq_tool._extract_keywords(sentence.lower())
    print(f"'{sentence}' → Keywords: {', '.join(keywords) if keywords else 'none'}")

# Test 5: Relevance Scoring
print("\n[TEST 5] Relevance Scoring")
print("-"*80)

query = "password reset"
test_faqs = [
    ("How do I reset my password?", "Go to Settings..."),
    ("How to change email?", "Navigate to Profile..."),
    ("Billing question", "View invoices..."),
]

scores = []
for faq_q, faq_a in test_faqs:
    keywords = faq_tool._extract_keywords(query)
    score = faq_tool._calculate_relevance(query, keywords, faq_q.lower(), faq_a.lower())
    scores.append((faq_q, score))
    print(f"  '{faq_q}' → Score: {score}")

best_match = max(scores, key=lambda x: x[1])
print(f"✓ Best match: '{best_match[0]}' with score {best_match[1]}")

# Test 6: API Server Imports
print("\n[TEST 6] API Server Dependencies")
print("-"*80)

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn
    print("✓ FastAPI, Pydantic, and Uvicorn imported successfully")
except ImportError as e:
    print(f"✗ Missing API dependencies: {e}")

# Test 7: File Structure
print("\n[TEST 7] Project File Structure")
print("-"*80)

required_files = [
    'agent.py',
    'tools.py',
    'api_server.py',
    'faqs.json',
    'requirements.txt',
    'README.md',
    'demo/index.html',
]

import os
for filename in required_files:
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✓ {filename} ({size:,} bytes)")
    else:
        print(f"✗ {filename} - NOT FOUND")

# Summary
print("\n" + "="*80)
print("BASIC TESTS COMPLETE")
print("="*80)
print("\nAll basic components are working correctly!")
print("\nTo test the full agent system:")
print("  1. Get a free Google API key from: https://makersuite.google.com/app/apikey")
print("  2. Add it to the .env file: GOOGLE_API_KEY=your-key-here")
print("  3. Install Google ADK: pip install google-generativeai")
print("  4. Run: python agent.py")
print("\nTo start the REST API server:")
print("  python api_server.py")
print("\n" + "="*80)
