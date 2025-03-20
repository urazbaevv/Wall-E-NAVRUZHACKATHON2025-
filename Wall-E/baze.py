import os

DATABASE_PATH = "data/containers.db"

# Eski bazani tozalash
if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)
    print("✅ The old database has been deleted!")
else:
    print("⚠️ The database is already gone!")