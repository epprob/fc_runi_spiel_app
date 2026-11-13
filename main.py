"""FC Runi App - Android/Kivy-Version.

Die Desktop-Version (Tkinter) liegt weiterhin in main_desktop.py + source/Gui.py.
"""

import os

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from source.game_logic import compute_match, to_float
from source.store import Store

COLOR_WP = (1, 1, 0.55, 1)       # gelb  (Würfelpunkte)
COLOR_ND = (1, 0.8, 0.5, 1)      # orange (Nilpferd-Dollar)
COLOR_OFF = (0.6, 0.72, 1, 1)    # blau  (Angriff)
COLOR_DEF = (0.6, 1, 0.72, 1)    # grün  (Verteidigung)
COLOR_BTN = (0.85, 0.2, 0.2, 1)  # rot   (Hauptknöpfe)


# ---------------------------------------------------------------- Helfer

def fmt_num(value):
    value = float(value)
    return str(int(value)) if value == int(value) else str(value)


def make_label(text, bold=False, font_size=None, halign="center"):
    """Label mit automatischem Zeilenumbruch und passender Höhe."""
    kwargs = {"text": text, "bold": bold, "halign": halign, "valign": "middle",
              "size_hint_y": None}
    if font_size:
        kwargs["font_size"] = font_size
    lbl = Label(**kwargs)
    lbl.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
    lbl.bind(texture_size=lambda inst, ts: setattr(inst, "height", max(ts[1] + dp(6), dp(30))))
    return lbl


def cell(text, width=None, halign="center", bold=False):
    lbl = Label(text=text, halign=halign, valign="middle", bold=bold)
    lbl.bind(size=lambda inst, s: setattr(inst, "text_size", s))
    if width is not None:
        lbl.size_hint_x = None
        lbl.width = width
    return lbl


def num_input(text, bg=(1, 1, 1, 1)):
    return TextInput(
        text=text, multiline=False, input_filter="float", input_type="number",
        halign="center", write_tab=False, background_color=bg,
        foreground_color=(0, 0, 0, 1), cursor_color=(0, 0, 0, 1),
        padding=[dp(6), dp(12)], size_hint_y=None, height=dp(48),
    )


def text_input(text):
    return TextInput(
        text=text, multiline=False, write_tab=False,
        background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1),
        cursor_color=(0, 0, 0, 1), padding=[dp(8), dp(12)],
        size_hint_y=None, height=dp(48),
    )


def red_button(text):
    return Button(text=text, size_hint_y=None, height=dp(52),
                  background_normal="", background_color=COLOR_BTN, color=(1, 1, 1, 1),
                  bold=True)


def vertical_scroll_box(spacing=10, padding=12):
    box = GridLayout(cols=1, spacing=dp(spacing), padding=dp(padding), size_hint_y=None)
    box.bind(minimum_height=box.setter("height"))
    return box


def team_choices(teams):
    return ["P%d – %s" % (i + 1, t.team_name) for i, t in enumerate(teams)]


def choice_index(text):
    """'P3 – Name' -> 2"""
    return int(text.split()[0][1:]) - 1


# ---------------------------------------------------------------- Spieltag

class MatchdayTab(ScrollView):

    def __init__(self, store, on_transferred, **kwargs):
        super().__init__(**kwargs)
        self.store = store
        self.on_transferred = on_transferred
        self.goals_home = 0
        self.goals_away = 0

        box = vertical_scroll_box()
        self.add_widget(box)

        choices = team_choices(store.teams)

        titles = BoxLayout(size_hint_y=None, height=dp(30))
        titles.add_widget(make_label("Home", bold=True))
        titles.add_widget(Label(size_hint_x=None, width=dp(36)))
        titles.add_widget(make_label("Away", bold=True))
        box.add_widget(titles)

        select = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        self.sp_home = Spinner(text=choices[0], values=choices)
        self.sp_away = Spinner(text=choices[1], values=choices)
        select.add_widget(self.sp_home)
        select.add_widget(Label(text="vs", size_hint_x=None, width=dp(30)))
        select.add_widget(self.sp_away)
        box.add_widget(select)

        box.add_widget(make_label("Angriff", bold=True))
        self.ent_off_home = num_input("0", COLOR_OFF)
        self.ent_off_away = num_input("0", COLOR_OFF)
        box.add_widget(self._pair_row(self.ent_off_home, self.ent_off_away))

        box.add_widget(make_label("Verteidigung", bold=True))
        self.ent_def_home = num_input("0", COLOR_DEF)
        self.ent_def_away = num_input("0", COLOR_DEF)
        box.add_widget(self._pair_row(self.ent_def_home, self.ent_def_away))

        box.add_widget(make_label("Basis WP", bold=True))
        self.lbl_wp_vals = make_label("0.0 : 0.0")
        box.add_widget(self.lbl_wp_vals)

        self.btn_game = red_button("Spiel")
        self.btn_game.bind(on_release=self.game_liga)
        box.add_widget(self.btn_game)

        box.add_widget(make_label("Endresultat", bold=True))
        self.lbl_final_res = make_label("x : x", bold=True, font_size=sp(34))
        box.add_widget(self.lbl_final_res)
        self.lbl_hometeam_reward = make_label("")
        self.lbl_winning_reward = make_label("")
        box.add_widget(self.lbl_hometeam_reward)
        box.add_widget(self.lbl_winning_reward)

        self.btn_transfer = Button(text="Transfer", size_hint_y=None, height=dp(52),
                                   disabled=True)
        self.btn_transfer.bind(on_release=self.transfer_results)
        box.add_widget(self.btn_transfer)
        self.lbl_status = make_label("")
        box.add_widget(self.lbl_status)

        self._refresh_wp()
        for widget in (self.sp_home, self.sp_away):
            widget.bind(text=self._on_input_changed)
        for widget in (self.ent_off_home, self.ent_off_away,
                       self.ent_def_home, self.ent_def_away):
            widget.bind(text=self._on_input_changed)

    @staticmethod
    def _pair_row(left, right):
        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        row.add_widget(left)
        row.add_widget(Label(text=":", size_hint_x=None, width=dp(24)))
        row.add_widget(right)
        return row

    # --- Teams / Anzeige

    def _ids(self):
        return choice_index(self.sp_home.text), choice_index(self.sp_away.text)

    def _refresh_wp(self):
        h, a = self._ids()
        self.lbl_wp_vals.text = "%s : %s" % (self.store.teams[h].wp, self.store.teams[a].wp)

    def _clear_result(self):
        self.goals_home = 0
        self.goals_away = 0
        self.lbl_final_res.text = "x : x"
        self.lbl_hometeam_reward.text = ""
        self.lbl_winning_reward.text = ""
        self.lbl_status.text = ""
        self.btn_transfer.disabled = True

    def _on_input_changed(self, *_):
        self._refresh_wp()
        self._clear_result()

    def refresh_teams(self):
        """Nach 'Update' im Teams-Tab: Namen/WP neu anzeigen, Auswahl beibehalten."""
        h, a = self._ids()
        choices = team_choices(self.store.teams)
        self.sp_home.values = choices
        self.sp_away.values = choices
        self.sp_home.text = choices[h]
        self.sp_away.text = choices[a]
        self._refresh_wp()

    # --- Aktionen

    def game_liga(self, *_):
        h, a = self._ids()
        if h == a:
            self._clear_result()
            self.lbl_status.text = "Bitte zwei verschiedene Teams wählen."
            return

        home, away = self.store.teams[h], self.store.teams[a]
        self.goals_home, self.goals_away = compute_match(
            to_float(self.ent_off_home.text), to_float(self.ent_def_home.text),
            to_float(self.ent_off_away.text), to_float(self.ent_def_away.text),
            home.wp, away.wp,
        )

        self.lbl_final_res.text = "%d : %d" % (int(self.goals_home), int(self.goals_away))
        self.lbl_hometeam_reward.text = "Stadion Einnahmen für %s: ND$ %.1fM" % (
            home.team_name, home.nd / 1e6)

        if self.goals_home > self.goals_away:
            self.lbl_winning_reward.text = "HEIMSIEG - %s erhält ND$ 2M von %s" % (
                home.team_name, away.team_name)
        elif self.goals_home < self.goals_away:
            self.lbl_winning_reward.text = "AUSWÄRTSSIEG - %s erhält ND$ 2M von %s" % (
                away.team_name, home.team_name)
        else:
            self.lbl_winning_reward.text = "UNENTSCHIEDEN"

        self.lbl_status.text = ""
        self.btn_transfer.disabled = False

    def transfer_results(self, *_):
        h, a = self._ids()
        if h == a:
            return
        self.store.teams[h].update_season_stats(self.goals_home, self.goals_away)
        self.store.teams[a].update_season_stats(self.goals_away, self.goals_home)
        self.store.save()
        # Doppeltes Übertragen verhindern (auf dem Touchscreen schnell passiert)
        self.btn_transfer.disabled = True
        self.lbl_status.text = "Ergebnis in die Meisterschaft übertragen."
        self.on_transferred()


# ---------------------------------------------------------------- Teams

class TeamsTab(ScrollView):

    def __init__(self, store, on_update, **kwargs):
        super().__init__(**kwargs)
        self.store = store
        self.on_update = on_update

        box = vertical_scroll_box()
        self.add_widget(box)

        self.ent_wp, self.ent_nd, self.ent_name = [], [], []

        for i, team in enumerate(store.teams):
            box.add_widget(make_label("P%d" % (i + 1), bold=True, halign="left"))

            grid = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
            grid.bind(minimum_height=grid.setter("height"))

            wp = num_input(fmt_num(team.wp), COLOR_WP)
            nd = num_input(fmt_num(team.nd), COLOR_ND)
            name = text_input(team.team_name)
            self.ent_wp.append(wp)
            self.ent_nd.append(nd)
            self.ent_name.append(name)

            for caption, widget in (("WP", wp), ("ND$", nd), ("Name", name)):
                lbl = Label(text=caption, size_hint_x=0.25, size_hint_y=None, height=dp(48))
                grid.add_widget(lbl)
                grid.add_widget(widget)
            box.add_widget(grid)

        btn = red_button("Update")
        btn.bind(on_release=self.update_team_vals)
        box.add_widget(btn)
        self.lbl_status = make_label("")
        box.add_widget(self.lbl_status)

    def update_team_vals(self, *_):
        for i, team in enumerate(self.store.teams):
            team.update_wp(to_float(self.ent_wp[i].text))
            team.update_nd(to_float(self.ent_nd[i].text))
            name = self.ent_name[i].text.strip() or ("Team %d" % (i + 1))
            team.update_team_name(name)
        self.store.save()
        self.lbl_status.text = "Gespeichert."
        self.on_update()


# ---------------------------------------------------------------- Meisterschaft

class StandingsTab(BoxLayout):

    def __init__(self, store, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(10), padding=dp(12), **kwargs)
        self.store = store

        scroll = ScrollView()
        self.table = GridLayout(cols=3, spacing=dp(4), size_hint_y=None,
                                row_default_height=dp(40), row_force_default=True)
        self.table.bind(minimum_height=self.table.setter("height"))
        scroll.add_widget(self.table)
        self.add_widget(scroll)

        btn = Button(text="Saison zurücksetzen", size_hint_y=None, height=dp(52))
        btn.bind(on_release=self.confirm_reset)
        self.add_widget(btn)

        self.refresh()

    def refresh(self):
        self.table.clear_widgets()
        self.table.add_widget(cell("#", width=dp(40), bold=True))
        self.table.add_widget(cell("Team", halign="left", bold=True))
        self.table.add_widget(cell("Punkte", width=dp(80), bold=True))

        ranked = sorted(self.store.teams, key=lambda t: t.punkte, reverse=True)
        for rank, team in enumerate(ranked, start=1):
            self.table.add_widget(cell(str(rank), width=dp(40)))
            self.table.add_widget(cell(team.team_name, halign="left"))
            self.table.add_widget(cell(str(team.punkte), width=dp(80)))

    def confirm_reset(self, *_):
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        question = Label(text="Alle Punkte wirklich auf 0 setzen?", halign="center")
        question.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        content.add_widget(question)
        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        yes = Button(text="Ja")
        no = Button(text="Abbrechen")
        buttons.add_widget(yes)
        buttons.add_widget(no)
        content.add_widget(buttons)

        popup = Popup(title="Saison zurücksetzen", content=content,
                      size_hint=(0.85, 0.4), auto_dismiss=False)

        def do_reset(*_):
            for team in self.store.teams:
                team.reset_season_stats()
            self.store.save()
            self.refresh()
            popup.dismiss()

        yes.bind(on_release=do_reset)
        no.bind(on_release=popup.dismiss)
        popup.open()


# ---------------------------------------------------------------- App

class FCRuniApp(App):

    title = "FC Runi App"

    def build(self):
        # Tastatur soll die Eingabefelder nicht verdecken
        Window.softinput_mode = "below_target"

        self.store = Store(os.path.join(self.user_data_dir, "teams.json"))
        self.store.load()

        self.matchday = MatchdayTab(self.store, on_transferred=self._on_transferred)
        self.teams_tab = TeamsTab(self.store, on_update=self._on_teams_updated)
        self.standings = StandingsTab(self.store)

        self.screens = ScreenManager(transition=NoTransition())
        for name, widget in (("matchday", self.matchday), ("teams", self.teams_tab),
                             ("standings", self.standings)):
            screen = Screen(name=name)
            screen.add_widget(widget)
            self.screens.add_widget(screen)

        nav = BoxLayout(size_hint_y=None, height=dp(52))
        for idx, (name, text) in enumerate((("matchday", "Spieltag"), ("teams", "Teams"),
                                            ("standings", "Meisterschaft"))):
            btn = ToggleButton(text=text, group="nav", allow_no_selection=False,
                               state="down" if idx == 0 else "normal")
            btn.bind(on_press=lambda inst, n=name: self._show(n))
            nav.add_widget(btn)

        root = BoxLayout(orientation="vertical")
        root.add_widget(self.screens)
        root.add_widget(nav)
        return root

    def _show(self, name):
        if name == "standings":
            self.standings.refresh()
        self.screens.current = name

    def _on_transferred(self):
        self.standings.refresh()

    def _on_teams_updated(self):
        self.matchday.refresh_teams()
        self.standings.refresh()

    def on_pause(self):
        self.store.save()
        return True  # App bleibt im Hintergrund erhalten (Android)

    def on_stop(self):
        self.store.save()


if __name__ == "__main__":
    FCRuniApp().run()
