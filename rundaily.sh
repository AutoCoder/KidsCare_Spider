# /bin/bash
cd /root/kidscare_src/KidsCare_Spider/
find ./ScrapyHistory -name "*.log"|xargs rm -rf
export PATH
/usr/local/bin/scrapy crawl dangdang
/usr/local/bin/scrapy crawl tmall
/usr/local/bin/scrapy crawl yhd
/usr/local/bin/scrapy crawl jd_ajax
/usr/local/bin/scrapy crawl sfbest
/usr/local/bin/scrapy crawl suning
/usr/local/bin/scrapy crawl weiwei
