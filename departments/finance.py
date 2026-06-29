from core.department_head import DepartmentHead

class FinanceDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="BOOK",
            team_keys=["INV","EXP","PAY"]
        )

    def create_invoice(self, client, services, amount):
        return self.team["INV"].think(
            f"Create professional invoice for:\n"
            f"Client: {client}\n"
            f"Services: {services}\n"
            f"Amount: {amount}"
        )

    def expense_report(self, expenses):
        return self.team["EXP"].think(
            f"Analyze and optimize these expenses: {expenses}"
        )

    def financial_summary(self, data):
        return self.quick_ask(
            "BOOK",
            f"Create financial summary from: {data}"
        )
