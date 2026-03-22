from services.api_service.leetify_api import LeetifyAPI, LeetifyAPIDataWorker


class GetLeetifySummary:

    async def execute(self, steam64_id: str) -> str:
        async with LeetifyAPI(steam64_id) as api:
            data = await api.get_matches(limit=10)

        if not data:
            return "❌ Failed to fetch matches."

        worker = LeetifyAPIDataWorker(data)
        summary = worker.get_matches_stats_summary()
        player = worker.get_player_info()

        if not summary:
            return "📊 No data available."

        # Format the response beautifully
        name = player.get('name', 'Unknown')
        total_matches = summary['total_matches']
        avg_kd = summary['avg_kd']
        avg_rating = summary['avg_rating']
        total_kills = summary['total_kills']
        total_deaths = summary['total_deaths']
        
        # Create a visual separator
        separator = "═" * 40
        
        return (
            f"\n{separator}\n"
            f"🎮 PLAYER STATISTICS\n"
            f"{separator}\n"
            f"👤 Player: {name}\n"
            f"🎯 Steam64 ID: {steam64_id}\n"
            f"{separator}\n"
            f"📈 MATCH SUMMARY\n"
            f"{separator}\n"
            f"🏆 Total Matches: {total_matches}\n"
            f"⚔️  K/D Ratio: {avg_kd:.2f}\n"
            f"⭐ Avg Rating: {avg_rating:.2f}\n"
            f"💀 Total Kills: {total_kills}\n"
            f"☠️  Total Deaths: {total_deaths}\n"
            f"{separator}\n"
            f"📊 Performance: {'🔴 Below Average' if avg_kd < 1.0 else '🟢 Above Average'}\n"
            f"{separator}"
        )