# Passport checker ![Passport Checker logo](https://github.com/faccimatteo/Passport_checker/blob/main/logo/passport.ico )

## What can I do? 
This ruby program is made to automatic check passport availability for a province in Italy.
Once passport is available for booking you will get notified with a Telegram message from a bot.

## Usage

1. Install Ruby from `https://rubyinstaller.org/downloads/` (if you don't already have)
2. Install requried gems with 
`gem install dotenv && gem install faraday && gem install telegram && gem install logger`
3. Create a telegram bot (check `https://core.telegram.org/bots#how-do-i-create-a-bot` for the simple guide). 
4. Get the token of the bot you've just created and assign it to `TOKEN` and assign to `PROVINCE` the province you want to monitorate. Both variables must be assigned in the `.env` file. This will be used from the program to integrate itself with the telegram bot and let you choose which city to check.
5. Run bot with `ruby check_passport.arb`

