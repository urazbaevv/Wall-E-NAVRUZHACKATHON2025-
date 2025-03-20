from backend.database import get_db_connection  # get_db_connection funksiyasini import qilish

def delete_all_containers():
    """ Barcha konteynerlarni chiqarish va o‘chirish """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 📝 Barcha konteynerlarni chiqarish
        cursor.execute("SELECT * FROM containers")
        rows = cursor.fetchall()

        if rows:
            print("📦 List of containers:")
            for row in rows:
                print(row)
        else:
            print("⚠️ No containers found!")

        # 🚮 Barcha konteynerlarni o‘chirish
        cursor.execute("DELETE FROM containers")
        conn.commit()
        print("✅ All containers have been deleted!")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    finally:
        conn.close()  # Ulanishni yopamiz

# Skript mustaqil ishlatilayotganini tekshiramiz
if __name__ == "__main__":
    delete_all_containers()
