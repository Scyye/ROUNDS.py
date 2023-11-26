from enum import Enum

from utils import validate_class_name, validate_general_string

default_card = open(r"../Assets/DefaultCardClass.txt", "r").read()


class Stat(Enum):
    Health = "Health"
    Damage = "Damage"
    Reload = "Reload Time"
    Ammo = "Ammunition"
    Projectiles = "Projectile Count"
    Bursts = "Bursts"
    TimeBetweenBullets = "Time Between Bullets"
    AttackSpeed = "ATKSPD"
    Bounces = "Bounces"
    BulletSpeed = "Bullet Speed"


mult = [
    Stat.Damage,
    Stat.Health,
    Stat.Reload,
    Stat.AttackSpeed,
    Stat.BulletSpeed,
]


class InfoStat:
    def __init__(self, stat: Stat, value: float, positive: bool):
        self.stat = stat
        self.value = value
        self.positive = positive

    def __str__(self):
        return \
            f"""new CardInfoStat()
            {{
                positive = {str(self.positive).lower()},
                stat = "{self.stat.value}",
                amount = "{"+" if self.stat not in mult else ""}{self.value if self.stat not in mult else self.value * 100}{"%" if self.stat in mult else ""}",
                simepleAmount = CardInfoStat.SimpleAmount.notAssigned
            }}"""


class Card:
    def __init__(self, name: str, description: str, stats: list[InfoStat]):
        self.name = name
        self.description = description
        self.stats = stats

    def generate_stats(self):
        return ",\n\t\t\t".join([str(stat) for stat in self.stats])

    def generate_actions(self):
        return '\n\t\t'.join([f"actions[\"{stat.stat.value}\"].Invoke({stat.value}f);"
                              for stat in self.stats])

    def __str__(self):
        return (default_card
                .replace("+TITLE_CLASS+", validate_class_name(self.name))
                .replace("+TITLE+", validate_general_string(self.name))
                .replace("+DESC+", validate_general_string(self.description))
                .replace("+STATS+", self.generate_stats())
                .replace("+ACTIONS+", self.generate_actions()))
