"""
Migration script to add Payment and Membership tables to existing database
"""
from database import Base, engine, init_db

def migrate():
    """Create payment and membership tables if they don't exist"""
    print("=" * 60)
    print("🔄 Starting Payment Tables Migration")
    print("=" * 60)

    try:
        # This will create all tables defined in Base metadata
        # It won't affect existing tables
        print("\n📝 Creating new tables (Payment, Membership)...")
        Base.metadata.create_all(bind=engine)

        print("\n✅ Migration completed successfully!")
        print("\nNew tables created:")
        print("  - payments")
        print("  - memberships")
        print("\nYou can now use the Kakao Pay payment features!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    migrate()
