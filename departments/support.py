from core.department_head import DepartmentHead

class SupportDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="SUP",
            team_keys=["TKT","FAQ","REV"]
        )

    def handle_issue(self, client, issue):
        response = self.team["TKT"].think(
            f"Triage and prioritize: Client={client}, Issue={issue}"
        )
        solution = self.quick_ask(
            "SUP",
            f"Resolve for {client}: {issue}"
        )
        return f"TRIAGE:\n{response}\n\nSOLUTION:\n{solution}"

    def generate_faqs(self, service):
        return self.team["FAQ"].think(
            f"Generate comprehensive FAQs for: {service}"
        )

    def collect_review(self, client, project):
        return self.team["REV"].think(
            f"Write review collection message for {client} "
            f"after completing: {project}"
        )
