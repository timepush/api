from psycopg import AsyncCursor
from app.db.pool import get_pool
from app.common.security import hash_password, verify_password, create_jwt_token
from app.features.auth.models import UserInManual, UserInOAuth

class InvalidCredentialsError(Exception): pass
class NotVerifiedError(Exception): pass

async def signup_manual(user: UserInManual):
    async with get_pool().connection() as conn:
        async with conn.transaction():
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT 1 FROM users WHERE email = %s AND login_type = 'manual'
                """, (user.email,))
                exists = await cur.fetchone()
                if exists:
                    raise ValueError("User already exists")

                await cur.execute("""
                    INSERT INTO users (email, first_name, last_name, login_type, password_hash)
                    VALUES (%s, %s, %s, 'manual', %s)
                """, (
                    user.email,
                    user.first_name,
                    user.last_name,
                    hash_password(user.password)
                ))

async def login_manual(email: str, password: str) -> str:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT id, password_hash, is_verified
                FROM users
                WHERE email = %s AND login_type = 'manual'
            """, (email,))
            row = await cur.fetchone()
            if not row:
                raise InvalidCredentialsError()

            user_id, password_hash, is_verified = row

            if not verify_password(password, password_hash):
                raise InvalidCredentialsError()

            if not is_verified:
                raise NotVerifiedError()

            return create_jwt_token(user_id)

async def login_or_register_oauth(user: UserInOAuth) -> str:
    async with get_pool().connection() as conn:
        async with conn.transaction():
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT id FROM users WHERE login_type = %s AND external_id = %s
                """, (user.login_type, user.external_id))
                row = await cur.fetchone()

                if row:
                    user_id = row[0]
                else:
                    await cur.execute("""
                        INSERT INTO users (email, first_name, last_name, login_type, external_id, is_verified)
                        VALUES (%s, %s, %s, %s, %s, true)
                        RETURNING id
                    """, (
                        user.email,
                        user.first_name,
                        user.last_name,
                        user.login_type,
                        user.external_id
                    ))
                    user_id = (await cur.fetchone())[0]

    return create_jwt_token(user_id)
