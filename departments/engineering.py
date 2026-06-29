from core.department_head import DepartmentHead

class EngineeringDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="CTO",
            team_keys=["FE","BE","MOB","AIB","API","CR","TEST","DOC"]
        )

    def build_project(self, project_description):
        """Full engineering: architect → build → review → test → document"""
        print(f"\n💻 Engineering: Building '{project_description[:40]}'")
        results = {}

        # Architecture first
        arch = self.team["BE"].think(
            f"Design complete architecture for: {project_description}"
        )
        results["BE"] = {"agent":"Backend","task":"Architecture","result":arch}

        # Frontend
        fe = self.team["FE"].think(
            f"Build frontend for: {project_description}\nArchitecture: {arch[:200]}"
        )
        results["FE"] = {"agent":"Frontend","task":"Frontend","result":fe}

        # Review
        review = self.team["CR"].think(
            f"Review this project plan:\n{arch[:300]}\n{fe[:300]}"
        )
        results["CR"] = {"agent":"Review","task":"Code Review","result":review}

        # Testing
        tests = self.team["TEST"].think(
            f"Create test plan for: {project_description}"
        )
        results["TEST"] = {"agent":"Testing","task":"Test Plan","result":tests}

        # Documentation
        docs = self.team["DOC"].think(
            f"Write documentation for: {project_description}"
        )
        results["DOC"] = {"agent":"Docs","task":"Documentation","result":docs}

        return self._synthesize(
            f"Build project: {project_description}", results
        )

    def build_website(self, client, requirements):
        fe = self.team["FE"].think(
            f"Build complete website for {client}. Requirements: {requirements}"
        )
        return fe

    def code_review(self, code, language):
        return self.team["CR"].think(
            f"Review this {language} code:\n{code}"
        )

    def ai_system(self, description):
        return self.team["AIB"].think(
            f"Design and build AI system for: {description}"
        )
