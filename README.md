# Credit-Metric-Scraping 
Python- Uses HTTP requests to automate the retrieval and graphing of credit metrics for a list of stocks

Helps reduce time with regards to the retrieval of financial data and the calculation and graphing of relevant credit metrics.
1.Asks user for the number of companies he would like to look up and the tickers for those companies
2.Uses multiple HTTP requests to pull financial data from gurufocus (reliable source)
3.Data then parsed via Beautiful Soup
4.Parsed Data is Graphing via Bar Graph

Debt-to-EBITSA and Debt-To-Asset Ratios may not appear if a company has no debt.
Interest Rate Coverage may not appear if the company has incurred a loss in the most recent period.

Note: In future, any unexpected results may be from changes to the Gurufocus website or the matplotlib library