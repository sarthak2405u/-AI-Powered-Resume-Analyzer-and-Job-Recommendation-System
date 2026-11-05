from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

password = "Test@12345"

hashed = hash_password(password)

print("Hashed password:", hashed)

print(
    "Password verification:",
    verify_password(password, hashed)
)

print("Authentication functions imported successfully!")