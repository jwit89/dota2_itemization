#!usr/bin/env python

# return item name associated with a given item id
def hero(hero_id):
    hero_id = int(hero_id)
    if hero_id == 1:
        hero_name = "Anti-Mage"
    elif hero_id == 2:
        hero_name = "Axe"
    elif hero_id == 3:
        hero_name = "Bane"
    elif hero_id == 4:
        hero_name = "Bloodseeker"
    elif hero_id == 5:
        hero_name = "CrystalMaiden"
    elif hero_id == 6:
        hero_name = "DrowRanger"
    elif hero_id == 7:
        hero_name = "Earthshaker"
    elif hero_id == 8:
        hero_name = "Juggernaut"
    elif hero_id == 9:
        hero_name = "Mirana"
    elif hero_id == 11:
        hero_name = "ShadowFiend"
    elif hero_id == 10:
        hero_name = "Morphling"
    elif hero_id == 12:
        hero_name = "PhantomLancer"
    elif hero_id == 13:
        hero_name = "Puck"
    elif hero_id == 14:
        hero_name = "Pudge"
    elif hero_id == 15:
        hero_name = "Razor"
    elif hero_id == 16:
        hero_name = "SandKing"
    elif hero_id == 17:
        hero_name = "StormSpirit"
    elif hero_id == 18:
        hero_name = "Sven"
    elif hero_id == 19:
        hero_name = "Tiny"
    elif hero_id == 20:
        hero_name = "VengefulSpirit"
    elif hero_id == 21:
        hero_name = "Windranger"
    elif hero_id == 22:
        hero_name = "Zeus"
    elif hero_id == 23:
        hero_name = "Kunkka"
    elif hero_id == 25:
        hero_name = "Lina"
    elif hero_id == 31:
        hero_name = "Lich"
    elif hero_id == 26:
        hero_name = "Lion"
    elif hero_id == 27:
        hero_name = "ShadowShaman"
    elif hero_id == 28:
        hero_name = "Slardar"
    elif hero_id == 29:
        hero_name = "Tidehunter"
    elif hero_id == 30:
        hero_name = "WitchDoctor"
    elif hero_id == 32:
        hero_name = "Riki"
    elif hero_id == 33:
        hero_name = "Enigma"
    elif hero_id == 34:
        hero_name = "Tinker"
    elif hero_id == 35:
        hero_name = "Sniper"
    elif hero_id == 36:
        hero_name = "Necrophos"
    elif hero_id == 37:
        hero_name = "Warlock"
    elif hero_id == 38:
        hero_name = "Beastmaster"
    elif hero_id == 39:
        hero_name = "QueenofPain"
    elif hero_id == 40:
        hero_name = "Venomancer"
    elif hero_id == 41:
        hero_name = "FacelessVoid"
    elif hero_id == 42:
        hero_name = "SkeletonKing"
    elif hero_id == 43:
        hero_name = "DeathProphet"
    elif hero_id == 44:
        hero_name = "PhantomAssassin"
    elif hero_id == 45:
        hero_name = "Pugna"
    elif hero_id == 46:
        hero_name = "TemplarAssassin"
    elif hero_id == 47:
        hero_name = "Viper"
    elif hero_id == 48:
        hero_name = "Luna"
    elif hero_id == 49:
        hero_name = "DragonKnight"
    elif hero_id == 50:
        hero_name = "Dazzle"
    elif hero_id == 51:
        hero_name = "Clockwerk"
    elif hero_id == 52:
        hero_name = "Leshrac"
    elif hero_id == 53:
        hero_name = "Nature'sProphet"
    elif hero_id == 54:
        hero_name = "Lelifestealer"
    elif hero_id == 55:
        hero_name = "DarkSeer"
    elif hero_id == 56:
        hero_name = "Clinkz"
    elif hero_id == 57:
        hero_name = "Omniknight"
    elif hero_id == 58:
        hero_name = "Enchantress"
    elif hero_id == 59:
        hero_name = "Huskar"
    elif hero_id == 60:
        hero_name = "NightStalker"
    elif hero_id == 61:
        hero_name = "Broodmother"
    elif hero_id == 62:
        hero_name = "BountyHunter"
    elif hero_id == 63:
        hero_name = "Weaver"
    elif hero_id == 64:
        hero_name = "Jakiro"
    elif hero_id == 65:
        hero_name = "Batrider"
    elif hero_id == 66:
        hero_name = "Chen"
    elif hero_id == 67:
        hero_name = "Spectre"
    elif hero_id == 69:
        hero_name = "Doom"
    elif hero_id == 68:
        hero_name = "AncientApparition"
    elif hero_id == 70:
        hero_name = "Ursa"
    elif hero_id == 71:
        hero_name = "SpiritBreaker"
    elif hero_id == 72:
        hero_name = "Gyrocopter"
    elif hero_id == 73:
        hero_name = "Alchemist"
    elif hero_id == 74:
        hero_name = "Invoker"
    elif hero_id == 75:
        hero_name = "Silencer"
    elif hero_id == 76:
        hero_name = "OutworldDevourer"
    elif hero_id == 77:
        hero_name = "Lycanthrope"
    elif hero_id == 78:
        hero_name = "Brewmaster"
    elif hero_id == 79:
        hero_name = "ShadowDemon"
    elif hero_id == 80:
        hero_name = "LoneDruid"
    elif hero_id == 81:
        hero_name = "ChaosKnight"
    elif hero_id == 82:
        hero_name = "Meepo"
    elif hero_id == 83:
        hero_name = "TreantProtector"
    elif hero_id == 84:
        hero_name = "OgreMagi"
    elif hero_id == 85:
        hero_name = "Undying"
    elif hero_id == 86:
        hero_name = "Rubick"
    elif hero_id == 87:
        hero_name = "Disruptor"
    elif hero_id == 88:
        hero_name = "NyxAssassin"
    elif hero_id == 89:
        hero_name = "NagaSiren"
    elif hero_id == 90:
        hero_name = "KeeperoftheLight"
    elif hero_id == 91:
        hero_name = "Wisp"
    elif hero_id == 92:
        hero_name = "Visage"
    elif hero_id == 93:
        hero_name = "Slark"
    elif hero_id == 94:
        hero_name = "Medusa"
    elif hero_id == 95:
        hero_name = "TrollWarlord"
    elif hero_id == 96:
        hero_name = "CentaurWarrunner"
    elif hero_id == 97:
        hero_name = "Magnus"
    elif hero_id == 98:
        hero_name = "Timbersaw"
    elif hero_id == 99:
        hero_name = "Bristleback"
    elif hero_id == 100:
        hero_name = "Tusk"
    elif hero_id == 101:
        hero_name = "SkywrathMage"
    elif hero_id == 102:
        hero_name = "Abaddon"
    elif hero_id == 103:
        hero_name = "ElderTitan"
    elif hero_id == 104:
        hero_name = "LegionCommander"
    elif hero_id == 106:
        hero_name = "EmberSpirit"
    elif hero_id == 107:
        hero_name = "EarthSpirit"
    elif hero_id == 108:
        hero_name = "AbyssalUnderlord"
    elif hero_id == 109:
        hero_name = "Terrorblade"
    elif hero_id == 110:
        hero_name = "Phoenix"
    elif hero_id == 105:
        hero_name = "Techies"
    elif hero_id == 111:
        hero_name = "Oracle"
    elif hero_id == 112:
        hero_name = "WinterWyvern"
    elif hero_id == 113:
        hero_name = "ArcWarden"
    elif hero_id == 114:
        hero_name = "MonkeyKing"
    else:
        hero_name = "N/A"
    return hero_name