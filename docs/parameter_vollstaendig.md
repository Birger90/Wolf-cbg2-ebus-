# Vollständige Parameterliste (Wolf-Datenbank, ism7mqtt)

Erzeugt von `tools/wolf_db_export.py`. Spalte Status: core = in den handgepflegten CSV, ext = in ext_*.csv, sonst Grund für Nichtübernahme.
Stand: core 333, ext 96, nicht übernommen 478.

## CGB-2 → hc (Adresse 08)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 180175 | PRELOAD_Firmware | US | 410 | core (`Firmware`) |
| 180176 | PRELOAD_Herstellwoche | US | 10877 | ext (`x_PRELOAD_Herstellwoche`) |
| 180177 | PRELOAD_Herstelljahr | US | 10878 | ext (`x_PRELOAD_Herstelljahr`) |
| 180178 | PRELOAD_Seriennummer | UINT32 | 10880 | ext (`x_PRELOAD_Seriennummer_lo`) |
| 180178 | PRELOAD_Seriennummer | UINT32 | 10879 | ext (`x_PRELOAD_Seriennummer_hi`) |
| 180162 | BUSCONFIG_Ausgang-A1 | US | 2751 | core (`Hg14`) |
| 180156 | BUSCONFIG_Ausgang-A3 | US | 10804 | ext (`x_BUSCONFIG_Ausgang_A3`) |
| 180157 | BUSCONFIG_Ausgang-A4 | US | 10805 | ext (`x_BUSCONFIG_Ausgang_A4`) |
| 180140 | BUSCONFIG_Warmwasserkonfiguration | US | 10075 | ext (`x_BUSCONFIG_Warmwasserkonfiguration`) |
| 180149 | BUSCONFIG_Anlagenkonfiguration | US | 10033 | ext (`x_BUSCONFIG_Anlagenkonfiguration`) |
| 180150 | BUSCONFIG_Anschluss-Speicher | US | 10017 | core (`Hg61raw`) |
| 180141 | Typ | US | 328 | ext (`x_Typ`) |
| 180142 | Betriebsart | US | 10067 | core (`Betriebsart`) |
| 180143 | Brennerstatus | US | 10068 | core (`Brennerstatus`) |
| 180154 | Kesselsolltemperatur | SS10 | 2 | core (`Flowtempdesired`) |
| 180005 | Kesseltemperatur | SS10 | 13 | core (`Flowtemp`) |
| 180048 | Sammlertemperatur | SS10 | 10007 | ext (`x_Sammlertemperatur`) |
| 180151 | 0 - 10 V GLT | SS10 | 10008 | ext (`x_0_10_V_GLT`) |
| 180016 | Brenner | US | 370 | ext (`x_Brenner`) |
| 180012 | Modulationsgrad | US | 367 | core (`Modulation`) |
| 180025 | Heizkreispumpe | US | 371 | core (`Outputs`) |
| 180110 | Drehzahl Heizkreispumpe | US | 10071 | core (`Pumpspeed`) |
| 180028 | Speicherladepumpe | US | 371 | core (`Outputs`) |
| 180026 | 3-Wege-Ventil | US | 371 | core (`Outputs`) |
| 180051 | Anlagendruck | SS100 | 10010 | core (`Pressure`) |
| 180155 | Warmwassersolltemperatur | SS10 | 3 | core (`Hwctempdesired`) |
| 180006 | Warmwassertemperatur | SS10 | 14 | core (`Hwctemp`) |
| 180050 | Auslauftemperatur Warmwasser | SS100 | 10009 | ext (`x_Auslauftemperatur_Warmwasser`) |
| 180010 | Durchfluss Warmwasser | SS10 | 364 | core (`Hwcflow`) |
| 180145 | Außentemperatur | SS10 | 12 | core (`Outsidetemp`) |
| 180054 | Abgastemperatur | SS10 | 10013 | core (`Exhausttemp`) |
| 180008 | Rücklauftemperatur | SS10 | 22 | core (`Returntemp`) |
| 180102 | IO-Istwert | US | 10063 | ext (`x_IO_Istwert`) |
| 180033 | Anzahl Brennerstarts | UINT32 | 550 | core (`BurnerStartsLow`) |
| 180033 | Anzahl Brennerstarts | UINT32 | 551 | core (`BurnerStartsHigh`) |
| 180035 | Brennerbetriebsstunden | US | 554 | core (`BurnerHours`) |
| 180034 | Netzbetriebsstunden | UINT32 | 552 | core (`NetHoursLow`) |
| 180034 | Netzbetriebsstunden | UINT32 | 553 | core (`NetHoursHigh`) |
| 180148 | Anzahl Netz-Starts | US | 10078 | core (`NetStarts`) |
| 180027 | Ausgang A1 | US | 371 | core (`Outputs`) |
| 180146 | Eingang E1 | US | 10006 | ext (`x_Eingang_E1`) |
| 180152 | Sicherheitstemperaturbegrenzer | US | 633 | core (`Stb`) |
| 180032 | Firmware | SS100 | 410 | core (`Firmware`) |
| 180158 | Herstellwoche | US | 10877 | doppelt (gleiche TN wie `x_PRELOAD_Herstellwoche`) |
| 180159 | Herstelljahr | US | 10878 | doppelt (gleiche TN wie `x_PRELOAD_Herstelljahr`) |
| 180160 | Seriennummer | UINT32 | 10880 | doppelt (gleiche TN wie `x_PRELOAD_Seriennummer_lo`) |
| 180160 | Seriennummer | UINT32 | 10879 | doppelt (gleiche TN wie `x_PRELOAD_Seriennummer_hi`) |
| 180161 | Status EA-Modul | US | 10833 | ext (`x_Status_EA_Modul`) |
| 180171 | Ausgang A3 | US | 371 | core (`Outputs`) |
| 180172 | Ausgang A4 | US | 371 | core (`Outputs`) |
| 180163 | Eingang E3 | US | 10806 | ext (`x_Eingang_E3`) |
| 180164 | Eingang E4 | US | 10807 | ext (`x_Eingang_E4`) |
| 180153 | Warmwasser Schnellstart | US | 10096 | ext (`x_Warmwasser_Schnellstart`) |
| 180113 | Schaltdifferenz Brenner | SS10 | 34 | core (`Hg01`) |
| 180114 | Untere Brennerleistung | US | 346 | core (`Hg02`) |
| 180115 | Obere Brennerleistung Warmwasser | US | 345 | core (`Hg03`) |
| 180116 | Obere Brennerleistung Heizung | US | 319 | core (`Hg04`) |
| 180117 | Nachlaufzeit Kesselkreispumpen | US | 322 | core (`Hg07`) |
| 180118 | Kesselmaximaltemperatur HZ TV-max | SS10 | 644 | core (`Hg08`) |
| 180119 | Brennertaktsperre Heizbetrieb | US | 323 | core (`Hg09`) |
| 180120 | eBus-Adresse | US | 376 | core (`Hg10`) |
| 180121 | Gasart | US | 363 | core (`Hg12`) |
| 180122 | Funktion Eingang E1 | US | 2651 | core (`Hg13`) |
| 180123 | Funktion Ausgang A1 | US | 2751 | core (`Hg14`) |
| 180124 | Speicherhysterese | SS10 | 320 | core (`Hg15`) |
| 180125 | Pumpenleistung HK minimal | US | 341 | core (`Hg16`) |
| 180126 | Pumpenleistung HK maximal | US | 342 | core (`Hg17`) |
| 180127 | Nachlaufzeit Speicherladepumpe | US | 383 | core (`Hg19`) |
| 180128 | Max. Speicherladezeit | US | 384 | core (`Hg20`) |
| 180129 | Kesselminimaltemperatur TK-min | SS10 | 31 | core (`Hg21`) |
| 180130 | Kesselmaximaltemperatur TK-max | SS10 | 39 | core (`Hg22`) |
| 180131 | Kesselübertemperatur bei Speicherladung | SS10 | 45 | core (`Hg25`) |
| 180132 | Laufzeit Brennerhysterese | US | 33 | core (`Hg33`) |
| 180133 | eBus Einspeisung | US | 65019 | core (`Hg34raw`) |
| 180134 | Typ Pumpenregelung | US | 10041 | core (`Hg37`) |
| 180135 | Soll-Spreizung dT Pumpenregelung | SS10 | 1486 | core (`Hg38`) |
| 180136 | Zeit Softstart | US | 339 | core (`Hg39`) |
| 180137 | Anlagenkonfiguration | US | 10076 | core (`Hg40`) |
| 180138 | Drehzahl ZHP WW | US | 10014 | core (`Hg41`) |
| 180139 | Hysterese Sammler | SS10 | 10030 | core (`Hg42`) |
| 180068 | Kesselübertemperatur Sammler | SS10 | 10028 | core (`Hg46`) |
| 180165 | Funktion Eingang E3 | US | 10802 | core (`FuncE3`) |
| 180166 | Funktion Eingang E4 | US | 10803 | core (`FuncE4`) |
| 180167 | Funktion Ausgang A3 | US | 10804 | doppelt (gleiche TN wie `x_BUSCONFIG_Ausgang_A3`) |
| 180168 | Funktion Ausgang A4 | US | 10805 | doppelt (gleiche TN wie `x_BUSCONFIG_Ausgang_A4`) |
| 180169 | Minimale Schalthysterese Brenner | SS10 | 10808 | core (`Hg60`) |
| 180170 | WW Regelung | US | 10017 | core (`Hg61raw`) |
| 180179 | Anlagenkorrekturfaktor | SS100 | 10887 | core (`Hg62`) |
| 180180 | erweiterte Statistik aktiv | US | 10888 | ext (`x_erweiterte_Statistik_aktiv`) |
| 180181 | Energiemenge HZ | UINT32 | 12399 | ext (`x_Energiemenge_HZ_lo`) |
| 180181 | Energiemenge HZ | UINT32 | 12400 | ext (`x_Energiemenge_HZ_hi`) |
| 180182 | Energiemenge WW | UINT32 | 12410 | ext (`x_Energiemenge_WW_lo`) |
| 180182 | Energiemenge WW | UINT32 | 12411 | ext (`x_Energiemenge_WW_hi`) |
| 180183 | Verbrauch aktueller Tag | US | 10881 | core (`EnergyToday`) |
| 180184 | Erzeugte Wärmemenge aktueller Tag | US | 10882 | core (`HeatToday`) |
| 180185 | Verbrauch Vortag | US | 13048 | core (`EnergyYesterday`) |
| 180186 | Erzeugte Wärmemenge Vortag | US | 13049 | core (`HeatYesterday`) |
| 180187 | Verbrauch aktuelles Jahr | UINT32 | 10885 | ext (`x_Verbrauch_aktuelles_Jahr_lo`) |
| 180187 | Verbrauch aktuelles Jahr | UINT32 | 10886 | ext (`x_Verbrauch_aktuelles_Jahr_hi`) |
| 180188 | Erzeugte Wärmemenge aktuelles Jahr | UINT32 | 10891 | ext (`x_Erzeugte_Waermemenge_aktuelles_Jahr_lo`) |
| 180188 | Erzeugte Wärmemenge aktuelles Jahr | UINT32 | 10892 | ext (`x_Erzeugte_Waermemenge_aktuelles_Jahr_hi`) |
| 180189 | Verbrauch Vorjahr | UINT32 | 10893 | ext (`x_Verbrauch_Vorjahr_lo`) |
| 180189 | Verbrauch Vorjahr | UINT32 | 10894 | ext (`x_Verbrauch_Vorjahr_hi`) |
| 180190 | Erzeugte Wärmemenge Vorjahr | UINT32 | 10895 | ext (`x_Erzeugte_Waermemenge_Vorjahr_lo`) |
| 180190 | Erzeugte Wärmemenge Vorjahr | UINT32 | 10896 | ext (`x_Erzeugte_Waermemenge_Vorjahr_hi`) |
| 180191 | Verbrauch Vorvorjahr | UINT32 | 10897 | ext (`x_Verbrauch_Vorvorjahr_lo`) |
| 180191 | Verbrauch Vorvorjahr | UINT32 | 10898 | ext (`x_Verbrauch_Vorvorjahr_hi`) |
| 180192 | Erzeugte Wärmemenge Vorvorjahr | UINT32 | 10899 | ext (`x_Erzeugte_Waermemenge_Vorvorjahr_lo`) |
| 180192 | Erzeugte Wärmemenge Vorvorjahr | UINT32 | 10900 | ext (`x_Erzeugte_Waermemenge_Vorvorjahr_hi`) |

## BM-2 → bm2 (Adresse 35)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 220043 | BUSCONFIG_Erkannte-Geraete-Low-Byte | US | 10163 | ext (`x_BUSCONFIG_Erkannte_Geraete_Low_Byte`) |
| 220044 | BUSCONFIG_Erkannte-Geraete-High-Byte | US | 10162 | ext (`x_BUSCONFIG_Erkannte_Geraete_High_Byte`) |
| 220045 | BUSCONFIG_Softwareversion | US | 10185 | ext (`x_BUSCONFIG_Softwareversion`) |
| 220046 | BUSCONFIG_Sollwertkorrektur | SS10 | 10165 | core (`HkSetpointcorr`) |
| 220129 | BUSCONFIG_SmartHome-System | US | 10920 | ext (`x_BUSCONFIG_SmartHome_System`) |
| 220107 | BUSCONFIG_Vereinfachter-Modus | US | 10812 | ext (`x_BUSCONFIG_Vereinfachter_Modus`) |
| 220130 | BUSCONFIG_Programmwahlschalter-Gemeinsam | US | 10130 | core (`CommonSwitch`) |
| 220001 | Funktion des Bedienmoduls | US | 10121 | core (`BmFunction`) |
| 220103 | Außentemperatur | SS10 | 10195 | core (`Outsidetemp`) |
| 220032 | Uhrzeit | BM2Time | 10161 | core (`Time`) |
| 220033 | Datum | BM2Date | 10160 | core (`Date`) |
| 220105 | Wartung Betriebsabhängig | US | 5249 | core (`Maintenance`) |
| 220106 | Wartung Datumsabhängig Fälligkeitsdatum | BM2Date | 5250 | core (`MaintenanceDate`) |
| 220141 | Winter-/Sommerzeitumstellung | US | 10102 | core (`DstAuto`) |
| 220134 | Firmware | SS100 | 10185 | doppelt (gleiche TN wie `x_BUSCONFIG_Softwareversion`) |
| 220021 | Raumeinflussfaktor | US | 271 | core (`RoomFactor`) |
| 220022 | Außenfühler gemittelt Berechnungszeitraum | US | 388 | core (`AvgPeriod`) |
| 220117 | Anpassung Raumfühler BM-2 0 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220118 | Anpassung Raumfühler BM-2 1 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220119 | Anpassung Raumfühler BM-2 2 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220120 | Anpassung Raumfühler BM-2 3 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220121 | Anpassung Raumfühler BM-2 4 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220122 | Anpassung Raumfühler BM-2 5 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220123 | Anpassung Raumfühler BM-2 6 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220124 | Anpassung Raumfühler BM-2 7 | SS10 | 265 | core (`RoomSensorAdj`) |
| 220023 | Antilegionellenfunktion | US | 257 | core (`Antilegionella`) |
| 220104 | Wartungsmeldung | US | 618 | core (`MaintenanceMode`) |
| 220025 | Freigabe Parallelbetrieb | US | 35 | core (`ParallelMode`) |
| 220026 | Raumtemperaturabhängige Abschaltung | US | 701 | core (`RoomShutdown`) |
| 220027 | Absenkstopp | SS10 | 702 | core (`Absenkstopp`) |
| 220028 | Warmwasserminimaltemperatur | SS10 | 408 | core (`WwMin`) |
| 220126 | Korrektur Außentemperatur | SS10 | 1443 | core (`OutsideCorr`) |
| 220127 | Reiner Raumregler | US | 20018 | core (`PureRoomControl`) |
| 220029 | PI-Regler Raumtemperatur Kp | US | 41 | core (`RoomPiKp`) |
| 220132 | PI-Regler Raumtemperatur Kp | US | 41 | core (`RoomPiKp`) |
| 220030 | PI-Regler Raumtemperatur Tn | SS10 | 42 | core (`RoomPiTn`) |
| 220133 | PI-Regler Raumtemperatur Tn | SS10 | 42 | core (`RoomPiTn`) |
| 220031 | Startzeit Antilegionellenfunktion | BM2Time | 10141 | core (`AntilegionellaStart`) |
| 220108 | Programmwahlschalter gemeinsam | US | 10130 | core (`CommonSwitch`) |
| 220128 | Wartungsmeldung Datum | BM2Date | 5264 | core (`MaintenanceMsgDate`) |
| 220095 | Freigabe SmartHome | US | 10912 | core (`SmarthomeEnable`) |
| 220019 | Zeitprogramm Zirkulation Heizgerät | US | 10157 | core (`CircTimeprogram`) |
| 320042 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320043 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320044 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320045 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320046 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320047 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320048 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320049 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320050 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320051 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320052 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320053 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320054 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320055 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320056 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320057 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320058 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320059 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320060 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320061 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320062 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 220047 | Zeitprogramm Zirkulation Heizgerät | – | – | kein Konverter |
| 220048 | Zeitprogramm Zirkulation Heizgerät | – | – | kein Konverter |
| 220042 | 1x Warmwasser | US | 10117 | core (`OneTimeHotwater`) |
| 220034 | Partymodus | US | 10150 | core (`PartyMode`) |
| 330000 | Uhrzeit Ende | BM2Time | 10151 | core (`PartyEnd`) |
| 330001 | Datum Ende | BM2Date | 10152 | core (`PartyEndDate`) |
| 330002 | Uhrzeit Start | BM2Time | 10153 | core (`PartyStart`) |
| 330003 | Datum Start | BM2Date | 10154 | core (`PartyStartDate`) |
| 330004 | Uhrzeit BM2 | BM2Time | 10161 | core (`Time`) |
| 330005 | Datum BM2 | BM2Date | 10160 | core (`Date`) |
| 220035 | Urlaubsmodus | US | 10145 | core (`HolidayMode`) |
| 330006 | Uhrzeit Ende | BM2Time | 10146 | core (`HolidayEnd`) |
| 330007 | Datum Ende | BM2Date | 10147 | core (`HolidayEndDate`) |
| 330008 | Uhrzeit Start | BM2Time | 10148 | core (`HolidayStart`) |
| 330009 | Datum Start | BM2Date | 10149 | core (`HolidayStartDate`) |
| 330010 | Uhrzeit BM2 | BM2Time | 10161 | core (`Time`) |
| 330011 | Datum BM2 | BM2Date | 10160 | core (`Date`) |
| 220036 | Programmwahl Lüftung | SS | 10127 | ext (`x_Programmwahl_Lueftung`) |
| 220135 | Programmwahl Lüftung | SS | 10127 | doppelt (gleiche TN wie `x_Programmwahl_Lueftung`) |
| 220040 | Anforderung Lüftung | SS | 10180 | ext (`x_Anforderung_Lueftung`) |
| 220041 | Status Lüftung | SS | 10181 | ext (`x_Status_Lueftung`) |
| 220136 | Status Filter | SS | 10184 | ext (`x_Status_Filter`) |
| 220037 | Zeitweise Intensivlüftung | SS | 10166 | ext (`x_Zeitweise_Intensivlueftung`) |
| 330012 | Uhrzeit Ende | BM2Time | 10167 | ext (`x_Uhrzeit_Ende`) |
| 330013 | Datum Ende | BM2Date | 10168 | ext (`x_Datum_Ende`) |
| 330014 | Uhrzeit Start | BM2Time | 10169 | ext (`x_Uhrzeit_Start`) |
| 330015 | Datum Start | BM2Date | 10170 | ext (`x_Datum_Start`) |
| 330016 | Uhrzeit BM2 | BM2Time | 10161 | core (`Time`) |
| 330017 | Datum BM2 | BM2Date | 10160 | core (`Date`) |
| 220038 | Zeitweise Feuchteschutz | SS | 10171 | ext (`x_Zeitweise_Feuchteschutz`) |
| 330018 | Uhrzeit Ende | BM2Time | 10172 | ext (`x_Uhrzeit_Ende_10172`) |
| 330019 | Datum Ende | BM2Date | 10173 | ext (`x_Datum_Ende_10173`) |
| 330020 | Uhrzeit Start | BM2Time | 10174 | ext (`x_Uhrzeit_Start_10174`) |
| 330021 | Datum Start | BM2Date | 10175 | ext (`x_Datum_Start_10175`) |
| 330022 | Uhrzeit BM2 | BM2Time | 10161 | core (`Time`) |
| 330023 | Datum BM2 | BM2Date | 10160 | core (`Date`) |
| 220039 | Zeitprogramm Lüftung | SS | 10178 | ext (`x_Zeitprogramm_Lueftung`) |
| 320378 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320379 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320380 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320381 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320382 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320383 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320384 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320385 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320386 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320387 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320388 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320389 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320390 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320391 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320392 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320393 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320394 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320395 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320396 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320397 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320398 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 220051 | Zeitprogramm Lüftung | – | – | kein Konverter |
| 220052 | Zeitprogramm Lüftung | – | – | kein Konverter |
| 220091 | SmartHome System | US | 10920 | doppelt (gleiche TN wie `x_BUSCONFIG_SmartHome_System`) |
| 220092 | Wolf Plug-in Version | US10 | 10921 | ext (`x_Wolf_Plug_in_Version`) |
| 220093 | Winter/Sommer Umschaltung, ECO/ABS | US | 10922 | ext (`x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220096 | Zeitprogramm | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220097 | Raumeinfluss im BM-2 | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220098 | Raumsolltemperatur für BM-2 | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220099 | Vorgabe Sollwertkorrektur von SmartHome | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220100 | Vorgabe absolute Vorlaufsolltemperatur von SmartHome | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220137 | Fernbedienung Lüftung | US | 10922 | doppelt (gleiche TN wie `x_Winter_Sommer_Umschaltung_ECO_ABS`) |
| 220094 | Direkter Heizkreis gesteuert von | US | 10923 | ext (`x_Direkter_Heizkreis_gesteuert_von`) |
| 220101 | Mischerkreis 1 gesteuert von | US | 10923 | doppelt (gleiche TN wie `x_Direkter_Heizkreis_gesteuert_von`) |
| 220102 | Mischerkreis 2 gesteuert von | US | 10923 | doppelt (gleiche TN wie `x_Direkter_Heizkreis_gesteuert_von`) |
| 220138 | Direktes Warmwasser gesteuert von | US | 10923 | doppelt (gleiche TN wie `x_Direkter_Heizkreis_gesteuert_von`) |
| 220139 | Warmwasser 1 gesteuert von | US | 10923 | doppelt (gleiche TN wie `x_Direkter_Heizkreis_gesteuert_von`) |
| 220140 | Warmwasser 2 gesteuert von | US | 10923 | doppelt (gleiche TN wie `x_Direkter_Heizkreis_gesteuert_von`) |
| 220142 | Programmwahl Lüftung SmartHome | SS | 10127 | doppelt (gleiche TN wie `x_Programmwahl_Lueftung`) |

## DHK_BM-2 → bm2 (Adresse 35)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 340033 | Reglertyp | US | 5266 | core (`HkControllertype`) |
| 340025 | CIRCULARSLIDER | – | – | kein Konverter |
| 340026 | Sollwertkorrektur | SS10 | 10165 | core (`HkSetpointcorr`) |
| 340001 | Gemittelte Außentemperatur | SS10 | 10179 | core (`OutsidetempAvg`) |
| 340031 | Sollwertkorrektur | SS10 | 10165 | core (`HkSetpointcorr`) |
| 340027 | CIRCULARSLIDER | – | – | kein Konverter |
| 340028 | Sollwertkorrektur | SS10 | 10165 | core (`HkSetpointcorr`) |
| 340034 | CIRCULARSLIDER | – | – | kein Konverter |
| 340035 | Tagtemperatur | SS10 | 10109 | core (`HkDaytemp`) |
| 340041 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 340037 | CIRCULARSLIDER | – | – | kein Konverter |
| 340038 | Tagtemperatur | SS10 | 10109 | core (`HkDaytemp`) |
| 340042 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 340009 | Tagtemperatur | SS10 | 10109 | core (`HkDaytemp`) |
| 340029 | Programmwahl | US | 10100 | core (`HkProgram`) |
| 340032 | Programmwahl | US | 10100 | core (`HkProgram`) |
| 340030 | Programmwahl | US | 10100 | core (`HkProgram`) |
| 340047 | Programmwahl | US | 9025 | ext (`x_Programmwahl`) |
| 340048 | Programmwahl | US | 9026 | ext (`x_Programmwahl_9026`) |
| 340018 | Sollwertkorrektur AFB | SS10 | 10142 | ext (`x_Sollwertkorrektur_AFB`) |
| 340017 | Programmwahl AFB | US | 274 | ext (`x_Programmwahl_AFB`) |
| 340000 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 340011 | Vorlauftemperatur | SS10 | 10119 | core (`Flowtemp`) |
| 340004 | Anforderung Heizkreis | US | 10155 | core (`HkDemand`) |
| 340005 | Heizkreis Status | US | 10156 | core (`HkStatus`) |
| 340006 | Sparfaktor | SS10 | 10113 | core (`HkSparfaktor`) |
| 340007 | Winter/Sommer Umschaltung | SS10 | 278 | core (`HkWintersummer`) |
| 340008 | ECO/ABS | SS10 | 279 | core (`HkEcoabs`) |
| 340044 | Kreisart | US | 9005 | core (`HkCircuitType`) |
| 340045 | aktuelle Kreisart in Kombination mit Heizgerät | US | 9024 | ext (`x_aktuelle_Kreisart_in_Kombination_mit_Hei`) |
| 340040 | Tagtemperatur | SS10 | 10109 | core (`HkDaytemp`) |
| 340049 | Tagtemperatur Kühlen | SS10 | 10831 | ext (`x_Tagtemperatur_Kuehlen`) |
| 340010 | Raumeinfluss | US | 651 | core (`HkRoomInfluence`) |
| 340050 | Raumeinfluss Kühlen | US | 9007 | ext (`x_Raumeinfluss_Kuehlen`) |
| 340012 | Sockeltemperatur Heizkurve | SS10 | 10107 | core (`HkCurveBasetemp`) |
| 340013 | Startpunkt Heizkurve | SS10 | 10110 | core (`HkCurveStart`) |
| 340014 | Normaußentemperatur Heizkurve | SS10 | 10111 | core (`HkCurveNormoutside`) |
| 340015 | Vorlauftemperatur Heizkurve | SS10 | 10108 | core (`HkCurveFlowtemp`) |
| 340055 | Kühlkurve global | US | 9028 | ext (`x_Kuehlkurve_global`) |
| 340051 | Endtemperatur VL Kühlkurve | SS10 | 10823 | ext (`x_Endtemperatur_VL_Kuehlkurve`) |
| 340052 | Starttemperatur VL Kühlkurve | SS10 | 10824 | ext (`x_Starttemperatur_VL_Kuehlkurve`) |
| 340053 | Endpunkt Kühlkurve | SS10 | 10825 | ext (`x_Endpunkt_Kuehlkurve`) |
| 340054 | Startpunkt Kühlkurve | SS10 | 10826 | ext (`x_Startpunkt_Kuehlkurve`) |
| 340016 | Zeitprogramm | US | 10159 | core (`HkTimeprogram`) |
| 320000 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320001 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320002 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320003 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320004 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320005 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320006 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320007 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320008 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320009 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320010 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320011 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320012 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320013 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320014 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320015 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320016 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320017 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320018 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320019 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320020 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 340019 | Zeitprogramm | – | – | kein Konverter |
| 340020 | Zeitprogramm | – | – | kein Konverter |
| 340059 | Zeitprogramm Kühlen | US | 10822 | ext (`x_Zeitprogramm_Kuehlen`) |
| 340021 | Sollwertkorrektur SmartHome | SS10 | 10906 | ext (`x_Sollwertkorrektur_SmartHome`) |
| 340022 | Programmwahl SmartHome | US | 10907 | ext (`x_Programmwahl_SmartHome`) |
| 340023 | Vorlaufsolltemperatur SmartHome | SS10 | 10905 | ext (`x_Vorlaufsolltemperatur_SmartHome`) |
| 340043 | Heizkreis Benamung | UnicodeTextConverter | – | nicht übernommen (UnicodeWithSpecialNull: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |

## WW_BM-2 → bm2 (Adresse 35)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 370011 | CIRCULARSLIDER | – | – | kein Konverter |
| 370012 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 50067 | Analogeingang E1 | SS10 | 2601 | ext (`x_Analogeingang_E1`) |
| 40024 | Analogeingang E1 | SS10 | 2601 | doppelt (gleiche TN wie `x_Analogeingang_E1`) |
| 370013 | CIRCULARSLIDER | – | – | kein Konverter |
| 370014 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370015 | CIRCULARSLIDER | – | – | kein Konverter |
| 370016 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370017 | CIRCULARSLIDER | – | – | kein Konverter |
| 370018 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370019 | CIRCULARSLIDER | – | – | kein Konverter |
| 370020 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370021 | CIRCULARSLIDER | – | – | kein Konverter |
| 370022 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370023 | CIRCULARSLIDER | – | – | kein Konverter |
| 370024 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370025 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370026 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370027 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370028 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370029 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370030 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370031 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370032 | CIRCULARSLIDER | – | – | kein Konverter |
| 370033 | Warmwassersolltemperatur eingestellt | SS10 | 19 | core (`WwSoll`) |
| 370034 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370035 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370036 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370037 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370038 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370039 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370040 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370041 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370042 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370043 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370044 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370045 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370046 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370047 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370048 | Programmwahl | US | 10101 | core (`WwProgram`) |
| 370005 | Programmwahl AFB | US | 10133 | ext (`x_Programmwahl_AFB_10133`) |
| 370053 | Programmwahl Fernbedienung | US | 10133 | doppelt (gleiche TN wie `x_Programmwahl_AFB_10133`) |
| 370001 | Warmwasser Status | US | 10134 | core (`WwStatus`) |
| 370004 | Zeitprogramm | US | 10158 | core (`WwTimeprogram`) |
| 320021 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320022 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320023 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320024 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320025 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320026 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320027 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320028 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320029 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320030 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320031 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320032 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320033 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320034 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320035 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320036 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320037 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320038 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320039 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320040 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320041 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320084 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320085 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320086 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320087 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320088 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320089 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320090 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320091 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320092 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320093 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320094 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320095 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320096 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320097 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320098 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320099 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320100 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320101 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320102 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320103 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320104 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320147 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320148 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320149 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320150 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320151 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320152 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320153 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320154 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320155 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320156 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320157 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320158 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320159 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320160 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320161 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320162 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320163 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320164 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320165 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320166 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320167 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320189 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320190 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320191 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320192 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320193 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320194 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320195 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320196 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320197 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320198 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320199 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320200 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320201 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320202 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320203 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320204 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320205 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320206 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320207 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320208 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320209 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320231 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320232 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320233 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320234 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320235 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320236 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320237 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320238 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320239 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320240 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320241 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320242 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320243 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320244 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320245 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320246 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320247 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320248 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320249 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320250 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320251 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320273 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320274 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320275 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320276 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320277 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320278 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320279 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320280 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320281 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320282 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320283 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320284 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320285 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320286 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320287 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320288 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320289 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320290 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320291 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320292 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320293 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320315 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320316 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320317 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320318 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320319 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320320 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320321 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320322 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320323 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320324 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320325 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320326 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320327 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320328 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320329 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320330 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320331 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320332 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320333 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320334 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320335 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320357 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320358 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320359 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320360 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320361 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320362 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320363 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320364 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320365 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320366 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320367 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320368 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320369 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320370 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320371 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320372 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320373 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320374 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320375 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320376 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320377 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 370006 | Zeitprogramm | – | – | kein Konverter |
| 370007 | Zeitprogramm | – | – | kein Konverter |
| 370049 | Warmwasserkreis Benamung | UnicodeTextConverter | – | nicht übernommen (UnicodeWithSpecialNull: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 370050 | Programmwahl SmartHome | US | 10904 | ext (`x_Programmwahl_SmartHome_10904`) |
| 370051 | Warmwassersolltemperatur SmartHome | SS10 | 10903 | ext (`x_Warmwassersolltemperatur_SmartHome`) |

## MK_BM-2 → mk (Adresse 86)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 360066 | Reglertyp | US | 5266 | core (`MkControllertype`) |
| 360028 | CIRCULARSLIDER | – | – | kein Konverter |
| 360029 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360001 | Gemittelte Außentemperatur | SS10 | 10179 | core (`OutsidetempAvg`) |
| 360030 | CIRCULARSLIDER | – | – | kein Konverter |
| 360031 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360032 | CIRCULARSLIDER | – | – | kein Konverter |
| 360033 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360034 | CIRCULARSLIDER | – | – | kein Konverter |
| 360035 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360036 | CIRCULARSLIDER | – | – | kein Konverter |
| 360037 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360038 | CIRCULARSLIDER | – | – | kein Konverter |
| 360039 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360040 | CIRCULARSLIDER | – | – | kein Konverter |
| 360041 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360042 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360043 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360044 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360045 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360046 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360047 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360048 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360049 | CIRCULARSLIDER | – | – | kein Konverter |
| 360050 | Sollwertkorrektur | SS10 | 10165 | core (`MkSetpointcorr`) |
| 360067 | CIRCULARSLIDER | – | – | kein Konverter |
| 360068 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360116 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360069 | CIRCULARSLIDER | – | – | kein Konverter |
| 360070 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360117 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360071 | CIRCULARSLIDER | – | – | kein Konverter |
| 360072 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360118 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360073 | CIRCULARSLIDER | – | – | kein Konverter |
| 360074 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360119 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360075 | CIRCULARSLIDER | – | – | kein Konverter |
| 360076 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360120 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360077 | CIRCULARSLIDER | – | – | kein Konverter |
| 360078 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360121 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360079 | CIRCULARSLIDER | – | – | kein Konverter |
| 360080 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360122 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360081 | CIRCULARSLIDER | – | – | kein Konverter |
| 360082 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360123 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360092 | CIRCULARSLIDER | – | – | kein Konverter |
| 360093 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360124 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360094 | CIRCULARSLIDER | – | – | kein Konverter |
| 360095 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360125 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360096 | CIRCULARSLIDER | – | – | kein Konverter |
| 360097 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360126 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360098 | CIRCULARSLIDER | – | – | kein Konverter |
| 360099 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360127 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360100 | CIRCULARSLIDER | – | – | kein Konverter |
| 360101 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360128 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360102 | CIRCULARSLIDER | – | – | kein Konverter |
| 360103 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360129 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360085 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360086 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360087 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360088 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360089 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360090 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360091 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360051 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360052 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360053 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360054 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360055 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360056 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360057 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360058 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360059 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360060 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360061 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360062 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360063 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360064 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360065 | Programmwahl | US | 10100 | core (`MkProgram`) |
| 360134 | Programmwahl | US | 9025 | ext (`x_Programmwahl`) |
| 360135 | Programmwahl | US | 9026 | ext (`x_Programmwahl_9026`) |
| 360018 | Sollwertkorrektur AFB | SS10 | 10142 | ext (`x_Sollwertkorrektur_AFB`) |
| 360017 | Programmwahl AFB | US | 274 | ext (`x_Programmwahl_AFB`) |
| 360000 | Raumtemperatur | SS10 | 10164 | core (`Roomtemp`) |
| 360011 | Vorlauftemperatur | SS10 | 10119 | core (`Flowtemp`) |
| 360004 | Anforderung Mischerkreis | US | 10155 | core (`MkDemand`) |
| 360005 | Mischerkreis Status | US | 10156 | core (`MkStatus`) |
| 360006 | Sparfaktor | SS10 | 10113 | core (`MkSparfaktor`) |
| 360007 | Winter/Sommer Umschaltung | SS10 | 278 | core (`MkWintersummer`) |
| 360008 | ECO/ABS | SS10 | 279 | core (`MkEcoabs`) |
| 360131 | Kreisart | US | 9005 | core (`MkCircuitType`) |
| 360132 | aktuelle Kreisart in Kombination mit Heizgerät | US | 9024 | ext (`x_aktuelle_Kreisart_in_Kombination_mit_Hei`) |
| 360084 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360110 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360111 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360112 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360113 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360114 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360115 | Tagtemperatur | SS10 | 10109 | core (`MkDaytemp`) |
| 360138 | Tagtemperatur Kühlen | SS10 | 10831 | ext (`x_Tagtemperatur_Kuehlen`) |
| 360139 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360140 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360141 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360142 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360143 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360144 | Tagtemperatur Kühlen | SS10 | 10831 | doppelt (gleiche TN wie `x_Tagtemperatur_Kuehlen`) |
| 360010 | Raumeinfluss | US | 651 | core (`MkRoomInfluence`) |
| 360136 | Raumeinfluss Kühlen | US | 9007 | ext (`x_Raumeinfluss_Kuehlen`) |
| 360012 | Sockeltemperatur Heizkurve | SS10 | 10107 | core (`MkCurveBasetemp`) |
| 360013 | Startpunkt Heizkurve | SS10 | 10110 | core (`MkCurveStart`) |
| 360014 | Normaußentemperatur Heizkurve | SS10 | 10111 | core (`MkCurveNormoutside`) |
| 360015 | Vorlauftemperatur Heizkurve | SS10 | 10108 | core (`MkCurveFlowtemp`) |
| 360145 | Kühlkurve global | US | 9028 | ext (`x_Kuehlkurve_global`) |
| 360147 | Endtemperatur VL Kühlkurve | SS10 | 10823 | ext (`x_Endtemperatur_VL_Kuehlkurve`) |
| 360148 | Starttemperatur VL Kühlkurve | SS10 | 10824 | ext (`x_Starttemperatur_VL_Kuehlkurve`) |
| 360149 | Endpunkt Kühlkurve | SS10 | 10825 | ext (`x_Endpunkt_Kuehlkurve`) |
| 360150 | Startpunkt Kühlkurve | SS10 | 10826 | ext (`x_Startpunkt_Kuehlkurve`) |
| 360016 | Zeitprogramm | US | 10159 | core (`MkTimeprogram`) |
| 320000 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320001 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320002 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320003 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320004 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320005 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320006 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320007 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320008 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320009 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320010 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320011 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320012 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320013 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320014 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320015 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320016 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320017 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320018 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320019 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320020 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320063 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320064 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320065 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320066 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320067 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320068 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320069 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320070 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320071 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320072 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320073 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320074 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320075 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320076 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320077 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320078 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320079 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320080 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320081 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320082 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320083 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320126 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320127 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320128 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320129 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320130 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320131 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320132 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320133 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320134 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320135 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320136 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320137 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320138 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320139 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320140 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320141 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320142 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320143 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320144 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320145 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320146 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320168 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320169 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320170 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320171 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320172 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320173 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320174 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320175 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320176 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320177 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320178 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320179 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320180 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320181 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320182 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320183 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320184 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320185 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320186 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320187 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320188 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320210 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320211 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320212 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320213 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320214 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320215 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320216 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320217 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320218 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320219 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320220 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320221 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320222 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320223 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320224 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320225 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320226 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320227 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320228 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320229 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320230 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320252 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320253 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320254 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320255 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320256 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320257 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320258 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320259 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320260 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320261 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320262 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320263 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320264 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320265 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320266 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320267 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320268 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320269 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320270 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320271 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320272 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320294 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320295 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320296 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320297 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320298 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320299 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320300 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320301 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320302 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320303 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320304 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320305 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320306 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320307 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320308 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320309 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320310 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320311 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320312 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320313 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320314 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320336 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320337 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320338 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320339 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320340 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320341 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320342 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320343 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320344 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320345 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320346 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320347 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320348 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320349 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320350 | Mo | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320351 | Di | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320352 | Mi | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320353 | Do | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320354 | Fr | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320355 | Sa | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 320356 | So | Timeprog03F1ConverterTemplate | – | nicht übernommen (TIMEPROG_03F1: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 360019 | Zeitprogramm | – | – | kein Konverter |
| 360020 | Zeitprogramm | – | – | kein Konverter |
| 360151 | Zeitprogramm Kühlen | US | 10822 | ext (`x_Zeitprogramm_Kuehlen`) |
| 360021 | Sollwertkorrektur SmartHome | SS10 | 10906 | ext (`x_Sollwertkorrektur_SmartHome`) |
| 360022 | Programmwahl SmartHome | US | 10907 | ext (`x_Programmwahl_SmartHome`) |
| 360023 | Vorlaufsolltemperatur SmartHome | SS10 | 10905 | ext (`x_Vorlaufsolltemperatur_SmartHome`) |
| 360130 | Heizkreis Benamung | UnicodeTextConverter | – | nicht übernommen (UnicodeWithSpecialNull: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |

## MM → mm (Adresse 52)

| PTID | Name | Konverter | TN | Status |
|---|---|---|---|---|
| 40093 | PRELOAD_Firmware | US | 410 | ext (`x_PRELOAD_Firmware`) |
| 40001 | Ausgang MKP | US | 82 | core (`Pump`) |
| 40070 | Mischerkreispumpe | US | 82 | core (`Pump`) |
| 40002 | Mischermotor | MixerStateConverterTemplate | – | nicht übernommen (Mischer: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 40003 | Ausgang A1 | US | 2701 | core (`OutputA1`) |
| 40033 | Speicherladepumpe | US | 2701 | core (`OutputA1`) |
| 40073 | Ladepumpe | US | 2701 | core (`OutputA1`) |
| 40031 | Heizkreispumpe | US | 2701 | core (`OutputA1`) |
| 40075 | Eingang E1 | US | 2601 | core (`InputE1`) |
| 40032 | Warmwassertemperatur | SS10 | 2601 | core (`InputE1`) |
| 40028 | Vorlauftemperatur | SS10 | 15 | core (`Flowtemp`) |
| 40080 | Rücklauftemperatur | SS10 | 15 | core (`Flowtemp`) |
| 40083 | Betriebsstatus Mischerkreis | READONLY_Bit4to7ConverterTemplate | – | nicht übernommen (READONLY_Bit4to7: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 40084 | Betriebsstatus Ausgang A1 | READONLY_Bit0to3ConverterTemplate | – | nicht übernommen (READONLY_Bit0to3: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |
| 40004 | Mischersolltemperatur | SS10 | 4 | core (`Flowtempdesired`) |
| 40081 | Mischersolltemperatur | SS10 | 4 | core (`Flowtempdesired`) |
| 40035 | Warmwassersolltemperatur | SS10 | 3 | core (`WwSoll`) |
| 40082 | Warmwassersolltemperatur | SS10 | 3 | core (`WwSoll`) |
| 40005 | Minimalbegrenzung Mischerkreis TV-min | SS10 | 299 | core (`TvMin`) |
| 40036 | Minimalbegrenzung Mischerkreis TV-min | SS10 | 299 | core (`TvMin`) |
| 40059 | Minimalbegrenzung Mischerkreis TV-min | SS10 | 299 | core (`TvMin`) |
| 40087 | Minimalbegrenzung Mischerkreis TV-min | SS10 | 299 | core (`TvMin`) |
| 40006 | Maximalbegrenzung Mischerkreis TV-max | SS10 | 40 | core (`TvMax`) |
| 40037 | Maximalbegrenzung Mischerkreis TV-max | SS10 | 40 | core (`TvMax`) |
| 40058 | Maximalbegrenzung Mischerkreis TV-max | SS10 | 40 | core (`TvMax`) |
| 40088 | Maximalbegrenzung Mischerkreis TV-max | SS10 | 40 | core (`TvMax`) |
| 40007 | Heizkurvenabstand | SS10 | 273 | core (`CurveDistance`) |
| 40038 | Heizkurvenabstand | SS10 | 273 | core (`CurveDistance`) |
| 40060 | Heizkurvenabstand | SS10 | 273 | core (`CurveDistance`) |
| 40089 | Heizkurvenabstand | SS10 | 273 | core (`CurveDistance`) |
| 40009 | Konfiguration | US | 2593 | core (`Config`) |
| 40010 | Nachlaufzeit Heizkreis | US | 322 | core (`PumpOverrun`) |
| 40041 | Nachlaufzeit Heizkreis | US | 322 | core (`PumpOverrun`) |
| 40061 | Nachlaufzeit Heizkreis | US | 322 | core (`PumpOverrun`) |
| 40090 | Nachlaufzeit Heizkreis | US | 322 | core (`PumpOverrun`) |
| 40011 | P-Bereich Mischer | SS10 | 399 | core (`MixerPband`) |
| 40042 | P-Bereich Mischer | SS10 | 399 | core (`MixerPband`) |
| 40062 | P-Bereich Mischer | SS10 | 399 | core (`MixerPband`) |
| 40091 | P-Bereich Mischer | SS10 | 399 | core (`MixerPband`) |
| 40012 | RL-Solltemperatur | SS10 | 400 | core (`Mi08ReturnSoll`) |
| 40063 | RL-Solltemperatur | SS10 | 400 | core (`Mi08ReturnSoll`) |
| 40013 | Max. Speicherladezeit | US | 384 | core (`Mi09MaxLoadTime`) |
| 40044 | Max. Speicherladezeit | US | 384 | core (`Mi09MaxLoadTime`) |
| 40014 | eBus Einspeisung | US | 65019 | core (`EbusPower`) |
| 40045 | eBus Einspeisung | US | 65019 | core (`EbusPower`) |
| 40015 | Hysterese Bypassfühler | SS10 | 340 | core (`Mi11BypassHyst`) |
| 40016 | Ladepumpensperre | US | 36 | core (`Mi12LoadPumpLock`) |
| 40047 | Ladepumpensperre | US | 36 | core (`Mi12LoadPumpLock`) |
| 40017 | Nachlaufzeit Ladepumpe | US | 383 | core (`Mi13PumpOverrun`) |
| 40048 | Nachlaufzeit Ladepumpe | US | 383 | core (`Mi13PumpOverrun`) |
| 40018 | Konstanttemperatur | SS10 | 711 | core (`Mi14ConstTemp`) |
| 40065 | Konstanttemperatur | SS10 | 711 | core (`Mi14ConstTemp`) |
| 40019 | dTAus (Ausschaltdifferenz) | SS10 | 405 | core (`Mi15DtOff`) |
| 40050 | dTAus (Ausschaltdifferenz) | SS10 | 405 | core (`Mi15DtOff`) |
| 40020 | dTEin (Einschaltdifferenz) | SS10 | 404 | core (`Mi16DtOn`) |
| 40051 | dTEin (Einschaltdifferenz) | SS10 | 404 | core (`Mi16DtOn`) |
| 40021 | Kesselübertemperatur bei Speicherladung | SS10 | 45 | core (`Tn45`) |
| 40052 | Kesselübertemperatur bei Speicherladung | SS10 | 45 | core (`Tn45`) |
| 40022 | Sperrung Brenner bei Rücklaufanhebung | US | 839 | core (`Mi18BurnerLock`) |
| 40053 | Sperrung Brenner bei Rücklaufanhebung | US | 839 | core (`Mi18BurnerLock`) |
| 40054 | Frostschutz LH-Kreis, ext. Wärmeanforderung | SS10 | 20035 | core (`FrostLh`) |
| 40085 | Speicherhysterese | SS10 | 320 | core (`StorageHyst`) |
| 40086 | Warmwassermaximaltemperatur | SS10 | 308 | core (`WwMaxTemp`) |
| 40024 | Analogeingang E1 | SS10 | 2601 | core (`InputE1`) |
| 40025 | Analogeingang E1 digital | US | 2601 | core (`InputE1`) |
| 40026 | Analogeingang E2 | SS10 | 2602 | core (`InputE2`) |
| 40027 | Analogeingang Vorlauffühler VF | SS10 | 15 | core (`Flowtemp`) |


## Ergebnis des Einlesens am 21.10.2026 (nach ebusd-Neustart, 3 Durchgänge)

96 ext-Nachrichten → 100 HA-Entitäten (Uhrzeiten als Stunde/Minute getrennt). 71 liefern Werte.
29 beantwortet das jeweilige Gerät mit „nicht verfügbar“ (Rohwert 32768 bzw. `-`), d. h. die Funktion ist an dieser
Anlage nicht vorhanden oder nicht freigeschaltet:

- Therme: Sammlertemperatur (kein Sammlerfühler), Eingang E3/E4 (kein E/A-Modul: `Status_EA_Modul = Nicht_vorhanden`),
  Auslauftemperatur Warmwasser (kein Kombigerät), erweiterte Statistik aktiv sowie alle Energie-/Wärmemengenzähler
  (Jahr, Vorjahr, Vorvorjahr, HZ/WW) – die Therme führt diese Statistik nicht (passt zu `EnergyToday` = 32768).
- BM-2/MK: Programmwahl mit Kühlvarianten (TN 9025/9026), aktuelle Kreisart, Kühlkurve global,
  Vorlaufsolltemperatur SmartHome – Kühlfunktionen, an dieser Anlage nicht aktiv.

Beispiele gelesener Werte: Typ = CGB_2, Herstelljahr/-woche 19/44, Warmwasserkonfiguration = DHWCoilStorNoHead
(Speicher mit Wendel, ohne Vorrangschaltung laut Wolf-Bezeichnung), Eingang E1 = Geöffnet, IO-Istwert 5,
BUSCONFIG_Anlagenkonfiguration Rohwert 1 (Wertetabelle der Wolf-DB: 1 → „2“; Deutung nicht verifiziert, HG40 liefert ebenfalls 1),
BM-2 Softwareversion 280, Lüftung Nennlüftung/Filter OK (Lüftungsgerät CWL vorhanden?), Kühlkurve 20/30 °C bei 35/45 °C Außentemperatur.
