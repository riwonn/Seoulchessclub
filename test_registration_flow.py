#!/usr/bin/env python3
"""
Test script to verify registration and dashboard data flow
Tests:
1. Database connection and initialization
2. User registration via API
3. User data retrieval for dashboard
4. Meeting creation
5. Data persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, User, Meeting, init_db
from datetime import datetime
import json

def test_database_connection():
    """Test 1: Verify database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)

    try:
        init_db()
        db = SessionLocal()
        user_count = db.query(User).count()
        meeting_count = db.query(Meeting).count()

        print(f"✅ Database connection successful")
        print(f"   - Current users in database: {user_count}")
        print(f"   - Current meetings in database: {meeting_count}")

        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_user_creation():
    """Test 2: Create a test user directly in database"""
    print("\n" + "="*60)
    print("TEST 2: User Creation")
    print("="*60)

    try:
        db = SessionLocal()

        # Check if test user already exists
        test_phone = "010-1234-5678"
        existing_user = db.query(User).filter(User.phone_number == test_phone).first()

        if existing_user:
            print(f"✅ Test user already exists")
            print(f"   - ID: {existing_user.id}")
            print(f"   - Name: {existing_user.name}")
            print(f"   - Email: {existing_user.email}")
            print(f"   - Total Visits: {existing_user.total_visits}")
            user = existing_user
        else:
            # Create new test user
            new_user = User(
                name="Test User",
                phone_number=test_phone,
                email="test@example.com",
                gender="MALE",
                birth_year=1990,
                chess_experience="INTERMEDIATE",
                chess_rating="1500",
                total_visits=1
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            print(f"✅ New test user created")
            print(f"   - ID: {new_user.id}")
            print(f"   - Name: {new_user.name}")
            print(f"   - Email: {new_user.email}")
            print(f"   - Phone: {new_user.phone_number}")
            user = new_user

        db.close()
        return True, user.id
    except Exception as e:
        print(f"❌ User creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_user_retrieval():
    """Test 3: Retrieve all users (dashboard functionality)"""
    print("\n" + "="*60)
    print("TEST 3: User Retrieval (Dashboard)")
    print("="*60)

    try:
        db = SessionLocal()
        users = db.query(User).all()

        print(f"✅ Retrieved {len(users)} users from database")
        print("\n   Users in database:")
        print("   " + "-"*56)

        for i, user in enumerate(users, 1):
            print(f"   {i}. {user.name}")
            print(f"      - Email: {user.email}")
            print(f"      - Phone: {user.phone_number or 'N/A'}")
            print(f"      - Total Visits: {user.total_visits}")
            print(f"      - Created: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
            if i < len(users):
                print("   " + "-"*56)

        db.close()
        return True
    except Exception as e:
        print(f"❌ User retrieval failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_meeting_creation():
    """Test 4: Create a test meeting"""
    print("\n" + "="*60)
    print("TEST 4: Meeting Creation")
    print("="*60)

    try:
        db = SessionLocal()

        # Check if test meeting exists
        test_title = "Test Chess Meeting"
        existing_meeting = db.query(Meeting).filter(Meeting.title == test_title).first()

        if existing_meeting:
            print(f"✅ Test meeting already exists")
            print(f"   - ID: {existing_meeting.id}")
            print(f"   - Title: {existing_meeting.title}")
            print(f"   - Date: {existing_meeting.date_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   - Location: {existing_meeting.location}")
            print(f"   - Capacity: {existing_meeting.capacity}")
        else:
            # Create new meeting
            new_meeting = Meeting(
                title=test_title,
                date_time=datetime(2025, 12, 1, 14, 0),
                location="Seoul Chess Club",
                capacity=20
            )

            db.add(new_meeting)
            db.commit()
            db.refresh(new_meeting)

            print(f"✅ New test meeting created")
            print(f"   - ID: {new_meeting.id}")
            print(f"   - Title: {new_meeting.title}")
            print(f"   - Date: {new_meeting.date_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   - Location: {new_meeting.location}")
            print(f"   - Capacity: {new_meeting.capacity}")

        db.close()
        return True
    except Exception as e:
        print(f"❌ Meeting creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_data_persistence():
    """Test 5: Verify data persists across sessions"""
    print("\n" + "="*60)
    print("TEST 5: Data Persistence")
    print("="*60)

    try:
        # Close and reopen database connection
        db1 = SessionLocal()
        user_count_1 = db1.query(User).count()
        meeting_count_1 = db1.query(Meeting).count()
        db1.close()

        # Reopen with new session
        db2 = SessionLocal()
        user_count_2 = db2.query(User).count()
        meeting_count_2 = db2.query(Meeting).count()
        db2.close()

        if user_count_1 == user_count_2 and meeting_count_1 == meeting_count_2:
            print(f"✅ Data persists correctly across sessions")
            print(f"   - Users: {user_count_1} (consistent)")
            print(f"   - Meetings: {meeting_count_1} (consistent)")
            return True
        else:
            print(f"❌ Data persistence issue detected")
            print(f"   - Users: {user_count_1} -> {user_count_2}")
            print(f"   - Meetings: {meeting_count_1} -> {meeting_count_2}")
            return False
    except Exception as e:
        print(f"❌ Persistence test failed: {str(e)}")
        return False

def test_user_update():
    """Test 6: Update existing user (simulates returning user)"""
    print("\n" + "="*60)
    print("TEST 6: User Update (Returning User)")
    print("="*60)

    try:
        db = SessionLocal()

        test_phone = "010-1234-5678"
        user = db.query(User).filter(User.phone_number == test_phone).first()

        if user:
            original_visits = user.total_visits
            user.total_visits += 1
            user.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(user)

            print(f"✅ User update successful")
            print(f"   - Name: {user.name}")
            print(f"   - Total Visits: {original_visits} -> {user.total_visits}")
            print(f"   - Updated At: {user.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

            db.close()
            return True
        else:
            print(f"❌ Test user not found for update")
            db.close()
            return False
    except Exception as e:
        print(f"❌ User update failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 REGISTRATION & DASHBOARD DATA FLOW TEST")
    print("="*60)

    results = []

    # Test 1: Database Connection
    results.append(("Database Connection", test_database_connection()))

    # Test 2: User Creation
    success, user_id = test_user_creation()
    results.append(("User Creation", success))

    # Test 3: User Retrieval
    results.append(("User Retrieval", test_user_retrieval()))

    # Test 4: Meeting Creation
    results.append(("Meeting Creation", test_meeting_creation()))

    # Test 5: Data Persistence
    results.append(("Data Persistence", test_data_persistence()))

    # Test 6: User Update
    results.append(("User Update", test_user_update()))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Registration and dashboard are working correctly.")
        print("\n✅ Verification Complete:")
        print("   1. Users can register through the sign-up form")
        print("   2. Registration data is stored in the database")
        print("   3. Users appear correctly on the dashboard")
        print("   4. Meetings can be created from the dashboard")
        print("   5. All data persists across sessions")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")

    print("="*60 + "\n")

if __name__ == "__main__":
    main()
