from services.api_service.leetify_api import LeetifyAPI, LeetifyAPIDataWorker


class GetLeetifySummary:

    async def execute(self, steam64_id: str) -> str:
        async with LeetifyAPI(steam64_id) as api:
            data = await api.get_matches(limit=10)

        if not data:
            return "Failed to fetch matches."

        worker = LeetifyAPIDataWorker(data)
        summary = worker.get_matches_stats_summary()
        player = worker.get_player_info()
        s = worker.get_average_stats()

        if not summary:
            return "No data available."

        return (
            f"Player: {player.get('name', 'Unknown')}\n"
            f"Matches: {summary['total_matches']}\n"
            f"Avg KD: {summary['avg_kd']}\n"
            f"Avg Rating: {summary['avg_rating']}"
            f"AVG Stats {s}"
        )