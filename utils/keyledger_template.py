# For Googlemaps Places query functionality and certain tile providers, you need an API key.
# All of these are available online for free, up to a certain quota (generally 1000s of monthly requests free).


class KeyLedger():
    def __init__(self):
        self.googlemaps_key = ""
        self.thunderforest_key = ""
        self.stadia_key = ""
