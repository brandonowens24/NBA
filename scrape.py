import mysql.connector
from datetime import datetime, timedelta
from threading import Thread
import pandas as pd
import os
import requests
import time, datetime
from bs4 import BeautifulSoup
import random
import numpy as np
import re


# Base for Scraper
class Scraper:
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        self.conn = conn
        self.season = season
        self.cursor = cursor
        self.date = date
        self.request_counter = request_counter
        self.yesterday_date = yesterday_date

    def fetch_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Scraper Class: Request Error")
            return None
    
    def make_web_request(self, url):
        if self.request_counter > 18:
            time.sleep(60)
            self.request_counter = 1
        time.sleep(1)
        response = url
        return response
        
    def query_call(self, values, columns, table, constraint):
        query = f'''INSERT INTO {table} ({', '.join(columns)})
                    VALUES ({', '.join(['?'] * len(columns))})
                    ON CONFLICT ({constraint}, season) DO UPDATE
                    SET
                    {', '.join([f"{column} = EXCLUDED.{column}" for column in columns[2:]])};'''
        try:
            self.cursor.execute(query, values)           
            self.conn.commit()
        except:
            print("Error: Scraper Class Couldn't Input Data")
    
# Class Obtaining Current
class TeamScraper(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, season, cursor, None, None, None)

    def parse_page(self, html):    
        tables = pd.read_html(html)
        if tables:
            wiki_df = pd.DataFrame(tables[0])
            wiki_df.columns = wiki_df.iloc[0]
            wiki_df = wiki_df.drop(0)
            wiki_df = wiki_df.reset_index(drop=True)
            return wiki_df
        else:
            print("TeamScraper: parse_page Error - Could Not Grab Current NBA teams.")

    def update_table(self):
        url = 'https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations'
        html = self.fetch_page(url)
        if html:
            wiki_df = self.parse_page(html)
            self.cursor.execute("SELECT team_name FROM teams WHERE season=?", (self.season,))
            teams = self.cursor.fetchall()
            for index,row in wiki_df.iterrows():
                try:
                    abbreviation = row['Abbreviation/ Acronym']
                    franchise = row['Franchise']

                    if franchise not in teams:
                        self.cursor.execute("INSERT OR IGNORE INTO teams (abbreviation, team_name, season) VALUES (?, ?, ?)", (abbreviation, franchise, self.season))
                    self.conn.commit()
                except:
                    print("TeamScraper: update_table Error - HTML found, Could Not Update Current NBA teams")
        elif not html:
            print("TeamScraper: update_table Error - HTML not found.")

# Class Showing Injuriese For Today
class InjuredPlayers(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, None, cursor, None, date, None)

    def update_table(self):
        self.cursor.execute("DELETE FROM injury_report")
        url = 'https://www.espn.com/nba/injuries'
        tables = pd.read_html(url)
        if not tables:
            print("InjuredPlayers: update_table Error - Could Not Find Tables of Injured Players")
            return
        if tables:
            amt = len(tables)
            for i in range(0, amt):
                df = tables[i]
                for index, row in df.iterrows():
                    try:
                        name = row['NAME']
                        status = row['STATUS']
                        if status in ('Out', 'Doubtful'):
                            self.cursor.execute("INSERT OR IGNORE INTO injury_report (date, player_name, description) VALUES (?, ?, ?)", (self.date, name, status))
                        self.conn.commit()
                    except:
                        print("InjuredPlayers: update_table Error - Tables of Injured Players Found - Could Not Insert Findings")

# Updates Referee Statistics For the Previous and Current Seasons
class RefStats(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, season, cursor, None, date, request_counter)

    def parse_page(self, url):
        tables = pd.read_html(url)
        if not tables:
                print("RefStats: parse_page Error - Ref Stats Not Found")
                return None
        return tables
    
    def update_table(self):
        for season in range ((self.season - 1), (self.season + 1)):
            url = f'https://www.basketball-reference.com/referees/{season}_register.html'
            try:
                url = self.make_web_request(url)
                df = pd.DataFrame(self.parse_page(url)[0])
            except:
                break
            try:
                for index, row in df.iterrows():
                    official = row['Unnamed: 0_level_0']['Referee']
                    G = row['Unnamed: 2_level_0']['G']
                    FGA = row['Per Game']['FGA']
                    FTA = row['Per Game']['FTA'] 
                    PF = row['Per Game']['PF'] 
                    PTS = row['Per Game']['PTS']
                    FGA_pgrel = row['Per Game Relative']['FGA'] 
                    FTA_pgrel = row['Per Game Relative']['FTA'] 
                    PF_pgrel = row['Per Game Relative']['PF'] 
                    PTS_pgrel = row['Per Game Relative']['PTS'] 
                    home_win_loss = row['Home Teams']['W/L%'] 
                    home_FGA = row['Home Teams']['FGA'] 
                    home_FTA = row['Home Teams']['FTA']  
                    home_PF = row['Home Teams']['PF'] 
                    home_PTS = row['Home Teams']['PTS'] 
                    away_win_loss = row['Visitor Teams']['W/L%'] 
                    away_FGA = row['Visitor Teams']['FGA'] 
                    away_FTA = row['Visitor Teams']['FTA'] 
                    away_PF = row['Visitor Teams']['PF']
                    away_PTS = row['Visitor Teams']['PTS'] 
                    win_loss_hvrel = row['Relative to Average*']['W/L%']
                    FGA_hvrel = row['Relative to Average*']['FGA'] 
                    FTA_hvrel = row['Relative to Average*']['FTA'] 
                    PF_hvrel = row['Relative to Average*']['PF']
                    PTS_hvrel = row['Relative to Average*']['PTS']

                    values = [official, season, G, FGA, FTA, PF, PTS, FGA_pgrel, FTA_pgrel, PF_pgrel, PTS_pgrel, home_win_loss, home_FGA, home_FTA, home_PF, home_PTS,
                        away_win_loss, away_FGA, away_FTA, away_PF, away_PTS, win_loss_hvrel, FGA_hvrel, FTA_hvrel, PF_hvrel, PTS_hvrel]
                    columns =["official", "season", "G", "FGA", "FTA", "PF", "PTS", "FGA_pgrel", "FTA_pgrel", "PF_pgrel", "PTS_pgrel", "home_win_loss", "home_FGA", "home_FTA", "home_PF", "home_PTS", "away_win_loss", "away_FGA", "away_FTA", "away_PF", "away_PTS", "win_loss_hvrel", "FGA_hvrel", "FTA_hvrel", "PF_hvrel", "PTS_hvrel"]
                    self.query_call(values, columns, table="officiating", constraint="official")
            except ValueError:
                print("RefStats: update_table Error - Ref Stats Found, Could Not Be Inserted")
                pass

# Updates Player Statistics For the Current Season
class PlayerStats(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, season, cursor, None, None, None)

    def parse_page(self, url):
        tables = pd.read_html(url)
        if not tables:
            print("PlayerStats: parse_page Error: Player Stats WebPage Non Existent")
            return None
        return tables
    
    def update_table(self):
        for season in range ((self.season), (self.season + 1)):
            for page in range(1, 10): 
                url = f'https://basketball.realgm.com/nba/stats/{season}/Averages/All/player/All/desc/{page}/Regular_Season'
                try:
                    tables = pd.read_html(url)
                    df = pd.DataFrame(tables[-1])
                except:
                    print("PlayerStats: update_table Error - No Further Player Stats To Report")
                    break
                if df is not None:
                    try:
                        for index, row in df.iterrows():
                            player_name = row['Player']
                            team_tag = row['Team']
                            GP = row['GP']
                            MPG = row['MPG']
                            PPG = row['PPG']
                            FGM = row['FGM']
                            FGA = row['FGA']
                            FGp = row['FG%']
                            ThreePM = row['3PM']
                            ThreePA = row['3PA']
                            ThreePp = row['3P%']
                            FTM = row['FTM']
                            FTA = row['FTA']
                            FTp = row['FT%']
                            ORB = row['ORB']
                            DRB = row['DRB']
                            RPG = row['RPG']
                            APG = row['APG']
                            SPG = row['SPG']
                            BPG = row['BPG']
                            TOV = row['TOV']
                            PF = row['PF']
                            
                            values = [player_name, season, team_tag, GP, MPG, PPG, FGM, FGA, FGp, ThreePM, ThreePA, ThreePp, FTM, FTA, FTp, ORB, DRB, RPG, APG, SPG, BPG, TOV, PF]
                            columns = ["player_name", "season", "team_tag", "GP", "MPG", "PPG", "FGM", "FGA", "FGp", "ThreePM", "ThreePA", "ThreePp", "FTM", "FTA", "FTp", "ORB", "DRB", "RPG", "APG", "SPG", "BPG", "TOV", "PF"]
                            self.query_call(values, columns, table="player_stats", constraint="player_name")
                    except ValueError:
                        print("PlayerStats: update_table Error - Player Stats Found - Could Not Be Inserted")
                        continue

            for page in range(1, 10): #Misc Stats
                url = f'https://basketball.realgm.com/nba/stats/{season}/Misc_Stats/All/player/All/desc/{page}/Regular_Season'
                try:
                    tables = pd.read_html(url)
                    df = pd.DataFrame(tables[-1])
                except:
                    print("PlayerStats: update_table Error - No Further Player Stats To Report")
                    break
                if df is not None:
                    try:
                        for index, row in df.iterrows():
                            player_name = row['Player']
                            DblDbl = row['Dbl Dbl']
                            TrpDbl = row['Tpl Dbl']
                            FortyBomb = row['40 Pts']
                            TwentyReb = row['20 Reb']
                            TwentyAst = row['20 Ast']
                            FiveStl = row['5 Stl']
                            FiveBlk = row['5 Blk']
                            High = row['High Game']
                            HandsOnBuckets = row['HOB']
                            AstToTovR = row['Ast/TO']
                            StlToTovR = row['Stl/TO']
                            FTFGAp = row['FT/FGA']
                            TeamW = row["W's"]
                            TeamL = row["L's"]
                            TeamWp = row['Win %']
                            OWS = row['OWS']
                            DWS = row['DWS']
                            WS = row['WS']
                            
                            values = [player_name, season, DblDbl, TrpDbl, FortyBomb, TwentyReb, TwentyAst, FiveStl, FiveBlk, High, HandsOnBuckets, AstToTovR, StlToTovR, FTFGAp, TeamW, TeamL, TeamWp, OWS, DWS, WS]
                            columns = ["player_name", "season", "DblDbl", "TrpDbl", "FortyBomb", "TwentyReb", "TwentyAst", "FiveStl", "FiveBlk", "High", "HandsOnBuckets", "AstToTovR", "StlToTovR", "FTFGAp", "TeamW", "TeamL", "TeamWp", "OWS", "DWS", "WS"]
                            self.query_call(values, columns, table="player_stats", constraint="player_name")
                    except ValueError:
                        print("PlayerStats: update_table Error - Player Stats Found - Could Not Be Inserted")
                        continue

            for page in range(1, 10): #Adv Stats
                url = f'https://basketball.realgm.com/nba/stats/{season}/Advanced_Stats/All/player/All/desc/{page}/Regular_Season'
                try:
                    tables = pd.read_html(url)
                    df = pd.DataFrame(tables[-1])
                except:
                    print("PlayerStats: update_table Error - No Further Player Stats To Report")
                    break
                if df is not None:
                    try:
                        for index, row in df.iterrows():
                            player_name = row['Player']
                            TS = row['TS%']
                            eFG = row['eFG%']
                            TotalSp = row['Total S %']
                            ORBp = row['ORB%']
                            DRBp = row['DRB%']
                            TRBp = row['TRB%']
                            ASTp = row['AST%']
                            TOVp = row['TOV%']
                            STLp = row['STL%']
                            BLKp = row['BLK%']
                            USG = row['USG%']
                            PPR = row['PPR']
                            PPS = row['PPS']
                            ORtg = row['ORtg']
                            DRtg = row['DRtg']
                            eDiff = row['eDiff']
                            FIC = row['FIC']
                            PER = row['PER']
                            
        
                            values = [player_name, season, TS, eFG, TotalSp, ORBp, DRBp, TRBp, ASTp, TOVp, STLp, BLKp, USG, PPR, PPS, ORtg, DRtg, eDiff, FIC, PER]
                            columns = ["player_name", "season", "TS", "eFG", "TotalSp", "ORBp", "DRBp", "TRBp", "ASTp", "TOVp", "STLp", "BLKp", "USG", "PPR", "PPS", "ORtg", "DRtg", "eDiff", "FIC", "PER"]
                            self.query_call(values, columns, table="player_stats", constraint="player_name")
                    except ValueError:
                        print("PlayerStats: update_table Error - Player Stats Found - Could Not Be Inserted")
                        continue

# Updates a Team Statistics For the Current Season
class TeamStats(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, season, cursor, None, None, request_counter)
    

    def update_table(self):
        for season in range ((self.season), (self.season + 1)):
            url = f'https://www.basketball-reference.com/leagues/NBA_{season}.html'
            try:
                url = self.make_web_request(url)
                tables = pd.read_html(url)
                if not tables:
                    print("TeamStats: update_table Error - Team Stats Not Found")
                    continue
                team_adv_df = tables[10]
                team_averages_df = tables[4]
                team_opp_averages_df = tables[5]
                team_shooting_stats_df = tables[12]
                
                # For Advanced Stats
                for index, row in team_adv_df.iterrows():
                    team_name = row['Unnamed: 1_level_0']['Team'].upper().replace('*', '')
                    if team_name == 'LEAGUE AVERAGE':
                        break 
                    age = row['Unnamed: 2_level_0']['Age']
                    W = row['Unnamed: 3_level_0']['W']
                    L = row['Unnamed: 4_level_0']['L']
                    MOV = row['Unnamed: 7_level_0']['MOV'] 
                    SOS = row['Unnamed: 8_level_0']['SOS']  
                    SRS = row['Unnamed: 9_level_0']['SRS']
                    ORtg = row['Unnamed: 10_level_0']['ORtg']
                    DRtg = row['Unnamed: 11_level_0']['DRtg'] 
                    NRtg = row['Unnamed: 12_level_0']['NRtg']
                    pace = row['Unnamed: 13_level_0']['Pace']
                    FTr = row['Unnamed: 14_level_0']['FTr']
                    ThreePAr = row['Unnamed: 15_level_0']['3PAr']
                    TSp = row['Unnamed: 16_level_0']['TS%']   
                    OeFG = row['Offense Four Factors']['eFG%']
                    OTOVp = row['Offense Four Factors']['TOV%']
                    ORBp = row['Offense Four Factors']['ORB%']
                    OFTFGAp = row['Offense Four Factors']['FT/FGA']
                    DeFG = row['Defense Four Factors']['eFG%']
                    DTOVp = row['Defense Four Factors']['TOV%']
                    DRBp = row['Defense Four Factors']['DRB%']
                    DFTFGAp = row['Defense Four Factors']['FT/FGA']

                    values = [team_name, season, age, W, L, MOV, SOS, SRS, ORtg, DRtg, NRtg, pace, FTr, ThreePAr, TSp, OeFG, OTOVp, ORBp, OFTFGAp, DeFG, DTOVp, DRBp, DFTFGAp]
                    columns = ["team_name", "season", "age", "W", "L", "MOV", "SOS", "SRS", "ORtg", "DRtg", "NRtg", "pace", "FTr", "ThreePAr", "TSp", "OeFG", "OTOVp", "ORBp", "OFTFGAp", "DeFG", "DTOVp", "DRBp", "DFTFGAp"]
                    self.query_call(values, columns, table="team_stats", constraint="team_name")

                # For Team Averages
                for index, row in team_averages_df.iterrows():
                    team_name = row['Team'].upper().replace('*', '')
                    if team_name == 'LEAGUE AVERAGE':
                        break 
                    G = row['G']
                    FG = row['FG']
                    FGA = row['FGA']
                    FGp = row['FG%']
                    ThreeP = row['3P']
                    ThreePA = row['3PA']
                    ThreePp = row['3P%']
                    TwoP = row['2P']
                    TwoPA = row['2PA']
                    TwoPp = row['2P%']
                    FT = row['FT']
                    FTA = row['FTA']
                    FTp = row['FT%']
                    ORB = row['ORB']
                    DRB = row['DRB']
                    TRB = row['TRB']
                    AST = row['AST']
                    STL = row['STL']
                    BLK = row['BLK']
                    TOV = row['TOV']
                    PF = row['PF']
                    PTS = row['PTS']

                    values = [team_name, season, G, FG, FGA, FGp, ThreeP, ThreePA, ThreePp, TwoP, TwoPA, TwoPp, FT, FTA, FTp, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS]
                    columns = ["team_name", "season", "G", "FG", "FGA", "FGp", "ThreeP", "ThreePA", "ThreePp", "TwoP", "TwoPA", "TwoPp", "FT", "FTA", "FTp", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
                    self.query_call(values, columns, table="team_stats", constraint="team_name")

                # For Team Opponents Averages
                for index, row in team_opp_averages_df.iterrows():
                    team_name = row['Team'].upper().replace('*', '')
                    if team_name == 'LEAGUE AVERAGE':
                        break 
                    oppG = row['G']
                    oppFG = row['FG']
                    oppFGA = row['FGA']
                    oppFGp = row['FG%']
                    oppThreeP = row['3P']
                    oppThreePA = row['3PA']
                    oppThreePp = row['3P%']
                    oppTwoP = row['2P']
                    oppTwoPA = row['2PA']
                    oppTwoPp = row['2P%']
                    oppFT = row['FT']
                    oppFTA = row['FTA']
                    oppFTp = row['FT%']
                    oppORB = row['ORB']
                    oppDRB = row['DRB']
                    oppTRB = row['TRB']
                    oppAST = row['AST']
                    oppSTL = row['STL']
                    oppBLK = row['BLK']
                    oppTOV = row['TOV']
                    oppPF = row['PF']
                    oppPTS = row['PTS']

                    values = [team_name, season, oppG, oppFG, oppFGA, oppFGp, oppThreeP, oppThreePA, oppThreePp, oppTwoP, oppTwoPA, oppTwoPp, oppFT, oppFTA, oppFTp, oppORB, oppDRB, oppTRB, oppAST, oppSTL, oppBLK, oppTOV, oppPF, oppPTS]
                    columns = ["team_name", "season", "oppG", "oppFG", "oppFGA", "oppFGp", "oppThreeP", "oppThreePA", "oppThreePp", "oppTwoP", "oppTwoPA", "oppTwoPp", "oppFT", "oppFTA", "oppFTp", "oppORB", "oppDRB", "oppTRB", "oppAST", "oppSTL", "oppBLK", "oppTOV", "oppPF", "oppPTS"]
                    self.query_call(values, columns, table="team_stats", constraint="team_name")

                # For Team Shooting Splits
                for index, row in team_shooting_stats_df.iterrows():
                    team_name = row['Unnamed: 1_level_0']['Team'].upper().replace('*', '')
                    if team_name == 'LEAGUE AVERAGE':
                        break 
                    avgD = row['Unnamed: 5_level_0']['Dist.']
                    pTwoP = row["% of FGA by Distance"]['2P']
                    pZeroToThree = row["% of FGA by Distance"]['0-3']
                    pThreeToTen = row["% of FGA by Distance"]['3-10']
                    pTenToSixteen = row["% of FGA by Distance"]['10-16']
                    pSixteenToThreeP = row["% of FGA by Distance"]['16-3P']
                    pDunksA = row["Dunks"]['%FGA']
                    pDunksM = row["Dunks"]["Md."]
                    TwoPointFGAst = row["% of FG Ast'd"]['2P']
                    ThreePointFGAst = row["% of FG Ast'd"]['3P']
                    FGpTwoP = row["FG% by Distance"]['2P']
                    FGpZeroToThreeP = row["FG% by Distance"]['0-3']
                    FGpThreeToTenP = row["FG% by Distance"]['3-10']
                    FGpTenToSixteenP = row["FG% by Distance"]['10-16']
                    FGpSixteenToThreeP = row["FG% by Distance"]['16-3P']
                    FGpThreeP = row["FG% by Distance"]['3P']

                    values = [team_name, season, avgD, pTwoP, pZeroToThree, pThreeToTen, pTenToSixteen, pSixteenToThreeP, pDunksA, pDunksM, TwoPointFGAst, ThreePointFGAst, FGpTwoP,
                              FGpZeroToThreeP, FGpThreeToTenP, FGpTenToSixteenP, FGpSixteenToThreeP, FGpThreeP]
                    columns = ["team_name", "season", "avgD", "pTwoP", "pZeroToThree", "pThreeToTen", "pTenToSixteen", "pSixteenToThreeP", "pDunksA", "pDunksM", "TwoPointFGAst", "ThreePointFGAst", "FGpTwoP", "FGpZeroToThreeP", "FGpThreeToTenP", "FGpTenToSixteenP", "FGpSixteenToThreeP", "FGpThreeP"]
                    self.query_call(values, columns, table="team_stats", constraint="team_name")
            except ValueError:
                print("TeamStats: update_table Error - Team Stats Found - Could Not Be Inserted")
                continue

# Checks Today's Games, Combines Ref Stats, Combines Injury Stats, Puts Into Box Score Table
class DBCompiler(Scraper):
    def __init__(self, conn, season, cursor, yesterday_date, date, request_counter):
        super().__init__(conn, season, cursor, yesterday_date, date, request_counter)

    def home_and_away(self):
        home_teams = []
        away_teams = []
        
        url = f'https://www.espn.com/nba/scoreboard/_/date/{self.date[:-1]}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("DBCompiler: home_and_away - No Games Found Today.")
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        teams = soup.find_all("div", class_="ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db")

        for i in range(len(teams)):
            team_name = teams[i].text.upper()
            if i % 2 == 1:
                home_teams.append(team_name)
            else:
                away_teams.append(team_name)
        #The home and away teams lists will line up. So home_teams[0] and away_teams[0] will be playing each other.
        return home_teams, away_teams
    
    def obtain_injury_accumulations(self, team_injuries):
        columns = [
                    "player_name", "season", "team_tag", "GP", "MPG", "PPG", "FGM", "FGA", "FGp", 
                    "ThreePM", "ThreePA", "ThreePp", "FTM", "FTA", "FTp", "ORB", "DRB", "RPG", 
                    "APG", "SPG", "BPG", "TOV", "PF", "DblDbl", "TrpDbl", "FortyBomb", "TwentyReb", 
                    "TwentyAst", "FiveStl", "FiveBlk", "High", "HandsOnBuckets", "AstToTovR", 
                    "StlToTovR", "FTFGAp", "TeamW", "TeamL", "TeamWp", "OWS", "DWS", "WS", "TS", 
                    "eFG", "TotalSp", "ORBp", "DRBp", "TRBp", "ASTp", "TOVp", "STLp", "BLKp", 
                    "USG", "PPR", "PPS", "ORtg", "DRtg", "eDiff", "FIC", "PER"]
        df = pd.DataFrame(team_injuries, columns=columns)
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
        df = df.groupby(['season']).agg(GP=("GP", "sum"),
                                                MPG = ("MPG", "mean"),
                                                PPG = ("PPG", "mean"),
                                                FGM = ("FGM", "sum"),
                                                FGA = ("FGA", "sum"),
                                                FGp = ("FGp", "mean"),
                                                ThreePM = ("ThreePM", "sum"),
                                                ThreePA = ("ThreePA", "sum"),
                                                ThreePp = ("ThreePp", "mean"),
                                                FTM = ("FTM", "sum"),
                                                FTA = ("FTA", "sum"),
                                                FTp = ("FTp", "mean"),
                                                ORB = ("ORB", "mean"),
                                                DRB = ("DRB", "mean"),
                                                RPG = ("RPG", "mean"),
                                                APG = ("APG", "mean"),
                                                SPG = ("SPG", "mean"),
                                                BPG = ("BPG", "mean"),
                                                TOV = ("TOV", "mean"),
                                                PF = ("PF", "mean"),
                                                DblDbl = ("DblDbl", "sum"),
                                                TrpDbl = ("TrpDbl", "sum"),
                                                FortyBomb = ("FortyBomb", "sum"),
                                                TwentyReb = ("TwentyReb", "sum"),
                                                TwentyAst = ("TwentyAst", "sum"),
                                                FiveStl = ("FiveStl", "sum"),
                                                FiveBlk = ("FiveBlk", "sum"),
                                                High= ("High", "sum"),
                                                HandsOnBuckets = ("HandsOnBuckets", "mean"),
                                                AstToTovR = ("AstToTovR", "mean"),
                                                StlToTovR = ("StlToTovR", "mean"),
                                                FTFGAp = ("FTFGAp", "mean"),
                                                TeamW = ("TeamW", "mean"),
                                                TeamL = ("TeamL", "mean"),
                                                TeamWp = ("TeamWp", "mean"),
                                                OWS = ("OWS", "mean"),
                                                DWS = ("DWS", "mean"),
                                                WS = ("WS", "mean"),
                                                TS = ("TS", "mean"),
                                                eFG = ("eFG", "mean"),
                                                TotalSp = ("TotalSp", "mean"),
                                                ORBp = ("ORBp", "mean"),
                                                DRBp = ("DRBp", "mean"),
                                                TRBp = ("TRBp", "mean"),
                                                ASTp = ("ASTp", "mean"),
                                                TOVp = ("TOVp", "mean"),
                                                STLp = ("STLp", "mean"),
                                                BLKp = ("BLKp", "mean"),
                                                USG = ("USG", "mean"),
                                                PPR = ("PPR", "mean"),
                                                PPS = ("PPS", "mean"),
                                                ORtg = ("ORtg", "mean"),
                                                DRtg = ("DRtg", "mean"),
                                                eDiff = ("eDiff", "mean"),
                                                FIC = ("FIC", "mean"),
                                                PER = ("PER", "mean")).reset_index()
        if not team_injuries:
            df = pd.DataFrame([[0] * (len(columns))], columns=columns)
            df = df.drop(columns=['player_name', 'team_tag'])
        del df['season']
        
        df = df.values.tolist()[0]

        return df

    def obtain_officials_accumulations(self, team):
        team = team.lower().title()
        url = 'https://official.nba.com/referee-assignments/'
        response = requests.get(url)
        if response.status_code != 200:
            print ("DBCompiler: obtain_officials_accumulations - Could Not Fetch Assigned Officials")
        soup = BeautifulSoup(response.content, "html.parser")
        refs_table = soup.find('div', class_='nba-refs-content')

        td_columns = refs_table.find_all('td') 
        data_dict = {}
        referee_names = []

        for i in range(0, len(td_columns), 5):
                key = td_columns[i].text.split('@ ', 1)[1]
                value1 = re.sub(r'\s+\(#[0-9]+\)', '', td_columns[i + 1].text.strip())
                value2 = re.sub(r'\s+\(#[0-9]+\)', '', td_columns[i + 2].text.strip())
                value3 = re.sub(r'\s+\(#[0-9]+\)', '', td_columns[i + 3].text.strip())

                data_dict[key] = value1, value2, value3

        for key, values in data_dict.items():
                key = re.sub(r'^[A-Za-z.]+ ', '', key) 
                if key in team:
                    referee_names = []
                    referee_names.append(values)
                    referee_names = list(referee_names[0])
                    self.cursor.execute("SELECT G, FGA, FTA, PF, PTS, FGA_pgrel, FTA_pgrel, PF_pgrel, PTS_pgrel, home_win_loss, home_FGA, home_FTA, home_PF, home_PTS, away_win_loss, away_FGA, away_FTA, away_PF, away_PTS, win_loss_hvrel, FGA_hvrel, FTA_hvrel, PF_hvrel, PTS_hvrel FROM officiating WHERE official IN ({})".format(', '.join(['?'] * len(referee_names))), referee_names)
                    official_stats = self.cursor.fetchall()
                    
                    if official_stats:
                        stats_arr = np.array(official_stats)
                        mean_official_stats = np.mean(stats_arr, axis=0)
                        mean_official_stats = mean_official_stats.tolist()
                        return mean_official_stats
                    else:
                        print("DBCompiler: obtain_officials_accumulations - Could Not Accumulate Official Stats")
                        return

    def update_table(self):
        try: 
            home_teams, away_teams = self.home_and_away()
        except:
            print("DBCompiler: update_table - Could Not Find Home or Away Teams")
            return
        
        if home_teams and away_teams:
            for home_team, away_team in zip(home_teams, away_teams):
                self.cursor.execute("SELECT * FROM team_stats WHERE team_name LIKE ? AND season = ?", ('% ' + home_team + '%', self.season))
                home_team_stats = self.cursor.fetchall()
                self.cursor.execute("SELECT * FROM team_stats WHERE team_name LIKE ? AND season = ?", ('% ' + away_team + '%', self.season))
                away_team_stats = self.cursor.fetchall()

                home_team_stats = [item for sublist in home_team_stats for item in sublist]
                away_team_stats = [item for sublist in away_team_stats for item in sublist]
                self.cursor.execute("SELECT * FROM player_stats WHERE team_tag IN (SELECT abbreviation FROM teams WHERE team_name LIKE ?) AND player_name IN (SELECT player_name FROM injury_report)", ('%' + home_team + '%',))
                home_team_injuries = self.cursor.fetchall()
                self.cursor.execute("SELECT * FROM player_stats WHERE team_tag IN (SELECT abbreviation FROM teams WHERE team_name LIKE ?) AND player_name IN (SELECT player_name FROM injury_report)", ('%' + away_team + '%',))
                away_team_injuries = self.cursor.fetchall()
                self.cursor.execute("SELECT team_name from teams WHERE team_name LIKE ?", ('% ' + home_team + '%',))
                home_team_full = self.cursor.fetchone()[0]

            
                home_injured_stats = self.obtain_injury_accumulations(home_team_injuries)
                away_injured_stats = self.obtain_injury_accumulations(away_team_injuries)
                    
                officials_stats = self.obtain_officials_accumulations(home_team_full)
                game_identifier = f'{home_team}' + f'{away_team}'

                try:
                    number = random.randint(0,1)
                    
                    if number == 0:
                        #Home team put into team 1
                        values = [self.date, game_identifier, self.season, 1, home_team] + home_team_stats[2:] + home_injured_stats + [0, away_team] + away_team_stats[2:] + away_injured_stats + officials_stats
                    else:
                        #Away team put into team 1
                        values = [self.date, game_identifier, self.season, 0, away_team] + away_team_stats[2:] + away_injured_stats + [1, home_team] + home_team_stats[2:] + home_injured_stats + officials_stats
                    columns = ["date", "game_identifier", "season", "team_1_is_home", "team_1_team_name", "team_1_G", "team_1_FG", "team_1_FGA", "team_1_FGp", "team_1_ThreeP", "team_1_ThreePA", "team_1_ThreePp", "team_1_TwoP", "team_1_TwoPA", "team_1_TwoPp", "team_1_FT", "team_1_FTA", "team_1_FTp", "team_1_ORB", "team_1_DRB", "team_1_TRB", "team_1_AST", "team_1_STL", "team_1_BLK", "team_1_TOV", "team_1_PF", "team_1_PTS", "team_1_age", "team_1_W", "team_1_L", "team_1_MOV", "team_1_SOS", "team_1_SRS", "team_1_ORtg", "team_1_DRtg", "team_1_NRtg", "team_1_pace", "team_1_FTr", "team_1_ThreePAr", "team_1_TSp", "team_1_OeFG", "team_1_OTOVp", "team_1_ORBp", "team_1_OFTFGAp", "team_1_DeFG", "team_1_DTOVp", "team_1_DRBp", "team_1_DFTFGAp", "team_1_avgD", "team_1_pTwoP", "team_1_pZeroToThree", "team_1_pThreeToTen", "team_1_pTenToSixteen", "team_1_pSixteenToThreeP", "team_1_pDunksA", "team_1_pDunksM", "team_1_TwoPointFGAst", "team_1_ThreePointFGAst", "team_1_FGpTwoP", "team_1_FGpZeroToThreeP", "team_1_FGpThreeToTenP", "team_1_FGpTenToSixteenP", "team_1_FGpSixteenToThreeP", "team_1_FGpThreeP", "team_1_oppG", "team_1_oppFG", "team_1_oppFGA", "team_1_oppFGp", "team_1_oppThreeP", "team_1_oppThreePA", "team_1_oppThreePp", "team_1_oppTwoP", "team_1_oppTwoPA", "team_1_oppTwoPp", "team_1_oppFT", "team_1_oppFTA", "team_1_oppFTp", "team_1_oppORB", "team_1_oppDRB", "team_1_oppTRB", "team_1_oppAST", "team_1_oppSTL", "team_1_oppBLK", "team_1_oppTOV", "team_1_oppPF", "team_1_oppPTS", "team_1_injured_GP", "team_1_injured_MPG", "team_1_injured_PPG", "team_1_injured_FGM", "team_1_injured_FGA", "team_1_injured_FGp", "team_1_injured_ThreePM", "team_1_injured_ThreePA", "team_1_injured_ThreePp", "team_1_injured_FTM", "team_1_injured_FTA", "team_1_injured_FTp", "team_1_injured_ORB", "team_1_injured_DRB", "team_1_injured_RPG", "team_1_injured_APG", "team_1_injured_SPG", "team_1_injured_BPG", "team_1_injured_TOV", "team_1_injured_PF", "team_1_injured_DblDbl", "team_1_injured_TrpDbl", "team_1_injured_FortyBomb", "team_1_injured_TwentyReb", "team_1_injured_TwentyAst", "team_1_injured_FiveStl", "team_1_injured_FiveBlk", "team_1_injured_High", "team_1_injured_HandsOnBuckets", "team_1_injured_AstToTovR", "team_1_injured_StlToTovR", "team_1_injured_FTFGAp", "team_1_injured_TeamW", "team_1_injured_TeamL", "team_1_injured_TeamWp", "team_1_injured_OWS", "team_1_injured_DWS", "team_1_injured_WS", "team_1_injured_TS", "team_1_injured_eFG", "team_1_injured_TotalSp", "team_1_injured_ORBp", "team_1_injured_DRBp", "team_1_injured_TRBp", "team_1_injured_ASTp", "team_1_injured_TOVp", "team_1_injured_STLp", "team_1_injured_BLKp", "team_1_injured_USG", "team_1_injured_PPR", "team_1_injured_PPS", "team_1_injured_ORtg", "team_1_injured_DRtg", "team_1_injured_eDiff", "team_1_injured_FIC", "team_1_injured_PER", "team_2_is_home", "team_2_team_name", "team_2_G", "team_2_FG", "team_2_FGA", "team_2_FGp", "team_2_ThreeP", "team_2_ThreePA", "team_2_ThreePp", "team_2_TwoP", "team_2_TwoPA", "team_2_TwoPp", "team_2_FT", "team_2_FTA", "team_2_FTp", "team_2_ORB", "team_2_DRB", "team_2_TRB", "team_2_AST", "team_2_STL", "team_2_BLK", "team_2_TOV", "team_2_PF", "team_2_PTS", "team_2_age", "team_2_W", "team_2_L", "team_2_MOV", "team_2_SOS", "team_2_SRS", "team_2_ORtg", "team_2_DRtg", "team_2_NRtg", "team_2_pace", "team_2_FTr", "team_2_ThreePAr", "team_2_TSp", "team_2_OeFG", "team_2_OTOVp", "team_2_ORBp", "team_2_OFTFGAp", "team_2_DeFG", "team_2_DTOVp", "team_2_DRBp", "team_2_DFTFGAp", "team_2_avgD", "team_2_pTwoP", "team_2_pZeroToThree", "team_2_pThreeToTen", "team_2_pTenToSixteen", "team_2_pSixteenToThreeP", "team_2_pDunksA", "team_2_pDunksM", "team_2_TwoPointFGAst", "team_2_ThreePointFGAst", "team_2_FGpTwoP", "team_2_FGpZeroToThreeP", "team_2_FGpThreeToTenP", "team_2_FGpTenToSixteenP", "team_2_FGpSixteenToThreeP", "team_2_FGpThreeP", "team_2_oppG", "team_2_oppFG", "team_2_oppFGA", "team_2_oppFGp", "team_2_oppThreeP", "team_2_oppThreePA", "team_2_oppThreePp", "team_2_oppTwoP", "team_2_oppTwoPA", "team_2_oppTwoPp", "team_2_oppFT", "team_2_oppFTA", "team_2_oppFTp", "team_2_oppORB", "team_2_oppDRB", "team_2_oppTRB", "team_2_oppAST", "team_2_oppSTL", "team_2_oppBLK", "team_2_oppTOV", "team_2_oppPF", "team_2_oppPTS", "team_2_injured_GP", "team_2_injured_MPG", "team_2_injured_PPG", "team_2_injured_FGM", "team_2_injured_FGA", "team_2_injured_FGp", "team_2_injured_ThreePM", "team_2_injured_ThreePA", "team_2_injured_ThreePp", "team_2_injured_FTM", "team_2_injured_FTA", "team_2_injured_FTp", "team_2_injured_ORB", "team_2_injured_DRB", "team_2_injured_RPG", "team_2_injured_APG", "team_2_injured_SPG", "team_2_injured_BPG", "team_2_injured_TOV", "team_2_injured_PF", "team_2_injured_DblDbl", "team_2_injured_TrpDbl", "team_2_injured_FortyBomb", "team_2_injured_TwentyReb", "team_2_injured_TwentyAst", "team_2_injured_FiveStl", "team_2_injured_FiveBlk", "team_2_injured_High", "team_2_injured_HandsOnBuckets", "team_2_injured_AstToTovR", "team_2_injured_StlToTovR", "team_2_injured_FTFGAp", "team_2_injured_TeamW", "team_2_injured_TeamL", "team_2_injured_TeamWp", "team_2_injured_OWS", "team_2_injured_DWS", "team_2_injured_WS", "team_2_injured_TS", "team_2_injured_eFG", "team_2_injured_TotalSp", "team_2_injured_ORBp", "team_2_injured_DRBp", "team_2_injured_TRBp", "team_2_injured_ASTp", "team_2_injured_TOVp", "team_2_injured_STLp", "team_2_injured_BLKp", "team_2_injured_USG", "team_2_injured_PPR", "team_2_injured_PPS", "team_2_injured_ORtg", "team_2_injured_DRtg", "team_2_injured_eDiff", "team_2_injured_FIC", "team_2_injured_PER", "official_stat_G", "official_stat_FGA", "official_stat_FTA", "official_stat_PF", "official_stat_PTS", "official_stat_FGA_pgrel", "official_stat_FTA_pgrel", "official_stat_PF_pgrel", "official_stat_PTS_pgrel", "official_stat_home_win_loss", "official_stat_home_FGA", "official_stat_home_FTA", "official_stat_home_PF", "official_stat_home_PTS", "official_stat_away_win_loss", "official_stat_away_FGA", "official_stat_away_FTA", "official_stat_away_PF", "official_stat_away_PTS", "official_stat_win_loss_hvrel", "official_stat_FGA_hvrel", "official_stat_FTA_hvrel", "official_stat_PF_hvrel", "official_stat_PTS_hvrel"]
                    
                    query = f'''INSERT INTO box_scores ({', '.join(columns)})
                                VALUES ({', '.join(['?'] * len(columns))})
                                ON CONFLICT (game_identifier, date) DO UPDATE
                                SET
                                {', '.join([f"{column} = EXCLUDED.{column}" for column in columns])};'''
                    self.cursor.execute(query, values)
                    self.conn.commit()

                except:
                    print("DBCompiler: update_table - Couldn't Insert Box Score Stats")
                
    def update_predictors_table(self, team1, team2, value1, value2, is_home, is_away, won, lost):
        total = int(value1) + int(value2)
        values = [self.yesterday_date, self.season, team1, is_home, value1, won, team2, is_away, value2, lost, total]
        
        self.cursor.execute(f"INSERT INTO predictors (date, season, team_1_team_name, team_1_is_home, team_1_score, team_1_was_winner, team_2_team_name, team_2_is_home, team_2_score, team_2_was_winner, total) VALUES ({', '.join(['?'] * len(values))})", values)
        self.conn.commit()

    def targets(self):
        home_scores = {}
        away_scores = {}
        url = f'https://www.espn.com/nba/scoreboard/_/date/{self.yesterday_date[:-1]}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("DBCompiler: targets - Could Not Access Yesterday's Scores From Internet")
            return
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            teams = soup.find_all("div", class_="ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db")
            scores = soup.find_all("div", class_="ScoreCell__Score h4 clr-gray-01 fw-heavy tar ScoreCell_Score--scoreboard pl2")

            for i in range(len(scores)):
                score = scores[i].text
                team = teams[i].text
                if i % 2 == 1:
                    home_scores[team] = score
                else:
                    away_scores[team] = score

            for (key1, value1), (key2, value2) in zip(home_scores.items(), away_scores.items()):
                value1 = int(value1)
                value2 = int(value2)
                
                if key1 == "NETS":
                    key1 == " NETS"
                if key2 == "NETS":
                    key2 == " NETS"

                self.cursor.execute("SELECT team_1_team_name FROM box_scores WHERE date = ? AND team_1_team_name LIKE ?", (self.yesterday_date, '%' + key1 + '%',))
                home_team_is_team1_exists = self.cursor.fetchone()
                self.cursor.execute("SELECT team_1_team_name FROM box_scores WHERE date = ? AND team_1_team_name LIKE ?", (self.yesterday_date, '%' + key2 + '%',))
                away_team_is_team1_exists = self.cursor.fetchone()
                
                try:
                    if home_team_is_team1_exists:
                        if (value1 > value2):
                            self.update_predictors_table(key1, key2, value1, value2, is_home=1, is_away=0, won=1, lost=0)
                        else:
                            self.update_predictors_table(key1, key2, value1, value2, is_home=1, is_away=0, won=0, lost=1)
                    if away_team_is_team1_exists:
                        if (value2 > value1):
                            self.update_predictors_table(key2, key1, value2, value1, is_home=0, is_away=1, won=1, lost=0)
                        else:
                            self.update_predictors_table(key2, key1, value2, value1, is_home=0, is_away=1, won=0, lost=1)
                except:
                    print("DBCompiler: targets - Predictors Already Inserted")
                    continue
        except:
            print("DBCompiler: targets - Predictor Table Failed")
  
def season_year():
    season, month = int(datetime.now().year), int(datetime.now().month)
    if month > 6:
        season = season + 1
    return int(season)

def connect_to_database():
    
    host = 'root'
    user = 'brandon'
    password = 'Hershey1BO24!'

    with open("mysql.sql", "r") as structure:
        structure = structure.read()

    try:
        conn = mysql.connector.connect (
            host=host,
            user=user,
            password=password
        ) 

        if conn.is_connected():
            cursor = conn.cursor()
            statements = structure.split(';')

            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            return conn
    except:
        print("Database Connection Error")
        return None

def main():
    print("Running")
    season = season_year()
    conn = connect_to_database()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y%m%d") + '0'
    yesterday_date = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday_date.strftime("%Y%m%d") + '0'
    global request_counter
    request_counter = 0

    thread_team = Thread(target=TeamScraper(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_injuries = Thread(target=InjuredPlayers(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_officiating = Thread(target=RefStats(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_players = Thread(target=PlayerStats(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_team_stats = Thread(target=TeamStats(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_box_score = Thread(target=DBCompiler(conn, season, cursor, yesterday_date, date, request_counter).update_table())
    thread_targets = Thread(target=DBCompiler(conn, season, cursor, yesterday_date, date, request_counter).targets())

    thread_team.start()
    thread_injuries.start()
    thread_officiating.start()
    thread_players.start()
    thread_team_stats.start()
    thread_box_score.start()
    thread_targets.start()

    thread_team.join()
    thread_injuries.join()
    thread_officiating.join()
    thread_players.join()
    thread_team_stats.join()
    thread_box_score.join()
    thread_targets.join()

    conn.close()
    print("Complete")

if __name__ ==  "__main__":
    main()


