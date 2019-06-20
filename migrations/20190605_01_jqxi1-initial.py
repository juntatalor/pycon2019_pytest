"""
Initial
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    CREATE TABLE wallets(
    wallet_id SERIAL PRIMARY KEY,
    balance INTEGER 
        NOT NULL CHECK (balance >= 0) DEFAULT 0
    )
    """, """
    DROP TABLE wallets
    """)
]

