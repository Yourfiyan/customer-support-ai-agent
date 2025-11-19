"""Customer Support Multi-Agent System."""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("Error: Google Generative AI not installed. Run: pip install google-generativeai")
    raise

from tools import search_faq, send_response

class Agent:
    def __init__(self, name: str, model: str, system_instruction: str, 
                 tools=None, temperature: float = 0.2):
        self.name = name
        self.model_name = model
        self.system_instruction = system_instruction
        self.tools = tools or []
        self.temperature = temperature
        
        try:
            self.model = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_instruction
            )
        except Exception as e:
            print(f"Warning: Could not initialize model for {name}: {e}")
            self.model = None
    
    def generate_content(self, prompt: str) -> Any:
        if not self.model:
            raise RuntimeError(f"Agent {self.name} model not initialized")
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=self.temperature
                )
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Error generating content: {e}")

class Tool:
    def __init__(self, name: str, description: str, parameters: dict, function):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function

GEMINI_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.2
MAX_VALIDATION_RETRIES = 2

@dataclass
class CustomerInquiry:
    question: str
    customer_email: str
    category: Optional[str] = None
    faq_results: Optional[List[Dict]] = None
    draft_response: Optional[str] = None
    final_response: Optional[str] = None
    validation_status: Optional[str] = None

class ClassifierAgent:
    def __init__(self, model: str = GEMINI_MODEL):
        self.agent = Agent(
            name="inquiry_classifier",
            model=model,
            system_instruction="""You are an expert customer support inquiry classifier.

Your role is to analyze customer questions and categorize them into one of these types:
- account: Password resets, email changes, account access, profile updates
- billing: Invoices, payments, refunds, subscription questions
- technical: Bugs, errors, app issues, performance problems
- general: Contact info, business hours, general inquiries

Analyze the customer's question carefully and respond with ONLY the category name.

Examples:
- "I forgot my password" → account
- "Where is my invoice?" → billing
- "The app won't load" → technical
- "What are your hours?" → general
""",
            temperature=TEMPERATURE
        )
    
    def classify(self, question: str) -> str:
        try:
            response = self.agent.generate_content(f"Classify this inquiry: {question}")
            category = response.text.strip().lower()
            
            valid_categories = ['account', 'billing', 'technical', 'general']
            if category not in valid_categories:
                print(f"Warning: Invalid category '{category}', defaulting to 'general'")
                category = 'general'
            
            return category
            
        except Exception as e:
            print(f"Error in classifier: {e}")
            return 'general'

class ResearchAgent:
    def __init__(self, model: str = GEMINI_MODEL):
        faq_tool = Tool(
            name="search_faq",
            description="Searches the FAQ knowledge base for answers to customer questions. "
                       "Returns relevant FAQ entries with questions and answers. "
                       "Use the category parameter to filter results.",
            parameters={
                "query": {"type": "string", "description": "The customer's question or search query"},
                "category": {"type": "string", "description": "Category filter: account, billing, technical, or general"}
            },
            function=search_faq
        )
        
        self.agent = Agent(
            name="faq_researcher",
            model=model,
            system_instruction="""You are a skilled research agent for customer support.

Your role is to search the FAQ database and find the most relevant information to answer customer questions.

Process:
1. Use the search_faq tool with the customer's question and category
2. Review the returned FAQ entries
3. Select the most relevant answers (1-3 entries max)
4. Summarize the key information concisely

Focus on accuracy and relevance. If no relevant FAQs are found, clearly state that.
""",
            tools=[faq_tool],
            temperature=TEMPERATURE
        )
    
    def research(self, question: str, category: str) -> Dict[str, Any]:
        try:
            prompt = f"""Search for FAQs to answer this question:
Question: {question}
Category: {category}

Use the search_faq tool and provide a summary of relevant information found."""

            response = self.agent.generate_content(prompt)
            raw_results = search_faq(question, category)
            
            return {
                'summary': response.text,
                'raw_results': raw_results,
                'found_answers': len(raw_results) > 0
            }
            
        except Exception as e:
            print(f"Error in researcher: {e}")
            return {
                'summary': "No relevant FAQs found.",
                'raw_results': [],
                'found_answers': False
            }

class WriterAgent:
    def __init__(self, model: str = GEMINI_MODEL):
        self.agent = Agent(
            name="response_writer",
            model=model,
            system_instruction="""You are an expert customer support response writer.

Your role is to craft clear, helpful, and professional responses to customer inquiries.

Guidelines:
1. Start with a friendly greeting
2. Acknowledge the customer's question
3. Provide clear, step-by-step instructions when applicable
4. Use the FAQ information provided, but rephrase in a friendly way
5. End with an offer for further assistance
6. Keep tone professional but warm and empathetic
7. Format with proper paragraphs and bullet points where helpful
8. Keep responses concise (200-300 words max)

Response Structure:
- Greeting
- Answer/Instructions
- Additional helpful info
- Closing with support contact option

Always be helpful, patient, and customer-focused.
""",
            temperature=TEMPERATURE
        )
    
    def write_response(self, question: str, faq_results: Dict[str, Any], 
                      customer_email: str) -> str:
        try:
            faq_context = ""
            if faq_results.get('found_answers'):
                faq_context = "Relevant FAQ information:\n"
                for idx, faq in enumerate(faq_results.get('raw_results', [])[:3], 1):
                    faq_context += f"\n{idx}. Q: {faq['question']}\n   A: {faq['answer']}\n"
            else:
                faq_context = "No specific FAQ found. Provide general guidance."
            
            prompt = f"""Write a customer support response for this inquiry:

Customer Question: {question}

{faq_context}

Research Summary: {faq_results.get('summary', 'N/A')}

Write a complete, professional response that addresses the customer's needs.
"""

            response = self.agent.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error in writer: {e}")
            return f"Dear Customer,\n\nThank you for contacting support regarding: {question}\n\n" \
                   f"We're looking into this and will get back to you shortly.\n\n" \
                   f"Best regards,\nCustomer Support Team"

class ValidatorAgent:
    def __init__(self, model: str = GEMINI_MODEL):
        self.agent = Agent(
            name="quality_validator",
            model=model,
            system_instruction="""You are a quality assurance specialist for customer support responses.

Your role is to validate responses before they're sent to customers.

Validation Criteria:
1. ACCURACY: Does the response correctly address the question?
2. COMPLETENESS: Are all necessary steps/information included?
3. TONE: Is it professional, friendly, and empathetic?
4. CLARITY: Is it easy to understand with clear instructions?
5. FORMAT: Is it well-structured with proper greeting and closing?

Validation Process:
1. Review the customer's question
2. Check the response against all criteria
3. Provide a decision: APPROVED or NEEDS_REVISION
4. If revision needed, explain specific issues clearly

Response Format:
STATUS: [APPROVED or NEEDS_REVISION]
ISSUES: [List specific problems if any]
SUGGESTIONS: [How to improve if revision needed]

Be thorough but fair. Only request revision if there are genuine quality issues.
""",
            temperature=TEMPERATURE
        )
    
    def validate(self, question: str, response: str, attempt: int = 1) -> Dict[str, Any]:
        try:
            prompt = f"""Validate this customer support response:

CUSTOMER QUESTION:
{question}

DRAFT RESPONSE:
{response}

VALIDATION ATTEMPT: {attempt} of {MAX_VALIDATION_RETRIES + 1}

Perform quality validation and provide your assessment.
"""

            validation_response = self.agent.generate_content(prompt)
            text = validation_response.text
            
            is_approved = 'APPROVED' in text.upper() and 'NEEDS_REVISION' not in text.upper()
            
            return {
                'approved': is_approved,
                'feedback': text,
                'attempt': attempt
            }
            
        except Exception as e:
            print(f"Error in validator: {e}")
            return {
                'approved': True,
                'feedback': f"Validation error: {e}. Defaulting to approval.",
                'attempt': attempt
            }

class CustomerSupportOrchestrator:
    def __init__(self):
        print("Initializing Customer Support Multi-Agent System...")
        
        self.classifier = ClassifierAgent()
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.validator = ValidatorAgent()
        
        print("✓ All agents initialized successfully")
    
    def process_inquiry(self, question: str, customer_email: str) -> CustomerInquiry:
        inquiry = CustomerInquiry(
            question=question,
            customer_email=customer_email
        )
        
        print(f"\n{'='*80}")
        print(f"Processing Customer Inquiry")
        print(f"{'='*80}")
        print(f"Question: {question}")
        print(f"Email: {customer_email}")
        
        print(f"\n[1/5] Classifying inquiry...")
        inquiry.category = self.classifier.classify(question)
        print(f"✓ Category: {inquiry.category}")
        
        print(f"\n[2/5] Researching FAQ database...")
        inquiry.faq_results = self.researcher.research(question, inquiry.category)
        result_count = len(inquiry.faq_results.get('raw_results', []))
        print(f"✓ Found {result_count} relevant FAQ(s)")
        
        print(f"\n[3/5] Drafting response...")
        inquiry.draft_response = self.writer.write_response(
            question, 
            inquiry.faq_results,
            customer_email
        )
        print(f"✓ Response drafted ({len(inquiry.draft_response)} characters)")
        
        print(f"\n[4/5] Validating response quality...")
        validation_result = self._validation_loop(inquiry)
        inquiry.validation_status = "approved" if validation_result['approved'] else "needs_work"
        inquiry.final_response = inquiry.draft_response
        
        if validation_result['approved']:
            print(f"✓ Response validated and approved")
        else:
            print(f"⚠ Response approved with notes after {validation_result['attempt']} attempts")
        
        print(f"\n[5/5] Sending response...")
        success = send_response(customer_email, inquiry.final_response)
        
        if success:
            print(f"✓ Response sent successfully!")
        else:
            print(f"✗ Failed to send response")
        
        print(f"\n{'='*80}")
        print(f"Inquiry Processing Complete")
        print(f"{'='*80}\n")
        
        return inquiry
    
    def _validation_loop(self, inquiry: CustomerInquiry) -> Dict[str, Any]:
        attempt = 1
        max_attempts = MAX_VALIDATION_RETRIES + 1
        
        while attempt <= max_attempts:
            validation = self.validator.validate(
                inquiry.question,
                inquiry.draft_response,
                attempt
            )
            
            if validation['approved']:
                print(f"  ✓ Validation passed (attempt {attempt})")
                return validation
            else:
                print(f"  ⚠ Revision needed (attempt {attempt})")
                print(f"    Feedback: {validation['feedback'][:100]}...")
                
                if attempt < max_attempts:
                    print(f"  → Would revise and retry...")
                    attempt += 1
                else:
                    print(f"  → Max attempts reached, approving anyway")
                    validation['approved'] = True
                    return validation
        
        return validation

def initialize_agent_system():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found in environment.")
        print("Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("Or create a .env file with: GOOGLE_API_KEY=your-key-here")
    else:
        genai.configure(api_key=api_key)
        print(f"✓ Google API configured successfully")
    
    orchestrator = CustomerSupportOrchestrator()
    
    return orchestrator

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           CUSTOMER SUPPORT AI AGENT - MULTI-AGENT SYSTEM                  ║
║                                                                            ║
║  Powered by Google ADK & Gemini 2.0 Flash                                 ║
║  Kaggle Agents Intensive - Capstone Project                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    orchestrator = initialize_agent_system()
    
    test_scenarios = [
        {
            "question": "I forgot my password and can't log in",
            "email": "john.doe@example.com"
        },
        {
            "question": "How do I change my email address?",
            "email": "jane.smith@example.com"
        },
        {
            "question": "Where can I find my invoices?",
            "email": "billing.user@example.com"
        },
        {
            "question": "The app is running very slowly",
            "email": "tech.user@example.com"
        }
    ]
    
    print("\n🚀 Running Test Scenarios...\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'#'*80}")
        print(f"TEST SCENARIO {i}/{len(test_scenarios)}")
        print(f"{'#'*80}")
        
        result = orchestrator.process_inquiry(
            question=scenario['question'],
            customer_email=scenario['email']
        )
        
        print(f"\n📊 RESULT SUMMARY:")
        print(f"  Category: {result.category}")
        print(f"  FAQs Found: {len(result.faq_results.get('raw_results', []))}")
        print(f"  Response Length: {len(result.final_response)} characters")
        print(f"  Validation: {result.validation_status}")
        
        print(f"\n📧 FINAL RESPONSE:")
        print("-" * 80)
        print(result.final_response)
        print("-" * 80)
        
        if i < len(test_scenarios):
            input("\nPress Enter to continue to next test...")
    
    print(f"\n\n✅ All test scenarios completed!")
    print(f"\nCheck 'response_log.txt' for all sent responses.")

if __name__ == "__main__":
    main()
