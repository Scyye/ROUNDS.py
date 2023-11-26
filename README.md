# ROUNDS.py V1.0.0
### By [Scyye](https://scyye.github.io/)

## Description
A framework for creating stat card mods for the game [ROUNDS](https://store.steampowered.com/app/1557740/ROUNDS/) in python.

More features coming soon, this is just the first release to get the ball rolling.


## How to use
Either
a. run `pip install ROUNDS.py` (As soon as pypi is back up)

Or b. download the [latest release](https://github.com/Scyye/ROUNDS.py/releases/latest) and extract it.

Then, create a new python file and import the package:
```py
from ROUNDS.mod import Mod
```

## Example
To initialise your mod:
```py
from ROUNDS.mod import Mod

# NOTE: Version must be in the format of "x.x.x" where x is any number (can be multiple digits)
mod = Mod(name="Your Mod Name", author="Your Name", description="Describe your mod", version="1.0.0")
```

To add a stat card:
```py
from ROUNDS.card import InfoStat, Stat

# NOTE: You can add as many cards as you want
mod.add_card(name="Name", description="What does your card do?", stats=[
    InfoStat(stat=Stat.Health, value=1.5), # Health is multiplied by 1.5
    InfoStat(stat=Stat.Damage, value=0.5), # Damage is multiplied by 0.5
    InfoStat(stat=Stat.Ammo, value=2) # Ammo is incremented (increased) by 2
])
```

Then, to save your mod:
```py
mod.build()
```
This will then create a folder called `build` in the same directory as your python file.
Inside will be a zip file with the name of your mod, and inside that will all the files
your mod needs in order to be uploaded to [thunderstore](https://rounds.thunderstore.io/) 
following this [guide](https://docs.google.com/document/d/1f0bZvolXIGhVRpIURijiVFN2k6p7bZQlzpfVuIE-HFw/edit).

## Publishing & Testing
To test your mod, simply build it as shown above, then go to Thunderstore or r2modman, go to settings -> import local mod and select the zip file.

Once you verify that it works, you can upload it to Thunderstore following the guide above.


# Bug Reports
If you find any bugs, or have any questions, either open an issue on the [github repo](https://github.com/Scyye/ROUNDS.py/issues) or join the [ROUNDS Modding Discord](https://discord.com/invite/rounds-modding) and ping me (`@scyye`) in #mod-bug-chat.