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

def main():
    print("CodeFuturo Backend Testing - New Tracks/Lessons Endpoints")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print()
    
    tests = [
        test_tracks_endpoint,
        test_python_zero_path,
        test_javascript_path,
        test_nonexistent_path,
        test_lesson_detail,
        test_nonexistent_lesson,
        test_end_to_end_flow,
        test_legacy_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ FAIL {test_func.__name__}: {str(e)}")
    
    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! New tracks/lessons endpoints are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())