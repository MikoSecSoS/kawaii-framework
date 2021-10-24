from platform import system
from termcolor import colored

__platform__ = system()
__prompt__ = "Kawaii"
__version__ = "v1.2.1.211024-beta-"
__baseBanner__ = r"""
 ____  __.                     .__.__ 
|    |/ _|____ __  _  _______  |__|__|
|      < \__  \\ \/ \/ /\__  \ |  |  |
|    |  \ / __ \\     /  / __ \|  |  |
|____|__ (____  /\/\_/  (____  /__|__|
        \/    \/             \/       
                            {version}

"""

__banner__ = colored(__baseBanner__, "blue").format(version=colored(__version__, "green"))