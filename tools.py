"""Customer support tools - FAQ search and email responses."""

import json
import os
from typing import List, Dict, Any
from datetime import datetime


class FAQSearchTool:
    def __init__(self, faq_file: str = "faqs.json"):
        self.faq_file = faq_file
        self.faqs = self._load_faqs()
    
    def _load_faqs(self) -> Dict[str, Any]:
        try:
            with open(self.faq_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: FAQ file '{self.faq_file}' not found. Using empty database.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse FAQ file: {e}")
            return {}
    
    def search(self, query: str, category: str = None, top_k: int = 3) -> List[Dict[str, str]]:
        query_lower = query.lower()
        results = []
        
        # Keywords for better matching
        keywords = self._extract_keywords(query_lower)
        
        # Search through categories
        categories_to_search = [category] if category else self.faqs.keys()
        
        for cat in categories_to_search:
            if cat not in self.faqs:
                continue
                
            for faq_key, faq_data in self.faqs[cat].items():
                score = self._calculate_relevance(
                    query_lower, 
                    keywords,
                    faq_data.get('question', '').lower(),
                    faq_data.get('answer', '').lower()
                )
                
                if score > 0:
                    results.append({
                        'category': cat,
                        'question': faq_data.get('question', ''),
                        'answer': faq_data.get('answer', ''),
                        'score': score
                    })
        
        # Sort by relevance score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def _extract_keywords(self, query: str) -> List[str]:
        # Remove common stop words
        stop_words = {'how', 'do', 'i', 'can', 'what', 'where', 'why', 'when', 
                     'is', 'are', 'the', 'a', 'an', 'to', 'my', 'me'}
        
        words = query.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
    
    def _calculate_relevance(self, query: str, keywords: List[str], 
                            faq_question: str, faq_answer: str) -> float:
        score = 0.0
        
        # Exact phrase match (highest priority)
        if query in faq_question or query in faq_answer:
            score += 10.0
        
        # Keyword matching in question (high priority)
        for keyword in keywords:
            if keyword in faq_question:
                score += 3.0
            elif keyword in faq_answer:
                score += 1.0
        
        return score


class EmailResponseTool:
    def __init__(self, log_file: str = "response_log.txt"):
        self.log_file = log_file
    
    def send(self, email: str, response: str, subject: str = "Customer Support Response") -> bool:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = f"""
{'='*80}
TIMESTAMP: {timestamp}
TO: {email}
SUBJECT: {subject}
{'='*80}
{response}
{'='*80}

"""
            
            # Append to log file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            print(f"✓ Response sent to {email}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send response: {e}")
            return False
    
    def get_recent_responses(self, count: int = 5) -> List[str]:
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by separator and get last N entries
            entries = content.split('='*80)
            entries = [e.strip() for e in entries if e.strip()]
            
            return entries[-count:] if entries else []
            
        except Exception as e:
            print(f"Error reading response log: {e}")
            return []


# Tool instances for easy import
faq_search = FAQSearchTool()
email_sender = EmailResponseTool()


def search_faq(query: str, category: str = None) -> List[Dict[str, str]]:
    return faq_search.search(query, category)


def send_response(email: str, response: str) -> bool:
    return email_sender.send(email, response)


# Tool descriptions for ADK agents
TOOL_DESCRIPTIONS = {
    "search_faq": {
        "name": "search_faq",
        "description": "Searches the FAQ knowledge base for answers to customer questions. "
                      "Returns relevant FAQ entries with questions and answers.",
        "parameters": {
            "query": "The customer's question or search query",
            "category": "Optional category filter: account, billing, technical, or general"
        }
    },
    "send_response": {
        "name": "send_response",
        "description": "Sends the customer support response via email. "
                      "Logs the response for tracking and quality assurance.",
        "parameters": {
            "email": "Customer's email address",
            "response": "The complete response message to send"
        }
    }
}


if __name__ == "__main__":
    # Test the tools
    print("Testing FAQ Search Tool...")
    print("-" * 80)
    
    # Test 1: Password reset
    results = search_faq("How do I reset my password?")
    print(f"\nQuery: 'How do I reset my password?'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result['category']}] {result['question']}")
        print(f"   Score: {result['score']}")
        print(f"   Answer: {result['answer'][:100]}...")
    
    # Test 2: Billing question with category filter
    results = search_faq("view invoices", category="billing")
    print(f"\n\nQuery: 'view invoices' (category: billing)")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result['category']}] {result['question']}")
        print(f"   Score: {result['score']}")
    
    # Test 3: Email sending
    print("\n\n" + "="*80)
    print("Testing Email Response Tool...")
    print("-" * 80)
    
    test_response = """
Dear Customer,

Thank you for contacting support. To reset your password:

1. Go to Settings > Security > Reset Password
2. Click the 'Forgot Password' link
3. Check your email for the reset link

Let us know if you need further assistance!

Best regards,
Customer Support Team
"""
    
    success = send_response("customer@example.com", test_response)
    print(f"\nEmail send status: {'Success' if success else 'Failed'}")
    
    # Test 4: Retrieve recent responses
    print("\n\nRecent responses:")
    recent = email_sender.get_recent_responses(count=2)
    for i, entry in enumerate(recent, 1):
        print(f"\n{i}. {entry[:200]}...")
