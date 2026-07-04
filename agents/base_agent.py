import asyncio
import os

class BaseAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.status = "HEALTH"
        self.directive = "SELF-HEAL + AUTO-INSTALL + AUTO-FAILOVER"

    async def run_safe(self):
        while True:
            try:
                await self.work()
                await asyncio.sleep(600)
            except Exception as e:
                await self.self_heal(e)

    async def self_heal(self, error):
        print(f"[{self.id}] SELF-HEALING: {error}")
        await asyncio.sleep(5)
        self.status = "RECOVERED"

    async def work(self):
        pass