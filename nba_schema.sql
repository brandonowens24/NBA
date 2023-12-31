CREATE TABLE IF NOT EXISTS nba.teams(
    abbreviation VARCHAR(50),
    team_name VARCHAR(50),
    season INTEGER,
    UNIQUE (abbreviation, team_name, season)
);


CREATE TABLE IF NOT EXISTS nba.injury_report(
    date VARCHAR(50),
    player_name VARCHAR(50),
    description VARCHAR(50),
    UNIQUE (date, player_name)
);

CREATE TABLE IF NOT EXISTS nba.officiating (
    official VARCHAR(50),
    season INTEGER,
    G INTEGER,
    FGA DECIMAL (4, 1),
    FTA DECIMAL (3, 1),
    PF DECIMAL (3, 1), 
    PTS DECIMAL (4, 1),
    FGA_pgrel DECIMAL (3, 1),
    FTA_pgrel DECIMAL (3, 1),
    PF_pgrel DECIMAL (3, 1), 
    PTS_pgrel DECIMAL (3, 1),
    home_win_loss DECIMAL (4, 3),
    home_FGA DECIMAL (4, 1),
    home_FTA DECIMAL (3, 1),
    home_PF DECIMAL (3, 1), 
    home_PTS DECIMAL (4, 1),
    away_win_loss DECIMAL (4, 3),
    away_FGA DECIMAL (4, 1),
    away_FTA DECIMAL (3, 1),
    away_PF DECIMAL (3, 1), 
    away_PTS DECIMAL (4, 1),
    win_loss_hvrel DECIMAL (4, 3),
    FGA_hvrel DECIMAL (3, 1),
    FTA_hvrel DECIMAL (3, 1),
    PF_hvrel DECIMAL (3, 1), 
    PTS_hvrel DECIMAL (3, 1),
    PRIMARY KEY (official, season)
);

CREATE TABLE IF NOT EXISTS nba.player_stats (
    player_name VARCHAR(50),
    season INTEGER,
    team_tag VARCHAR(50),
    GP INTEGER,
    MPG DECIMAL (3, 1),
    PPG DECIMAL (3, 1),
    FGM DECIMAL (3, 1),
    FGA DECIMAL (3, 1),
    FGp DECIMAL (4, 3),
    ThreePM DECIMAL (3, 1),
    ThreePA DECIMAL (3, 1),
    ThreePp DECIMAL (4, 3),
    FTM DECIMAL (3, 1),
    FTA DECIMAL (3, 1),
    FTp DECIMAL (4, 3),
    ORB DECIMAL (3, 1),
    DRB DECIMAL (3, 1),
    RPG DECIMAL (3, 1),
    APG DECIMAL (3, 1),
    SPG DECIMAL (3, 1),
    BPG DECIMAL (3, 1),
    TOV DECIMAL (3, 1),
    PF DECIMAL (3, 1),
    DblDbl INTEGER,
    TrpDbl INTEGER,
    FortyBomb INTEGER,
    TwentyReb INTEGER,
    TwentyAst INTEGER,
    FiveStl INTEGER,
    FiveBlk INTEGER,
    High INTEGER,
    HandsOnBuckets DECIMAL (3, 3),
    AstToTovR DECIMAL (3, 1),
    StlToTovR DECIMAL (3, 1),
    FTFGAp DECIMAL (3, 1),
    TeamW INTEGER,
    TeamL INTEGER,
    TeamWp DECIMAL (4, 3),
    OWS DECIMAL (3, 1),
    DWS DECIMAL (3, 1),
    WS DECIMAL (3, 1),
    TS DECIMAL (4, 3),
    eFG DECIMAL (4, 3),
    TotalSp DECIMAL (4, 1),
    ORBp DECIMAL (4, 1),
    DRBp DECIMAL (4, 1),
    TRBp DECIMAL (4, 1),
    ASTp DECIMAL (4, 1),
    TOVp DECIMAL (4, 1),
    STLp DECIMAL (4, 1),
    BLKp DECIMAL (4, 1),
    USG DECIMAL (4, 1),
    PPR DECIMAL (3, 1),
    PPS DECIMAL (3, 1),
    ORtg DECIMAL (4, 1),
    DRtg DECIMAL (4, 1),
    eDiff DECIMAL (4, 1),
    FIC DECIMAL (5, 1),
    PER DECIMAL (3, 1),
    PRIMARY KEY (player_name, season) 
);

CREATE TABLE IF NOT EXISTS nba.team_stats(
    team_name VARCHAR(50),
    season INTEGER, 
    G INTEGER,
    FG DECIMAL (3, 1), 
    FGA DECIMAL (4, 1),
    FGp DECIMAL (4, 3),
    ThreeP DECIMAL (3, 1),
    ThreePA DECIMAL (3, 1), 
    ThreePp DECIMAL (3, 3), 
    TwoP DECIMAL (3, 1), 
    TwoPA DECIMAL (3, 1), 
    TwoPp DECIMAL (4, 3), 
    FT DECIMAL (3, 1), 
    FTA DECIMAL (3, 1), 
    FTp DECIMAL (4, 3),  
    ORB DECIMAL (3, 1), 
    DRB DECIMAL (3, 1), 
    TRB DECIMAL (3, 1),
    AST DECIMAL (3, 1), 
    STL DECIMAL (3, 1), 
    BLK DECIMAL (3, 1), 
    TOV DECIMAL (3, 1), 
    PF DECIMAL (3, 1), 
    PTS DECIMAL (4, 1), 
    age DECIMAL (3, 1), 
    W INTEGER, 
    L INTEGER, 
    MOV DECIMAL (4, 2),
    SOS DECIMAL (4, 2), 
    SRS DECIMAL (4, 2),
    ORtg DECIMAL (4, 1), 
    DRtg DECIMAL (4, 1), 
    NRtg DECIMAL (3, 1), 
    pace DECIMAL (4, 1), 
    FTr DECIMAL (4, 3), 
    ThreePAr DECIMAL (4, 3), 
    TSp DECIMAL (4, 3), 
    OeFG DECIMAL (4, 3), 
    OTOVp DECIMAL (4, 1), 
    ORBp DECIMAL (4, 1), 
    OFTFGAp DECIMAL (4, 3), 
    DeFG DECIMAL (4, 3), 
    DTOVp DECIMAL (4, 1), 
    DRBp DECIMAL (4, 1), 
    DFTFGAp DECIMAL (4, 3),
    avgD DECIMAL (3, 1), 
    pTwoP DECIMAL (4, 3), 
    pZeroToThree DECIMAL (4, 3), 
    pThreeToTen DECIMAL (4, 3), 
    pTenToSixteen DECIMAL (4, 3), 
    pSixteenToThreeP DECIMAL (4, 3), 
    pDunksA DECIMAL (4, 3), 
    pDunksM INTEGER, 
    TwoPointFGAst DECIMAL (4, 3), 
    ThreePointFGAst DECIMAL (4, 3), 
    FGpTwoP DECIMAL (4, 3),
    FGpZeroToThreeP DECIMAL (4, 3), 
    FGpThreeToTenP DECIMAL (4, 3), 
    FGpTenToSixteenP DECIMAL (4, 3), 
    FGpSixteenToThreeP DECIMAL (4, 3), 
    FGpThreeP DECIMAL (4, 3),
    oppG INTEGER,
    oppFG DECIMAL (3, 1), 
    oppFGA DECIMAL (4, 1),
    oppFGp DECIMAL (4, 3),
    oppThreeP DECIMAL (3, 1),
    oppThreePA DECIMAL (3, 1), 
    oppThreePp DECIMAL (4, 3), 
    oppTwoP DECIMAL (3, 1), 
    oppTwoPA DECIMAL (3, 1), 
    oppTwoPp DECIMAL (4, 3), 
    oppFT DECIMAL (3, 1), 
    oppFTA DECIMAL (3, 1), 
    oppFTp DECIMAL (4, 3),  
    oppORB DECIMAL (3, 1), 
    oppDRB DECIMAL (3, 1), 
    oppTRB DECIMAL (3, 1),
    oppAST DECIMAL (3, 1), 
    oppSTL DECIMAL (3, 1), 
    oppBLK DECIMAL (3, 1), 
    oppTOV DECIMAL (3, 1), 
    oppPF DECIMAL (3, 1), 
    oppPTS DECIMAL (4, 1),
    PRIMARY KEY (team_name, season)
);


CREATE TABLE IF NOT EXISTS nba.box_scores (
    date VARCHAR(50),
    game_identifier VARCHAR(50),
    season INTEGER,
    team_1_is_home INTEGER,
    team_1_team_name VARCHAR(50), 
    team_1_G INTEGER,
    team_1_FG DECIMAL (3, 1), 
    team_1_FGA DECIMAL (4, 1),
    team_1_FGp DECIMAL (4, 3),
    team_1_ThreeP DECIMAL (3, 1),
    team_1_ThreePA DECIMAL (3, 1), 
    team_1_ThreePp DECIMAL (4, 3), 
    team_1_TwoP DECIMAL (3, 1), 
    team_1_TwoPA DECIMAL (3, 1), 
    team_1_TwoPp DECIMAL (4, 3), 
    team_1_FT DECIMAL (3, 1), 
    team_1_FTA DECIMAL (3, 1), 
    team_1_FTp DECIMAL (4, 3),  
    team_1_ORB DECIMAL (3, 1), 
    team_1_DRB DECIMAL (3, 1), 
    team_1_TRB DECIMAL (3, 1),
    team_1_AST DECIMAL (3, 1), 
    team_1_STL DECIMAL (3, 1), 
    team_1_BLK DECIMAL (3, 1), 
    team_1_TOV DECIMAL (3, 1), 
    team_1_PF DECIMAL (3, 1), 
    team_1_PTS DECIMAL (4, 1), 
    team_1_age DECIMAL (3, 1), 
    team_1_W INTEGER, 
    team_1_L INTEGER, 
    team_1_MOV DECIMAL (4, 2),
    team_1_SOS DECIMAL (4, 2), 
    team_1_SRS DECIMAL (4, 2),
    team_1_ORtg DECIMAL (4, 1), 
    team_1_DRtg DECIMAL (4, 1), 
    team_1_NRtg DECIMAL (3, 1), 
    team_1_pace DECIMAL (4, 1), 
    team_1_FTr DECIMAL (4, 3), 
    team_1_ThreePAr DECIMAL (4, 3), 
    team_1_TSp DECIMAL (4, 3), 
    team_1_OeFG DECIMAL (4, 3), 
    team_1_OTOVp DECIMAL (4, 1), 
    team_1_ORBp DECIMAL (4, 1), 
    team_1_OFTFGAp DECIMAL (4, 3), 
    team_1_DeFG DECIMAL (4, 3), 
    team_1_DTOVp DECIMAL (4, 1), 
    team_1_DRBp DECIMAL (4, 1), 
    team_1_DFTFGAp DECIMAL (4, 3),
    team_1_avgD DECIMAL (3, 1), 
    team_1_pTwoP DECIMAL (4, 3), 
    team_1_pZeroToThree DECIMAL (4, 3), 
    team_1_pThreeToTen DECIMAL (4, 3), 
    team_1_pTenToSixteen DECIMAL (4, 3), 
    team_1_pSixteenToThreeP DECIMAL (4, 3), 
    team_1_pDunksA DECIMAL (4, 3), 
    team_1_pDunksM INTEGER, 
    team_1_TwoPointFGAst DECIMAL (4, 3), 
    team_1_ThreePointFGAst DECIMAL (4, 3), 
    team_1_FGpTwoP DECIMAL (4, 3),
    team_1_FGpZeroToThreeP DECIMAL (4, 3), 
    team_1_FGpThreeToTenP DECIMAL (4, 3), 
    team_1_FGpTenToSixteenP DECIMAL (4, 3), 
    team_1_FGpSixteenToThreeP DECIMAL (4, 3), 
    team_1_FGpThreeP DECIMAL (4, 3),
    team_1_oppG INTEGER,
    team_1_oppFG DECIMAL (3, 1), 
    team_1_oppFGA DECIMAL (4, 1),
    team_1_oppFGp DECIMAL (4, 3),
    team_1_oppThreeP DECIMAL (3, 1),
    team_1_oppThreePA DECIMAL (3, 1), 
    team_1_oppThreePp DECIMAL (4, 3), 
    team_1_oppTwoP DECIMAL (3, 1), 
    team_1_oppTwoPA DECIMAL (3, 1), 
    team_1_oppTwoPp DECIMAL (4, 3), 
    team_1_oppFT DECIMAL (3, 1), 
    team_1_oppFTA DECIMAL (3, 1), 
    team_1_oppFTp DECIMAL (4, 3),  
    team_1_oppORB DECIMAL (3, 1), 
    team_1_oppDRB DECIMAL (3, 1), 
    team_1_oppTRB DECIMAL (3, 1),
    team_1_oppAST DECIMAL (3, 1), 
    team_1_oppSTL DECIMAL (3, 1), 
    team_1_oppBLK DECIMAL (3, 1), 
    team_1_oppTOV DECIMAL (3, 1), 
    team_1_oppPF DECIMAL (3, 1), 
    team_1_oppPTS DECIMAL (4, 1),
    team_1_injured_GP INTEGER,
    team_1_injured_MPG DECIMAL (3, 1),
    team_1_injured_PPG DECIMAL (3, 1),
    team_1_injured_FGM DECIMAL (3, 1),
    team_1_injured_FGA DECIMAL (3, 1),
    team_1_injured_FGp DECIMAL (4, 3),
    team_1_injured_ThreePM DECIMAL (3, 1),
    team_1_injured_ThreePA DECIMAL (3, 1),
    team_1_injured_ThreePp DECIMAL (4, 3),
    team_1_injured_FTM DECIMAL (3, 1),
    team_1_injured_FTA DECIMAL (3, 1),
    team_1_injured_FTp DECIMAL (4, 3),
    team_1_injured_ORB DECIMAL (3, 1),
    team_1_injured_DRB DECIMAL (3, 1),
    team_1_injured_RPG DECIMAL (3, 1),
    team_1_injured_APG DECIMAL (3, 1),
    team_1_injured_SPG DECIMAL (3, 1),
    team_1_injured_BPG DECIMAL (3, 1),
    team_1_injured_TOV DECIMAL (3, 1),
    team_1_injured_PF DECIMAL (3, 1),
    team_1_injured_DblDbl INTEGER,
    team_1_injured_TrpDbl INTEGER,
    team_1_injured_FortyBomb INTEGER,
    team_1_injured_TwentyReb INTEGER,
    team_1_injured_TwentyAst INTEGER,
    team_1_injured_FiveStl INTEGER,
    team_1_injured_FiveBlk INTEGER,
    team_1_injured_High INTEGER,
    team_1_injured_HandsOnBuckets DECIMAL (4, 3),
    team_1_injured_AstToTovR DECIMAL (4, 1),
    team_1_injured_StlToTovR DECIMAL (4, 1),
    team_1_injured_FTFGAp DECIMAL (4, 1),
    team_1_injured_TeamW INTEGER,
    team_1_injured_TeamL INTEGER,
    team_1_injured_TeamWp DECIMAL (4, 3),
    team_1_injured_OWS DECIMAL (3, 1),
    team_1_injured_DWS DECIMAL (3, 1),
    team_1_injured_WS DECIMAL (3, 1),
    team_1_injured_TS DECIMAL (3, 1),
    team_1_injured_eFG DECIMAL (4, 1),
    team_1_injured_TotalSp DECIMAL (4, 1),
    team_1_injured_ORBp DECIMAL (4, 1),
    team_1_injured_DRBp DECIMAL (4, 1),
    team_1_injured_TRBp DECIMAL (4, 1),
    team_1_injured_ASTp DECIMAL (4, 1),
    team_1_injured_TOVp DECIMAL (4, 1),
    team_1_injured_STLp DECIMAL (4, 1),
    team_1_injured_BLKp DECIMAL (4, 1),
    team_1_injured_USG DECIMAL (4, 1),
    team_1_injured_PPR DECIMAL (4, 1),
    team_1_injured_PPS DECIMAL (4, 1),
    team_1_injured_ORtg DECIMAL (4, 1),
    team_1_injured_DRtg DECIMAL (4, 1),
    team_1_injured_eDiff DECIMAL (3, 1),
    team_1_injured_FIC DECIMAL (5, 1),
    team_1_injured_PER DECIMAL (4, 1),
    team_2_is_home INTEGER,
    team_2_team_name VARCHAR(50), 
    team_2_G INTEGER,
    team_2_FG DECIMAL (3, 1), 
    team_2_FGA DECIMAL (4, 1),
    team_2_FGp DECIMAL (4, 3),
    team_2_ThreeP DECIMAL (3, 1),
    team_2_ThreePA DECIMAL (3, 1), 
    team_2_ThreePp DECIMAL (4, 3), 
    team_2_TwoP DECIMAL (3, 1), 
    team_2_TwoPA DECIMAL (3, 1), 
    team_2_TwoPp DECIMAL (4, 3), 
    team_2_FT DECIMAL (3, 1), 
    team_2_FTA DECIMAL (3, 1), 
    team_2_FTp DECIMAL (4, 3),  
    team_2_ORB DECIMAL (3, 1), 
    team_2_DRB DECIMAL (3, 1), 
    team_2_TRB DECIMAL (3, 1),
    team_2_AST DECIMAL (3, 1), 
    team_2_STL DECIMAL (3, 1), 
    team_2_BLK DECIMAL (3, 1), 
    team_2_TOV DECIMAL (3, 1), 
    team_2_PF DECIMAL (3, 1), 
    team_2_PTS DECIMAL (4, 1), 
    team_2_age DECIMAL (3, 1), 
    team_2_W INTEGER, 
    team_2_L INTEGER, 
    team_2_MOV DECIMAL (4, 2),
    team_2_SOS DECIMAL (4, 2), 
    team_2_SRS DECIMAL (4, 2),
    team_2_ORtg DECIMAL (4, 1), 
    team_2_DRtg DECIMAL (4, 1), 
    team_2_NRtg DECIMAL (3, 1), 
    team_2_pace DECIMAL (4, 1), 
    team_2_FTr DECIMAL (4, 3), 
    team_2_ThreePAr DECIMAL (4, 3), 
    team_2_TSp DECIMAL (4, 3), 
    team_2_OeFG DECIMAL (4, 3), 
    team_2_OTOVp DECIMAL (4, 1), 
    team_2_ORBp DECIMAL (4, 1), 
    team_2_OFTFGAp DECIMAL (4, 3), 
    team_2_DeFG DECIMAL (4, 3), 
    team_2_DTOVp DECIMAL (4, 1), 
    team_2_DRBp DECIMAL (4, 1), 
    team_2_DFTFGAp DECIMAL (4, 3),
    team_2_avgD DECIMAL (3, 1), 
    team_2_pTwoP DECIMAL (4, 3), 
    team_2_pZeroToThree DECIMAL (4, 3), 
    team_2_pThreeToTen DECIMAL (4, 3), 
    team_2_pTenToSixteen DECIMAL (4, 3), 
    team_2_pSixteenToThreeP DECIMAL (4, 3), 
    team_2_pDunksA DECIMAL (4, 3), 
    team_2_pDunksM INTEGER, 
    team_2_TwoPointFGAst DECIMAL (4, 3), 
    team_2_ThreePointFGAst DECIMAL (4, 3), 
    team_2_FGpTwoP DECIMAL (4, 3),
    team_2_FGpZeroToThreeP DECIMAL (4, 3), 
    team_2_FGpThreeToTenP DECIMAL (4, 3), 
    team_2_FGpTenToSixteenP DECIMAL (4, 3), 
    team_2_FGpSixteenToThreeP DECIMAL (4, 3), 
    team_2_FGpThreeP DECIMAL (4, 3),
    team_2_oppG INTEGER,
    team_2_oppFG DECIMAL (3, 1), 
    team_2_oppFGA DECIMAL (4, 1),
    team_2_oppFGp DECIMAL (4, 3),
    team_2_oppThreeP DECIMAL (3, 1),
    team_2_oppThreePA DECIMAL (3, 1), 
    team_2_oppThreePp DECIMAL (4, 3), 
    team_2_oppTwoP DECIMAL (3, 1), 
    team_2_oppTwoPA DECIMAL (3, 1), 
    team_2_oppTwoPp DECIMAL (4, 3), 
    team_2_oppFT DECIMAL (3, 1), 
    team_2_oppFTA DECIMAL (3, 1), 
    team_2_oppFTp DECIMAL (4, 3),  
    team_2_oppORB DECIMAL (3, 1), 
    team_2_oppDRB DECIMAL (3, 1), 
    team_2_oppTRB DECIMAL (3, 1),
    team_2_oppAST DECIMAL (3, 1), 
    team_2_oppSTL DECIMAL (3, 1), 
    team_2_oppBLK DECIMAL (3, 1), 
    team_2_oppTOV DECIMAL (3, 1), 
    team_2_oppPF DECIMAL (3, 1), 
    team_2_oppPTS DECIMAL (4, 1),
    team_2_injured_GP INTEGER,
    team_2_injured_MPG DECIMAL (3, 1),
    team_2_injured_PPG DECIMAL (3, 1),
    team_2_injured_FGM DECIMAL (3, 1),
    team_2_injured_FGA DECIMAL (3, 1),
    team_2_injured_FGp DECIMAL (4, 3),
    team_2_injured_ThreePM DECIMAL (3, 1),
    team_2_injured_ThreePA DECIMAL (3, 1),
    team_2_injured_ThreePp DECIMAL (4, 3),
    team_2_injured_FTM DECIMAL (3, 1),
    team_2_injured_FTA DECIMAL (3, 1),
    team_2_injured_FTp DECIMAL (4, 3),
    team_2_injured_ORB DECIMAL (3, 1),
    team_2_injured_DRB DECIMAL (3, 1),
    team_2_injured_RPG DECIMAL (3, 1),
    team_2_injured_APG DECIMAL (3, 1),
    team_2_injured_SPG DECIMAL (3, 1),
    team_2_injured_BPG DECIMAL (3, 1),
    team_2_injured_TOV DECIMAL (3, 1),
    team_2_injured_PF DECIMAL (3, 1),
    team_2_injured_DblDbl INTEGER,
    team_2_injured_TrpDbl INTEGER,
    team_2_injured_FortyBomb INTEGER,
    team_2_injured_TwentyReb INTEGER,
    team_2_injured_TwentyAst INTEGER,
    team_2_injured_FiveStl INTEGER,
    team_2_injured_FiveBlk INTEGER,
    team_2_injured_High INTEGER,
    team_2_injured_HandsOnBuckets DECIMAL (4, 3),
    team_2_injured_AstToTovR DECIMAL (4, 1),
    team_2_injured_StlToTovR DECIMAL (4, 1),
    team_2_injured_FTFGAp DECIMAL (3, 1),
    team_2_injured_TeamW INTEGER,
    team_2_injured_TeamL INTEGER,
    team_2_injured_TeamWp DECIMAL (3, 3),
    team_2_injured_OWS DECIMAL (3, 1),
    team_2_injured_DWS DECIMAL (3, 1),
    team_2_injured_WS DECIMAL (3, 1),
    team_2_injured_TS DECIMAL (4, 1),
    team_2_injured_eFG DECIMAL (4, 1),
    team_2_injured_TotalSp DECIMAL (4, 1),
    team_2_injured_ORBp DECIMAL (4, 1),
    team_2_injured_DRBp DECIMAL (4, 1),
    team_2_injured_TRBp DECIMAL (4, 1),
    team_2_injured_ASTp DECIMAL (4, 1),
    team_2_injured_TOVp DECIMAL (4, 1),
    team_2_injured_STLp DECIMAL (4, 1),
    team_2_injured_BLKp DECIMAL (4, 1),
    team_2_injured_USG DECIMAL (4, 1),
    team_2_injured_PPR DECIMAL (4, 1),
    team_2_injured_PPS DECIMAL (4, 1),
    team_2_injured_ORtg DECIMAL (4, 1),
    team_2_injured_DRtg DECIMAL (4, 1),
    team_2_injured_eDiff DECIMAL (3, 1),
    team_2_injured_FIC DECIMAL (5, 1),
    team_2_injured_PER DECIMAL (4, 1),
    official_stat_G INTEGER,
    official_stat_FGA DECIMAL (4, 1),
    official_stat_FTA DECIMAL (3, 1),
    official_stat_PF DECIMAL (3, 1), 
    official_stat_PTS DECIMAL (4, 1),
    official_stat_FGA_pgrel DECIMAL (3, 1),
    official_stat_FTA_pgrel DECIMAL (3, 1),
    official_stat_PF_pgrel DECIMAL (3, 1), 
    official_stat_PTS_pgrel DECIMAL (3, 1),
    official_stat_home_win_loss DECIMAL (4, 3),
    official_stat_home_FGA DECIMAL (4, 1),
    official_stat_home_FTA DECIMAL (3, 1),
    official_stat_home_PF DECIMAL (3, 1), 
    official_stat_home_PTS DECIMAL (4, 1),
    official_stat_away_win_loss DECIMAL (4, 3),
    official_stat_away_FGA DECIMAL (4, 1),
    official_stat_away_FTA DECIMAL (3, 1),
    official_stat_away_PF DECIMAL (3, 1), 
    official_stat_away_PTS DECIMAL (4, 1),
    official_stat_win_loss_hvrel DECIMAL (4, 3),
    official_stat_FGA_hvrel DECIMAL (3, 1),
    official_stat_FTA_hvrel DECIMAL (3, 1),
    official_stat_PF_hvrel DECIMAL (3, 1), 
    official_stat_PTS_hvrel DECIMAL (3, 1),
    PRIMARY KEY (game_identifier, date)
);


CREATE TABLE IF NOT EXISTS nba.predictors(
    date VARCHAR(50),
    season INTEGER,
    team_1_team_name VARCHAR(50),
    team_1_is_home INTEGER,
    team_1_score INTEGER,
    team_1_was_winner INTEGER,
    team_2_team_name VARCHAR(50),
    team_2_is_home INTEGER,
    team_2_score INTEGER,
    team_2_was_winner INTEGER,
    total INTEGER,
    PRIMARY KEY(date, team_1_team_name, team_2_team_name)
);

