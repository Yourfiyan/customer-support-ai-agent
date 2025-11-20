"""
Demo script showing various customer inquiry prompts and FAQ search results.
This demonstrates the FAQ search capability with diverse real-world scenarios.
"""

from tools import search_faq
from datetime import datetime

def print_header(title):
    """Print formatted header."""
    print("\n" + "╔" + "═" * 78 + "╗")
    print(f"║ {title:^76} ║")
    print("╚" + "═" * 78 + "╝")

def print_result_card(idx, result):
    """Print a formatted result card."""
    print(f"\n┌─ Result {idx} ─────────────────────────────────────────────────────────────┐")
    print(f"│ Category: {result['category'].upper():<64} │")
    print(f"│ Score: {result['score']:<71} │")
    print("├─────────────────────────────────────────────────────────────────────────────┤")
    print(f"│ Q: {result['question']:<72} │")
    print("├─────────────────────────────────────────────────────────────────────────────┤")
    
    # Word wrap the answer
    answer = result['answer']
    max_width = 73
    words = answer.split()
    current_line = "│ A: "
    
    for word in words:
        if len(current_line) + len(word) + 1 > max_width + 2:
            print(current_line + " " * (77 - len(current_line)) + "│")
            current_line = "│    " + word
        else:
            if current_line == "│ A: ":
                current_line += word
            else:
                current_line += " " + word
    
    if current_line != "│ A: ":
        print(current_line + " " * (77 - len(current_line)) + "│")
    
    print("└─────────────────────────────────────────────────────────────────────────────┘")

def demo_query(query, category=None):
    """Run a demo query and display results."""
    print(f"\n🔍 Customer Query: \"{query}\"")
    if category:
        print(f"   Category Filter: {category}")
    
    results = search_faq(query, category)
    
    if results:
        print(f"\n✅ Found {len(results)} relevant answer(s):")
        for idx, result in enumerate(results, 1):
            print_result_card(idx, result)
    else:
        print("\n❌ No relevant FAQs found.")
        print("   (This query would be escalated to a human agent)")

def main():
    print_header("CUSTOMER SUPPORT AI AGENT - DEMO")
    print(f"\nDemo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This demo shows how the FAQ search handles various customer inquiries.")
    
    # ========================================================================
    # ACCOUNT QUERIES
    # ========================================================================
    print_header("ACCOUNT MANAGEMENT QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 1: Customer forgot their password")
    print("─" * 80)
    demo_query("I can't remember my password, how do I reset it?", "account")
    
    print("\n" + "─" * 80)
    print("Scenario 2: Customer wants to enable security features")
    print("─" * 80)
    demo_query("How can I make my account more secure?")
    
    print("\n" + "─" * 80)
    print("Scenario 3: Customer wants to update their information")
    print("─" * 80)
    demo_query("I need to change my email and profile picture")
    
    # ========================================================================
    # BILLING QUERIES
    # ========================================================================
    print_header("BILLING AND SUBSCRIPTION QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 4: Customer wants to upgrade their plan")
    print("─" * 80)
    demo_query("What's the difference between your plans? I want to upgrade", "billing")
    
    print("\n" + "─" * 80)
    print("Scenario 5: Payment issue")
    print("─" * 80)
    demo_query("My credit card was declined, what should I do?")
    
    print("\n" + "─" * 80)
    print("Scenario 6: Subscription cancellation")
    print("─" * 80)
    demo_query("I want to cancel my subscription")
    
    # ========================================================================
    # TECHNICAL QUERIES
    # ========================================================================
    print_header("TECHNICAL SUPPORT QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 7: App performance issue")
    print("─" * 80)
    demo_query("The app is really slow and laggy", "technical")
    
    print("\n" + "─" * 80)
    print("Scenario 8: Mobile app crash")
    print("─" * 80)
    demo_query("My mobile app keeps crashing on iPhone")
    
    print("\n" + "─" * 80)
    print("Scenario 9: Sync problem")
    print("─" * 80)
    demo_query("My data isn't syncing between my laptop and phone")
    
    # ========================================================================
    # GENERAL QUERIES
    # ========================================================================
    print_header("GENERAL INFORMATION QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 10: New user onboarding")
    print("─" * 80)
    demo_query("I just signed up, how do I get started?", "general")
    
    print("\n" + "─" * 80)
    print("Scenario 11: Free trial question")
    print("─" * 80)
    demo_query("Can I try it before paying?")
    
    print("\n" + "─" * 80)
    print("Scenario 12: Security and privacy concern")
    print("─" * 80)
    demo_query("Is my personal data safe with you?")
    
    # ========================================================================
    # COMPLEX QUERIES
    # ========================================================================
    print_header("COMPLEX MULTI-TOPIC QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 13: Multiple issues combined")
    print("─" * 80)
    demo_query("I'm having trouble logging in and my payment failed")
    
    print("\n" + "─" * 80)
    print("Scenario 14: Vague question")
    print("─" * 80)
    demo_query("How does your service work?")
    
    print("\n" + "─" * 80)
    print("Scenario 15: Feature availability")
    print("─" * 80)
    demo_query("Do you have a mobile app and API?")
    
    # ========================================================================
    # EDGE CASES
    # ========================================================================
    print_header("EDGE CASES AND UNUSUAL QUERIES")
    
    print("\n" + "─" * 80)
    print("Scenario 16: Very short query")
    print("─" * 80)
    demo_query("billing")
    
    print("\n" + "─" * 80)
    print("Scenario 17: Query with typos (demonstrates keyword matching)")
    print("─" * 80)
    demo_query("passwrd reste")
    
    print("\n" + "─" * 80)
    print("Scenario 18: Question not covered by FAQs")
    print("─" * 80)
    demo_query("Can I integrate with Salesforce?")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print_header("DEMO SUMMARY")
    
    print("\n📊 Demo Statistics:")
    print("   • Total scenarios tested: 18")
    print("   • Categories covered: Account, Billing, Technical, General")
    print("   • Query types: Simple, complex, multi-topic, edge cases")
    print("   • FAQ database size: 39 questions")
    
    print("\n💡 Key Takeaways:")
    print("   1. FAQ search handles natural language variations effectively")
    print("   2. Keyword matching works even with typos and informal language")
    print("   3. Category filtering improves result relevance")
    print("   4. Multiple results allow customers to find best match")
    print("   5. Queries without matches can be escalated to human agents")
    
    print("\n🎯 Next Steps:")
    print("   • Test with Google Gemini API to see full agent workflow")
    print("   • Try the web demo at demo/index.html")
    print("   • Start the API server with: python api_server.py")
    print("   • Run comprehensive tests with: python test_expanded_faqs.py")
    
    print_header("END OF DEMO")
    print()

if __name__ == "__main__":
    main()
