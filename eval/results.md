# FinChat Evaluation - FinanceBench (corpus-aligned subset)

FinChat is graded by an LLM-as-judge against gold answers from the [FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench) benchmark, on every 10-K question whose company + fiscal year is in the corpus. FinanceBench is expert-written and intentionally hard.

- **Questions evaluated:** 30
- **CORRECT:** 10   **PARTIAL:** 10   **INCORRECT:** 10
- **Score:** 15.0 / 30
- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** 50%

**Accuracy by FinanceBench question type:**

| Question type | Accuracy | N |
|---|---|---|
| domain-relevant | 52% | 21 |
| metrics-generated | 50% | 2 |
| novel-generated | 43% | 7 |

| # | Company | FY | Verdict | Question |
|---|---------|----|---------|----------|
| 1 | 3M | 2022 | PARTIAL | Is 3M a capital-intensive business based on FY2022 data? |
| 2 | 3M | 2022 | INCORRECT | If we exclude the impact of M&A, which segment has dragged down 3M's overall growth in 2022? |
| 3 | Adobe | 2022 | PARTIAL | Does Adobe have an improving Free cashflow conversion as of FY2022? |
| 4 | AES Corporation | 2022 | PARTIAL | Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why. |
| 5 | Amcor | 2023 | INCORRECT | Has AMCOR's quick ratio improved or declined between FY2023 and FY2022? If the quick ratio is not something that a financial analyst would ask about a company like this, then state that and explain why. |
| 6 | Amcor | 2023 | CORRECT | What industry does AMCOR primarily operate in? |
| 7 | AMD | 2022 | CORRECT | Does AMD have a reasonably healthy liquidity profile based on its quick ratio for FY22? If the quick ratio is not relevant to measure liquidity, please state that and explain why. |
| 8 | AMD | 2022 | INCORRECT | What drove revenue change as of the FY22 for AMD? |
| 9 | AMD | 2022 | CORRECT | Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for AMD in FY22? |
| 10 | AMD | 2022 | INCORRECT | Did AMD report customer concentration in FY22? |
| 11 | American Express | 2022 | PARTIAL | What are the geographies that American Express primarily operates in as of 2022? |
| 12 | American Express | 2022 | INCORRECT | What drove gross margin change as of the FY2022 for American Express? If gross margin is not a useful metric for a company like this, then please state that and explain why. |
| 13 | American Express | 2022 | CORRECT | What was the largest liability in American Express's Balance Sheet in 2022? |
| 14 | Best Buy | 2023 | PARTIAL | Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why. |
| 15 | Best Buy | 2023 | CORRECT | Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Best Buy in FY2023? |
| 16 | Boeing | 2022 | PARTIAL | Has Boeing reported any materially important ongoing legal battles from FY2022? |
| 17 | Boeing | 2022 | INCORRECT | Who are the primary customers of Boeing as of FY2022? |
| 18 | Boeing | 2022 | PARTIAL | What production rate changes is Boeing forecasting for FY2023? |
| 19 | Coca-Cola | 2022 | CORRECT | What is Coca Cola's FY2022 dividend payout ratio (using total cash dividends paid and net income attributable to shareholders)? Round answer to two decimal places. Answer the question asked by assuming you only have access to information clearly displayed in the cash flow statement and the income statement. |
| 20 | Corning | 2022 | CORRECT | Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why. |
| 21 | CVS Health | 2022 | PARTIAL | Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020? |
| 22 | Johnson & Johnson | 2022 | PARTIAL | Are JnJ's FY2022 financials that of a high growth company? |
| 23 | Johnson & Johnson | 2022 | CORRECT | Roughly how many times has JnJ sold its inventory in FY2022? Calculate inventory turnover ratio for FY2022; if conventional inventory management is not meaningful for the company then state that and explain why. |
| 24 | Nike | 2023 | CORRECT | Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Nike in FY2023? |
| 25 | PepsiCo | 2022 | INCORRECT | Has Pepsico reported any materially important ongoing legal battles from FY2022 and FY2021? |
| 26 | PepsiCo | 2022 | INCORRECT | What is the FY2022 unadjusted EBITDA less capex for PepsiCo? Define unadjusted EBITDA as unadjusted operating income + depreciation and amortization [from cash flow statement]. Answer in USD millions. Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the statement of cash flows and the income statement. |
| 27 | Pfizer | 2021 | CORRECT | Did Pfizer grow its PPNE between FY20 and FY21? |
| 28 | Pfizer | 2021 | INCORRECT | What are three main companies acquired by Pfizer mentioned in this 10K report? |
| 29 | Ulta Beauty | 2023 | INCORRECT | What are major acquisitions that Ulta Beauty has done in FY2023 and FY2022? |
| 30 | Verizon | 2022 | PARTIAL | Is Verizon a capital intensive business based on FY 2022 data? |

---

## Detailed results

### 1. Is 3M a capital-intensive business based on FY2022 data?
- **Company / FY:** 3M 2022  |  **Routed to:** None  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies 3M as not extremely capital-intensive but incorrectly concludes that it is capital-intensive overall, whereas the reference answer states the opposite.
- **FinanceBench gold:** No, the company is managing its CAPEX and Fixed Assets pretty efficiently, which is evident from below key metrics:
CAPEX/Revenue Ratio: 5.1%
Fixed assets/Total Assets: 20%
Return on Assets= 12.4%
- **FinChat:** To determine if 3M is a capital-intensive business, we can look at the ratio of property, plant, and equipment (PP&E) to total assets. According to the FY2022 data, 3M's PP&E (net) is $9.18 billion, and total assets are $46.45 billion. The ratio of PP&E to total assets is 19.8% (Source: [1] 3M 10-K (FY2022) - Balance Sheet (XBRL), [4] 3M 10-K (FY2022) - Financial Trends (XBRL)). 

Additionally, the capital expenditure as a percentage of revenue is 5.1% (Source: [4] 3M 10-K (FY2022) - Financial Trends (XBRL), [8] 3M 10-K (FY2022) - Key Ratios (XBRL)). 

Considering these metrics, 3M can be considered a capital-intensive business, but not extremely so, as the PP&E ratio and capital expenditure percentage are significant but not overwhelmingly high.

Sources:
[1] 3M 10-K (FY2022) - Balance Sheet (XBRL)
[4] 3M 10-K (FY2022) - Financial Trends (XBRL)
[8] 3M 10-K (FY2022) - Key Ratios (XBRL)

### 2. If we exclude the impact of M&A, which segment has dragged down 3M's overall growth in 2022?
- **Company / FY:** 3M 2022  |  **Routed to:** None  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, whereas the reference answer provides a specific fact.
- **FinanceBench gold:** The consumer segment shrunk by 0.9% organically.
- **FinChat:** I couldn't find that in the filings I have.

Sources: [1] 3M 10-K (FY2022), [2] 3M 10-K (FY2022), [3] 3M 10-K (FY2022), [4] 3M 10-K (FY2022), [5] 3M 10-K (FY2022), [8] 3M 10-K (FY2022)

### 3. Does Adobe have an improving Free cashflow conversion as of FY2022?
- **Company / FY:** Adobe 2022  |  **Routed to:** ADBE  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly states the FCF conversion for FY2022 but fails to provide a comparison to the previous year's data to determine if it's improving.
- **FinanceBench gold:** Yes, the FCF conversion (using net income as the denominator) for Adobe has improved by ~13% from 143% in 2021 to 156% in 2022
- **FinChat:** Adobe's Free cash flow conversion (FCF / net income) for FY2022 is 155.5%. However, there is no previous year's data provided to compare and determine if it's improving. 
Sources:
[3] Adobe 10-K (FY2022) - Key Ratios (XBRL)

### 4. Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- **Company / FY:** AES Corporation 2022  |  **Routed to:** AES  |  **Verdict:** PARTIAL
- **Judge:** The system answer calculates the inventory turnover ratio but with a different value than the reference answer, and also provides a valid explanation for why conventional inventory management may not be entirely meaningful for AES Corporation.
- **FinanceBench gold:** AES has converted inventory 9.5 times in FY 2022.
- **FinChat:** AES Corporation, FY2022. The inventory turnover ratio can be calculated as the cost of goods sold divided by the average inventory. 

Cost of Goods and Services Sold: $10.07 billion (from [3] AES Corporation 10-K (FY2022) - Income Statement)
Inventory: $1.05 billion (from [3] AES Corporation 10-K (FY2022) - Income Statement and [7] AES Corporation 10-K (FY2022))
Previous year's inventory: $604 million (from [2] AES Corporation 10-K (FY2022) - Financial Trends and [7] AES Corporation 10-K (FY2022))

Average inventory = ($1.05 billion + $604 million) / 2 = $827 million

Inventory turnover ratio = $10.07 billion / $827 million = 12.17

However, according to [1] AES Corporation 10-K (FY2022) - Key Ratios, the inventory turnover is given as 9.54. 

Conventional inventory management may not be entirely meaningful for AES Corporation as it is an electric power generation and distribution company, and its inventory may not be as significant a component of its operations as it would be for a manufacturing or retail company. Nevertheless, the inventory turnover ratio can still provide some insight into the company's ability to manage its inventory.

Sources:
[1] AES Corporation 10-K (FY2022) - Key Ratios
[2] AES Corporation 10-K (FY2022) - Financial Trends
[3] AES Corporation 10-K (FY2022) - Income Statement
[7] AES Corporation 10-K (FY2022)

### 5. Has AMCOR's quick ratio improved or declined between FY2023 and FY2022? If the quick ratio is not something that a financial analyst would ask about a company like this, then state that and explain why.
- **Company / FY:** Amcor 2023  |  **Routed to:** AMCR  |  **Verdict:** INCORRECT
- **Judge:** The system answer incorrectly states that the quick ratio improved from 0.93 to 0.96, whereas the reference answer states it improved from 0.67 to 0.69.
- **FinanceBench gold:** The quick ratio has slightly improved from 0.67 times to 0.69 times between FY 2023 and FY 2022.(3.4% jump)
- **FinChat:** The quick ratio of Amcor (AMCR) has improved between FY2022 and FY2023, from 0.93 to 0.96, which represents a 3.8% increase. 

This is a relevant metric for a financial analyst to consider, as the quick ratio is a liquidity metric that assesses a company's ability to meet its short-term obligations using its liquid assets. It is particularly useful for analyzing companies with significant current liabilities, such as Amcor.

Sources:
[1] Amcor 10-K (FY2023) - Financial Trends (XBRL)
[2] Amcor 10-K (FY2023) - Key Ratios (XBRL)

### 6. What industry does AMCOR primarily operate in?
- **Company / FY:** Amcor 2023  |  **Routed to:** AMCR  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately describes Amcor's primary industry as packaging and lists its specific end markets.
- **FinanceBench gold:** Amcor is a global leader in packaging production for various use cases.
- **FinChat:** Amcor primarily operates in the packaging industry, specifically in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets. (Amcor, FY2023)

Sources:
[1] Amcor 10-K (FY2023)
[2] Amcor 10-K (FY2023)
[3] Amcor 10-K (FY2023)
[4] Amcor 10-K (FY2023)

### 7. Does AMD have a reasonably healthy liquidity profile based on its quick ratio for FY22? If the quick ratio is not relevant to measure liquidity, please state that and explain why.
- **Company / FY:** AMD 2022  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact (quick ratio of 1.77) and provides a correct explanation of the quick ratio's relevance to liquidity.
- **FinanceBench gold:** Yes. The quick ratio is 1.57, calculated as (cash and cash equivalents+Short term investments+Accounts receivable, net+receivables from related parties)/ (current liabilities).
- **FinChat:** Advanced Micro Devices (AMD) has a quick ratio of 1.77 for FY2022. This suggests that AMD has a reasonably healthy liquidity profile, as the quick ratio is above 1, indicating that the company has sufficient liquid assets to cover its current liabilities, even if it doesn't sell any inventory.

The quick ratio is relevant to measure liquidity because it assesses a company's ability to meet its short-term obligations using its most liquid assets, such as cash, cash equivalents, and accounts receivable, excluding inventory.

Sources:
[1] Advanced Micro Devices 10-K (FY2022) - Key Ratios (XBRL)

### 8. What drove revenue change as of the FY22 for AMD?
- **Company / FY:** AMD 2022  |  **Routed to:** AMD  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it cannot find the answer, whereas the reference answer provides specific information about the drivers of revenue change for AMD as of FY22.
- **FinanceBench gold:** In 2022, AMD reported Higher sales of their EPYC server processors, higher semi-custom product sales, and the inclusion of Xilinx embedded product sales
- **FinChat:** I couldn't find that in the filings I have.

### 9. Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for AMD in FY22?
- **Company / FY:** AMD 2022  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact that operating activities brought in the most cash flow for AMD in FY22.
- **FinanceBench gold:** In 2022, AMD brought in the most cashflow from Operations
- **FinChat:** Among operations, investing, and financing activities, operating activities brought in the most cash flow for AMD in FY22, with $3.56 billion in net cash provided. 

Sources:
[1] Advanced Micro Devices 10-K (FY2022) - Cash Flow Statement (XBRL)

### 10. Did AMD report customer concentration in FY22?
- **Company / FY:** AMD 2022  |  **Routed to:** AMD  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it cannot find the answer, whereas the reference answer confirms that AMD did report customer concentration in FY22.
- **FinanceBench gold:** Yes, one customer accounted for 16% of consolidated net revenue
- **FinChat:** I couldn't find that in the filings I have.
Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 11. What are the geographies that American Express primarily operates in as of 2022?
- **Company / FY:** American Express 2022  |  **Routed to:** AXP  |  **Verdict:** PARTIAL
- **Judge:** The system answer lists more specific countries than the reference answer, but the reference answer's broader geography categories (EMEA, APAC, LACC) are not mentioned.
- **FinanceBench gold:** United States, EMEA, APAC, and LACC
- **FinChat:** As of 2022, American Express operates in various geographies including the U.S., Canada, Mexico, England, India, Philippines, Japan, Malaysia, Australia, and Spain, among others. 

Sources:
[5] American Express 10-K (FY2022)

### 12. What drove gross margin change as of the FY2022 for American Express? If gross margin is not a useful metric for a company like this, then please state that and explain why.
- **Company / FY:** American Express 2022  |  **Routed to:** AXP  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, but the reference answer provides a clear explanation that gross margin is not a useful metric for American Express.
- **FinanceBench gold:** Performance is not measured through gross margin
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 13. What was the largest liability in American Express's Balance Sheet in 2022?
- **Company / FY:** American Express 2022  |  **Routed to:** AXP  |  **Verdict:** CORRECT
- **Judge:** The system answer matches the reference answer on the key fact (customer deposits) and number ($110.24 billion).
- **FinanceBench gold:** Customer deposits
- **FinChat:** The largest liability in American Express's Balance Sheet in 2022 was Customer deposits, totaling $110.24 billion. 
Company: American Express, Fiscal Year: 2022
Sources: [1] American Express 10-K (FY2022) - Balance Sheet (XBRL)

### 14. Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why.
- **Company / FY:** Best Buy 2023  |  **Routed to:** BBY  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly states the decline in gross margins but incorrectly states that they have fluctuated, when in fact they have been historically consistent with a minor decline.
- **FinanceBench gold:** Yes, the margins have been consistent, there has been a minor decline of 1.1% in gross margins between FY2022 and FY2023.
- **FinChat:** Best Buy's gross margins have fluctuated. In FY2023, the gross margin was 21.4%, and in FY2022, it was 22.5%, a decrease of 1.1 percentage points. 
Best Buy, as a retailer, uses gross margin as a relevant metric to evaluate its profitability.

Company: Best Buy (BBY), Fiscal Year: 2023
Sources: [1] Best Buy 10-K (FY2023) - Financial Trends (XBRL), [2] Best Buy 10-K (FY2023) - Key Ratios (XBRL)

### 15. Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Best Buy in FY2023?
- **Company / FY:** Best Buy 2023  |  **Routed to:** BBY  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact(s) or number(s), specifically that operating activities brought in the most cash flow for Best Buy in FY2023.
- **FinanceBench gold:** Best Buy generated the most cash flow from operating activities in FY 2023 ($1.8 bn)
- **FinChat:** According to the provided context, the cash flow from operations brought in the most cash for Best Buy in FY2023, with $1.82 billion in total cash provided by operating activities.

Sources:
[1] Best Buy 10-K (FY2023) - Cash Flow Statement (XBRL)

### 16. Has Boeing reported any materially important ongoing legal battles from FY2022?
- **Company / FY:** Boeing 2022  |  **Routed to:** BA  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies the relevant legal battles but incorrectly states that they were resolved in 2021, when in fact the reference answer indicates that the lawsuits are ongoing.
- **FinanceBench gold:** Yes. Multiple lawsuits have been filed against Boeing resulting from a 2018 Lion Air crash and a 2019 Ethiopian Airlines crash.
- **FinChat:** Boeing has reported legal actions related to the October 29, 2018 accident of Lion Air Flight 610 and the March 10, 2019 accident of Ethiopian Airlines Flight 302. However, it is mentioned that during 2021, Boeing entered into a Deferred Prosecution Agreement with the U.S. Department of Justice, which resolved the Department of Justice's investigation. 
Boeing, FY2022. 
Sources:
[1] Boeing 10-K (FY2022)

### 17. Who are the primary customers of Boeing as of FY2022?
- **Company / FY:** Boeing 2022  |  **Routed to:** BA  |  **Verdict:** INCORRECT
- **Judge:** The system answer states it cannot find the answer, whereas the reference answer provides specific information about Boeing's primary customers.
- **FinanceBench gold:** Boeing's primary customers as of FY2022 are a limited number of commercial airlines and the US government. The US government accounted for 40% of Boeing's total revenues in FY2022.
- **FinChat:** I couldn't find that in the filings I have.

Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 18. What production rate changes is Boeing forecasting for FY2023?
- **Company / FY:** Boeing 2022  |  **Routed to:** BA  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies the 787 production rate increase but incorrectly states the 777X production rate and does not mention the 777X production resuming in 2023.
- **FinanceBench gold:** Boeing forecasts an increase in the production rates for the 737, 777X and 787 aircrafts in 2023.
- **FinChat:** Boeing is forecasting the following production rate changes for FY2023: 
- The 787 program is expected to gradually increase to 5 per month. 
- The 777X production is expected to resume in 2023, but no specific rate is mentioned.
- The 737 production rate is expected to have further gradual increases based on market demand and supply chain capacity, with a current rate of 31 per month.

Sources:
[1] Boeing 10-K (FY2022)
[5] Boeing 10-K (FY2022)
[8] Boeing 10-K (FY2022)

### 19. What is Coca Cola's FY2022 dividend payout ratio (using total cash dividends paid and net income attributable to shareholders)? Round answer to two decimal places. Answer the question asked by assuming you only have access to information clearly displayed in the cash flow statement and the income statement.
- **Company / FY:** Coca-Cola 2022  |  **Routed to:** KO  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly calculates the dividend payout ratio as 0.80, matching the reference answer.
- **FinanceBench gold:** 0.8
- **FinChat:** To calculate the dividend payout ratio, we need to divide the total cash dividends paid by the net income attributable to shareholders. 

From the Cash Flow Statement (excerpt [1]), the total cash dividends paid are $7.62 billion. 
From the Income Statement (excerpt [2]), the net income attributable to shareholders is $9.54 billion.

Dividend payout ratio = Total cash dividends paid / Net income attributable to shareholders
= $7.62 billion / $9.54 billion
= 0.80

Rounded to two decimal places, the dividend payout ratio is 0.80.

Sources:
[1] Coca-Cola 10-K (FY2022) - Cash Flow Statement (XBRL)
[2] Coca-Cola 10-K (FY2022) - Income Statement (XBRL)

### 20. Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- **Company / FY:** Corning 2022  |  **Routed to:** GLW  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly calculates Corning's working capital as $2.28 billion, which is positive, and explains why working capital is relevant for the company.
- **FinanceBench gold:** Yes. Corning had a positive working capital amount of $831 million by FY 2022 close. This answer considers only operating current assets and current liabilities that were clearly shown in the balance sheet.
- **FinChat:** To determine if Corning has positive working capital, we need to calculate it by subtracting current liabilities from current assets. 
Current assets: $7.45 billion
Current liabilities: $5.17 billion
Working capital: $7.45 billion - $5.17 billion = $2.28 billion

Since working capital is positive ($2.28 billion), Corning has positive working capital based on FY2022 data.

Working capital is a relevant metric for Corning as it indicates the company's ability to meet its short-term obligations.

Sources:
[1] Corning 10-K (FY2022) - Balance Sheet (XBRL)

### 21. Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020?
- **Company / FY:** CVS Health 2022  |  **Routed to:** CVS  |  **Verdict:** PARTIAL
- **Judge:** The system answer partially captures the ongoing legal battles of CVS Health, but misses the "usual and customary pricing litigation" and "PBM litigation and investigations" mentioned in the reference answer.
- **FinanceBench gold:** Yes, CVS Health has been involved in multiple ongoing legal battles. Some notable legal dispute areas for CVS are: (1) usual and customary pricing litigation: where it's claimed that CVSâs retail pharmacies overcharged for prescription drugs; (2) PBM litigation and investigations: where it's claimed that that rebate agreements between the drug manufacturers and PBMs caused inflated prices for certain drug products; and (3) controlled substances litigation: legal matters around opioids for which CVS has agreed to pay up to $4.3 billion to claimants in remediation and $625 million to attorneys and fees
- **FinChat:** CVS Health reported ongoing legal battles related to prescription opioids and other controlled substances, as well as prescription processing practices. In 2022, the DOJ served the Company with a CID regarding potential violations of the federal Controlled Substances Act and the federal False Claims Act. In 2020, the DOJ served the Company with a DEA administrative subpoena on similar subjects. The Company is also named as a defendant in several lawsuits concerning its prescription processing practices.

Sources:
[4] CVS Health 10-K (FY2022)

### 22. Are JnJ's FY2022 financials that of a high growth company?
- **Company / FY:** Johnson & Johnson 2022  |  **Routed to:** None  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies significant growth in revenue and net income, but incorrectly labels JnJ as a high growth company based on this information.
- **FinanceBench gold:** No, JnJ's FY2022 financials are not of a high growth company as sales grew by 1.3% in FY2022.
- **FinChat:** Johnson & Johnson (JNJ) FY2022 revenue grew 13.6% year-over-year, and net income grew 41.9%. While this indicates significant growth, the company's 5-year shareholder return performance shows more modest growth compared to some indices, such as the S&P 500 Index and the S&P Healthcare Equipment Index. 

Sources:
[1] Johnson & Johnson 10-K (FY2022) - Financial Trends (XBRL)
[6] Johnson & Johnson 10-K (FY2022)

### 23. Roughly how many times has JnJ sold its inventory in FY2022? Calculate inventory turnover ratio for FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- **Company / FY:** Johnson & Johnson 2022  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer matches the reference answer on the key fact of inventory turnover ratio and its implication for the number of times JnJ sold its inventory in FY2022.
- **FinanceBench gold:** JnJ sold its inventory 2.7 times in FY2022.
- **FinChat:** Johnson & Johnson (JNJ) FY2022 inventory turnover ratio is 2.87. This means the company has sold its inventory approximately 2.87 times in FY2022.

Sources:
[1] Johnson & Johnson 10-K (FY2022) - Key Ratios (XBRL)

### 24. Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Nike in FY2023?
- **Company / FY:** Nike 2023  |  **Routed to:** NKE  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact that cash flow from operations was the highest for Nike in FY2023.
- **FinanceBench gold:** Among the three, cash flow from operations was the highest for Nike in FY2023.
- **FinChat:** Among operations, investing, and financing activities, operating activities brought in the most cash flow for Nike in FY2023, with $5.84 billion in cash provided by operations. 

Sources:
[1] Nike 10-K (FY2023) - Cash Flow Statement (XBRL)

### 25. Has Pepsico reported any materially important ongoing legal battles from FY2022 and FY2021?
- **Company / FY:** PepsiCo 2022  |  **Routed to:** PEP  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, but the reference answer states that Pepsico is not involved in material legal battles, suggesting the information should be available.
- **FinanceBench gold:** No, Pepsico is not involved in material legal battles.
- **FinChat:** I couldn't find that in the filings I have.

Sources: [1] PepsiCo 10-K (FY2022) - Financial Trends (XBRL), [2] PepsiCo 10-K (FY2022) - Cash Flow Statement (XBRL), [3] PepsiCo 10-K (FY2022) - Balance Sheet (XBRL), [4] PepsiCo 10-K (FY2022) - Income Statement (XBRL), [5] PepsiCo 10-K (FY2022), [6] PepsiCo 10-K (FY2022), [7] PepsiCo 10-K (FY2022), [8] PepsiCo 10-K (FY2022)

### 26. What is the FY2022 unadjusted EBITDA less capex for PepsiCo? Define unadjusted EBITDA as unadjusted operating income + depreciation and amortization [from cash flow statement]. Answer in USD millions. Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the statement of cash flows and the income statement.
- **Company / FY:** PepsiCo 2022  |  **Routed to:** PEP  |  **Verdict:** INCORRECT
- **Judge:** The system answer incorrectly calculates the unadjusted EBITDA less capex for PepsiCo in FY2022 as $24,281 million, whereas the reference answer is $9,068 million.
- **FinanceBench gold:** $9068.00
- **FinChat:** To calculate the unadjusted EBITDA less capex for PepsiCo in FY2022, we first need to find the unadjusted operating income and depreciation and amortization. 

From the provided context, specifically the Cash Flow Statement (XBRL) for PepsiCo (PEP) FY2022, we can find the following relevant figures:
- Net income: $8.98 billion
- Depreciation and amortization: $2.76 billion
- Impairment and other charges: $3.62 billion
- Restructuring and impairment charges: $411.0 million

However, to calculate the unadjusted operating income, we need to add back the impairment and other charges, and the restructuring and impairment charges to the net income, and then subtract the gain associated with the Juice Transaction. 

Given:
- Net income: $8.98 billion
- Gain associated with the Juice Transaction: $-3.32 billion (this is a gain, so we add it back to get to operating income)
- Impairment and other charges: $3.62 billion
- Restructuring and impairment charges: $411.0 million

Unadjusted operating income = Net income - Gain associated with the Juice Transaction + Impairment and other charges + Restructuring and impairment charges
Unadjusted operating income = $8.98 billion - (-$3.32 billion) + $3.62 billion + $0.411 billion
Unadjusted operating income = $8.98 billion + $3.32 billion + $3.62 billion + $0.411 billion
Unadjusted operating income = $16.311 billion

Now, to find the unadjusted EBITDA, we add the depreciation and amortization to the unadjusted operating income:
Unadjusted EBITDA = Unadjusted operating income + Depreciation and amortization
Unadjusted EBITDA = $16.311 billion + $2.76 billion
Unadjusted EBITDA = $19.071 billion

Next, to find the EBITDA less capex, we subtract the capital spending from the unadjusted EBITDA:
- Capital spending: $-5.21 billion (negative because it's an outflow)

Unadjusted EBITDA less capex = Unadjusted EBITDA - Capital spending
Unadjusted EBITDA less capex = $19.071 billion - (-$5.21 billion)
Unadjusted EBITDA less capex = $19.071 billion + $5.21 billion
Unadjusted EBITDA less capex = $24.281 billion

In USD millions, the unadjusted EBITDA less capex for PepsiCo in FY2022 is $24,281 million.

Sources:
[1] PepsiCo 10-K (FY2022) - Cash Flow Statement (XBRL)

### 27. Did Pfizer grow its PPNE between FY20 and FY21?
- **Company / FY:** Pfizer 2021  |  **Routed to:** PFE  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact that Pfizer grew its PPNE between FY20 and FY21.
- **FinanceBench gold:** Yes, change in PPNE was positive year over year
- **FinChat:** Yes, Pfizer grew its Property, Plant & Equipment (net) by 8.3% from $13.74 billion in FY2020 to $14.88 billion in FY2021.
Sources:
[1] Pfizer 10-K (FY2021) - Financial Trends (XBRL)

### 28. What are three main companies acquired by Pfizer mentioned in this 10K report?
- **Company / FY:** Pfizer 2021  |  **Routed to:** PFE  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it cannot find the answer in the available filings.
- **FinanceBench gold:** Trillium, Array, and Therachon
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 29. What are major acquisitions that Ulta Beauty has done in FY2023 and FY2022?
- **Company / FY:** Ulta Beauty 2023  |  **Routed to:** ULTA  |  **Verdict:** INCORRECT
- **Judge:** The system answer states it couldn't find the information, but the reference answer confirms that there were no acquisitions.
- **FinanceBench gold:** Ulta Beauty did not make any acquisitions in FY2023 and FY2022.
- **FinChat:** I couldn't find that in the filings I have. 
Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 30. Is Verizon a capital intensive business based on FY 2022 data?
- **Company / FY:** Verizon 2022  |  **Routed to:** VZ  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies Verizon as a capital-intensive business but uses a different method to calculate capital intensity (16.9% of revenue) compared to the reference answer (approximately $2.77 of assets to generate $1 of revenue).
- **FinanceBench gold:** Yes. Verizon's capital intensity ratio was approximately 2.774729. This means that it took approximately $2.77 of assets to generate $1 of revenue and thus, Verizon can be considered capital intensive.
- **FinChat:** Yes, Verizon is a capital-intensive business. According to the FY2022 data, Verizon's capital expenditures were $23.09 billion, which is approximately 16.9% of its revenue ($136.84 billion). This suggests a significant investment in property, plant, and equipment, indicating a capital-intensive business.

Sources:
[1] Verizon 10-K (FY2022) - Cash Flow Statement (XBRL)
[2] Verizon 10-K (FY2022) - Financial Trends (XBRL)
