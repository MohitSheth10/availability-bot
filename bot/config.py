import os

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'your_discord_bot_token_here')

# Available regions for gaming with their timezones
REGIONS = [
    "North America East",
    "North America West", 
    "Europe West",
    "Europe East",
    "Asia Pacific",
    "Southeast Asia",
    "South America",
    "Oceania",
    "Middle East",
    "Africa"
]

# Timezone mapping for regions (UTC offsets in hours)
REGION_TIMEZONES = {
    "North America East": -5,      # EST/EDT
    "North America West": -8,      # PST/PDT
    "Europe West": 1,              # CET/CEST
    "Europe East": 2,              # EET/EEST
    "Asia Pacific": 8,             # China/Singapore time
    "Southeast Asia": 7,           # Thailand/Vietnam time
    "South America": -3,           # Brazil time
    "Oceania": 10,                 # AEST
    "Middle East": 3,              # Arabia time
    "Africa": 2                    # CAT
}

# Time format examples for help messages
TIME_FORMAT_EXAMPLES = [
    "Not Available",
    "3-4",
    "12:30-13:15",
    "9:00-10:30",
    "3-4, 14:30-16:00",
    "2:15-3:45, 18:00-20:30"
]
