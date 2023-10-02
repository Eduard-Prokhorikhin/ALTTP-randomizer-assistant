# ALTTP-randomizer-assistant

This is a project i developed during last year of highschool, utilizing my personal expiriances with A Link to the Past randomizer and some helpfull reasources i found online made by the community. 
The the trackers logic is based on data.json file which consists of all possible locations of interest and their respective item requirments. The whole project is a bit jank i must admit but it was fun to make at the time.

## Intall
- Clone repo
- Make sure dependencies are installed
  - Non standard modules:
  - ```pip install tk```
  - ```pip install tkScrolledFrame```
  - ```pip install Pillow```
- Enjoy ;)

## Features
- Interactable inventory view where you would register current intventory status
  - Left click to mark item as aquired
  - Right click to change the variant of an item (like the medalions)
- View of accesible locations sorted by amount of checks and if its fully clearable
  - Click the "DONE" button to remove the location from the view
  - Some locations may only be partially clearable and therefore will be grayed out with the number of items indicating the the total not the accesible amount
