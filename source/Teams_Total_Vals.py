

class Teams_Total_Vals(object):

    def __init__(self):

        self.wp = 0.
        self.nd = 0.
        self.team_name = "None"

        self.punkte = 0
        self.tore_geschossen = 0
        self.tore_erhalten = 0

    def update_wp(self, wp):

        self.wp = wp

    def update_nd(self, nd):

        self.nd = nd

    def update_team_name(self, name):

        self.team_name = name

    def reset_season_stats(self):
        self.punkte = 0
        self.tore_geschossen = 0
        self.tore_erhalten = 0

    def update_season_stats(self, goals_scored, goals_received):

        if goals_scored > goals_received:
            self.punkte += 3
        elif goals_scored < goals_received:
            pass
        else:
            self.punkte += 1

    def to_dict(self):
        return {
            "wp": self.wp,
            "nd": self.nd,
            "team_name": self.team_name,
            "punkte": self.punkte,
            "tore_geschossen": self.tore_geschossen,
            "tore_erhalten": self.tore_erhalten,
        }

    def from_dict(self, data):
        self.wp = float(data.get("wp", self.wp))
        self.nd = float(data.get("nd", self.nd))
        self.team_name = str(data.get("team_name", self.team_name))
        self.punkte = int(data.get("punkte", self.punkte))
        self.tore_geschossen = data.get("tore_geschossen", self.tore_geschossen)
        self.tore_erhalten = data.get("tore_erhalten", self.tore_erhalten)
