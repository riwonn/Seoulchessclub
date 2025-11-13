#!/usr/bin/env python3
"""
Database migration script to add missing columns
"""

import sqlite3
import os

def get_db_path():
    """Get the correct database path"""
    is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_STATIC_URL") or (os.getenv("PORT") and not os.path.exists("./venv"))

    if is_production:
        return "/tmp/community_control.db"
    else:
        return "./community_control.db"

def migrate_users_table():
    """Add missing columns to users table"""
    db_path = get_db_path()

    print(f"\n{'='*60}")
    print("Database Migration Script")
    print(f"{'='*60}")
    print(f"Database path: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check existing columns
        cursor.execute("PRAGMA table_info(users);")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nExisting columns in users table:")
        for col in columns:
            print(f"  - {col}")

        # Add missing columns
        migrations = []

        if 'social_provider' not in columns:
            migrations.append("ALTER TABLE users ADD COLUMN social_provider VARCHAR")

        if 'social_id' not in columns:
            migrations.append(("ALTER TABLE users ADD COLUMN social_id VARCHAR",
                             "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_social_id ON users (social_id)"))

        if migrations:
            print(f"\n{'='*60}")
            print("Applying migrations:")
            print(f"{'='*60}")

            for migration in migrations:
                if isinstance(migration, tuple):
                    # Execute multiple statements
                    for stmt in migration:
                        print(f"\n✅ Executing: {stmt}")
                        cursor.execute(stmt)
                else:
                    # Execute single statement
                    print(f"\n✅ Executing: {migration}")
                    cursor.execute(migration)

            conn.commit()
            print(f"\n✅ Migration completed successfully!")
        else:
            print(f"\n✅ No migrations needed - all columns exist")

        # Verify final schema
        print(f"\n{'='*60}")
        print("Final table schema:")
        print(f"{'='*60}")
        cursor.execute("PRAGMA table_info(users);")
        for row in cursor.fetchall():
            print(f"  {row[0]:2d}. {row[1]:20s} {row[2]:10s} (NOT NULL: {row[3]}, DEFAULT: {row[4] or 'None'})")

        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_users_table()

    if success:
        print(f"\n{'='*60}")
        print("✅ Database migration completed successfully!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("❌ Database migration failed!")
        print(f"{'='*60}\n")
