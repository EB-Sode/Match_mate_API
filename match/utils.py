from datetime import datetime
import requests
from .models import Fixtures, Team, League
from predictions.models import MatchResult

API_KEY = "5fc979c5c56e4721a0b76f6ef58c5699"
COMPETITIONS = ["PL", "BL1", "SA", "PD"]  # Premier League, Bundesliga, Serie A, La Liga
BASE_URL = "https://api.football-data.org/v4/competitions/{}/matches"


def import_fixtures():
    headers = {"X-Auth-Token": API_KEY}
    imported = 0
    results_updated = 0   # ✅ initialize this
    print("Starting fixture import...")

    for code in COMPETITIONS:
        URL = BASE_URL.format(code)
        response = requests.get(URL, headers=headers)

        if response.status_code != 200:
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


            # ✅ Always update fixture if it already exists
            fixture, created = Fixtures.objects.update_or_create(
                external_id=match["id"],  # use API's fixture ID
                defaults={
                    "home_team": home_team,
                    "away_team": away_team,
                    "match_date_time": datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00")),
                    "status": match["status"].lower(),   # make sure status is up to date
                }
            )

            if created:
                imported += 1

            # ✅ If match has finished, store the result
            if match["status"].lower() == "finished": 
                full_time = match.get("score", {}).get("fullTime", {})
                home_score = full_time.get("home")
                away_score = full_time.get("away")

                if home_score is not None and away_score is not None:
                    MatchResult.objects.update_or_create(
                        fixture=fixture,
                        defaults={
                            "actual_home_score": home_score,
                            "actual_away_score": away_score,
                        }
                    )
                    results_updated += 1
    
    print(f"Imported {imported} new fixtures, updated {results_updated} results")
    return imported, results_updated