# Web Advert Notifier

*Web Advert Notifier is a web application, which search stored Olx filters for new adverts and send notification on Slack.*


**Requirements:**
- Configured **Slack** Workspace with at least one channel  
    **Hint:** *[Create a Slack workspace](https://slack.com/intl/en-pl/help/articles/206845317-Create-a-Slack-workspace)*  
- Setted up **incoming webhooks** in Slack  
    **Hint:** *[Incoming WebHooks App](https://my.slack.com/services/new/incoming-webhook/)*  
- Configured **Python** environment in version >=**3.7.6** with installed dependencies from **requirements.txt**  
- Downloaded all **notifier** files from repository  
- Valid **config.yaml** file  


## Configuration


*To run, program demand a valid config **config.yaml** file.*  
In config file, needs to provide:  
- Slack webhook URL  
- Database file path  
- Adverts portal URL filters  

Example of **config.yaml** file:

```shell
slack:
  webhook_url: https://hooks.slack.com/services/12345/ABCDE/xyz123
database:
  path: notifier.db
filters:
  olx:
    - https://www.olx.pl/sport-hobby/rowery/wroclaw/q-FUJI-JARI-CARBON/
```

>**Note**: Each advert portal URL filter needs to be passed after '-'.


## Usage

*Program may periodically checks stored filters for new adverts and run as an OS service, or it might be refreshed manually. Behaviour depends from passing arguments. In case of periodically run, the user specifies the interval of refreshing web pages (in seconds).*  

Program accepts following parameters: 

```shell
usage: notifier_runner.py [-h] [-c] [-i INTERVAL] [--debug]

Web Adverts Notifier

optional arguments:
  -h, --help            show this help message and exit
  -c, --collect         check stored filters for new adverds
  -i INTERVAL, --interval INTERVAL
                        periodically check stored filters for new adverts with
                        provided interval (in seconds)
  --debug               debug flag
```  

## Example of usage:

To run program, execute in console:
```shell
python notifier/notifier_runner.py -c
``` 
Shell output:
```shell
2020-10-06 15:27:39,918 - INFO - Creating database...
2020-10-06 15:27:40,043 - INFO - Database created!
2020-10-06 15:27:40,640 - INFO - Found new advert: 'FUJI JARI CARBON 1.3 SRAM RIVAL 1X11 2019 - rozmiar 54 (M)' - 'https://www.olx.pl/oferta/fuji-jari-carbon-1-3-sram-rival-1x11-2019-rozmiar-54-m-CID767-IDG4F2c.html#0508b0a2b6;promoted'
2020-10-06 15:27:40,689 - INFO - Sending message...
2020-10-06 15:27:41,049 - INFO - Message succesfully sent!
``` 
Slack message:  
![slack message](images/slack.png "Slack message")

