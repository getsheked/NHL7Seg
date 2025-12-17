# Welcome to the NHL7Seg Project!
Thanks for checking this out, it's not very much code nor very impressive, but I hope what I have done sparks some insperation for someone else and maybe acts as a starting point to build off from. Im not very good at python, so there are plenty of bugs, poorly witten syntax, optimization issues, etc. But I can promise eventually it will *mostly* work. If you want to work on it or copy it feel free, it is under an MIT license for that purpose. If you decide that you want to actaully use this for some reason, the steps to install it and the diagrams for the ciruit I created with the LEDs is shown below. -Getsheked

## Setup Stage 1: Software:
    
#### Step 1: Configure Config file
First you need to set up the config file. This infoms what team the scoreboard will track and other settings. This file can be found in source/config.ini. 
* ##### Set Team ID
  Look in the drop down table below to find your teams id and abbrevation, then enter these in the config file

<details>
<summary> Team IDs and Abbrevations List </summary> 
    
| Team Name     | Abbrevations  | ID    |
| ------------- |:-------------:| -----:|
| Anaheim Ducks      | ANA | 24 |
| Boston Bruins      | BOS     | 6  |
| Buffalo Sabers |BUF      | 7  |
|Calgary Flames| CGY| 20|
Carolina Huricanes |CAR |12|
Chicago Blackhawks |CHI |16|
Colorado Avalanche |COL |21|
Columbus Blue Jackets| CBJ |29|
Dallas Stars|DAL |25|
Detriot Red Wings |DET |17|
Edmonton Oilers |EDM |22|
Florida Panthers |FLA |13|
Los Angeles Kings| LAK |26|
Minnesota Wild |MIN |30|
Monteral Canadiens |MTL |8|
Nashville Predators |NSH |18|
New Jersey Devils |NJD |1|
New York Islanders| NYI |2|
New York Rangers |NYR |3|
Ottawa Senators  |OTT |30|
Philadelphia Flyers |PHI |4|
Pittsburgh Penguins |PIT |5|
San Jose Sharks|SJS |28|
Seattle Kraken |SEA |55|
St. Louis Blues |STL |19|
Tampa Bay Lighting |TBL |14|
Toronto Maple Leafs |TOR |10|
Utah Hockey Club |UTA |59|
Vancouver Canucks |VAN |23|
Vegas Golden Knights |VGK |54|
Washington Capitals |WSH |15|
Winnipeg Jets |WPG |52|
</details>
  
* ##### Set date and time formats
    The program displays when a teams next game is, for example: "Next Game MIN at OTT 1-15 700 PM" You can choose if you want this to be month day like the example or day month, additionally you can chose if you want the     clock to be in 24 hour or not. To have the date be month-day put in 1 for the seconddigit value. For day-month you can put anything else in. For 12 hr time (am/pm) put in 12 for the 24hr value. Else, enter anything         else. Make sure you have something and dont have it empty otherwise it will throw an error
