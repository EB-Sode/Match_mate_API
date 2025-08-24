from datetime import datetime
import requests
from .models import Fixtures, Team, League

API_KEY = "5fc979c5c56e4721a0b76f6ef58c5699"
COMPETITIONS = ["PL", "BL1", "SA", "PD"]  # Premier League, Bundesliga, Serie A, La Liga
BASE_URL = "https://api.football-data.org/v4/competitions/{}/matches"


def import_fixtures():
    headers = {"X-Auth-Token": API_KEY}
    imported = 0

    for code in COMPETITIONS:
        URL = BASE_URL.format(code)
        response = requests.get(URL, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve code {code}: {response.status_code}")
            continue

        data = response.json()

        league_name = data.get("competition", {}).get("name", "Unknown League")
        league, _ = League.objects.get_or_create(name=league_name)

        
        for match in data.get("matches", []):
            home_name = match["homeTeam"]["name"]
            away_name = match["awayTeam"]["name"]

            # Ensure teams exist
            home_team, _ = Team.objects.get_or_create(name=home_name, defaults={"league": league})
            away_team, _ = Team.objects.get_or_create(name=away_name, defaults={"league": league})

            # Save/update fixture
            _, created = Fixtures.objects.update_or_create(
                homeTeam=home_team,
                awayTeam=away_team,
                matchDate=datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00")).date(),
                defaults={
                    "actualHomeScore": match["score"]["fullTime"]["home"] or 0,
                    "actualAwayScore": match["score"]["fullTime"]["away"] or 0,
                    "league": league,
                    "status": match["status"].lower(),  # scheduled/live/finished
                }
            )
            if created:
                imported += 1

    return imported
