import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from source.game_logic import compute_match, to_float
from source.store import Store


class TestLogic(unittest.TestCase):

    def test_compute_match_basic(self):
        # Heim: Angriff 3, Verteidigung 1, WP 1 / Auswaerts: Angriff 2, Verteidigung 2, WP 0
        gh, ga = compute_match(3, 1, 2, 2, 1, 0)
        # off_h=4, def_h=2, off_a=2, def_a=2 -> 4-2=2, 2-2=0
        self.assertEqual((gh, ga), (2, 0))

    def test_no_negative_goals(self):
        gh, ga = compute_match(0, 0, 0, 5, 0, 0)
        self.assertEqual((gh, ga), (0, 0))

    def test_half_points(self):
        gh, ga = compute_match(1.5, 0, 0.5, 1, 0, 0)
        # 1.5-1 = 0.5 ; 0.5-0 = 0.5
        self.assertEqual((gh, ga), (0.5, 0.5))

    def test_to_float(self):
        self.assertEqual(to_float("1,5"), 1.5)
        self.assertEqual(to_float(""), 0.0)
        self.assertEqual(to_float("abc", 7), 7)

    def test_season_stats(self):
        from source.Teams_Total_Vals import Teams_Total_Vals
        t = Teams_Total_Vals()
        t.update_season_stats(2, 1)
        t.update_season_stats(1, 1)
        t.update_season_stats(0, 3)
        self.assertEqual(t.punkte, 4)

    def test_store_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "teams.json")
            s = Store(path)
            s.teams[2].update_team_name("Hippos")
            s.teams[2].update_wp(2.0)
            s.teams[2].update_season_stats(3, 0)
            s.save()
            s2 = Store(path)
            s2.load()
            self.assertEqual(s2.teams[2].team_name, "Hippos")
            self.assertEqual(s2.teams[2].wp, 2.0)
            self.assertEqual(s2.teams[2].punkte, 3)
            self.assertEqual(s2.teams[0].team_name, "Team 1")

    def test_store_corrupt_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "teams.json")
            with open(path, "w") as f:
                f.write("{kaputt")
            s = Store(path)
            s.load()
            self.assertEqual(s.teams[0].team_name, "Team 1")


if __name__ == "__main__":
    unittest.main()
