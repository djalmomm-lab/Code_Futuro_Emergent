#!/usr/bin/env python3
"""
CodeFuturo Backend Testing - New Tracks/Lessons Endpoints
Testing the new tracks and lessons endpoints as requested.
"""

import requests
import json
import sys
from datetime import datetime

# Use the production URL from frontend/.env
BASE_URL = "https://web-replica-128.preview.emergentagent.com/api"

def log_test(test_name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")
    print()

def test_tracks_endpoint():
    """Test GET /api/tracks - should return 9 tracks with proper structure"""
    print("=== Testing GET /api/tracks ===")
    
    try:
        response = requests.get(f"{BASE_URL}/tracks")
        
        if response.status_code != 200:
            log_test("Tracks endpoint status", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        if "paths" not in data:
            log_test("Tracks response structure", False, "Missing 'paths' key in response")
            return False
            
        paths = data["paths"]
        
        # Check we have 9 tracks
        expected_tracks = ["python-zero", "javascript", "html-css", "sql", "typescript", "java", "cpp", "go", "ai-prompts"]
        if len(paths) != 9:
            log_test("Tracks count", False, f"Expected 9 tracks, got {len(paths)}")
            return False
            
        # Check each track has required fields
        required_fields = ["slug", "name", "language", "color", "desc", "real_exec", "total_lessons"]
        for path in paths:
            for field in required_fields:
                if field not in path:
                    log_test("Track structure", False, f"Missing field '{field}' in track {path.get('slug', 'unknown')}")
                    return False
                    
        # Check specific tracks exist
        track_slugs = [p["slug"] for p in paths]
        for expected in expected_tracks:
            if expected not in track_slugs:
                log_test("Expected tracks", False, f"Missing expected track: {expected}")
                return False
                
        log_test("Tracks endpoint", True, f"Found {len(paths)} tracks with proper structure")
        return True
        
    except Exception as e:
        log_test("Tracks endpoint", False, f"Exception: {str(e)}")
        return False

def test_python_zero_path():
    """Test GET /api/paths/python-zero - should return 12 Python lessons"""
    print("=== Testing GET /api/paths/python-zero ===")
    
    try:
        response = requests.get(f"{BASE_URL}/paths/python-zero")
        
        if response.status_code != 200:
            log_test("Python-zero path status", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        if "path" not in data or "lessons" not in data:
            log_test("Python-zero response structure", False, "Missing 'path' or 'lessons' key")
            return False
            
        path = data["path"]
        lessons = data["lessons"]
        
        # Check we have 12 lessons
        if len(lessons) != 12:
            log_test("Python-zero lessons count", False, f"Expected 12 lessons, got {len(lessons)}")
            return False
            
        # Check lesson structure
        required_lesson_fields = ["slug", "path_slug", "order", "title", "chapter", 
                                "instruction_pt", "instruction_en", "instruction_es", 
                                "starter_code", "hint", "tests", "language", "real_exec"]
        
        for lesson in lessons:
            for field in required_lesson_fields:
                if field not in lesson:
                    log_test("Lesson structure", False, f"Missing field '{field}' in lesson {lesson.get('slug', 'unknown')}")
                    return False
                    
        # Check lessons are ordered
        orders = [lesson["order"] for lesson in lessons]
        if orders != sorted(orders):
            log_test("Lesson ordering", False, "Lessons are not properly ordered")
            return False
            
        log_test("Python-zero path", True, f"Found path with {len(lessons)} properly structured lessons")
        return True
        
    except Exception as e:
        log_test("Python-zero path", False, f"Exception: {str(e)}")
        return False

def test_javascript_path():
    """Test GET /api/paths/javascript - should return 10 JS lessons"""
    print("=== Testing GET /api/paths/javascript ===")
    
    try:
        response = requests.get(f"{BASE_URL}/paths/javascript")
        
        if response.status_code != 200:
            log_test("JavaScript path status", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        if "path" not in data or "lessons" not in data:
            log_test("JavaScript response structure", False, "Missing 'path' or 'lessons' key")
            return False
            
        lessons = data["lessons"]
        
        # Check we have 10 lessons
        if len(lessons) != 10:
            log_test("JavaScript lessons count", False, f"Expected 10 lessons, got {len(lessons)}")
            return False
            
        log_test("JavaScript path", True, f"Found path with {len(lessons)} lessons")
        return True
        
    except Exception as e:
        log_test("JavaScript path", False, f"Exception: {str(e)}")
        return False

def test_nonexistent_path():
    """Test GET /api/paths/inexistente - should return 404"""
    print("=== Testing GET /api/paths/inexistente ===")
    
    try:
        response = requests.get(f"{BASE_URL}/paths/inexistente")
        
        if response.status_code != 404:
            log_test("Nonexistent path", False, f"Expected 404, got {response.status_code}")
            return False
            
        log_test("Nonexistent path", True, "Correctly returned 404 for nonexistent path")
        return True
        
    except Exception as e:
        log_test("Nonexistent path", False, f"Exception: {str(e)}")
        return False

def test_lesson_detail():
    """Test GET /api/lessons/<slug> - should return lesson with 'next' field"""
    print("=== Testing GET /api/lessons/<slug> ===")
    
    try:
        # First get a lesson slug from python-zero path
        response = requests.get(f"{BASE_URL}/paths/python-zero")
        if response.status_code != 200:
            log_test("Lesson detail setup", False, "Could not get python-zero lessons")
            return False
            
        lessons = response.json()["lessons"]
        if not lessons:
            log_test("Lesson detail setup", False, "No lessons found in python-zero")
            return False
            
        # Test first lesson
        first_lesson_slug = lessons[0]["slug"]
        response = requests.get(f"{BASE_URL}/lessons/{first_lesson_slug}")
        
        if response.status_code != 200:
            log_test("Lesson detail status", False, f"Expected 200, got {response.status_code}")
            return False
            
        lesson = response.json()
        
        # Check lesson has 'next' field
        if "next" not in lesson:
            log_test("Lesson next field", False, "Missing 'next' field in lesson response")
            return False
            
        # For first lesson, next should point to second lesson
        if lesson["next"] is None:
            log_test("Lesson next value", False, "First lesson should have a next lesson")
            return False
            
        # Test last lesson (should have next = null)
        last_lesson_slug = lessons[-1]["slug"]
        response = requests.get(f"{BASE_URL}/lessons/{last_lesson_slug}")
        
        if response.status_code != 200:
            log_test("Last lesson detail", False, f"Expected 200, got {response.status_code}")
            return False
            
        last_lesson = response.json()
        if last_lesson["next"] is not None:
            log_test("Last lesson next", False, "Last lesson should have next = null")
            return False
            
        log_test("Lesson detail", True, "Lesson endpoint returns proper structure with 'next' field")
        return True
        
    except Exception as e:
        log_test("Lesson detail", False, f"Exception: {str(e)}")
        return False

def test_nonexistent_lesson():
    """Test GET /api/lessons/inexistente - should return 404"""
    print("=== Testing GET /api/lessons/inexistente ===")
    
    try:
        response = requests.get(f"{BASE_URL}/lessons/inexistente")
        
        if response.status_code != 404:
            log_test("Nonexistent lesson", False, f"Expected 404, got {response.status_code}")
            return False
            
        log_test("Nonexistent lesson", True, "Correctly returned 404 for nonexistent lesson")
        return True
        
    except Exception as e:
        log_test("Nonexistent lesson", False, f"Exception: {str(e)}")
        return False

def test_end_to_end_flow():
    """Test end-to-end: register user → complete lesson → verify XP"""
    print("=== Testing End-to-End Flow ===")
    
    try:
        # 1. Register new user
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "email": f"testuser_{timestamp}@codefuturo.com",
            "password": "testpass123",
            "name": f"Test User {timestamp}"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 200:
            log_test("E2E - User registration", False, f"Registration failed: {response.status_code}")
            return False
            
        auth_data = response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        log_test("E2E - User registration", True, "User registered successfully")
        
        # 2. Get initial progress
        response = requests.get(f"{BASE_URL}/progress", headers=headers)
        if response.status_code != 200:
            log_test("E2E - Initial progress", False, f"Could not get progress: {response.status_code}")
            return False
            
        initial_progress = response.json()
        initial_xp = initial_progress["xp_total"]
        
        # 3. Get a real lesson slug from python-zero
        response = requests.get(f"{BASE_URL}/paths/python-zero")
        if response.status_code != 200:
            log_test("E2E - Get lesson", False, "Could not get python-zero lessons")
            return False
            
        lessons = response.json()["lessons"]
        if not lessons:
            log_test("E2E - Get lesson", False, "No lessons found")
            return False
            
        lesson_slug = lessons[0]["slug"]
        
        # 4. Complete the lesson
        complete_data = {
            "lesson_slug": lesson_slug,
            "path_slug": "python-zero"
        }
        
        response = requests.post(f"{BASE_URL}/progress/complete", json=complete_data, headers=headers)
        if response.status_code != 200:
            log_test("E2E - Complete lesson", False, f"Could not complete lesson: {response.status_code}")
            return False
            
        completion_result = response.json()
        
        # 5. Verify XP was incremented
        if completion_result.get("already_completed"):
            log_test("E2E - XP increment", False, "Lesson was already completed")
            return False
            
        xp_earned = completion_result.get("xp_earned", 0)
        if xp_earned != 50:
            log_test("E2E - XP amount", False, f"Expected 50 XP, got {xp_earned}")
            return False
            
        # 6. Verify progress was updated
        response = requests.get(f"{BASE_URL}/progress", headers=headers)
        if response.status_code != 200:
            log_test("E2E - Final progress", False, "Could not get final progress")
            return False
            
        final_progress = response.json()
        final_xp = final_progress["xp_total"]
        
        if final_xp != initial_xp + 50:
            log_test("E2E - XP verification", False, f"XP not properly incremented: {initial_xp} -> {final_xp}")
            return False
            
        log_test("E2E - Complete flow", True, f"Successfully completed lesson and earned {xp_earned} XP")
        return True
        
    except Exception as e:
        log_test("E2E - Complete flow", False, f"Exception: {str(e)}")
        return False

def test_legacy_endpoints():
    """Verify that old endpoints still work without regression"""
    print("=== Testing Legacy Endpoints (No Regression) ===")
    
    try:
        # Test health check
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            log_test("Legacy - Health check", False, f"Health check failed: {response.status_code}")
            return False
        log_test("Legacy - Health check", True, "Health endpoint working")
        
        # Test leaderboard (public endpoint)
        response = requests.get(f"{BASE_URL}/leaderboard")
        if response.status_code != 200:
            log_test("Legacy - Leaderboard", False, f"Leaderboard failed: {response.status_code}")
            return False
        log_test("Legacy - Leaderboard", True, "Leaderboard endpoint working")
        
        # Test auth endpoints with invalid credentials (should return 401)
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": "invalid@test.com", "password": "wrong"})
        if response.status_code != 401:
            log_test("Legacy - Auth validation", False, f"Expected 401, got {response.status_code}")
            return False
        log_test("Legacy - Auth validation", True, "Auth endpoints working")
        
        return True
        
    except Exception as e:
        log_test("Legacy endpoints", False, f"Exception: {str(e)}")
        return False

def test_subscription_plans():
    """Test GET /api/subscription/plans - should return 3 plans"""
    print("=== Testing GET /api/subscription/plans ===")
    
    try:
        response = requests.get(f"{BASE_URL}/subscription/plans")
        
        if response.status_code != 200:
            log_test("Subscription plans status", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        if "plans" not in data:
            log_test("Plans response structure", False, "Missing 'plans' key in response")
            return False
            
        plans = data["plans"]
        
        # Check we have 3 plans
        if len(plans) != 3:
            log_test("Plans count", False, f"Expected 3 plans, got {len(plans)}")
            return False
            
        # Check specific plans exist with correct structure
        expected_plans = {
            "pro_annual": {"price_brl": 347.00, "interval": "year", "trial_days": 7},
            "pro_pioneer": {"price_brl": 197.00, "interval": "year", "trial_days": 7},
            "lifetime": {"price_brl": 997.00, "interval": "one_time", "trial_days": 0}
        }
        
        plan_ids = [p["id"] for p in plans]
        for expected_id, expected_data in expected_plans.items():
            if expected_id not in plan_ids:
                log_test("Expected plans", False, f"Missing expected plan: {expected_id}")
                return False
                
            # Find the plan and verify its data
            plan = next(p for p in plans if p["id"] == expected_id)
            for key, value in expected_data.items():
                if plan.get(key) != value:
                    log_test(f"Plan {expected_id} data", False, f"Expected {key}={value}, got {plan.get(key)}")
                    return False
                    
        log_test("Subscription plans", True, f"Found {len(plans)} plans with correct structure")
        return True
        
    except Exception as e:
        log_test("Subscription plans", False, f"Exception: {str(e)}")
        return False

def test_subscription_me_new_user():
    """Test GET /api/subscription/me - new user should have is_pro=false"""
    print("=== Testing GET /api/subscription/me (new user) ===")
    
    try:
        # Register new user
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "email": f"stripe_test_{timestamp}@codefuturo.com",
            "password": "testpass123",
            "name": f"Stripe Test {timestamp}"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 200:
            log_test("Subscription me - registration", False, f"Registration failed: {response.status_code}")
            return False
            
        auth_data = response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get subscription status
        response = requests.get(f"{BASE_URL}/subscription/me", headers=headers)
        
        if response.status_code != 200:
            log_test("Subscription me status", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        required_fields = ["is_pro", "plan", "tier", "subscription_ends_at", "stripe_customer_id"]
        for field in required_fields:
            if field not in data:
                log_test("Subscription me structure", False, f"Missing field: {field}")
                return False
                
        # New user should not be pro
        if data["is_pro"] != False:
            log_test("Subscription me - is_pro", False, f"Expected is_pro=false, got {data['is_pro']}")
            return False
            
        log_test("Subscription me (new user)", True, "New user correctly shows is_pro=false")
        return True, token  # Return token for next tests
        
    except Exception as e:
        log_test("Subscription me", False, f"Exception: {str(e)}")
        return False

def test_subscription_checkout():
    """Test POST /api/subscription/checkout - create checkout session"""
    print("=== Testing POST /api/subscription/checkout ===")
    
    try:
        # Register new user
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "email": f"checkout_test_{timestamp}@codefuturo.com",
            "password": "testpass123",
            "name": f"Checkout Test {timestamp}"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 200:
            log_test("Checkout - registration", False, f"Registration failed: {response.status_code}")
            return False
            
        auth_data = response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create checkout session
        checkout_data = {
            "plan_id": "pro_annual",
            "origin_url": "https://web-replica-128.preview.emergentagent.com"
        }
        
        response = requests.post(f"{BASE_URL}/subscription/checkout", json=checkout_data, headers=headers)
        
        if response.status_code != 200:
            log_test("Checkout status", False, f"Expected 200, got {response.status_code}: {response.text}")
            return False
            
        data = response.json()
        
        # Check response structure
        if "url" not in data or "session_id" not in data:
            log_test("Checkout response structure", False, "Missing 'url' or 'session_id'")
            return False
            
        # Verify URL is a Stripe checkout URL
        if not data["url"].startswith("https://checkout.stripe.com/"):
            log_test("Checkout URL", False, f"URL doesn't start with https://checkout.stripe.com/: {data['url']}")
            return False
            
        # Verify session_id format
        if not data["session_id"].startswith("cs_"):
            log_test("Checkout session_id", False, f"session_id doesn't start with 'cs_': {data['session_id']}")
            return False
            
        log_test("Checkout session creation", True, f"Created session: {data['session_id']}")
        
        # Test invalid plan_id
        invalid_checkout = {
            "plan_id": "invalid_plan",
            "origin_url": "https://web-replica-128.preview.emergentagent.com"
        }
        
        response = requests.post(f"{BASE_URL}/subscription/checkout", json=invalid_checkout, headers=headers)
        
        if response.status_code != 400:
            log_test("Checkout invalid plan", False, f"Expected 400 for invalid plan, got {response.status_code}")
            return False
            
        log_test("Checkout invalid plan validation", True, "Correctly rejected invalid plan_id")
        
        return True, data["session_id"], token  # Return session_id and token for next tests
        
    except Exception as e:
        log_test("Checkout", False, f"Exception: {str(e)}")
        return False

def test_subscription_status():
    """Test GET /api/subscription/status/{session_id}"""
    print("=== Testing GET /api/subscription/status/{session_id} ===")
    
    try:
        # First create a checkout session
        checkout_result = test_subscription_checkout()
        if not checkout_result or len(checkout_result) < 3:
            log_test("Status - setup", False, "Could not create checkout session")
            return False
            
        _, session_id, token = checkout_result
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get session status
        response = requests.get(f"{BASE_URL}/subscription/status/{session_id}", headers=headers)
        
        if response.status_code != 200:
            log_test("Status endpoint", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        # Check response structure
        required_fields = ["status", "payment_status", "amount_total", "currency"]
        for field in required_fields:
            if field not in data:
                log_test("Status response structure", False, f"Missing field: {field}")
                return False
                
        # For unpaid session, payment_status should be 'unpaid' or status should be 'open'
        if data["payment_status"] not in ["unpaid", "paid"] and data["status"] not in ["open", "complete"]:
            log_test("Status values", False, f"Unexpected status values: {data}")
            return False
            
        log_test("Subscription status", True, f"Status: {data['status']}, Payment: {data['payment_status']}")
        return True
        
    except Exception as e:
        log_test("Subscription status", False, f"Exception: {str(e)}")
        return False

def test_webhook_stripe():
    """Test POST /api/webhook/stripe - should validate signature"""
    print("=== Testing POST /api/webhook/stripe ===")
    
    try:
        # Test without stripe-signature header (should fail)
        response = requests.post(f"{BASE_URL}/webhook/stripe", json={"test": "data"})
        
        if response.status_code != 400:
            log_test("Webhook without signature", False, f"Expected 400, got {response.status_code}")
            return False
            
        log_test("Webhook signature validation", True, "Correctly rejected request without stripe-signature header")
        return True
        
    except Exception as e:
        log_test("Webhook stripe", False, f"Exception: {str(e)}")
        return False

def test_subscription_portal():
    """Test POST /api/subscription/portal"""
    print("=== Testing POST /api/subscription/portal ===")
    
    try:
        # Test with user who has no stripe_customer_id (should fail)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "email": f"portal_test_{timestamp}@codefuturo.com",
            "password": "testpass123",
            "name": f"Portal Test {timestamp}"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 200:
            log_test("Portal - registration", False, f"Registration failed: {response.status_code}")
            return False
            
        auth_data = response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to access portal without having a customer_id
        response = requests.post(f"{BASE_URL}/subscription/portal", json={}, headers=headers)
        
        if response.status_code != 400:
            log_test("Portal without customer", False, f"Expected 400, got {response.status_code}")
            return False
            
        log_test("Portal validation", True, "Correctly rejected user without stripe_customer_id")
        
        # Now create a checkout session (which creates a customer)
        checkout_data = {
            "plan_id": "pro_annual",
            "origin_url": "https://web-replica-128.preview.emergentagent.com"
        }
        
        response = requests.post(f"{BASE_URL}/subscription/checkout", json=checkout_data, headers=headers)
        
        if response.status_code != 200:
            log_test("Portal - checkout setup", False, f"Checkout failed: {response.status_code}")
            return False
            
        # Now try portal again (should work)
        portal_data = {
            "origin_url": "https://web-replica-128.preview.emergentagent.com"
        }
        
        response = requests.post(f"{BASE_URL}/subscription/portal", json=portal_data, headers=headers)
        
        if response.status_code != 200:
            log_test("Portal after checkout", False, f"Expected 200, got {response.status_code}")
            return False
            
        data = response.json()
        
        if "url" not in data:
            log_test("Portal response", False, "Missing 'url' in response")
            return False
            
        # Verify URL is a Stripe portal URL
        if not data["url"].startswith("https://billing.stripe.com/"):
            log_test("Portal URL", False, f"URL doesn't start with https://billing.stripe.com/: {data['url']}")
            return False
            
        log_test("Subscription portal", True, "Portal URL created successfully")
        return True
        
    except Exception as e:
        log_test("Subscription portal", False, f"Exception: {str(e)}")
        return False

def test_stripe_integration_flow():
    """Test complete Stripe integration flow"""
    print("=== Testing Complete Stripe Integration Flow ===")
    
    try:
        # 1. Register new user
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "email": f"flow_test_{timestamp}@codefuturo.com",
            "password": "testpass123",
            "name": f"Flow Test {timestamp}"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 200:
            log_test("Flow - registration", False, f"Registration failed: {response.status_code}")
            return False
            
        auth_data = response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        log_test("Flow - User registration", True, "User registered")
        
        # 2. Check subscription status (should be is_pro=false)
        response = requests.get(f"{BASE_URL}/subscription/me", headers=headers)
        if response.status_code != 200:
            log_test("Flow - subscription/me", False, f"Failed: {response.status_code}")
            return False
            
        sub_data = response.json()
        if sub_data["is_pro"] != False:
            log_test("Flow - initial is_pro", False, f"Expected false, got {sub_data['is_pro']}")
            return False
            
        log_test("Flow - Initial subscription status", True, "is_pro=false confirmed")
        
        # 3. Create checkout session
        checkout_data = {
            "plan_id": "pro_annual",
            "origin_url": "https://web-replica-128.preview.emergentagent.com"
        }
        
        response = requests.post(f"{BASE_URL}/subscription/checkout", json=checkout_data, headers=headers)
        if response.status_code != 200:
            log_test("Flow - checkout", False, f"Checkout failed: {response.status_code}")
            return False
            
        checkout_result = response.json()
        session_id = checkout_result["session_id"]
        
        if not checkout_result["url"].startswith("https://checkout.stripe.com/"):
            log_test("Flow - checkout URL", False, "Invalid checkout URL")
            return False
            
        log_test("Flow - Checkout session", True, f"Session created: {session_id}")
        
        # 4. Verify payment_transactions record was created
        # We can't directly query the DB, but we can verify the session status endpoint works
        response = requests.get(f"{BASE_URL}/subscription/status/{session_id}", headers=headers)
        if response.status_code != 200:
            log_test("Flow - session status", False, f"Status check failed: {response.status_code}")
            return False
            
        status_data = response.json()
        log_test("Flow - Session status check", True, f"Status: {status_data['status']}")
        
        # 5. Verify user now has stripe_customer_id
        response = requests.get(f"{BASE_URL}/subscription/me", headers=headers)
        if response.status_code != 200:
            log_test("Flow - final subscription/me", False, f"Failed: {response.status_code}")
            return False
            
        final_sub_data = response.json()
        if not final_sub_data.get("stripe_customer_id"):
            log_test("Flow - stripe_customer_id", False, "Customer ID not set after checkout")
            return False
            
        log_test("Flow - Customer created", True, "stripe_customer_id set")
        
        log_test("Complete Stripe flow", True, "All steps completed successfully")
        return True
        
    except Exception as e:
        log_test("Stripe integration flow", False, f"Exception: {str(e)}")
        return False

def main():
    print("CodeFuturo Backend Testing - Stripe Integration + Legacy Endpoints")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print()
    
    # Stripe integration tests
    stripe_tests = [
        test_subscription_plans,
        test_subscription_me_new_user,
        test_subscription_checkout,
        test_subscription_status,
        test_webhook_stripe,
        test_subscription_portal,
        test_stripe_integration_flow
    ]
    
    # Legacy tests (regression check)
    legacy_tests = [
        test_tracks_endpoint,
        test_python_zero_path,
        test_javascript_path,
        test_nonexistent_path,
        test_lesson_detail,
        test_nonexistent_lesson,
        test_end_to_end_flow,
        test_legacy_endpoints
    ]
    
    print("\n" + "=" * 60)
    print("STRIPE INTEGRATION TESTS")
    print("=" * 60 + "\n")
    
    stripe_passed = 0
    for test_func in stripe_tests:
        try:
            result = test_func()
            # Handle tests that return tuples (with additional data)
            if isinstance(result, tuple):
                if result[0]:
                    stripe_passed += 1
            elif result:
                stripe_passed += 1
        except Exception as e:
            print(f"❌ FAIL {test_func.__name__}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("LEGACY ENDPOINTS (REGRESSION CHECK)")
    print("=" * 60 + "\n")
    
    legacy_passed = 0
    for test_func in legacy_tests:
        try:
            if test_func():
                legacy_passed += 1
        except Exception as e:
            print(f"❌ FAIL {test_func.__name__}: {str(e)}")
    
    print("=" * 60)
    print(f"STRIPE TESTS: {stripe_passed}/{len(stripe_tests)} passed")
    print(f"LEGACY TESTS: {legacy_passed}/{len(legacy_tests)} passed")
    print(f"TOTAL: {stripe_passed + legacy_passed}/{len(stripe_tests) + len(legacy_tests)} passed")
    
    if stripe_passed == len(stripe_tests) and legacy_passed == len(legacy_tests):
        print("🎉 All tests passed! Stripe integration working correctly, no regressions.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())