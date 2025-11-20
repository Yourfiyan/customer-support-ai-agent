# Testing Guide for Customer Support AI Agent

This guide explains how to test the expanded FAQ system with various tools and scripts.

## 📁 Testing Files Overview

### 1. `test_expanded_faqs.py` - Comprehensive Test Suite
**Purpose**: Validates all 39 FAQs with 48 different test queries

**What it tests**:
- All 4 categories (Account, Billing, Technical, General)
- Natural language query variations
- Category filtering
- Edge cases (gibberish, generic terms)
- Multi-keyword queries
- Cross-category search

**How to run**:
```bash
python test_expanded_faqs.py
```

**Expected output**:
- 48 test queries executed
- 100% success rate
- Detailed results for each query showing matched FAQs
- Summary statistics

**Duration**: ~5-10 seconds

---

### 2. `demo_prompts.py` - Interactive Demo
**Purpose**: Shows real-world customer inquiries and FAQ responses

**What it demonstrates**:
- 18 realistic customer scenarios
- Various query styles (simple, complex, vague)
- Formatted result cards for easy reading
- Edge cases and typo handling

**How to run**:
```bash
python demo_prompts.py
```

**To save output**:
```bash
python demo_prompts.py > demo_output.txt
```

**Example scenarios**:
- "I forgot my password"
- "My credit card was declined"
- "The app keeps crashing"
- "How do I get started?"

**Duration**: ~10-15 seconds

---

### 3. `tools.py` - Basic Tool Testing
**Purpose**: Tests FAQ search and email logging tools directly

**What it tests**:
- FAQ JSON loading
- Search functionality
- Email response logging
- Recent response retrieval

**How to run**:
```bash
python tools.py
```

**Expected output**:
- Password reset FAQ search demo
- Billing invoice search demo
- Email sending test
- Recent responses display

**Duration**: ~2-3 seconds

---

## 🧪 Quick Testing Checklist

### Before Running Tests
- [ ] Ensure Python 3.12+ is installed
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify `faqs.json` exists (should have 39 entries)

### Run All Tests
```bash
# 1. Basic tool tests (no API key needed)
python tools.py

# 2. Comprehensive FAQ tests
python test_expanded_faqs.py

# 3. Interactive demo
python demo_prompts.py
```

### Test Results to Verify
- ✅ All tools load without errors
- ✅ JSON parsing succeeds
- ✅ Search returns relevant results
- ✅ Category filtering works
- ✅ 100% test pass rate

---

## 📊 Testing Without Google API Key

**Good news**: All the tests above work without a Google API key!

These tests only use:
- FAQ search tool (keyword matching)
- JSON file reading
- Email logging (to file)

**What requires API key**:
- Full agent workflow (`agent.py`)
- API server with AI responses (`api_server.py`)
- Web demo with real AI interactions

---

## 🔍 Testing Specific Categories

### Test Account FAQs Only
```python
from tools import search_faq

# Password reset
print(search_faq("reset password", "account"))

# Profile updates
print(search_faq("update profile", "account"))

# Login issues
print(search_faq("can't login", "account"))
```

### Test Billing FAQs Only
```python
# Subscription info
print(search_faq("subscription plans", "billing"))

# Payment issues
print(search_faq("payment failed", "billing"))

# Refunds
print(search_faq("refund", "billing"))
```

### Test Technical FAQs Only
```python
# Performance
print(search_faq("slow app", "technical"))

# Crashes
print(search_faq("app crashes", "technical"))

# Sync issues
print(search_faq("not syncing", "technical"))
```

### Test General FAQs Only
```python
# Getting started
print(search_faq("how to start", "general"))

# Support contact
print(search_faq("contact support", "general"))

# Free trial
print(search_faq("free trial", "general"))
```

---

## 🎯 Advanced Testing Scenarios

### Custom Query Testing
Create your own test script:

```python
from tools import search_faq

def test_custom_query(query):
    print(f"Query: {query}")
    results = search_faq(query)
    
    if results:
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['category']}] {r['question']}")
            print(f"   Score: {r['score']}")
    else:
        print("No results found")
    print()

# Your custom tests
test_custom_query("two factor authentication")
test_custom_query("cancel my account")
test_custom_query("mobile app download")
```

### Performance Testing
```python
import time
from tools import search_faq

queries = [
    "password reset",
    "billing invoice",
    "slow performance",
    "contact support"
]

start = time.time()
for query in queries * 100:  # Run 400 searches
    search_faq(query)
end = time.time()

print(f"400 searches in {end-start:.2f} seconds")
print(f"Average: {(end-start)/400*1000:.2f}ms per search")
```

### Coverage Testing
```python
from tools import FAQSearchTool
import json

faq_tool = FAQSearchTool()

# Count FAQs per category
for category in faq_tool.faqs:
    count = len(faq_tool.faqs[category])
    print(f"{category}: {count} FAQs")

# Total FAQs
total = sum(len(faq_tool.faqs[cat]) for cat in faq_tool.faqs)
print(f"Total: {total} FAQs")
```

---

## 🐛 Troubleshooting

### Issue: "FileNotFoundError: faqs.json"
**Solution**: Run from project root directory
```bash
cd /path/to/customer-support-ai-agent
python test_expanded_faqs.py
```

### Issue: "No results found" for valid queries
**Possible causes**:
1. Check `faqs.json` is properly formatted
2. Verify search keywords match FAQ content
3. Try broader search terms

**Debug**:
```python
from tools import FAQSearchTool

faq_tool = FAQSearchTool()
print(faq_tool.faqs.keys())  # Should show all categories
```

### Issue: Test script errors
**Solution**: Verify dependencies
```bash
pip install -r requirements.txt
python --version  # Should be 3.12+
```

---

## 📈 Success Metrics

When tests complete successfully, you should see:

**test_expanded_faqs.py**:
- ✅ 48/48 tests passed
- ✅ 100% success rate
- ✅ All categories tested
- ✅ Edge cases handled

**demo_prompts.py**:
- ✅ 18 scenarios demonstrated
- ✅ Relevant results for each query
- ✅ Formatted output cards
- ✅ Summary statistics

**tools.py**:
- ✅ FAQ search working
- ✅ Email logging successful
- ✅ No errors or warnings

---

## 🚀 Next Steps After Testing

1. **Review test results** - Verify all queries return relevant FAQs
2. **Add more FAQs** - Expand `faqs.json` with additional questions
3. **Customize tests** - Add your own test scenarios
4. **Set up API key** - Test full agent workflow with Gemini AI
5. **Run API server** - Start production-like environment
6. **Try web demo** - Test in browser interface

---

## 📚 Additional Resources

- **Full Documentation**: `README.md`
- **Analysis Report**: `ANALYSIS_AND_TESTING.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **FAQ Database**: `faqs.json` (39 entries)

---

**Last Updated**: 2025-11-20
**FAQ Count**: 39
**Test Coverage**: 100%
**Status**: ✅ All Tests Passing
