"""
Test script for expanded FAQ database with various customer inquiries.
Tests the FAQ search functionality with diverse prompts across all categories.
"""

from tools import search_faq, FAQSearchTool
import json

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_query(query, category=None, expected_results=1):
    """Test a single query and display results."""
    print(f"\n📝 Query: \"{query}\"")
    if category:
        print(f"   Category: {category}")
    
    results = search_faq(query, category)
    print(f"   Found: {len(results)} result(s)")
    
    if results:
        for i, result in enumerate(results[:3], 1):
            print(f"\n   {i}. [{result['category'].upper()}] {result['question']}")
            print(f"      Score: {result['score']}")
            print(f"      Answer: {result['answer'][:100]}...")
    else:
        print("   ⚠️  No results found")
    
    return len(results) >= expected_results

def main():
    print_section("FAQ DATABASE TEST SUITE")
    print("Testing expanded FAQ database with diverse customer inquiries")
    
    # Load FAQ stats
    faq_tool = FAQSearchTool()
    total_faqs = sum(len(faq_tool.faqs[cat]) for cat in faq_tool.faqs)
    print(f"\n📊 Database Stats:")
    print(f"   Total FAQs: {total_faqs}")
    for category in faq_tool.faqs:
        print(f"   - {category}: {len(faq_tool.faqs[category])} FAQs")
    
    # Test counters
    tests_passed = 0
    tests_total = 0
    
    # =========================================================================
    # ACCOUNT CATEGORY TESTS
    # =========================================================================
    print_section("ACCOUNT CATEGORY TESTS")
    
    account_queries = [
        ("I forgot my password", None, 1),
        ("reset password help", "account", 1),
        ("change my email address", None, 1),
        ("update my profile picture", None, 1),
        ("enable two factor authentication", "account", 1),
        ("my account is locked out", None, 1),
        ("can't login to my account", "account", 1),
        ("change username", None, 1),
        ("delete my account permanently", "account", 1),
    ]
    
    for query, cat, expected in account_queries:
        tests_total += 1
        if test_query(query, cat, expected):
            tests_passed += 1
    
    # =========================================================================
    # BILLING CATEGORY TESTS
    # =========================================================================
    print_section("BILLING CATEGORY TESTS")
    
    billing_queries = [
        ("where are my invoices", "billing", 1),
        ("update credit card information", None, 1),
        ("I want a refund", "billing", 1),
        ("what subscription plans do you have", None, 1),
        ("cancel my subscription", "billing", 1),
        ("upgrade to pro plan", None, 1),
        ("my payment didn't go through", "billing", 1),
        ("change billing address", None, 1),
        ("need tax invoice", "billing", 1),
    ]
    
    for query, cat, expected in billing_queries:
        tests_total += 1
        if test_query(query, cat, expected):
            tests_passed += 1
    
    # =========================================================================
    # TECHNICAL CATEGORY TESTS
    # =========================================================================
    print_section("TECHNICAL CATEGORY TESTS")
    
    technical_queries = [
        ("app is slow", "technical", 1),
        ("website not loading", None, 1),
        ("connection timeout error", "technical", 1),
        ("mobile app crashes", None, 1),
        ("data not syncing between devices", "technical", 1),
        ("can't upload files", None, 1),
        ("notifications not working", "technical", 1),
        ("which browser should I use", None, 1),
        ("how to export my data", "technical", 1),
        ("technical error message", None, 1),
    ]
    
    for query, cat, expected in technical_queries:
        tests_total += 1
        if test_query(query, cat, expected):
            tests_passed += 1
    
    # =========================================================================
    # GENERAL CATEGORY TESTS
    # =========================================================================
    print_section("GENERAL CATEGORY TESTS")
    
    general_queries = [
        ("how do I contact support", "general", 1),
        ("what are your hours", None, 1),
        ("getting started guide", "general", 1),
        ("do you have a free trial", None, 1),
        ("is my data secure", "general", 1),
        ("free vs paid plan differences", None, 1),
        ("privacy policy", "general", 1),
        ("API documentation", None, 1),
        ("mobile app download", "general", 1),
        ("check service status", None, 1),
        ("send feedback", "general", 1),
        ("terms of service", None, 1),
    ]
    
    for query, cat, expected in general_queries:
        tests_total += 1
        if test_query(query, cat, expected):
            tests_passed += 1
    
    # =========================================================================
    # EDGE CASE TESTS
    # =========================================================================
    print_section("EDGE CASE TESTS")
    
    edge_cases = [
        ("asdf random gibberish xyz", None, 0),  # Should find nothing
        ("help", None, 0),  # Too generic
        ("password email billing browser", None, 1),  # Multiple keywords
        ("subscription plan upgrade payment method", "billing", 1),  # Complex query
    ]
    
    print("\nTesting edge cases (queries that should return few or no results):")
    for query, cat, expected in edge_cases:
        tests_total += 1
        if test_query(query, cat, expected):
            tests_passed += 1
    
    # =========================================================================
    # CATEGORY FILTERING TESTS
    # =========================================================================
    print_section("CATEGORY FILTERING TESTS")
    
    print("\nTesting same query across different categories:")
    test_word = "update"
    for category in ["account", "billing", "technical", "general"]:
        tests_total += 1
        print(f"\n🔍 Searching for '{test_word}' in category: {category}")
        results = search_faq(test_word, category)
        print(f"   Found: {len(results)} result(s)")
        if results:
            tests_passed += 1
            for i, result in enumerate(results[:2], 1):
                print(f"   {i}. {result['question']}")
    
    # =========================================================================
    # FINAL RESULTS
    # =========================================================================
    print_section("TEST RESULTS SUMMARY")
    
    success_rate = (tests_passed / tests_total * 100) if tests_total > 0 else 0
    
    print(f"\n📊 Results:")
    print(f"   Tests Passed: {tests_passed}/{tests_total}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Total FAQs: {total_faqs}")
    
    if success_rate >= 80:
        print(f"\n✅ EXCELLENT! FAQ search is working well!")
    elif success_rate >= 60:
        print(f"\n✓ GOOD! Most queries return relevant results.")
    else:
        print(f"\n⚠️  NEEDS IMPROVEMENT. Consider adding more FAQs or improving search.")
    
    print("\n" + "=" * 80)
    print("Test suite completed!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
