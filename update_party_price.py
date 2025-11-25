"""
Script to update SCC End of Year Party price to 30,000 won
"""
from database import SessionLocal, Meeting

def update_party_price():
    """Update the End of Year Party price to 30,000 won"""
    db = SessionLocal()

    try:
        # Find the End of Year Party meeting
        party = db.query(Meeting).filter(
            Meeting.title == "SCC End of Year Party"
        ).first()

        if not party:
            print("❌ SCC End of Year Party meeting not found")
            return

        # Update the price
        old_price = party.price
        party.price = 30000.0
        db.commit()

        print("=" * 60)
        print("✅ Successfully updated SCC End of Year Party price!")
        print("=" * 60)
        print(f"Meeting ID: {party.id}")
        print(f"Title: {party.title}")
        print(f"Old Price: ₩{int(old_price):,}")
        print(f"New Price: ₩{int(party.price):,}")
        print("=" * 60)
        print("\n🎉 Users will now see ₩30,000 when registering for this event!")

    except Exception as e:
        print(f"❌ Error updating price: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_party_price()
