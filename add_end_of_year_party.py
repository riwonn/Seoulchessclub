"""
Script to add SCC End of Year Party meeting to the database
"""
from datetime import datetime
from database import SessionLocal, Meeting

def add_end_of_year_party():
    """Add the December 20th SCC End of Year Party meeting"""
    db = SessionLocal()

    try:
        # Create the meeting
        end_of_year_party = Meeting(
            title="SCC End of Year Party",
            date_time=datetime(2024, 12, 20, 18, 0),  # December 20, 2024, 6:00 PM
            location="Seoul Chess Club Venue (TBA)",
            capacity=40
        )

        db.add(end_of_year_party)
        db.commit()
        db.refresh(end_of_year_party)

        print("=" * 60)
        print("✅ Successfully added SCC End of Year Party!")
        print("=" * 60)
        print(f"Meeting ID: {end_of_year_party.id}")
        print(f"Title: {end_of_year_party.title}")
        print(f"Date & Time: {end_of_year_party.date_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Location: {end_of_year_party.location}")
        print(f"Capacity: {end_of_year_party.capacity} people")
        print("=" * 60)
        print("\n🎉 The meeting is now available for registration with payment!")
        print("Users can pay ₩10,000 to register for this event.")

    except Exception as e:
        print(f"❌ Error adding meeting: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_end_of_year_party()
