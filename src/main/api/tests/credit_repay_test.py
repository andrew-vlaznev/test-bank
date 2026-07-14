from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_repay_request import RepayRequest


class TestCreditRepayAccount:
    def test_credit_account_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_amount = 5000

        term_months = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=credit_amount,
            termMonths=term_months
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        repay_amount = credit_amount

        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=repay_amount
        )

        api_manager.user_steps.deposit(
            create_credit_user_request,
            deposit_request
        )

        credit_repay_request = RepayRequest(
            creditId=credit_response.creditId,
            accountId=create_account_response.id,
            amount=repay_amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )

        expected_balance = credit_amount

        assert credit_repay_response.creditId == credit_response.creditId
        assert credit_repay_response.amountDeposited == repay_amount

        account_from_db = Account.get_account_by_id(
            db_session,
            create_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance


    def test_credit_account_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_amount = 5000

        term_months = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=credit_amount,
            termMonths=term_months
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        repay_amount = credit_amount

        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=repay_amount
        )

        api_manager.user_steps.deposit(
            create_credit_user_request,
            deposit_request
        )

        credit_repay_request = RepayRequest(
            creditId=credit_response.creditId,
            accountId=create_account_response.id,
            amount=repay_amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )

        second_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request,
            ResponseSpecs.request_conflict()
        )

        assert "The credit has already been repaid" in second_repay_response.json()["error"]

        account_from_db = Account.get_account_by_id(
            db_session,
            create_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == credit_amount


