# Blackcoffer Project

## Step 1 - Select the Python Environment
Make sure you have the appropriate Python environment activated.

## Step 2 - Clone the Project
Clone the project from GitHub using the following command:

```bash
git clone https://github.com/ParitKansal/blackcoffer
```

## Step 3 - Install the Required Python Modules
Navigate to the project directory and install the required Python modules by running:

```bash
pip install -r requirements.txt
```

## Step 4 - Run the Project
After installing the necessary modules, you can run the Python Scrapy Spider as follows:

1. Navigate to the `Scraper` directory:

    ```bash
    cd Scraper
    ```

2. View the available spiders:

    ```bash
    scrapy list
    ```

3. Run the specific spider (i.e., `websiteSpider`):

    ```bash
    scrapy crawl websiteSpider
    ```

--- 
4. Doing setting.py
    i. For ScrapeOpsFakeBrowserHeaderAgentMiddleware
          SCRAPEOPS_API_KEY = '8857a1e3-3e44-428f-8809-d6028ba24f0f'
          SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = "https://headers.scrapeops.io/v1/browser-headers"
          SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
          SCRAPEOPS_NUM_RESULTS = 50
     if not present then
         in DOWNLOADER_MIDDLEWARES list of settings.py
             comment or remove 'Scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 700,
ii. For MyProxyMiddleware
          PROXY_USER = 'bshsdswo-rotate'
PROXY_PASSWORD = 'tpti8er7yyw6'
PROXY_ENDPOINT = 'p.webshare.io'
PROXY_PORT = '80'
     if not present then
         in DOWNLOADER_MIDDLEWARES list of settings.py
             comment or remove 'Scraper.middlewares.MyProxyMiddleware': 610, 
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 650,

This should work correctly for running your Scrapy project.
