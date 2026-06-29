from core.department_head import DepartmentHead

class BusinessDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="SALES",
            team_keys=["LEAD","CRM","PROP","FLUP"]
        )

    def get_new_client(self, target):
        """Full pipeline: find → pitch → propose → follow up"""
        print(f"\n🎯 Business Dept: Full client acquisition for {target}")
        leads = self.team["LEAD"].think(
            f"Find and qualify leads for: {target}"
        )
        outreach = self.team["CRM"].think(
            f"Create outreach strategy for: {target}\nLeads found: {leads[:200]}"
        )
        proposal = self.team["PROP"].think(
            f"Write proposal for: {target}"
        )
        followup = self.team["FLUP"].think(
            f"Write follow-up sequence for: {target}"
        )
        return self._synthesize(
            f"Get new client: {target}",
            {
                "LEAD": {"agent":"Lead Gen","task":target,"result":leads},
                "CRM":  {"agent":"CRM","task":target,"result":outreach},
                "PROP": {"agent":"Proposal","task":target,"result":proposal},
                "FLUP": {"agent":"Follow-up","task":target,"result":followup},
            }
        )

    def write_proposal(self, client, service, budget=""):
        return self.team["PROP"].think(
            f"Write complete proposal for {client} needing {service}. Budget: {budget}"
        )

    def find_leads(self, niche):
        return self.team["LEAD"].think(
            f"Find and qualify leads in: {niche}"
        )
