from dataclasses import dataclass, asdict
from asyncpg.pool import Pool
from asyncpg.exceptions import CheckViolationError


class WalletOperationError(Exception):
    def __init__(self, message: str):
        self.message = message


@dataclass
class Wallet:

    wallet_id: int
    balance: int = 0

    @classmethod
    async def create(cls, pool: Pool) -> 'Wallet':
        result = await pool.fetchrow(
            """
            INSERT INTO wallets DEFAULT VALUES 
            RETURNING wallet_id
            """
        )
        return Wallet(wallet_id=result['wallet_id'])

    @classmethod
    async def get(cls, pool: Pool,
                  wallet_id: int) -> 'Wallet':
        result = await pool.fetchrow(
            """
            SELECT * FROM wallets
            WHERE wallet_id = $1
            """,
            wallet_id
        )

        if not result:
            raise WalletOperationError('Wallet not found')

        return Wallet(wallet_id=result['wallet_id'],
                      balance=result['balance'])

    async def delete(self, pool: Pool):
        await pool.execute(
            """
            DELETE FROM wallets
            WHERE wallet_id = $1
            """,
            self.wallet_id
        )

    async def deposit(self, pool: Pool, val: int):
        try:
            result = await pool.fetchrow(
                """
                UPDATE wallets
                SET balance = balance + $2
                WHERE wallet_id = $1
                RETURNING balance 
                """,
                self.wallet_id, val, timeout=1
            )
        except CheckViolationError:
            raise WalletOperationError('Not enough money')

        if result is None:
            raise WalletOperationError('Wallet not found')

        self.balance = result['balance']

    def serialize(self) -> dict:
        return asdict(self)
