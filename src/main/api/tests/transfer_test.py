from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransferAccount:
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        sender_account_response = api_manager.user_steps.create_account(
            create_user_request
        )
        receiver_account_response = api_manager.user_steps.create_account(
            create_user_request
        )


        deposit_amount = 1000

        transfer_amount = 500

        deposit_request = DepositRequest(
            accountId=sender_account_response.id,
            amount=deposit_amount
        )

        deposit_response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        transfer_request = TransferRequest(
            fromAccountId=sender_account_response.id,
            toAccountId=receiver_account_response.id,
            amount=transfer_amount
        )

        expected_sender_balance = deposit_amount - transfer_amount

        expected_receiver_balance = transfer_amount

        transfer_response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_request
        )

        assert transfer_response.fromAccountId == sender_account_response.id
        assert transfer_response.toAccountId == receiver_account_response.id
        assert transfer_response.fromAccountIdBalance == expected_sender_balance


        sender_account_from_db = Account.get_account_by_id(
            db_session,
            sender_account_response.id
        )

        receiver_account_from_db = Account.get_account_by_id(
            db_session,
            receiver_account_response.id
        )

        assert sender_account_from_db is not None, "Аккаунт не найден в БД"
        assert receiver_account_from_db is not None, "Аккаунт не найден в БД"
        assert sender_account_from_db.balance == expected_sender_balance
        assert receiver_account_from_db.balance == expected_receiver_balance


    def test_transfer_other_user_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        user1_request = create_user_request
        user2_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user2_request)

        user1_account_response = api_manager.user_steps.create_account(
            user1_request
        )

        deposit_amount = 1000

        transfer_amount = 500

        deposit_request = DepositRequest(
            accountId=user1_account_response.id,
            amount=deposit_amount
        )

        deposit_response = api_manager.user_steps.deposit(
            user1_request,
            deposit_request
        )

        user2_account_response = api_manager.user_steps.create_account(
            user2_request
        )

        transfer_request = TransferRequest(
            fromAccountId=user1_account_response.id,
            toAccountId=user2_account_response.id,
            amount=transfer_amount
        )

        transfer_response = api_manager.user_steps.transfer(
            user2_request,
            transfer_request,
            ResponseSpecs.request_not_found()
        )

        assert "does not belong" in transfer_response.json()["error"]

        user1_from_db = Account.get_account_by_id(
            db_session,
            user1_account_response.id
        )

        user2_from_db = Account.get_account_by_id(
            db_session,
            user2_account_response.id
        )

        assert user1_from_db is not None, "Аккаунт не найден в БД"
        assert user1_from_db.balance == 1000
        assert user2_from_db is not None, "Аккаунт не найден в БД"
        assert user2_from_db.balance == 0