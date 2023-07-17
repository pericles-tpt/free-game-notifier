# Free (PC) Game Notifier
A small python program I made to notify me (via [PushOver](https://pushover.net/)) of free pc games whenever they get announced. It currently scrapes [gg.deals](https://gg.deals/) to find "freebies" and bundles (might not be the best data source) and uses PushOver to send the notification (PushOver is a paid service but it's a very good value in my opinion). This program is intended to run 24/7 and check for new games periodically.

## Setup
1. IMPORTANT: Duplicate `cfg/creds.example.yml` and rename it to `cfg/creds.yml`
2. Put your API User Key and API Token Key from PushOver into `cfg/creds.yml`
3. Change the global variables (lines 6 - 8) in `src/api.py` to your liking
4. Change `RUN_EVERY` in `src/main.py` to set the delay between checks for new free games
5. Run `pip3 install -r requirements.txt`
6. Finally, run `python3 src/main.py` to start the program

OPTIONAL: Alternative to **6** (if you'd like to be notified when the program terminates due to an exception):
* Provide an additional PushOver token to `PO_TOKEN_KEY_FAIL` in `cfg/creds.yml`
* FIRST TIME ONLY: Run `chmod a+x run.sh` to allow you to execute the run script
* Run `./run.sh` (instead of `python3 src/main.py`)

## Future Improvements
1. Streamline the setup process
2. <s>Store previously found games to a file to avoid duplicate alerts when running the program multiple times</s>
3. <s>Find a better data source than gg.deals?</s> (I think gg.deals is ok)
