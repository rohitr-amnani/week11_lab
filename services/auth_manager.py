import bcrypt
from services.database_manager import DatabaseManager

class BcryptHasher:
    def hash_password(plain: str) -> str:
        password_bytes = plain.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(plain: str, hashed: str) -> bool:
        password_bytes = plain.encode('utf-8')
        hash_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)

class AuthManager:
    def __init__(self, db: DatabaseManager):
        self._db = db

    def user_exists(self, username: str) -> bool:
        """Checks if a user already exists in the database."""
        df = self._db.fetch_data("SELECT username FROM users WHERE username = ?", (username,))
        return not df.empty

    def register_user(self, username: str, password: str, role: str = "user"):
        if self.user_exists(username):
            print("Username already exists. Please choose a different username.")
            return False, "Username already exists."

        password_hash = BcryptHasher.hash_password(password)
        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        print("User registered successfully.")
        return True, "User registered successfully."

    def login_user(self, username: str, password: str) -> bool:
        if not self.user_exists(username):
            print("Username does not exist.")
            return False

        df = self._db.fetch_data(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        
        if df.empty:
            return False
        
        row = df.iloc[0]
        password_hash_db = row['password_hash']

        if BcryptHasher.check_password(password, password_hash_db):
            print("Login successful.")
            return True
        else:
            print("Incorrect password.")
            return False

    def validate_username(self, username: str):
        if not username:
            return False, "Username cannot be empty."
        return True, ""

    def validate_password(self, password: str):
        if not password:
            return False, "Password cannot be empty."
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        return True, ""