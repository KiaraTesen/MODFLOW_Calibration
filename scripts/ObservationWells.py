# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 15:48:58 2021
@author: Kiara Tesen
"""
import win32com.client as win32

WEAP = win32.Dispatch("WEAP.WEAPApplication")

WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW"
WEAP.ActiveScenario = WEAP.Scenarios("Current Accounts")

WEAP.Branch('\Key Assumptions\MODFLOW\ObservationWells').AddChildren("OW22,OW29,OW35,OW36,OW43,OW48,OW51,OW83,OW87,OW97,OW100,OW157,OW159,OW167,OW169,OW181,OW188,OW209,OW233,OW234,OW235,OW236,OW237,OW238,OW239,OW240,OW241,OW242,OW243,OW244,OW249")

WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW22').Variables(1).Expression = 'ModflowCellHead(1,75,145)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW29').Variables(1).Expression = 'ModflowCellHead(1,80,96)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW35').Variables(1).Expression = 'ModflowCellHead(1,74,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW36').Variables(1).Expression = 'ModflowCellHead(1,80,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW43').Variables(1).Expression = 'ModflowCellHead(1,77,53)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW48').Variables(1).Expression = 'ModflowCellHead(1,79,40)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW51').Variables(1).Expression = 'ModflowCellHead(1,74,19)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW83').Variables(1).Expression = 'ModflowCellHead(1,52,103)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW87').Variables(1).Expression = 'ModflowCellHead(1,45,75)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW97').Variables(1).Expression = 'ModflowCellHead(1,45,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW100').Variables(1).Expression = 'ModflowCellHead(1,55,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW157').Variables(1).Expression = 'ModflowCellHead(1,26,75)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW159').Variables(1).Expression = 'ModflowCellHead(1,23,59)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW167').Variables(1).Expression = 'ModflowCellHead(1,29,68)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW169').Variables(1).Expression = 'ModflowCellHead(1,29,59)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW181').Variables(1).Expression = 'ModflowCellHead(1,35,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW188').Variables(1).Expression = 'ModflowCellHead(1,36,71)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW209').Variables(1).Expression = 'ModflowCellHead(1,32,49)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW233').Variables(1).Expression = 'ModflowCellHead(1,16,62)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW234').Variables(1).Expression = 'ModflowCellHead(1,16,63)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW235').Variables(1).Expression = 'ModflowCellHead(1,19,62)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW236').Variables(1).Expression = 'ModflowCellHead(1,21,57)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW237').Variables(1).Expression = 'ModflowCellHead(1,20,57)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW238').Variables(1).Expression = 'ModflowCellHead(1,21,56)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW239').Variables(1).Expression = 'ModflowCellHead(1,21,57)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW240').Variables(1).Expression = 'ModflowCellHead(1,22,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW241').Variables(1).Expression = 'ModflowCellHead(1,22,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW242').Variables(1).Expression = 'ModflowCellHead(1,23,58)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW243').Variables(1).Expression = 'ModflowCellHead(1,20,62)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW244').Variables(1).Expression = 'ModflowCellHead(1,20,63)'
WEAP.Branch('\\Key Assumptions\\MODFLOW\\ObservationWells\\OW249').Variables(1).Expression = 'ModflowCellHead(1,19,23)'
