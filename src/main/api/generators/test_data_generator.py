class TestDataGenerator:
    @staticmethod
    def transfer(deposit_amount: float, transfer_amount: float):
        return {
            "expected_sender_balance": deposit_amount - transfer_amount,
            "expected_receiver_balance": transfer_amount
        }

    @staticmethod
    def credit_repay(balance: float, amount: float):
        return {
            "expected_balance": balance + amount
        }