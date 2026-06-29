from core.department_head import DepartmentHead

class MarketingDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="ANA",
            team_keys=["SEO","CONT","FB","IG","LI","EMAIL"]
        )

    def full_campaign(self, topic):
        """Full marketing campaign across all channels"""
        print(f"\n📣 Marketing: Full campaign for '{topic}'")
        results = {}
        tasks = {
            "SEO":   f"SEO strategy and keywords for: {topic}",
            "CONT":  f"Write blog post and content for: {topic}",
            "LI":    f"Write LinkedIn post for: {topic}",
            "IG":    f"Write Instagram caption for: {topic}",
            "FB":    f"Write Facebook post for: {topic}",
            "EMAIL": f"Write email campaign for: {topic}",
        }
        for code, task in tasks.items():
            result = self.team[code].think(task)
            results[code] = {
                "agent": code, "task": task, "result": result
            }
        return self._synthesize(f"Full campaign: {topic}", results)

    def linkedin_post(self, topic):
        return self.team["LI"].think(f"Write LinkedIn post: {topic}")

    def blog_post(self, topic):
        return self.team["CONT"].think(f"Write full blog post: {topic}")

    def seo_strategy(self, service):
        return self.team["SEO"].think(f"Full SEO strategy for: {service}")

    def email_sequence(self, target, service):
        return self.team["EMAIL"].think(
            f"Write cold email sequence for {target} about {service}"
        )
