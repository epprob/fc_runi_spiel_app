"""Hält die 6 Teams und speichert sie als JSON (wichtig auf dem Handy,
weil Android Apps jederzeit im Hintergrund beenden kann)."""

import json
import os

from source.Teams_Total_Vals import Teams_Total_Vals

NUM_TEAMS = 6
DEFAULT_ND = 1e5  # wie in der Desktop-Version vorbelegt


class Store(object):

    def __init__(self, path=None):
        self.path = path
        self.teams = []
        for i in range(NUM_TEAMS):
            team = Teams_Total_Vals()
            team.update_wp(0.)
            team.update_nd(DEFAULT_ND)
            team.update_team_name("Team " + str(i + 1))
            self.teams.append(team)

    def load(self):
        if not self.path or not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for team, entry in zip(self.teams, data.get("teams", [])):
                team.from_dict(entry)
        except (OSError, ValueError, TypeError):
            # defekte Datei ignorieren, Standardwerte bleiben
            pass

    def save(self):
        if not self.path:
            return
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({"teams": [t.to_dict() for t in self.teams]}, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        except OSError:
            pass
