# free-game-notifier
A small python program I made to notify me (via PushOver) of free pc games whenever they get announced. It currently scrapes gg.deals to find "freebies" (might not be the best data source) and uses PushOver to send the notification (PushOver is a paid service but it's a very good value imo).

## Setup
1. IMPORTANT, rename `creds.example.yml` to `creds.yml`
2. Put in your API User Key and API Token Key from PushOver
3. Change the global variables (lines 6 - 8) in `api.py` to your liking
4. Change `RUN_EVERY` in `main.py` to set the delay between checks for new free games
5. Run `pip install -r requirements.txt`
6. Finally, run `python3 src/main.py` to start the program

## Future Improvements
1. Streamline the setup process
2. Store previously found games to a file to avoid duplicate alerts when running the program multiple times
3. Find a better data source than gg.deals?

## Donations
If you've benefitted from this code, feel free to donate to one of the following cryptocurrency addresses

    BTC: 37iH1qF13dgzcsd5HAntpKAYf6oaoZK77z
    ETH: 0x4c4386c78FBD6CC3a5BB41cD21CB3276a716a787
