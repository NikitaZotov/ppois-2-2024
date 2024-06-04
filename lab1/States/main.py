# this module runs all the project

from states import SiteStates
from Save.siteFile import SiteFile, File

file: File = SiteFile("file.pickle")

state = SiteStates(file)

while True:
    state.next_state(input())
