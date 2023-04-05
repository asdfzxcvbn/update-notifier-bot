# update-notifier-bot
telegram bot to monitor new apps in your instance of [update-notifier](https://github.com/asdfzxcvbn/update-notifier). made really lazily.

## setup
just fill in the first 3 variables in `newMonitorBot.py`. for example:

```python
TOKEN = "1234567890:6zzD8swuBXhY9hHaWHMFBRKsXZmR2V2R2HM"
COUNTRY = "us"
MY_ID = 1234567890
```

`TOKEN` is your bot's token. this should be a different bot than the one used in update-notifier. `COUNTRY` should ideally be the same country being used in your instance of update-notifier. `MY_ID` is the id of your telegram account so only you can add new apps. get your id by DMing [@username_to_id_bot](https://t.me/username_to_id_bot).

## usage
`python3 newMonitorBot.py` running in the background on the same machine running update-notifier. you can use a tool like `screen` to accomplish this.
