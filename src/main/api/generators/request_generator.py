from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.credit_repay_request import RepayRequest


class RequestGenerator:
    @staticmethod
    def credit(
            account_id: int,
            amount: float = 5000,
            term_months: int = 12
    ):
        return CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=term_months
        )

    @staticmethod
    def deposit(
            account_id: int,
            amount: float = 1000
    ):
        return DepositRequest(
            accountId=account_id,
            amount=amount
        )

    @staticmethod
    def transfer(
            from_account: int,
            to_account: int,
            amount: float = 500
    ):
        return TransferRequest(
            fromAccountId=from_account,
            toAccountId=to_account,
            amount=amount
        )

    @staticmethod
    def repay(
            account_id: int,
            credit_id: int,
            amount: float = 5000
    ):
        return RepayRequest(
            accountId=account_id,
            creditId=credit_id,
            amount=amount
        )