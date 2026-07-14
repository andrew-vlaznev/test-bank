from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requsters.validate_crud_requster import ValidateCrudRequester
from src.main.api.models import credit_request, credit_repay_request
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.admin_steps import BaseSteps
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_repay_request import RepayRequest



class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest, response_spec=ResponseSpecs.request_ok()):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            response_spec
        ).post(deposit_request)
        return response

    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest, response_spec=ResponseSpecs.request_ok()):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            response_spec
        ).post(transfer_request)
        return response

    def credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest, response_spec=ResponseSpecs.request_created()):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_ACCOUNT,
            response_spec
        ).post(credit_request)
        return response

    def credit_repay(self, create_user_request: CreateUserRequest, credit_repay_request: RepayRequest, response_spec=ResponseSpecs.request_ok()):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            response_spec
        ).post(credit_repay_request)
        return response