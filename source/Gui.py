import tkinter as tk
import tkinter.ttk

class MainApplication(tk.Frame):

    def __init__(self, parent, Teams, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.title("FC Runi App")

        self.Teams = Teams

        self.make_tabs()

        self.make_tab_matchday()
        self.make_tab_teams()

        self.goals_final_hometeam = 0
        self.goals_final_awayteam = 0

    def make_tabs(self):

        tab_control = tk.ttk.Notebook(master=self.parent)

        self.tab1 = tk.Frame(tab_control) # tab matchday
        self.tab2 = tk.Frame(tab_control)
        self.tab3 = tk.Frame(tab_control)
        self.tab4 = tk.Frame(tab_control)

        tab_control.add(self.tab1, text='Spieltag')
        tab_control.add(self.tab2, text='Teams')
        tab_control.add(self.tab3, text='Meisterschaft')
        tab_control.add(self.tab4, text='Einstellungen')

        tab_control.pack(expand=1, fill='both')

    def make_tab_teams(self):

        frm_teams_top = tk.Frame(master=self.tab2)
        frm_teams_bot = tk.Frame(master=self.tab2)

        frm_teams = []

        frm_teams_wp = []
        frm_teams_nd = []
        frm_teams_name = []

        self.ent_teams_wp = [] # wurfelpunkte
        self.ent_teams_nd = [] # nilpferd dollar for teams
        self.ent_teams_names = []  # nilpferd dollar for teams

        for i in range(6):
            frm_teams.append(tk.Frame(master=frm_teams_top))

            tk.Label(master=frm_teams[i], text="P"+str(i+1)).pack()

            frm_teams_wp.append(tk.Frame(master=frm_teams[i]))
            tk.Label(master=frm_teams_wp[i], text="WP  ").grid(row=0, column=0)
            self.ent_teams_wp.append(tk.Entry(master=frm_teams_wp[i], width=2, background="yellow", foreground="black",
                                     relief=tk.RIDGE, borderwidth=3))

            self.ent_teams_wp[i].insert("end", '0')
            self.ent_teams_wp[i].grid(row=0, column=1)

            frm_teams_nd.append(tk.Frame(master=frm_teams[i]))
            tk.Label(master=frm_teams_nd[i], text="ND$ ").grid(row=0, column=0)
            self.ent_teams_nd.append(tk.Entry(master=frm_teams_nd[i], width=10, background="orange", foreground="black",
                                     relief=tk.RIDGE, borderwidth=3))
            self.ent_teams_nd[i].insert("end", '1e5')
            self.ent_teams_nd[i].grid(row=0, column=1)

            frm_teams_name.append(tk.Frame(master=frm_teams[i]))
            tk.Label(master=frm_teams_name[i], text="#   ").grid(row=0, column=0)
            self.ent_teams_names.append(tk.Entry(master=frm_teams_name[i], width=15, background="white", foreground="black",
                                     relief=tk.RIDGE, borderwidth=3))
            self.ent_teams_names[i].insert("end", "Team "+str(i+1))
            self.ent_teams_names[i].grid(row=0, column=1)


            frm_teams_wp[i].pack(padx=12,pady=10, anchor="w")
            frm_teams_nd[i].pack(padx=12, pady=5, anchor="w")
            frm_teams_name[i].pack(padx=12, pady=5, anchor="w")

            frm_teams[i].grid(row=i//3, column=i%3, padx=10, pady=10)

        frm_teams_top.pack()

        self.btn_team_update = tk.Button(master=frm_teams_bot,
            relief=tk.RAISED,
            borderwidth=5,
            text="Update",
            command=self.update_team_vals,  # <--- Add this line
            background="red",
            fg="white",
        ).pack(pady=15)

        frm_teams_bot.pack()

    def make_tab_matchday(self):

        # top block for entering data
        self.frm_top_block = tk.Frame(master=self.tab1)
        self.make_matchday_top_block()
        self.frm_top_block.grid(row=0, column=0, padx=20)  # placing

        seperator = tk.ttk.Separator(master=self.tab1, orient="horizontal")
        seperator.grid(row=1, column=0, sticky="ew", pady=10)

        # bottom block for output (final result, points, who pays to who)
        self.frm_bot_block = tk.Frame(master=self.tab1)
        self.make_matchday_bottom_block()
        self.frm_bot_block.grid(row=2, column=0, padx=10, pady=10)

    def make_matchday_bottom_block(self):

        tk.Label(master=self.frm_bot_block, text="Endresultat").pack()
        self.lbl_final_res = tk.Label(master=self.frm_bot_block, text="x : x", background="white", foreground="red", borderwidth=4) #, font=('Helvetica', 14, 'bold'))
        self.lbl_final_res.pack(pady=3)

        self.lbl_hometeam_reward = tk.Label(master=self.frm_bot_block, text="")
        self.lbl_winning_reward = tk.Label(master=self.frm_bot_block, text="")

        self.lbl_final_res.pack(pady=5)
        self.lbl_hometeam_reward.pack(pady=5)
        self.lbl_winning_reward.pack(pady=5)

        btn_transfer_results = tk.Button(master=self.frm_bot_block,
            relief=tk.RAISED,
            borderwidth=5,
            text="Transfer",
            command=self.transfer_results_to_teams_stats,
            fg="black",
        )

        btn_transfer_results.pack(pady=10)


    def make_matchday_top_block(self):

        frm_home_block = tk.Frame(master=self.frm_top_block)
        frm_resu_block = tk.Frame(master=self.frm_top_block)
        frm_away_block = tk.Frame(master=self.frm_top_block)

        frm_home_block.grid(row=0, column=0, padx=20)  # placing
        frm_resu_block.grid(row=0, column=1, padx=20)  # placing
        frm_away_block.grid(row=0, column=2, padx=20)  # placing

        # Blocks for home and away (left and right blocks
        lbl_home_block_title = tk.Label(master=frm_home_block, text="Home").pack(pady=10)
        lbl_away_block_title = tk.Label(master=frm_away_block, text="Away").pack(pady=10)

        # https://www.tutorialspoint.com/python/tk_radiobutton.htm

        self.rbt_home = []
        self.rbt_away = []

        self.varhome = tk.IntVar()
        self.varaway = tk.IntVar()

        for i in range(6):
            self.rbt_home.append(
                tk.Radiobutton(master=frm_home_block, text=" P" + str(i + 1), value=i, variable=self.varhome,
                               command=self.update_team_vals_game))  # variable=var, value=1, command=sel)
            self.rbt_home[i].pack(pady=3)
            self.rbt_away.append(
                tk.Radiobutton(master=frm_away_block, text=" P" + str(i + 1), value=i, variable=self.varaway,
                               command=self.update_team_vals_game))
            self.rbt_away[i].pack(pady=3)

        self.lbl_home_block_teamname = tk.Label(master=frm_home_block, text="HOME")
        self.lbl_home_block_teamname.pack(pady=10)
        self.lbl_away_block_teamname = tk.Label(master=frm_away_block, text="AWAY")
        self.lbl_away_block_teamname.pack(pady=10)

        # Central blocks for entering results

        # Offense
        frm_offence = tk.Frame(master=frm_resu_block)
        frm_offence.pack(pady=10)

        lbl_offence = tk.Label(master=frm_offence, text="Angriff")
        frm_off_ent = tk.Frame(master=frm_offence)
        lbl_offence.pack(pady=3)
        frm_off_ent.pack()

        self.ent_off_home = tk.Entry(master=frm_off_ent, width=2, background="blue", foreground="white",
                                    relief=tk.RIDGE, borderwidth=3)

        self.ent_off_home.insert(-1, '0')

        lbl_off_ent = tk.Label(master=frm_off_ent, text=":")
        self.ent_off_away = tk.Entry(master=frm_off_ent, width=2, background="blue", foreground="white",
                                    relief=tk.RIDGE, borderwidth=3)

        self.ent_off_away.insert(-1, '0')

        self.ent_off_home.grid(row=0, column=0, sticky="e")
        lbl_off_ent.grid(row=0, column=1, sticky="e")
        self.ent_off_away.grid(row=0, column=2, sticky="e")

        # Defence
        frm_defence = tk.Frame(master=frm_resu_block)
        frm_defence.pack(pady=10)

        lbl_defence = tk.Label(master=frm_defence, text="Verteidigung")
        frm_def_ent = tk.Frame(master=frm_defence)
        lbl_defence.pack(pady=3)
        frm_def_ent.pack()

        self.ent_def_home = tk.Entry(master=frm_def_ent, width=2, background="green", foreground="white",
                                    relief=tk.RIDGE, borderwidth=3)
        self.ent_def_home.insert(-1, '0')
        lbl_def_ent = tk.Label(master=frm_def_ent, text=":")
        self.ent_def_away = tk.Entry(master=frm_def_ent, width=2, background="green", foreground="white",
                                    relief=tk.RIDGE, borderwidth=3)
        self.ent_def_away.insert(-1, '0')

        self.ent_def_home.grid(row=0, column=0, sticky="e")
        lbl_def_ent.grid(row=0, column=1, sticky="e")
        self.ent_def_away.grid(row=0, column=2, sticky="e")

        # WP transfer

        frm_wp = tk.Frame(master=frm_resu_block)
        frm_wp.pack(pady=10)

        lbl_wp = tk.Label(master=frm_wp, text="Basis WP").pack(pady=3)
        self.lbl_wp_vals = tk.Label(master=frm_wp, text="0.0 : 0.0")
        self.lbl_wp_vals.pack()

        # Button spiel

        btn_spiel = tk.Button(master=frm_resu_block,
            relief=tk.RAISED,
            borderwidth=5,
            text="Spiel",
            command=self.game_liga,
            background="red",
            fg="white",
        )

        btn_spiel.pack(pady=10)

    def game_liga(self):

        home_team_id = self.varhome.get()
        away_team_id = self.varaway.get()
        wp_home = self.Teams[home_team_id].wp
        wp_away = self.Teams[away_team_id].wp

        offence_home = float(self.ent_off_home.get()) + wp_home
        offence_away = float(self.ent_off_away.get()) + wp_away

        defence_home = float(self.ent_def_home.get()) + wp_home
        defence_away = float(self.ent_def_away.get()) + wp_away

        netto_home = offence_home - defence_away
        netto_away = offence_away - defence_home

        if netto_home < 0:
            netto_home = 0

        if netto_away < 0:
            netto_away = 0

        self.goals_final_hometeam = netto_home
        self.goals_final_awayteam = netto_away

        self.lbl_final_res["text"] = f"{int(netto_home)}" + " : " + f"{int(netto_away)}"

        teamname_home = self.Teams[home_team_id].team_name
        teamname_away = self.Teams[away_team_id].team_name

        nd_reward_home = self.Teams[home_team_id].nd

        self.lbl_hometeam_reward["text"] = "Stadion Einnahmen für " + teamname_home + ": ND$ " + "{:.1f}".format(nd_reward_home/1e6) + 'M'

        if netto_home > netto_away:
            self.lbl_winning_reward["text"] = "HEIMSIEG - " + teamname_home + " erhält ND$ 2M von " + teamname_away
        elif netto_home < netto_away:
            self.lbl_winning_reward["text"] = "AUSWÄRTSSIEG - " + teamname_away + " erhält ND$ 2M von " + teamname_home
        else:
            self.lbl_winning_reward["text"] = "UNENTSCHIEDEN"

    def update_team_vals(self):

        for i in range(6):
            current_wp = float((self.ent_teams_wp[i]).get())
            current_nd = float((self.ent_teams_nd[i]).get())
            current_name = self.ent_teams_names[i].get()

            self.Teams[i].update_wp(current_wp)
            self.Teams[i].update_nd(current_nd)
            self.Teams[i].update_team_name(current_name)

        self.update_team_vals_game()

    def update_team_vals_game(self):

        home_team_id = self.varhome.get()
        away_team_id = self.varaway.get()
        self.lbl_wp_vals["text"] = str(self.Teams[home_team_id].wp)+" : "+str(self.Teams[away_team_id].wp)

        self.lbl_home_block_teamname["text"] = self.Teams[home_team_id].team_name
        self.lbl_away_block_teamname["text"] = self.Teams[away_team_id].team_name

    def transfer_results_to_teams_stats(self):

        home_team_id = self.varhome.get()
        away_team_id = self.varaway.get()

        self.Teams[home_team_id].update_season_stats(self.goals_final_hometeam, self.goals_final_awayteam)
        self.Teams[away_team_id].update_season_stats(self.goals_final_awayteam, self.goals_final_hometeam)

# if __name__ == "__main__":
#
#     Teams_Objects = []
#     for i in range(6):
#         Teams_obj = Teams_Total_Vals.Teams_Total_Vals()
#         Teams_Objects.append(Teams_obj)
#
#     root = tk.Tk()
#     MainApplication(root, Teams_Objects).pack(side="top", fill="both", expand=True)
#
#     root.mainloop()