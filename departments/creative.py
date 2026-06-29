from core.department_head import DepartmentHead

class CreativeDept(DepartmentHead):
    def __init__(self):
        super().__init__(
            head_key="BRAND",
            team_keys=["UI","UX","GFX","VID"]
        )

    def full_brand(self, business_info):
        """Complete brand identity package"""
        print(f"\n🎨 Creative: Full brand for '{business_info[:40]}'")
        results = {}
        tasks = {
            "BRAND": f"Create brand identity for: {business_info}",
            "UI":    f"Create design system for: {business_info}",
            "GFX":  f"Describe visual assets needed for: {business_info}",
            "VID":  f"Write brand video script for: {business_info}",
        }
        for code, task in tasks.items():
            if code in self.team:
                result = self.team[code].think(task)
            else:
                from agents.base_agent import Agent
                result = Agent(code).think(task)
            results[code] = {"agent":code,"task":task,"result":result}
        return self._synthesize(f"Brand package: {business_info}", results)

    def design_system(self, brand):
        return self.team["UI"].think(f"Create complete design system for: {brand}")

    def video_script(self, topic, duration):
        return self.team["VID"].think(
            f"Write {duration} video script for: {topic}"
        )
