# Scrapy settings for kidscare project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kidscare'

SPIDER_MODULES = ['kidscare.spiders']
NEWSPIDER_MODULE = 'kidscare.spiders'

COMMANDS_MODULE = 'kidscare.commands'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kidscare (+http://www.yourdomain.com)'
