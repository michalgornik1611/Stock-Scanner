# Content of Project
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed informations about modules](#more-detailed-information-about-modules)


## General info
The project is to help scan companies from the American S&P. After typing the ticker, we have the opportunity to see a chart that contains the period we set (the charts can be of the type that we set ourselves). In addition, the program helps you evaluate the capitalization of companies based on indicator comparisons to other companies in the industry. New feature (forecast) allow you to count growth dynamics of specified financial positions in last years. You can also see our forecast of the results for 2023.

## Technologies
<ul>
<li>Python</li>
<li>Pandas</li>
<li>yfinance</li>
<li>aiohttp</li>
<li>asyncio</li>
<li>aiohttp</li>
<li>matplotlib</li>
<li>mplfinance</li>
</ul>


## Setup

Clone the repo
```git clone https://github.com/michalgornik1611/Stock-Scanner.git```

## More detailed informations about modules
<b>Module indicators</b> contains code that helps to create a group of companies from a given sector, which will be used in benchmarking. Using asynchronous programming, the program downloads data and creates a report on the company's key indicators against the background of the entire sector. This helps to value the company against other companies in the industry. In addition, the analysis includes its own assessment of indicators, in which the higher the score, the better.

<b>Module classes</b> is used to download information about a given company and recommendations of professional analysts. In addition, this module uses a code to create personalized charts.

<b>Module forecast</b> is used to calculate the growth dynamics of the company's result items and forecast their results in 2023.

<b>Module main</b> starts the program.