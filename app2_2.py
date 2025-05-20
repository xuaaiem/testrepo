import streamlit as st
import pandas as pd
from datetime import datetime
import io
import base64
from io import StringIO


# 🚘 Embedded CSV data as strings
data_fahrzeuge = """Product Name,List price
MG HS AT COM MY24,25201.68
MG HS AT LUX MY24,26882.35
MG HS MT COM MY24,23521.01
MG HS MT LUX MY24,25201.68
MG HS PHEV COM MY24,33605.04
MG HS PHEV LUX MY24,35285.71
MG ZS 1.5L 5MT COM MY24,20159.66
MG ZS 1.5L 5MT LUX MY24,-
MG ZS 1.5L 5MT STD MY24,17638.66
MG ZS HEV COM MY24,21000
MG ZS HEV LUX MY24,22680.67
MG ZS HEV STD MY24,19319.33
MG3 1.5L 5MT STD MY24.5,15117.65
MG3 1.5L 5MT COM MY24.5,16378.15
MG3 HEV STD,16798.32
MG3 HEV COM,18058.82
MG3 HEV COM MY24.5,18058.82
MG3 HEV LUX,20159.66
MG3 HEV LUX MY24.5,20159.66"""

# Add all other CSV strings below similarly...

data_bonus = """Product Name,Start,Ende,Bonus [€],Zulassungsbonus [%],Marketingbonus [%],Dokumentennummer,*Registration Date (Report) als Bemessungsgrundlage
MG HS AT COM MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW5000005gyPtMAI/edit
MG HS AT LUX MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG HS MT COM MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG HS MT LUX MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG HS PHEV COM MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG HS PHEV LUX MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS 1.5L 5MT COM MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS 1.5L 5MT LUX MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS 1.5L 5MT STD MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS HEV COM MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS HEV LUX MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS HEV STD MY24,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 1.5L 5MT STD MY24.5,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 1.5L 5MT COM MY24.5,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV STD,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV STD MY24.5,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV COM,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV COM MY24.5,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV LUX,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG3 HEV LUX MY24.5,2024-06-01,2024-12-31,0,0.015,0.0,-BN-001,
MG ZS 1.5L 5MT COM,2024-06-01,2024-12-31,250,0.0,0.0,-002,
MG ZS 1.5L 5MT LUX,2024-06-01,2024-12-31,750,0.0,0.0,-002,
MG ZS 1.0T 6AT LUX,2024-06-01,2024-12-31,1750,0.0,0.0,-002,
MG ZS 1.0T 6MT LUX,2024-06-01,2024-12-31,1000,0.0,0.0,-002,
MG HS 1.5T AT COM MY23,2024-06-01,2024-12-31,2000,0.0,0.0,-002,
MG HS 1.5T AT LUX,2024-06-01,2024-12-31,2250,0.0,0.0,-002,
MG HS 1.5T AT LUX MY23,2024-06-01,2024-12-31,2250,0.0,0.0,-002,
MG HS 1.5T MT COM MY23,2024-06-01,2024-12-31,1500,0.0,0.0,-002,
MG HS 1.5T MT LUX,2024-06-01,2024-12-31,1750,0.0,0.0,-002,
MG HS 1.5T MT LUX MY23,2024-06-01,2024-12-31,1750,0.0,0.0,-002,
MG HS AT COM MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG HS AT LUX MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG HS MT COM MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG HS MT LUX MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG HS PHEV COM MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG HS PHEV LUX MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS 1.5L 5MT LUX MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS HEV COM MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS HEV LUX MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG ZS HEV STD MY24,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV STD,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV STD MY24.5,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV COM,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV COM MY24.5,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV LUX,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
MG3 HEV LUX MY24.5,2025-01-01,2025-06-30,0,0.01,0.005,-BN-001,
"""
data_endkunde = """Product Name,Start,Ende,Bonus [€],Dokumentennummer,*Contract Date als Bemessungsparameter
MG HS AT COM MY24,2025-01-01,2025-06-30,1750,-1.0,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000DDlhZMAT/view?queryScope=userFolders
MG HS AT LUX MY24,2025-01-01,2025-03-31,2000,-1.0,
MG HS MT COM MY24,2025-01-01,2025-06-30,1500,-1.0,
MG HS MT LUX MY24,2025-01-01,2025-06-30,1750,-1.0,
MG HS PHEV COM MY24,2025-01-01,2025-06-30,3500,-1.0,
MG HS PHEV LUX MY24,2025-01-01,2025-06-30,3750,-1.0,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-06-30,1500,-1.0,
MG ZS 1.5L 5MT LUX MY24,2025-01-01,2025-06-30,0,,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-06-30,1000,-1.0,
MG ZS HEV COM MY24,2025-01-01,2025-06-30,1500,-1.0,
MG ZS HEV LUX MY24,2025-01-01,2025-06-30,2000,-1.0,
MG ZS HEV STD MY24,2025-01-01,2025-06-30,1000,-1.0,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-06-30,750,-1.0,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-06-30,950,-1.0,
MG3 HEV STD,2025-01-01,2025-06-30,1000,-1.0,
MG3 HEV STD MY24.5,2025-01-01,2025-06-30,1000,-1.0,
MG3 HEV COM,2025-01-01,2025-06-30,1250,-1.0,
MG3 HEV COM MY24.5,2025-01-01,2025-06-30,1250,-1.0,
MG3 HEV LUX,2025-01-01,2025-06-30,1500,-1.0,
MG3 HEV LUX MY24.5,2025-01-01,2025-06-30,1500,-1.0,
MG HS AT LUX MY24,2025-04-01,2025-06-30,1000,-1.0,
MG HS AT COM MY24,2024-06-01,2024-12-31,1750,,
MG HS AT LUX MY24,2024-06-01,2024-12-31,2000,,
MG HS MT COM MY24,2024-06-01,2024-12-31,1500,,
MG HS MT LUX MY24,2024-06-01,2024-12-31,1750,,
MG HS PHEV COM MY24,2024-06-01,2024-12-31,3500,,
MG HS PHEV LUX MY24,2024-06-01,2024-12-31,3750,,
MG ZS 1.5L 5MT COM MY24,2024-06-01,2024-12-31,1500,,
MG ZS 1.5L 5MT LUX MY24,2024-06-01,2024-12-31,0,,
MG ZS 1.5L 5MT STD MY24,2024-06-01,2024-12-31,1000,,
MG ZS HEV COM MY24,2024-06-01,2024-12-31,1500,,
MG ZS HEV LUX MY24,2024-06-01,2024-12-31,2000,,
MG ZS HEV STD MY24,2024-06-01,2024-12-31,1000,,
MG3 1.5L 5MT STD MY24.5,2024-06-01,2024-12-31,750,,
MG3 1.5L 5MT COM MY24.5,2024-06-01,2024-12-31,950,,
MG3 HEV STD,2024-06-01,2024-12-31,1000,,
MG3 HEV STD MY24.5,2024-06-01,2024-12-31,1000,,
MG3 HEV COM,2024-06-01,2024-12-31,1250,,
MG3 HEV COM MY24.5,2024-06-01,2024-12-31,1250,,
MG3 HEV LUX,2024-06-01,2024-12-31,1500,,
MG3 HEV LUX MY24.5,2024-06-01,2024-12-31,1500,,
"""
data_fleet = """Product Name,Start,Ende,Fleet Size,Bonus [%],Dokumentennummer,*Bemessungsgrundlage Fleet Size & Contract Date
MG HS AT COM MY24,2025-01-01,2025-06-30,SMALL,0.02,-FLEET-001,*Hybridwochen inkludiert
MG HS AT COM MY24,2025-01-01,2025-06-30,MEDIUM,0.03,-FLEET-001,
MG HS AT COM MY24,2025-01-01,2025-06-30,BIG,0.04,-FLEET-001,
MG HS AT LUX MY24,2025-01-01,2025-06-30,SMALL,0.02,-FLEET-001,
MG HS AT LUX MY24,2025-01-01,2025-06-30,MEDIUM,0.03,-FLEET-001,
MG HS AT LUX MY24,2025-01-01,2025-06-30,BIG,0.04,-FLEET-001,
MG HS MT COM MY24,2025-01-01,2025-06-30,SMALL,0.02,-FLEET-001,
MG HS MT COM MY24,2025-01-01,2025-06-30,MEDIUM,0.03,-FLEET-001,
MG HS MT COM MY24,2025-01-01,2025-06-30,BIG,0.04,-FLEET-001,
MG HS MT LUX MY24,2025-01-01,2025-06-30,SMALL,0.02,-FLEET-001,
MG HS MT LUX MY24,2025-01-01,2025-06-30,MEDIUM,0.03,-FLEET-001,
MG HS MT LUX MY24,2025-01-01,2025-06-30,BIG,0.04,-FLEET-001,
MG HS PHEV COM MY24,2025-01-01,2025-02-28,SMALL,0.02,-FLEET-001,
MG HS PHEV COM MY24,2025-01-01,2025-02-28,MEDIUM,0.03,-FLEET-001,
MG HS PHEV COM MY24,2025-01-01,2025-02-28,BIG,0.04,-FLEET-001,
MG HS PHEV LUX MY24,2025-01-01,2025-02-28,SMALL,0.02,-FLEET-001,
MG HS PHEV LUX MY24,2025-01-01,2025-02-28,MEDIUM,0.03,-FLEET-001,
MG HS PHEV LUX MY24,2025-01-01,2025-02-28,BIG,0.04,-FLEET-001,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG ZS 1.5L 5MT LUX MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS 1.5L 5MT LUX MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS 1.5L 5MT LUX MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG ZS HEV COM MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS HEV COM MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS HEV COM MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG ZS HEV LUX MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS HEV LUX MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS HEV LUX MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG ZS HEV STD MY24,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG ZS HEV STD MY24,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG ZS HEV STD MY24,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV STD,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV STD,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV STD,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV STD MY24.5,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV STD MY24.5,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV STD MY24.5,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV COM,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV COM,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV COM,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV COM MY24.5,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV COM MY24.5,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV COM MY24.5,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV LUX,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV LUX,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV LUX,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG3 HEV LUX MY24.5,2025-01-01,2025-06-30,SMALL,0.01,-FLEET-001,
MG3 HEV LUX MY24.5,2025-01-01,2025-06-30,MEDIUM,0.02,-FLEET-001,
MG3 HEV LUX MY24.5,2025-01-01,2025-06-30,BIG,0.03,-FLEET-001,
MG HS PHEV COM MY24,2025-03-01,2025-06-30,SMALL,0.06,-FLEET-001,
MG HS PHEV COM MY24,2025-03-01,2025-06-30,MEDIUM,0.07,-FLEET-001,
MG HS PHEV COM MY24,2025-03-01,2025-06-30,BIG,0.08,-FLEET-001,
MG HS PHEV LUX MY24,2025-03-01,2025-06-30,SMALL,0.06,-FLEET-001,
MG HS PHEV LUX MY24,2025-03-01,2025-06-30,MEDIUM,0.07,-FLEET-001,
MG HS PHEV LUX MY24,2025-03-01,2025-06-30,BIG,0.08,-FLEET-001,
"""
data_fruhling = """Product Name,Start,Ende,Bonus €],Dokumentennummer,"*Contract Date als Bemessungsgrundlage, Registration Date <= 31.03.2025"
MG HS AT COM MY24,2025-02-01,2025-02-12,0,,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000EE82TMAT/view
MG HS AT LUX MY24,2025-02-01,2025-02-12,0,,
MG HS MT COM MY24,2025-02-01,2025-02-12,0,,
MG HS MT LUX MY24,2025-02-01,2025-02-12,0,,
MG HS PHEV COM MY24,2025-02-01,2025-02-12,1000,-7.0,
MG HS PHEV LUX MY24,2025-02-01,2025-02-12,1500,-7.0,
MG ZS 1.5L 5MT COM MY24,2025-02-01,2025-02-12,0,,
MG ZS 1.5L 5MT LUX MY24,2025-02-01,2025-02-12,0,,
MG ZS 1.5L 5MT STD MY24,2025-02-01,2025-02-12,0,,
MG ZS HEV COM MY24,2025-02-01,2025-02-12,750,-7.0,
MG ZS HEV LUX MY24,2025-02-01,2025-02-12,1000,-7.0,
MG ZS HEV STD MY24,2025-02-01,2025-02-12,500,-7.0,
MG3 1.5L 5MT STD MY24.5,2025-02-01,2025-02-12,0,,
MG3 1.5L 5MT COM MY24.5,2025-02-01,2025-02-12,0,,
MG3 HEV STD,2025-02-01,2025-02-12,250,-7.0,
MG3 HEV STD MY24.5,2025-02-01,2025-02-12,250,-7.0,
MG3 HEV COM,2025-02-01,2025-02-12,500,-7.0,
MG3 HEV COM MY24.5,2025-02-01,2025-02-12,500,-7.0,
MG3 HEV LUX,2025-02-01,2025-02-12,750,-7.0,
MG3 HEV LUX MY24.5,2025-02-01,2025-02-12,750,-7.0,"""
data_hybrid = """Product Name,Start,Ende,Bonus €],Dokumentennummer,"*Contract Date als Bemessungsgrundlage, Registration Date <= 30.04.2025; First Registration >= 01.01.2025 possible, no VFW, s. FLEET for HS PHEV",Unnamed: 6
MG HS AT COM MY24,2025-03-01,2025-03-31,0,,Report,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000FNZMDMA5/view
MG HS AT LUX MY24,2025-03-01,2025-03-31,0,,History,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000FNaWnMAL/view?queryScope=userFolders
MG HS MT COM MY24,2025-03-01,2025-03-31,0,,,
MG HS MT LUX MY24,2025-03-01,2025-03-31,0,,,
MG HS PHEV COM MY24,2025-03-01,2025-03-31,0,,,
MG HS PHEV LUX MY24,2025-03-01,2025-03-31,0,,,
MG ZS 1.5L 5MT COM MY24,2025-03-01,2025-03-31,0,,,
MG ZS 1.5L 5MT LUX MY24,2025-03-01,2025-03-31,0,,,
MG ZS 1.5L 5MT STD MY24,2025-03-01,2025-03-31,0,,,
MG ZS HEV COM MY24,2025-03-01,2025-03-31,750,-6.0,,
MG ZS HEV LUX MY24,2025-03-01,2025-03-31,1000,-6.0,,
MG ZS HEV STD MY24,2025-03-01,2025-03-31,500,-6.0,,
MG3 1.5L 5MT STD MY24.5,2025-03-01,2025-03-31,0,,,
MG3 1.5L 5MT COM MY24.5,2025-03-01,2025-03-31,0,,,
MG3 HEV STD,2025-03-01,2025-03-31,0,,,
MG3 HEV STD MY24.5,2025-03-01,2025-03-31,0,,,
MG3 HEV COM,2025-03-01,2025-03-31,0,,,
MG3 HEV COM MY24.5,2025-03-01,2025-03-31,0,,,
MG3 HEV LUX,2025-03-01,2025-03-31,0,,,
MG3 HEV LUX MY24.5,2025-03-01,2025-03-31,0,,,"""
data_loan = """Product Name,Start,Ende,Name Consors,Name MG,Bonus [€],Dokumentennummer,*Anfragedatum bei Consors als Bemessungsgrundlage
MG3 HEV STD,2024-08-01,2024-08-31,Leasing,Leasing,1500.0,-SUB001,*Die Neuen: Contract Date = [01.03.2025 - 31.03.2025]; Registration Date = [01.03.2025 - 31.05.2025]
MG3 HEV COM,2024-08-01,2024-08-31,Leasing,Leasing,1700.0,-SUB001,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000EWP3FMAX/view?queryScope=userFolders
MG3 HEV LUX,2024-08-01,2024-08-31,Leasing,Leasing,3300.0,-SUB001,
MG3 HEV STD,2024-09-01,2024-09-30,Leasing,Leasing,2025.87,-SUB001,
MG3 HEV COM,2024-09-01,2024-09-30,Leasing,Leasing,1700.0,-SUB001,
MG3 HEV LUX,2024-09-01,2024-09-30,Leasing,Leasing,3823.57,-SUB001,
MG3 HEV STD,2024-05-01,2024-11-30,Loan,Finanzierung,750.0,-SUB001,
MG3 HEV COM,2024-05-01,2024-11-30,Loan,Finanzierung,750.0,-SUB001,
MG3 HEV LUX,2024-05-01,2024-11-30,Loan,Finanzierung,1000.0,-SUB001,
MG3 HEV STD,2025-01-01,2024-11-28,Loan,Finanzierung,750.0,-SUB001,
MG3 HEV COM,2025-01-01,2024-11-28,Loan,Finanzierung,750.0,-SUB001,
MG3 HEV LUX,2025-01-01,2024-11-28,Loan,Finanzierung,1000.0,-SUB001,
MG ZS HEV STD MY24,2024-10-01,2024-11-28,Loan,Finanzierung,1000.0,-SUB001,
MG ZS HEV COM MY24,2024-10-01,2024-11-28,Loan,Finanzierung,1000.0,-SUB001,
MG ZS HEV LUX MY24,2024-10-01,2024-11-28,Loan,Finanzierung,1000.0,-SUB001,
MG3 HEV STD,2024-11-29,2024-12-31,Loan,Finanzierung,2000.0,-SUB001,
MG3 HEV COM,2024-11-29,2024-12-31,Loan,Finanzierung,2000.0,-SUB001,
MG3 HEV LUX,2024-11-29,2024-12-31,Loan,Finanzierung,2750.0,-SUB001,
MG ZS HEV STD MY24,2024-11-29,2024-12-31,Loan,Finanzierung,2000.0,-SUB001,
MG ZS HEV COM MY24,2024-11-29,2024-12-31,Loan,Finanzierung,2000.0,-SUB001,
MG ZS HEV LUX MY24,2024-11-29,2024-12-31,Loan,Finanzierung,2750.0,-SUB001,
MG HS AT COM MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1250.0,-SUB001,
MG HS AT LUX MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1250.0,-SUB001,
MG HS MT COM MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1250.0,-SUB001,
MG HS MT LUX MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1250.0,-SUB001,
MG HS PHEV COM MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1750.0,-SUB001,
MG HS PHEV LUX MY24,2024-10-01,2024-12-31,Loan,Finanzierung,1750.0,-SUB001,
MG3 1.5L 5MT STD MY24.5,2025-01-01,2025-02-28,Loan,Finanzierung,250.0,-SUB001,
MG3 1.5L 5MT COM MY24.5,2025-01-01,2025-02-28,Loan,Finanzierung,250.0,-SUB001,
MG ZS HEV STD MY24,2025-01-01,2025-03-31,Loan,Finanzierung,500.0,-SUB001,
MG ZS HEV COM MY24,2025-01-01,2025-03-31,Loan,Finanzierung,500.0,-SUB001,
MG ZS HEV LUX MY24,2025-01-01,2025-03-31,Loan,Finanzierung,500.0,-SUB001,
MG ZS 1.5L 5MT STD MY24,2025-01-01,2025-02-28,Loan,Finanzierung,500.0,-SUB001,
MG ZS 1.5L 5MT COM MY24,2025-01-01,2025-02-28,Loan,Finanzierung,500.0,-SUB001,
MG HS AT COM MY24,2025-01-01,2025-03-31,Loan,Finanzierung,500.0,-SUB001,
MG HS AT LUX MY24,2025-01-01,2025-03-31,Loan,Finanzierung,750.0,-SUB001,
MG HS MT COM MY24,2025-01-01,2025-03-31,Loan,Finanzierung,750.0,-SUB001,
MG HS MT LUX MY24,2025-01-01,2025-03-31,Loan,Finanzierung,1000.0,-SUB001,
MG HS PHEV COM MY24,2025-01-01,2025-03-31,Loan,Finanzierung,3500.0,-SUB001,
MG HS PHEV LUX MY24,2025-01-01,2025-03-31,Loan,Finanzierung,3750.0,-SUB001,
MG3 1.5L 5MT STD MY24.5,2025-03-01,2025-03-31,Loan,Finanzierung - Die Neuen,1600.0,-SUB001,
MG3 1.5L 5MT COM MY24.5,2025-03-01,2025-03-31,Loan,Finanzierung - Die Neuen,1550.0,-SUB001,
MG ZS 1.5L 5MT STD MY24,2025-03-01,2025-03-31,Loan,Finanzierung - Die Neuen,1650.0,-SUB001,
MG ZS 1.5L 5MT COM MY24,2025-03-01,2025-03-31,Loan,Finanzierung - Die Neuen,1500.0,-SUB001,
"""
data_mg3 = """Product Name,Start,Ende,Bonus €],Production date >= 270 Tage,Dokumentennummer,"*Contract Date als Bemessungsgrundlage, First Registration = [20.03.2025-31.03.2025], VIN in Excel-list"
MG HS AT COM MY24,2025-03-20,2025-03-31,0,,,*Contract Date - Production date >= 270Tage
MG HS AT LUX MY24,2025-03-20,2025-03-31,0,,,https://saicsmilorg2.lightning.force.com/lightning/r/Report/00OW500000FNWUnMAP/view
MG HS MT COM MY24,2025-03-20,2025-03-31,0,,,
MG HS MT LUX MY24,2025-03-20,2025-03-31,0,,,
MG HS PHEV COM MY24,2025-03-20,2025-03-31,0,,,
MG HS PHEV LUX MY24,2025-03-20,2025-03-31,0,,,
MG ZS 1.5L 5MT COM MY24,2025-03-20,2025-03-31,0,,,
MG ZS 1.5L 5MT LUX MY24,2025-03-20,2025-03-31,0,,,
MG ZS 1.5L 5MT STD MY24,2025-03-20,2025-03-31,0,,,
MG ZS HEV COM MY24,2025-03-20,2025-03-31,0,,,
MG ZS HEV LUX MY24,2025-03-20,2025-03-31,0,,,
MG ZS HEV STD MY24,2025-03-20,2025-03-31,0,,,
MG3 1.5L 5MT STD MY24.5,2025-03-20,2025-03-31,0,,,
MG3 1.5L 5MT COM MY24.5,2025-03-20,2025-03-31,0,,,
MG3 HEV STD,2025-03-20,2025-03-31,1750,yes,-5.0,
MG3 HEV STD MY24.5,2025-03-20,2025-03-31,1750,yes,-5.0,
MG3 HEV COM,2025-03-20,2025-03-31,1750,yes,-5.0,
MG3 HEV COM MY24.5,2025-03-20,2025-03-31,1750,yes,-5.0,
MG3 HEV LUX,2025-03-20,2025-03-31,1000,yes,-5.0,
MG3 HEV LUX MY24.5,2025-03-20,2025-03-31,1000,yes,-5.0,
MG3 HEV STD,2025-03-20,2025-03-31,750,no,-5.0,
MG3 HEV STD MY24.5,2025-03-20,2025-03-31,750,no,-5.0,
MG3 HEV COM,2025-03-20,2025-03-31,750,no,-5.0,
MG3 HEV COM MY24.5,2025-03-20,2025-03-31,750,no,-5.0,
MG3 HEV LUX,2025-03-20,2025-03-31,0,no,,
MG3 HEV LUX MY24.5,2025-03-20,2025-03-31,0,no,,
"""
data_vfw = """Product Name;Start;Ende;Bonus [€];Bonus [%];Dokumentennummer;;;;;;;
MG HS AT COM MY24;01.10.2024;31.12.2024; 1.750,00 € ;0,00%;-VFW002;;;;;;;
MG HS AT LUX MY24;01.10.2024;31.12.2024; 3.000,00 € ;0,00%;-VFW002;;;;;;;
MG HS MT COM MY24;01.10.2024;31.12.2024; 1.000,00 € ;0,00%;-VFW002;;;;;;;
MG HS MT LUX MY24;01.10.2024;31.12.2024; 1.750,00 € ;0,00%;-VFW002;;;;;;;
MG HS PHEV COM MY24;01.10.2024;31.12.2024; 1.500,00 € ;0,00%;-VFW002;;;;;;;
MG HS PHEV LUX MY24;01.10.2024;31.12.2024; 5.000,00 € ;0,00%;-VFW002;;;;;;;
MG ZS 1.5L 5MT COM MY24;01.10.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG ZS 1.5L 5MT LUX MY24;01.10.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG ZS 1.5L 5MT STD MY24;01.10.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG ZS HEV COM MY24;01.10.2024;31.12.2024; 1.000,00 € ;0,00%;-VFW002;;;;;;;
MG ZS HEV LUX MY24;01.10.2024;31.12.2024; 2.500,00 € ;0,00%;-VFW002;;;;;;;
MG ZS HEV STD MY24;01.10.2024;31.12.2024; 1.000,00 € ;0,00%;-VFW002;;;;;;;
MG3 1.5L 5MT STD MY24.5;01.06.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG3 1.5L 5MT COM MY24.5;01.06.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG3 HEV STD;01.06.2024;31.12.2024; 1.000,00 € ;0,00%;-VFW002;;;;;;;
MG3 HEV STD MY24.5;01.06.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG3 HEV COM;01.06.2024;31.12.2024; 1.250,00 € ;0,00%;-VFW002;;;;;;;
MG3 HEV COM MY24.5;01.06.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG3 HEV LUX;01.06.2024;31.12.2024; 2.000,00 € ;0,00%;-VFW002;;;;;;;
MG3 HEV LUX MY24.5;01.06.2024;31.12.2024; -   € ;0,00%;;;;;;;;
MG HS AT COM MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG HS AT LUX MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG HS MT COM MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG HS MT LUX MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG HS PHEV COM MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG HS PHEV LUX MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG ZS 1.5L 5MT COM MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG ZS 1.5L 5MT LUX MY24;01.01.2025;30.06.2025; -   € ;;;;;;;;;
MG ZS 1.5L 5MT STD MY24;01.01.2025;30.06.2025; -   € ;0,00%;;;;;;;;
MG ZS HEV COM MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG ZS HEV LUX MY24;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG ZS HEV STD MY24;01.01.2025;30.06.2025; -   € ;0,00%;;;;;;;;
MG3 1.5L 5MT STD MY24.5;01.01.2025;30.06.2025; -   € ;0,00%;;;;;;;;
MG3 1.5L 5MT COM MY24.5;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG3 HEV STD;01.01.2025;30.06.2025; -   € ;0,00%;;;;;;;;
MG3 HEV STD MY24.5;01.01.2025;30.06.2025; -   € ;0,00%;;;;;;;;
MG3 HEV COM;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG3 HEV COM MY24.5;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG3 HEV LUX;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;
MG3 HEV LUX MY24.5;01.01.2025;30.06.2025; -   € ;2,00%;-VFW001;;;;;;;"""

@st.cache_data
def load_data():
    df_fahrzeuge = pd.read_csv(StringIO(data_fahrzeuge))
    df_vfw = pd.read_csv(StringIO(data_vfw))
    df_bonus = pd.read_csv(StringIO(data_bonus))
    df_endkunde = pd.read_csv(StringIO(data_endkunde))
    df_fleet = pd.read_csv(StringIO(data_fleet))
    df_fruhling = pd.read_csv(StringIO(data_fruhling))
    df_hybrid = pd.read_csv(StringIO(data_hybrid))
    df_loan = pd.read_csv(StringIO(data_loan))
    df_mg3 = pd.read_csv(StringIO(data_mg3))

    # 轉換日期格式
    for df in [df_vfw, df_bonus, df_endkunde, df_fleet, df_fruhling, df_hybrid, df_loan, df_mg3]:
        if 'Start' in df.columns:
            df['Start'] = pd.to_datetime(df['Start'])
        if 'Ende' in df.columns:
            df['Ende'] = pd.to_datetime(df['Ende'])
        if 'Product Name' in df.columns:
            df['Product Name'] = df['Product Name'].str.strip().str.lower()

    return df_fahrzeuge, df_vfw, df_bonus, df_endkunde, df_fleet, df_fruhling, df_hybrid, df_loan, df_mg3

(df_fahrzeuge, df_vfw, df_bonus, df_endkunde, df_fleet, df_fruhling, df_hybrid, df_loan, df_mg3) = load_data()

# 🧮 價格計算類別
class VehiclePriceCalculator:
    def __init__(self, df_vehicles, *dfs):
        self.df_vehicles = df_vehicles
        self.dfs = {df.name: df for df in dfs if hasattr(df, 'name')}
        
    def get_base_price(self, vehicle_name):
        vehicle_name = vehicle_name.strip()
        match = self.df_vehicles[self.df_vehicles["Product Name"] == vehicle_name]
        
        if match.empty:
            return None
        
        price = match["List price"].values[0]
        if price == "-":
            return None
        
        try:
            return float(price)
        except (ValueError, TypeError):
            return None
    
    def calculate_total_price(self, vehicle_name, color_option):
        base_price = self.get_base_price(vehicle_name)
        if base_price is None:
            return None
        
        color_price = 546.22 if color_option == "with color" else 0
        return round(base_price + color_price, 2)
    
    def calculate_test_drive_bonus(self, vehicle_name, is_test_drive, first_reg_date_str, vehicle_price):
        """計算試乘車補貼 (VFW) - 修正版本"""
        if is_test_drive.lower() != "yes":
            return 0
        
        try:
            # 解析日期為Excel兼容格式
            first_reg_date = pd.to_datetime(first_reg_date_str, dayfirst=True)
            excel_date_format = first_reg_date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            st.warning(f"⚠️ 日期解析錯誤: {e}")
            return 0
        
        # 標準化車型名稱
        vehicle_name = vehicle_name.strip().lower()
        
        try:
            # 查找百分比補貼 (完全按照Excel邏輯)
            mask = (
                (df_vfw["Product Name"].str.strip().str.lower() == vehicle_name) &
                (df_vfw["Start"].astype(str) <= excel_date_format) &
                (df_vfw["Ende"].astype(str) >= excel_date_format)
            )
            
            # 獲取百分比補貼 (E列)
            bonus_percent = df_vfw.loc[mask, "Bonus [%]"].sum()
            
            if bonus_percent > 0:
                return round(vehicle_price * bonus_percent, 2)
            
            return 0
        except Exception as e:
            st.error(f"試乘車補貼計算錯誤: {e}")
            return 0
    
    def calculate_registration_bonus(self, vehicle_name, reg_date_str, vehicle_price):
        """計算註冊補貼 (Bonus)"""
        try:
            reg_date = datetime.strptime(reg_date_str, "%d.%m.%Y")
        except ValueError:
            return 0
        
        vehicle_name = vehicle_name.strip().lower()
        
        # 獲取註冊補貼百分比 (Zulassungsbonus + Marketingbonus)
        bonus_percent = df_bonus[
            (df_bonus["Product Name"].str.strip().str.lower() == vehicle_name) &
            (df_bonus["Start"] <= reg_date) &
            (df_bonus["Ende"] >= reg_date)
        ][["Zulassungsbonus [%]", "Marketingbonus [%]"]].sum().sum()
        
        if bonus_percent > 0:
            return round(vehicle_price * bonus_percent, 2)
        return 0
    
    def calculate_endkunde_bonus(self, vehicle_name, contract_date_str):
        """計算終端客戶補貼"""
        try:
            contract_date = datetime.strptime(contract_date_str, "%d.%m.%Y")
        except ValueError:
            return 0
        
        vehicle_name = vehicle_name.strip().lower()
        
        bonus = df_endkunde[
            (df_endkunde["Product Name"].str.strip().str.lower() == vehicle_name) &
            (df_endkunde["Start"] <= contract_date) &
            (df_endkunde["Ende"] >= contract_date)
        ]["Bonus [€]"].sum()
        
        return round(bonus, 2)
    
    def calculate_fleet_bonus(self, vehicle_name, fleet_size, contract_date_str, vehicle_price):
        """計算車隊客戶補貼"""
        if fleet_size == "N/A":
            return 0
        
        try:
            contract_date = datetime.strptime(contract_date_str, "%d.%m.%Y")
        except ValueError:
            return 0
        
        vehicle_name = vehicle_name.strip().lower()
        
        # 獲取車隊補貼百分比
        bonus_percent = df_fleet[
            (df_fleet["Product Name"].str.strip().str.lower() == vehicle_name) &
            (df_fleet["Fleet Size"] == fleet_size.upper()) &
            (df_fleet["Start"] <= contract_date) &
            (df_fleet["Ende"] >= contract_date)
        ]["Bonus [%]"].sum()
        
        if bonus_percent > 0:
            return round(vehicle_price * bonus_percent, 2)
        return 0
    
    def calculate_loan_bonus(self, vehicle_name, purchase_type, contract_date_str):
        """計算貸款/租賃補貼"""
        if purchase_type.lower() not in ["loan"]:
            return 0
        
        try:
            contract_date = datetime.strptime(contract_date_str, "%d.%m.%Y")
        except ValueError:
            return 0
        
        vehicle_name = vehicle_name.strip().lower()
        
        bonus = df_loan[
            (df_loan["Product Name"].str.strip().str.lower() == vehicle_name) &
            (df_loan["Start"] <= contract_date) &
            (df_loan["Ende"] >= contract_date)
        ]["Bonus [€]"].sum()
        
        return round(bonus, 2)
    
    def calculate_special_bonus(self, vehicle_name, extra_bonus_type, contract_date_str, reg_date_str):
        """計算特殊活動補貼"""
        if extra_bonus_type == "N/A":
            return 0
        
        try:
            contract_date = datetime.strptime(contract_date_str, "%d.%m.%Y")
            reg_date = datetime.strptime(reg_date_str, "%d.%m.%Y")
        except ValueError:
            return 0
        
        vehicle_name = vehicle_name.strip().lower()
        
        # 春季促銷補貼
        if extra_bonus_type == "Frühlingserwachen":
            bonus = df_fruhling[
                (df_fruhling["Product Name"].str.strip().str.lower() == vehicle_name) &
                (df_fruhling["Start"] <= contract_date) &
                (df_fruhling["Ende"] >= contract_date) &
                (reg_date <= datetime(2025, 3, 31))
            ]["Bonus €]"].sum()
            return round(bonus, 2)
        
        # 混合動力周補貼
        elif extra_bonus_type == "Hybridwochen":
            bonus = df_hybrid[
                (df_hybrid["Product Name"].str.strip().str.lower() == vehicle_name) &
                (df_hybrid["Start"] <= contract_date) &
                (df_hybrid["Ende"] >= contract_date) &
                (reg_date <= datetime(2025, 4, 30))
            ]["Bonus €]"].sum()
            return round(bonus, 2)
        
        # MG3特別補貼
        elif extra_bonus_type == "MG3":
            bonus = df_mg3[
                (df_mg3["Product Name"].str.strip().str.lower() == vehicle_name) &
                (df_mg3["Start"] <= contract_date) &
                (df_mg3["Ende"] >= contract_date)
            ]["Bonus €]"].sum()
            return round(bonus, 2)
        
        return 0

# 🌐 Streamlit 用戶界面
st.title("🚗 MG 車輛價格與補貼計算系統 (完整修正版)")
st.write("全面計算車輛價格與各類補貼金額，包含試乘車補貼、註冊補貼、特殊活動補貼等。")

with st.form("main_form"):
    # 基本資訊
    col1, col2 = st.columns(2)
    with col1:
        vehicle_options = df_fahrzeuge[df_fahrzeuge["List price"] != "-"]["Product Name"].tolist()
        selected_vehicle = st.selectbox("📌 選擇車型", vehicle_options, index=vehicle_options.index("MG HS PHEV LUX MY24") if "MG HS PHEV LUX MY24" in vehicle_options else 0)
    with col2:
        color_option = st.radio("🎨 外觀顏色", ["with color", "without color"], index=0, horizontal=True)
    
    # 日期資訊
    col1, col2 = st.columns(2)
    with col1:
        first_reg_date = st.text_input("📅 首次註冊日期 (DD.MM.YYYY)", "12.01.2025")
    with col2:
        reg_date = st.text_input("📅 計劃註冊日期 (DD.MM.YYYY)", "31.03.2025")
    
    contract_date = st.text_input("📅 合約日期 (DD.MM.YYYY)", "20.03.2025")
    
    # 其他條件
    col1, col2, col3 = st.columns(3)
    with col1:
        is_test_drive = st.radio("🧪 是否為試乘車", ["yes", "no"], index=1, horizontal=True)
    with col2:
        customer_type = st.selectbox("👥 客戶類型", ["Private", "Fleet"], index=1)
    with col3:
        if customer_type == "Fleet":
            fleet_size = st.selectbox("📊 車隊規模", ["SMALL", "MEDIUM", "LARGE"], index=0)
        else:
            fleet_size = "N/A"
    
    purchase_type = st.radio("💳 購買方式", ["Outright Purchase", "Loan", "Leasing"], index=0, horizontal=True)
    
    extra_bonus_type = st.selectbox("🎁 特別促銷活動", ["N/A", "Frühlingserwachen", "Hybridwochen", "MG3"], index=3)
    
    submitted = st.form_submit_button("計算總價")

if submitted:
    calculator = VehiclePriceCalculator(df_fahrzeuge, df_vfw, df_bonus, df_endkunde, 
                                      df_fleet, df_fruhling, df_hybrid, df_loan, df_mg3)
    
    # 計算基礎價格
    base_price = calculator.get_base_price(selected_vehicle)
    if base_price is None:
        st.error("❌ 無法獲取此車型的基礎價格")
        st.stop()
    
    total_price = calculator.calculate_total_price(selected_vehicle, color_option)
    
    # 計算各類補貼
    test_drive_bonus = calculator.calculate_test_drive_bonus(selected_vehicle, is_test_drive, first_reg_date, total_price)
    reg_bonus = calculator.calculate_registration_bonus(selected_vehicle, reg_date, total_price)
    endkunde_bonus = calculator.calculate_endkunde_bonus(selected_vehicle, contract_date)
    fleet_bonus = calculator.calculate_fleet_bonus(selected_vehicle, fleet_size, contract_date, total_price) if customer_type == "Fleet" else 0
    loan_bonus = calculator.calculate_loan_bonus(selected_vehicle, purchase_type, contract_date)
    special_bonus = calculator.calculate_special_bonus(selected_vehicle, extra_bonus_type, contract_date, reg_date)
    
    # 顯示結果
    st.divider()
    st.subheader("💰 價格明細")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("基礎價格", f"{base_price:,.2f} €")
        st.metric("顏色加價", f"{546.22 if color_option == 'with color' else 0:,.2f} €")
    with col2:
        st.metric("車輛總價", f"{total_price:,.2f} €", delta=f"{(546.22 if color_option == 'with color' else 0):,.2f} €")
    
    st.divider()
    st.subheader("🎁 補貼明細")
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("試乘車補貼", f"{test_drive_bonus:,.2f} €")
        st.metric("註冊補貼", f"{reg_bonus:,.2f} €")
    with cols[1]:
        st.metric("終端客戶補貼", f"{endkunde_bonus:,.2f} €")
        st.metric("車隊補貼" if customer_type == "Fleet" else "車隊補貼 (不適用)", f"{fleet_bonus:,.2f} €")
    with cols[2]:
        st.metric("貸款/租賃補貼", f"{loan_bonus:,.2f} €")
        st.metric(f"特別促銷 ({extra_bonus_type})", f"{special_bonus:,.2f} €")
    
    # 計算總價
    total_bonus = test_drive_bonus  + endkunde_bonus + fleet_bonus + loan_bonus + special_bonus
    subtotal = total_price - total_bonus
    tax = subtotal * 0.19
    grand_total = subtotal + tax
    
    st.divider()
    st.subheader("🧮 最終價格")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("總補貼金額", f"{total_bonus:,.2f} €")
    with col2:
        st.metric("小計 (淨額)", f"{subtotal:,.2f} €")
    with col3:
        st.metric("稅金 (19%)", f"{tax:,.2f} €")
    
    st.success(f"## 總價 (含稅): {grand_total:,.2f} €")

# 顯示參考資料
with st.expander("📊 參考資料"):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "車輛價格", "試乘車補貼", "註冊補貼", "終端客戶補貼", 
        "車隊補貼", "春季促銷", "混合動力周", "貸款/租賃"
    ])
    
    with tab1:
        st.dataframe(df_fahrzeuge)
    with tab2:
        st.dataframe(df_vfw)
    with tab3:
        st.dataframe(df_bonus)
    with tab4:
        st.dataframe(df_endkunde)
    with tab5:
        st.dataframe(df_fleet)
    with tab6:
        st.dataframe(df_fruhling)
    with tab7:
        st.dataframe(df_hybrid)
    with tab8:
        st.dataframe(df_loan)

with st.expander("ℹ️ 計算邏輯說明"):
    st.write("""
    ### 完整計算規則
    
    1. **基礎價格計算**：
       - 從 Fahrzeuge 表獲取車輛基礎價格
       - 顏色加價：546.22 € (選擇 "with color" 時)
    
    2. **試乘車補貼 (VFW)**：
       - 僅當標記為 "yes" 時計算
       - 從 Konditionen_VFW 表的 "Bonus [%]" 列獲取百分比補貼
       - 計算公式：車輛總價 × 補貼百分比
       - 必須在優惠有效期內 (Start ≤ 首次註冊日期 ≤ Ende)
    
    3. **註冊補貼 (Bonus)**：
       - 從 Konditionen_Bonus 表獲取百分比補貼 (Zulassungsbonus + Marketingbonus)
       - 計算公式：車輛總價 × (補貼百分比)
       - 必須在優惠有效期內 (Start ≤ 註冊日期 ≤ Ende)
    
    4. **終端客戶補貼**：
       - 從 Konditionen_Endkundenprämie 表獲取固定金額補貼
       - 必須在優惠有效期內 (Start ≤ 合約日期 ≤ Ende)
    
    5. **車隊客戶補貼**：
       - 僅當客戶類型為 "Fleet" 時計算
       - 從 Konditionen_FLEET 表獲取百分比補貼
       - 計算公式：車輛總價 × (補貼百分比)
       - 必須在優惠有效期內 (Start ≤ 合約日期 ≤ Ende)
    
    6. **貸款/租賃補貼**：
       - 從 Konditionen_Loan 表獲取固定金額補貼
       - 必須在優惠有效期內 (Start ≤ 合約日期 ≤ Ende)
    
    7. **特別促銷補貼**：
       - 春季促銷 (Frühlingserwachen): 需在 2025-03-31 前註冊
       - 混合動力周 (Hybridwochen): 需在 2025-04-30 前註冊
       - MG3特別補貼: 需在指定日期範圍內簽約
    
    8. **稅金計算**：
       - 小計 = 車輛總價 - 所有補貼
       - 稅金 = 小計 × 19%
       - 總價 = 小計 + 稅金
    """)