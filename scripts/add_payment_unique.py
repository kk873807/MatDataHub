from sqlalchemy import text
from app.database import engine

def add_unique_constraint():
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE transactions ADD CONSTRAINT unique_payment_id UNIQUE (payment_id);"))
            print("Successfully added UNIQUE constraint to payment_id")
        except Exception as e:
            print(f"Failed or already exists: {e}")

if __name__ == "__main__":
    add_unique_constraint()
