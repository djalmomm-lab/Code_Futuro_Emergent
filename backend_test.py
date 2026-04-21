#!/usr/bin/env python3
"""
CodeFuturo Backend API Test Suite
Tests all endpoints as specified in the review request.
"""

import requests
import json
import sys
from datetime import datetime, date
from typing import Dict, Any, Optional

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip() + '/api'
        return 'http://localhost:8001/api'
    except:
        return 'http://localhost:8001/api'

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def success(self, test_name: str):
        self.passed += 1
        print(f"✅ {test_name}")
        
    def failure(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"❌ {test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.errors:
            print(f"\nFAILURES:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*50}")
        return self.failed == 0

results = TestResults()

def make_request(method: str, endpoint: str, data: Dict = None, headers: Dict = None, expected_status: int = 200) -> Optional[Dict]:
    """Make HTTP request and handle response"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        if response.status_code != expected_status:
            raise Exception(f"Expected status {expected_status}, got {response.status_code}: {response.text}")
            
        return response.json() if response.content else {}
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")

# Test data
test_user_data = {
    "email": "maria.silva@codefuturo.com",
    "password": "senhaSegura123",
    "name": "Maria Silva"
}

test_child_data = {
    "email": "crianca.teste@codefuturo.com", 
    "password": "senhaSegura456",
    "name": "João Santos"
}

# Global variables for test flow
user_token = None
child_token = None

def test_health_check():
    """Test 1: GET /api/ - health check"""
    try:
        response = make_request('GET', '/')
        if response.get('status') == 'ok':
            results.success("Health check")
        else:
            results.failure("Health check", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("Health check", str(e))

def test_register():
    """Test 2: POST /api/auth/register"""
    global user_token, child_token
    
    # Test successful registration
    try:
        response = make_request('POST', '/auth/register', test_user_data)
        if 'token' in response and 'user' in response:
            user_token = response['token']
            results.success("User registration")
        else:
            results.failure("User registration", f"Missing token or user in response: {response}")
    except Exception as e:
        results.failure("User registration", str(e))
    
    # Test duplicate email (409)
    try:
        make_request('POST', '/auth/register', test_user_data, expected_status=409)
        results.success("Duplicate email rejection")
    except Exception as e:
        results.failure("Duplicate email rejection", str(e))
    
    # Register child user for later tests
    try:
        response = make_request('POST', '/auth/register', test_child_data)
        if 'token' in response:
            child_token = response['token']
            results.success("Child user registration")
        else:
            results.failure("Child user registration", f"Missing token in response: {response}")
    except Exception as e:
        results.failure("Child user registration", str(e))

def test_login():
    """Test 3: POST /api/auth/login"""
    # Test successful login
    try:
        login_data = {"email": test_user_data["email"], "password": test_user_data["password"]}
        response = make_request('POST', '/auth/login', login_data)
        if 'token' in response and 'user' in response:
            results.success("User login")
        else:
            results.failure("User login", f"Missing token or user in response: {response}")
    except Exception as e:
        results.failure("User login", str(e))
    
    # Test invalid credentials (401)
    try:
        invalid_data = {"email": test_user_data["email"], "password": "wrongpassword"}
        make_request('POST', '/auth/login', invalid_data, expected_status=401)
        results.success("Invalid credentials rejection")
    except Exception as e:
        results.failure("Invalid credentials rejection", str(e))

def test_auth_me():
    """Test 4: GET /api/auth/me"""
    if not user_token:
        results.failure("Auth me test", "No user token available")
        return
        
    # Test with valid token
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('GET', '/auth/me', headers=headers)
        if 'user' in response and 'progress' in response:
            results.success("Auth me with token")
        else:
            results.failure("Auth me with token", f"Missing user or progress in response: {response}")
    except Exception as e:
        results.failure("Auth me with token", str(e))
    
    # Test without token (401)
    try:
        make_request('GET', '/auth/me', expected_status=401)
        results.success("Auth me without token rejection")
    except Exception as e:
        results.failure("Auth me without token rejection", str(e))

def test_onboarding():
    """Test 5: POST /api/onboard"""
    if not user_token or not child_token:
        results.failure("Onboarding test", "Missing tokens")
        return
    
    # Test adult user (≥13) onboarding
    try:
        adult_onboard_data = {
            "birth_date": "1995-05-15",  # Adult
            "interest": "programacao",
            "diagnostic_score": 75,
            "recommendation": {"type": "module", "id": "m3", "reason": "Bom conhecimento básico"}
        }
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('POST', '/onboard', adult_onboard_data, headers=headers)
        if response.get('ok') and 'profile' in response:
            results.success("Adult onboarding")
        else:
            results.failure("Adult onboarding", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("Adult onboarding", str(e))
    
    # Test child (<13) without consent (422)
    try:
        child_onboard_data = {
            "birth_date": "2015-03-10",  # Child (9 years old)
            "interest": "jogos",
            "diagnostic_score": 45,
            "recommendation": {"type": "module", "id": "m2", "reason": "Iniciante em programação"}
        }
        headers = {"Authorization": f"Bearer {child_token}"}
        make_request('POST', '/onboard', child_onboard_data, headers=headers, expected_status=422)
        results.success("Child onboarding without consent rejection")
    except Exception as e:
        results.failure("Child onboarding without consent rejection", str(e))
    
    # Test child (<13) with consent
    try:
        child_onboard_with_consent = {
            "birth_date": "2015-03-10",  # Child (9 years old)
            "parent_name": "Ana Santos",
            "parent_email": "ana.santos@email.com",
            "consent_data": True,
            "consent_comm": True,
            "interest": "jogos",
            "diagnostic_score": 45,
            "recommendation": {"type": "module", "id": "m2", "reason": "Iniciante em programação"}
        }
        headers = {"Authorization": f"Bearer {child_token}"}
        response = make_request('POST', '/onboard', child_onboard_with_consent, headers=headers)
        if response.get('ok') and 'profile' in response:
            profile = response['profile']
            if profile.get('consent_ip') and profile.get('consent_at'):
                results.success("Child onboarding with consent")
            else:
                results.failure("Child onboarding with consent", "Missing consent_ip or consent_at")
        else:
            results.failure("Child onboarding with consent", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("Child onboarding with consent", str(e))

def test_progress():
    """Test 6: GET /api/progress"""
    if not user_token:
        results.failure("Progress test", "No user token available")
        return
        
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('GET', '/progress', headers=headers)
        if 'xp_total' in response and 'level' in response and 'energy' in response:
            results.success("Get progress")
        else:
            results.failure("Get progress", f"Missing progress fields: {response}")
    except Exception as e:
        results.failure("Get progress", str(e))

def test_complete_lesson():
    """Test 7: POST /api/progress/complete"""
    if not user_token:
        results.failure("Complete lesson test", "No user token available")
        return
    
    # Test first completion (50 XP)
    try:
        lesson_data = {"lesson_slug": "variaveis-python", "path_slug": "python-zero"}
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('POST', '/progress/complete', lesson_data, headers=headers)
        if response.get('already_completed') == False and response.get('xp_earned') == 50:
            results.success("First lesson completion")
        else:
            results.failure("First lesson completion", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("First lesson completion", str(e))
    
    # Test second completion (idempotent, 0 XP)
    try:
        lesson_data = {"lesson_slug": "variaveis-python", "path_slug": "python-zero"}
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('POST', '/progress/complete', lesson_data, headers=headers)
        if response.get('already_completed') == True and response.get('xp_earned') == 0:
            results.success("Idempotent lesson completion")
        else:
            results.failure("Idempotent lesson completion", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("Idempotent lesson completion", str(e))

def test_energy_consume():
    """Test 8: POST /api/energy/consume"""
    if not user_token:
        results.failure("Energy consume test", "No user token available")
        return
    
    # Test energy consumption
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('POST', '/energy/consume', headers=headers)
        if 'energy' in response and 'max_energy' in response:
            results.success("Energy consumption")
        else:
            results.failure("Energy consumption", f"Missing energy fields: {response}")
    except Exception as e:
        results.failure("Energy consumption", str(e))
    
    # Consume all energy to test 429 response
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        # Consume remaining energy (should be 4 more times)
        for i in range(5):
            try:
                make_request('POST', '/energy/consume', headers=headers)
            except:
                break
        
        # This should return 429
        make_request('POST', '/energy/consume', headers=headers, expected_status=429)
        results.success("Energy depletion (429)")
    except Exception as e:
        results.failure("Energy depletion (429)", str(e))

def test_leaderboard():
    """Test 9: GET /api/leaderboard"""
    try:
        response = make_request('GET', '/leaderboard?period=week')
        if 'period' in response and 'rows' in response and isinstance(response['rows'], list):
            results.success("Leaderboard")
        else:
            results.failure("Leaderboard", f"Invalid leaderboard format: {response}")
    except Exception as e:
        results.failure("Leaderboard", str(e))

def test_tracks():
    """Test 10: GET /api/tracks"""
    try:
        response = make_request('GET', '/tracks')
        if 'modules' in response and 'specialized' in response:
            modules = response['modules']
            specialized = response['specialized']
            if isinstance(modules, list) and isinstance(specialized, list) and len(modules) > 0:
                results.success("Tracks")
            else:
                results.failure("Tracks", "Empty or invalid tracks data")
        else:
            results.failure("Tracks", f"Missing modules or specialized: {response}")
    except Exception as e:
        results.failure("Tracks", str(e))

def test_privacy_export():
    """Test 11: GET /api/privacy/export"""
    if not user_token:
        results.failure("Privacy export test", "No user token available")
        return
        
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = make_request('GET', '/privacy/export', headers=headers)
        if 'user' in response and 'profile' in response and 'progress' in response and 'completions' in response:
            results.success("Privacy data export (LGPD)")
        else:
            results.failure("Privacy data export (LGPD)", f"Missing data fields: {response}")
    except Exception as e:
        results.failure("Privacy data export (LGPD)", str(e))

def test_privacy_delete():
    """Test 12: DELETE /api/privacy/delete"""
    if not child_token:
        results.failure("Privacy delete test", "No child token available")
        return
        
    try:
        headers = {"Authorization": f"Bearer {child_token}"}
        response = make_request('DELETE', '/privacy/delete', headers=headers)
        if response.get('ok') and 'deleted_user_id' in response:
            results.success("Account deletion (LGPD)")
        else:
            results.failure("Account deletion (LGPD)", f"Unexpected response: {response}")
    except Exception as e:
        results.failure("Account deletion (LGPD)", str(e))

def run_all_tests():
    """Run all tests in sequence"""
    print("Starting CodeFuturo Backend API Tests...")
    print(f"Backend URL: {BASE_URL}")
    print("="*50)
    
    # Run tests in order
    test_health_check()
    test_register()
    test_login()
    test_auth_me()
    test_onboarding()
    test_progress()
    test_complete_lesson()
    test_energy_consume()
    test_leaderboard()
    test_tracks()
    test_privacy_export()
    test_privacy_delete()
    
    # Print summary
    success = results.summary()
    return success

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)