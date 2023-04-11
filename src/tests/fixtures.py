from uuid import UUID

from sqlalchemy import text

user_type = {
    "id": UUID("1e071719-148a-4156-86d5-28f042186b99"),
    "name": "user",
}
user_type_sql = text(
    """
    INSERT INTO auth_user_types
    (
        id,
        name
    ) values (
        :id,
        :name
    )
"""
)

user = {
    "id": UUID("9ecbd724-e7f9-4246-bc46-ef6261744dbe"),
    "email": "test@example.com",
    "hashed_password": "$2a$10$U3imCSSjGdwZwKw.Jrvxze7Cndnkw5aG9q2tYmMP/EDwqJNSnl4oi",
    "first_name": "Test",
    "last_name": "User",
    "user_type_id": user_type["id"],
    "is_active": True,
    "is_verified": False,
}
user_sql = text(
    """
    INSERT INTO auth_users
    (
        id,
        email,
        hashed_password,
        first_name,
        last_name,
        user_type_id,
        is_active,
        is_verified
    ) values (
        :id,
        :email,
        :hashed_password,
        :first_name,
        :last_name,
        :user_type_id,
        :is_active,
        :is_verified
    )
"""
)
