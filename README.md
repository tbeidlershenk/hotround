### HotRound

HotRound aggregates PDGA sanctioned tournament data to calculate accurate disc golf round ratings for casual, non-sanctioned rounds.

~~Check it out at **[hotround.ddns.net](https://hotround.ddns.net)** !~~ Website in progress<br/>
Invite the bot to your Discord server **[here](https://discord.com/oauth2/authorize?client_id=1300645264591294475)**<br/>
Kaggle dataset of all my data is **[here](https://www.kaggle.com/datasets/tobiasbeidlershenk/pdga-sanctioned-disc-golf-tournament-data)**

### Example Usage

![Website example](./assets/website_1.png)

### Built using

The frontend site is built using the Flask web framework to serve a ReactJS application, and NGINX as a reverse proxy.

The discord bot is built using the Disnake python library.

The dataset used by the project was scraped using Selenium and stored in a SQL database.

Docker is used to deploy the two applications and Github Actions for automatically building images.

[![My Skills](https://skillicons.dev/icons?i=python,flask,react,nginx,docker,selenium,sqlite,githubactions)](https://skillicons.dev)

### Credits

The data used in this project was sourced through web scraping from [PDGALive](https://pdga.com/live) and is not being used for commercial purposes.
