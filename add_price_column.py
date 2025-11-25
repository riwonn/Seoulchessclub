"""
Script to add price column to meetings table
"""
from database import engine
import sqlite3

def add_price_column():
    """Add price column to meetings table"""
    print("=" * 60)
    print("🔄 Adding price column to meetings table")
    print("=" * 60)

    try:
        # Get the database path from the engine
        db_path = engine.url.database

        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("PRAGMA table_info(meetings)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'price' in columns:
            print("\n✅ Price column already exists!")
        else:
            # Add price column with default value
            cursor.execute("""
                ALTER TABLE meetings
                ADD COLUMN price REAL NOT NULL DEFAULT 10000.0
            """)
            conn.commit()
            print("\n✅ Successfully added price column to meetings table!")
            print("   Default value: ₩10,000")

        conn.close()

        print("\n" + "=" * 60)
        print("Migration completed! You can now set custom prices for meetings.")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    add_price_column()
