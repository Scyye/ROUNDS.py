__all__ = [
    'Stat',
    'InfoStat',
    'Mod',
    'Card',
]

from enum import Enum

import re
import os
import shutil
import subprocess


def use_regex(input_text):
    pattern = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+", re.IGNORECASE)
    return pattern.match(input_text)


def validate_class_name(name):
    return validate_nospace(name.replace("'", "").replace("-", "").title())


def validate_nospace(name):
    return name.replace(" ", "").replace("\"", "")


def validate_general_string(string):
    return string.replace("\"", "\\\"")


default_card = open(r"Assets/DefaultCardClass.txt", "r").read()


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


default_main = open(r"Assets/DefaultMainClass.txt", "r").read()

lib_dir = r"../lib"

icon_dir = r"Assets/default_icon.png"


class Mod:
    def __init__(self, name, author, version, description):
        self.name, self.author, self.version, self.description = name, author, version, description
        self.cards = []

    def add_card(self, name, description, stats):
        self.cards.append(Card(name, description, stats))

    def generate_cards(self):
        return '\n'.join(str(card) for card in self.cards)

    def generate_card_builds(self):
        return '\n\t\t'.join(f"CustomCard.BuildCard<{validate_class_name(card.name)}>();" for card in self.cards)

    def __str__(self):
        return (default_main
                .replace("+CARDS+", self.generate_card_builds())
                .replace("+MODNAME+", validate_general_string(self.name))
                .replace("+MODNAME_LOWER+", validate_class_name(self.name.lower()))
                .replace("+MODNAME_NAMESPACE+", validate_class_name(self.name))
                .replace("+VERSION+", self.version if use_regex(self.version) else "0.0.0")
                .replace("+AUTHOR_LOWER+", validate_general_string(self.author.lower())))

    def write(self):
        open(f"{self.name}.cs", "w").write(f"{self.__str__()}\n\n{self.generate_cards()}")
        open(f"{self.name}.csproj", "w").write(
            open("Assets/DefaultCsprojFile.txt", "r").read().replace("+LIB_DIR+", lib_dir))

    def package(self):
        os.mkdir("BUILD")
        subprocess.run(["dotnet", "build"])
        shutil.move(f"bin/Debug/netstandard2.1/{self.name}.dll", f"BUILD/{validate_class_name(self.name)}.dll")
        open("BUILD/manifest.json", "w").write(
            open("Assets/DefaultManifest.txt", "r").read()
            .replace("+MODNAME+", validate_class_name(self.name))
            .replace("+VERSION+", self.version if use_regex(self.version) else "1.0.0")
            .replace("+DESC+", validate_general_string(self.description))
        )
        open("BUILD/README.md", "w").write(f"# {self.name}\n\n{self.description}")
        shutil.copy(icon_dir if icon_dir else "Assets/default_icon.png", "BUILD/icon.png")
        shutil.make_archive(self.name, "zip", "BUILD")

    def clean(self):
        shutil.rmtree("BUILD")
        os.mkdir("BUILD")
        shutil.move(f"{self.name}.zip", f"BUILD\\{self.name}.zip")
        os.remove(f"{self.name}.cs")
        os.remove(f"{self.name}.csproj")
        shutil.rmtree("bin")
        shutil.rmtree("obj")

    def build(self):
        if os.path.exists("BUILD"):
            shutil.rmtree("BUILD")
        self.write()
        self.package()
        self.clean()
