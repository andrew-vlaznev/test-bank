from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.generators.request_generator import RequestGenerator
from src.main.api.generators.test_data_generator import TestDataGenerator


class TestTransferAccount:
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, two_accounts_with_balance):
        sender_account, receiver_account, deposit_request = two_accounts_with_balance

        transfer_request = RequestGenerator.transfer(
            sender_account.id,
            receiver_account.id
        )

        expected = TestDataGenerator.transfer(
            deposit_request.amount,
            transfer_request.amount
        )

        transfer_response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_request
        )

        assert transfer_response.fromAccountId == sender_account.id, "Неверный id счета отправителя"
        assert transfer_response.toAccountId == receiver_account.id, "Неверный id счета получателя"
        assert transfer_response.fromAccountIdBalance == expected["expected_sender_balance"], "Баланс счета отправителя после перевода неверный"

        sender_account_from_db = Account.get_account_by_id(
            db_session,
            sender_account.id
        )

        receiver_account_from_db = Account.get_account_by_id(
            db_session,
            receiver_account.id
        )

        assert sender_account_from_db is not None, "Счет отправителя не найден в БД"
        assert receiver_account_from_db is not None, "Счет получателя не найден в БД"
        assert sender_account_from_db.balance == expected["expected_sender_balance"], "Баланс счета отправителя в БД не совпадает"
        assert receiver_account_from_db.balance == expected["expected_receiver_balance"], "Баланс счета получателя в БД не совпадает"

    def test_transfer_other_user_account(self, db_session: Session, api_manager: ApiManager, account_with_balance, second_user: CreateUserRequest, second_user_account):
        account, deposit_request = account_with_balance

        transfer_request = RequestGenerator.transfer(
            account.id,
            second_user_account.id
        )

        transfer_response = api_manager.user_steps.transfer(
            second_user,
            transfer_request,
            ResponseSpecs.request_not_found()
        )

        assert "does not belong" in transfer_response.json()["error"], "Получено неверное сообщение об ошибке"

        user1_from_db = Account.get_account_by_id(
            db_session,
            account.id
        )

        user2_from_db = Account.get_account_by_id(
            db_session,
            second_user_account.id
        )

        assert user1_from_db is not None, "Счет первого пользователя не найден в БД"
        assert user1_from_db.balance == deposit_request.amount, "Баланс первого пользователя изменился после неуспешного перевода"
        assert user2_from_db is not None, "Счет второго пользователя не найден в БД"
        assert user2_from_db.balance == 0, "Баланс второго пользователя изменился после неуспешного перевода"