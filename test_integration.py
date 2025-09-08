#!/usr/bin/env python3
"""
Integration test script to demonstrate the survey API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_survey_flow():
    """Test the complete survey flow"""
    
    # 1. Participate in survey
    print("1. Participating in survey...")
    response = requests.post(f"{BASE_URL}/api/v1/survey/participate", 
                           json={"email": "integration-test@example.com"})
    
    if response.status_code != 200:
        print(f"❌ Participation failed: {response.status_code} {response.text}")
        return False
    
    token_data = response.json()
    token = token_data["token"]
    print(f"✅ Got token: {token[:20]}...")
    
    # 2. Get questions
    print("2. Getting survey questions...")
    response = requests.get(f"{BASE_URL}/api/v1/survey/questions", 
                          params={"token": token})
    
    if response.status_code != 200:
        print(f"❌ Getting questions failed: {response.status_code} {response.text}")
        return False
    
    questions = response.json()
    print(f"✅ Got {len(questions)} questions")
    
    # 3. Submit answers for each question
    for i, question in enumerate(questions, 1):
        print(f"3.{i}. Answering question: {question['text'][:50]}...")
        
        answer_data = {
            "token": token,
            "question_id": question["id"]
        }
        
        # Choose answer based on question type
        if question["type"] == "single_choice" and question.get("options"):
            answer_data["selected_option_ids"] = [question["options"][0]["id"]]
        elif question["type"] == "multiple_choice" and question.get("options"):
            answer_data["selected_option_ids"] = [opt["id"] for opt in question["options"][:2]]
        elif question["type"] == "text":
            answer_data["text_answer"] = "This is a test answer for integration testing."
        elif question["type"] == "number":
            answer_data["number_answer"] = 5
        
        response = requests.post(f"{BASE_URL}/api/v1/survey/answer", json=answer_data)
        
        if response.status_code != 200:
            print(f"❌ Submitting answer failed: {response.status_code} {response.text}")
            return False
        
        print(f"✅ Answer submitted for question {i}")
    
    # 4. Get results
    print("4. Getting survey results...")
    response = requests.get(f"{BASE_URL}/api/v1/survey/results", 
                          params={"token": token})
    
    if response.status_code != 200:
        print(f"❌ Getting results failed: {response.status_code} {response.text}")
        return False
    
    results = response.json()
    print(f"✅ Got results for {results['user_email']}")
    print(f"   Survey: {results['survey_title']}")
    print(f"   Answers: {len(results['answers'])}")
    
    # Display answers
    for answer in results["answers"]:
        print(f"   - {answer['question_text'][:40]}...")
        if answer['selected_options']:
            print(f"     Selected: {', '.join(answer['selected_options'])}")
        if answer['text_answer']:
            print(f"     Text: {answer['text_answer'][:50]}...")
        if answer['number_answer'] is not None:
            print(f"     Number: {answer['number_answer']}")
    
    # 5. Mark survey complete
    print("5. Marking survey as complete...")
    response = requests.post(f"{BASE_URL}/api/v1/survey/complete", 
                           json={"token": token})
    
    if response.status_code != 200:
        print(f"❌ Completing survey failed: {response.status_code} {response.text}")
        return False
    
    print("✅ Survey marked as complete")
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Survey API Integration")
    print("=" * 50)
    
    # Wait for API to be ready
    print("Checking API availability...")
    for attempt in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ API is ready")
                break
        except requests.exceptions.RequestException:
            pass
        
        if attempt == 9:
            print("❌ API not available after 10 attempts")
            exit(1)
        
        print(f"⏳ Waiting for API... (attempt {attempt + 1}/10)")
        time.sleep(2)
    
    # Run the test
    success = test_survey_flow()
    
    if success:
        print("\n🎉 Integration test completed successfully!")
        print("The survey API is fully functional and ready for frontend integration.")
    else:
        print("\n❌ Integration test failed!")
        exit(1)