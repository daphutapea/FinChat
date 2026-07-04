# FinChat Evaluation — FinanceBench (corpus-aligned subset)

FinChat is graded by an LLM-as-judge against gold answers from the [FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench) benchmark, on every 10-K question whose company + fiscal year is in the corpus. FinanceBench is expert-written and intentionally hard.

- **Questions evaluated:** 30
- **CORRECT:** 10   **PARTIAL:** 7   **INCORRECT:** 13
- **Score:** 13.5 / 30
- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** 45%

**Accuracy by FinanceBench question type:**

| Question type | Accuracy | N |
|---|---|---|
| domain-relevant | 50% | 21 |
| metrics-generated | 50% | 2 |
| novel-generated | 29% | 7 |

| # | Company | FY | Verdict | Question |
|---|---------|----|---------|----------|
| 1 | 3M | 2022 | INCORRECT | Is 3M a capital-intensive business based on FY2022 data? |
| 2 | 3M | 2022 | INCORRECT | If we exclude the impact of M&A, which segment has dragged down 3M's overall growth in 2022? |
| 3 | Adobe | 2022 | PARTIAL | Does Adobe have an improving Free cashflow conversion as of FY2022? |
| 4 | AES Corporation | 2022 | INCORRECT | Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why. |
| 5 | Amcor | 2023 | INCORRECT | Has AMCOR's quick ratio improved or declined between FY2023 and FY2022? If the quick ratio is not something that a financial analyst would ask about a company like this, then state that and explain why. |
| 6 | Amcor | 2023 | CORRECT | What industry does AMCOR primarily operate in? |
| 7 | AMD | 2022 | CORRECT | Does AMD have a reasonably healthy liquidity profile based on its quick ratio for FY22? If the quick ratio is not relevant to measure liquidity, please state that and explain why. |
| 8 | AMD | 2022 | INCORRECT | What drove revenue change as of the FY22 for AMD? |
| 9 | AMD | 2022 | CORRECT | Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for AMD in FY22? |
| 10 | AMD | 2022 | INCORRECT | Did AMD report customer concentration in FY22? |
| 11 | American Express | 2022 | PARTIAL | What are the geographies that American Express primarily operates in as of 2022? |
| 12 | American Express | 2022 | CORRECT | What drove gross margin change as of the FY2022 for American Express? If gross margin is not a useful metric for a company like this, then please state that and explain why. |
| 13 | American Express | 2022 | CORRECT | What was the largest liability in American Express's Balance Sheet in 2022? |
| 14 | Best Buy | 2023 | INCORRECT | Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why. |
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
| 27 | Pfizer | 2021 | INCORRECT | Did Pfizer grow its PPNE between FY20 and FY21? |
| 28 | Pfizer | 2021 | INCORRECT | What are three main companies acquired by Pfizer mentioned in this 10K report? |
| 29 | Ulta Beauty | 2023 | INCORRECT | What are major acquisitions that Ulta Beauty has done in FY2023 and FY2022? |
| 30 | Verizon | 2022 | PARTIAL | Is Verizon a capital intensive business based on FY 2022 data? |

---

## Detailed results

### 1. Is 3M a capital-intensive business based on FY2022 data?
- **Company / FY:** 3M 2022  |  **Routed to:** None  |  **Verdict:** INCORRECT
- **Judge:** The system answer concludes that 3M is a capital-intensive business, which contradicts the reference answer.
- **FinanceBench gold:** No, the company is managing its CAPEX and Fixed Assets pretty efficiently, which is evident from below key metrics:
CAPEX/Revenue Ratio: 5.1%
Fixed assets/Total Assets: 20%
Return on Assets= 12.4%
- **FinChat:** To determine if 3M is a capital-intensive business, we can look at the capital expenditure as a percentage of revenue. According to the provided context, the capital expenditure as a percentage of revenue is 5.1% (Source: [7] 3M 10-K (FY2022) - Key Ratios). 

Additionally, 3M's property, plant, and equipment - net is $9.18 billion, which is approximately 19.8% of total assets (Source: [1] 3M 10-K (FY2022) - Balance Sheet). The company also expects 2023 capital spending to be approximately $1.5 billion to $1.8 billion (Source: [3] 3M 10-K (FY2022)).

Considering these factors, it can be inferred that 3M has significant investments in property, plant, and equipment, and spends a notable amount on capital expenditures. Therefore, based on FY2022 data, 3M can be considered a capital-intensive business.

Sources:
[1] 3M 10-K (FY2022) - Balance Sheet
[3] 3M 10-K (FY2022)
[7] 3M 10-K (FY2022) - Key Ratios

### 2. If we exclude the impact of M&A, which segment has dragged down 3M's overall growth in 2022?
- **Company / FY:** 3M 2022  |  **Routed to:** None  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, whereas the reference answer provides a specific fact.
- **FinanceBench gold:** The consumer segment shrunk by 0.9% organically.
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1] 3M 10-K (FY2022), [2] 3M 10-K (FY2022), [3] 3M 10-K (FY2022), [4] 3M 10-K (FY2022), [5] 3M 10-K (FY2022), [8] 3M 10-K (FY2022)

### 3. Does Adobe have an improving Free cashflow conversion as of FY2022?
- **Company / FY:** Adobe 2022  |  **Routed to:** ADBE  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly calculates the free cash flow conversion for FY2022 but fails to confirm if it's an improvement due to lack of previous years' data.
- **FinanceBench gold:** Yes, the FCF conversion (using net income as the denominator) for Adobe has improved by ~13% from 143% in 2021 to 156% in 2022
- **FinChat:** To assess if Adobe has an improving free cash flow conversion, we need to compare the free cash flow to the net income. 
Adobe (ADBE) FY2022: Net income: $4.76 billion, Free cash flow: $7.40 billion.
Since free cash flow ($7.40 billion) is greater than net income ($4.76 billion), the free cash flow conversion is over 155% (7.40/4.76). 
However, without previous years' data, we cannot confirm if this is an improvement.

Sources:
[1] Adobe 10-K (FY2022) - Cash Flow Statement (XBRL)
[2] Adobe 10-K (FY2022) - Key Ratios (XBRL)
[8] Adobe 10-K (FY2022) - Income Statement (XBRL)

### 4. Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- **Company / FY:** AES Corporation 2022  |  **Routed to:** AES  |  **Verdict:** INCORRECT
- **Judge:** The system answer incorrectly states that AES Corporation sold its inventory roughly 12 times in FY2022, whereas the reference answer states 9.5 times.
- **FinanceBench gold:** AES has converted inventory 9.5 times in FY 2022.
- **FinChat:** To calculate the inventory turnover ratio, we need to know the cost of goods sold and the average inventory. 

From [2] AES Corporation 10-K (FY2022) - Income Statement (XBRL), we have:
Cost of Goods and Services Sold: $10.07 billion

From [6] AES Corporation 10-K (FY2022), we have:
Total Inventory (at the end of FY2022): $1,055 million
Total Inventory (at the end of FY2021): $604 million
We can calculate the average inventory: ($1,055 million + $604 million) / 2 = $829.5 million

Inventory turnover ratio = Cost of Goods and Services Sold / Average Inventory
= $10.07 billion / $829.5 million
= 12.14

So, AES Corporation has sold its inventory roughly 12 times in FY2022.

Conventional inventory management is meaningful for the company as it has a significant amount of inventory ($1,055 million) and the inventory turnover ratio is reasonably high (12.14), indicating that the company is able to sell and replace its inventory multiple times during the year.

Sources:
[2] AES Corporation 10-K (FY2022) - Income Statement (XBRL)
[6] AES Corporation 10-K (FY2022)

### 5. Has AMCOR's quick ratio improved or declined between FY2023 and FY2022? If the quick ratio is not something that a financial analyst would ask about a company like this, then state that and explain why.
- **Company / FY:** Amcor 2023  |  **Routed to:** AMCR  |  **Verdict:** INCORRECT
- **Judge:** The system answer does not provide a comparison between FY2023 and FY2022, as it only mentions the FY2023 quick ratio without any information about FY2022.
- **FinanceBench gold:** The quick ratio has slightly improved from 0.67 times to 0.69 times between FY 2023 and FY 2022.(3.4% jump)
- **FinChat:** I couldn't find that in the filings I have.

The quick ratio for FY2023 is provided as 0.96, but there is no information provided about the quick ratio for FY2022 to compare it to. 

Sources: [1] Amcor 10-K (FY2023) - Key Ratios (XBRL)

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
- **Judge:** The system answer agrees with the reference on the key fact (quick ratio of 1.57 vs 1.77) and the interpretation of the quick ratio as a measure of liquidity.
- **FinanceBench gold:** Yes. The quick ratio is 1.57, calculated as (cash and cash equivalents+Short term investments+Accounts receivable, net+receivables from related parties)/ (current liabilities).
- **FinChat:** Advanced Micro Devices (AMD) has a quick ratio of 1.77 for FY2022. This suggests that AMD has a reasonably healthy liquidity profile, as the quick ratio is above 1, indicating that the company has sufficient liquid assets to cover its current liabilities, even if it doesn't sell its inventories.

Sources:
[1] Advanced Micro Devices 10-K (FY2022) - Key Ratios (XBRL)

### 8. What drove revenue change as of the FY22 for AMD?
- **Company / FY:** AMD 2022  |  **Routed to:** AMD  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, but the reference answer provides specific details about the drivers of revenue change for AMD in FY22.
- **FinanceBench gold:** In 2022, AMD reported Higher sales of their EPYC server processors, higher semi-custom product sales, and the inclusion of Xilinx embedded product sales
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1] Advanced Micro Devices 10-K (FY2022) - Cash Flow Statement (XBRL), [2] Advanced Micro Devices 10-K (FY2022) - Income Statement (XBRL), [3] Advanced Micro Devices 10-K (FY2022) - Key Ratios (XBRL), [4] Advanced Micro Devices 10-K (FY2022) - Balance Sheet (XBRL), [5] Advanced Micro Devices 10-K (FY2022), [6] Advanced Micro Devices 10-K (FY2022), [7] Advanced Micro Devices 10-K (FY2022), [8] Advanced Micro Devices 10-K (FY2022)

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
- **Company / FY:** American Express 2022  |  **Routed to:** AXP  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly states that gross margin is not explicitly mentioned in the provided excerpts.
- **FinanceBench gold:** Performance is not measured through gross margin
- **FinChat:** I couldn't find that in the filings I have. 

The provided excerpts do not mention gross margin or its change. They do provide information on revenues, expenses, and other financial metrics, but gross margin is not explicitly mentioned.

Sources:
[1] American Express 10-K (FY2022) - Cash Flow Statement (XBRL)
[2] American Express 10-K (FY2022) - Income Statement (XBRL)

### 13. What was the largest liability in American Express's Balance Sheet in 2022?
- **Company / FY:** American Express 2022  |  **Routed to:** AXP  |  **Verdict:** CORRECT
- **Judge:** The system answer matches the reference answer on the key fact (customer deposits) and provides a specific amount ($110.24 billion).
- **FinanceBench gold:** Customer deposits
- **FinChat:** The largest liability in American Express's Balance Sheet in 2022 was Customer deposits, totaling $110.24 billion. 
Sources:
[1] American Express 10-K (FY2022) - Balance Sheet (XBRL)

### 14. Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why.
- **Company / FY:** Best Buy 2023  |  **Routed to:** BBY  |  **Verdict:** INCORRECT
- **Judge:** The system answer states it couldn't find the information, but the reference answer provides the specific data needed to determine consistency.
- **FinanceBench gold:** Yes, the margins have been consistent, there has been a minor decline of 1.1% in gross margins between FY2022 and FY2023.
- **FinChat:** I couldn't find that in the filings I have. 

The provided context only includes the gross margin for FY2023, which is 21.4%. There is no historical data provided to determine if the gross margins are consistent.

Sources: [1] Best Buy 10-K (FY2023) - Key Ratios (XBRL)

### 15. Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Best Buy in FY2023?
- **Company / FY:** Best Buy 2023  |  **Routed to:** BBY  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact(s) or number(s), specifically that operating activities brought in the most cash flow for Best Buy in FY2023.
- **FinanceBench gold:** Best Buy generated the most cash flow from operating activities in FY 2023 ($1.8 bn)
- **FinChat:** Among operations, investing, and financing activities, operating activities brought in the most cash flow for Best Buy in FY2023, with $1.82 billion in total cash provided. 

Sources:
[1] Best Buy 10-K (FY2023) - Cash Flow Statement (XBRL)

### 16. Has Boeing reported any materially important ongoing legal battles from FY2022?
- **Company / FY:** Boeing 2022  |  **Routed to:** BA  |  **Verdict:** PARTIAL
- **Judge:** The system answer is partially correct, as it mentions the relevant lawsuits, but incorrectly states that the investigation was resolved through a Deferred Prosecution Agreement in 2021, when in fact the reference answer mentions the crashes as ongoing legal battles from FY2022.
- **FinanceBench gold:** Yes. Multiple lawsuits have been filed against Boeing resulting from a 2018 Lion Air crash and a 2019 Ethiopian Airlines crash.
- **FinChat:** Boeing has reported legal actions related to the accidents of Lion Air Flight 610 and Ethiopian Airlines Flight 302, but it entered into a Deferred Prosecution Agreement with the U.S. Department of Justice in 2021, which resolved the investigation. Additionally, it entered into a proposed settlement with plaintiffs in a shareholder derivative lawsuit. 
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
- **Judge:** The system answer correctly identifies the 787 and 737 production rate changes, but fails to mention the 777X production rate increase.
- **FinanceBench gold:** Boeing forecasts an increase in the production rates for the 737, 777X and 787 aircrafts in 2023.
- **FinChat:** Boeing is forecasting the following production rate changes for FY2023: 
- The 787 program is expected to gradually increase to 5 per month. 
- The 777X production is expected to resume in 2023, but no specific rate is mentioned.
- The 737 program production rate is expected to increase further, based on market demand and supply chain capacity, from the current 31 per month.

Sources:
[1] Boeing 10-K (FY2022)
[4] Boeing 10-K (FY2022)
[7] Boeing 10-K (FY2022)

### 19. What is Coca Cola's FY2022 dividend payout ratio (using total cash dividends paid and net income attributable to shareholders)? Round answer to two decimal places. Answer the question asked by assuming you only have access to information clearly displayed in the cash flow statement and the income statement.
- **Company / FY:** Coca-Cola 2022  |  **Routed to:** KO  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly calculates the dividend payout ratio using the provided information from the cash flow statement and income statement.
- **FinanceBench gold:** 0.8
- **FinChat:** To calculate the dividend payout ratio, we need to divide the total cash dividends paid by the net income attributable to shareholders. 

From the Cash Flow Statement (FY2022), the total cash dividends paid is $7.62 billion. 
From the Income Statement (FY2022), the net income attributable to shareholders is $9.54 billion.

Dividend payout ratio = Total cash dividends paid / Net income attributable to shareholders
= $7.62 billion / $9.54 billion
= 0.80

Rounded to two decimal places, the dividend payout ratio is 0.80.

Sources:
[1] Coca-Cola 10-K (FY2022) - Cash Flow Statement (XBRL)
[2] Coca-Cola 10-K (FY2022) - Income Statement (XBRL)

### 20. Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- **Company / FY:** Corning 2022  |  **Routed to:** GLW  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly calculates Corning's working capital as $2.28 billion, which is positive.
- **FinanceBench gold:** Yes. Corning had a positive working capital amount of $831 million by FY 2022 close. This answer considers only operating current assets and current liabilities that were clearly shown in the balance sheet.
- **FinChat:** To determine if Corning has positive working capital, we need to calculate it. Working capital is calculated as current assets minus current liabilities. 
According to Corning's 10-K (FY2022), current assets are $7.45 billion and current liabilities are $5.17 billion. 
Working capital = Current assets - Current liabilities = $7.45 billion - $5.17 billion = $2.28 billion.

Since working capital is positive, Corning has positive working capital based on FY2022 data.

Sources:
[1] Corning 10-K (FY2022) - Balance Sheet (XBRL)

### 21. Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020?
- **Company / FY:** CVS Health 2022  |  **Routed to:** CVS  |  **Verdict:** PARTIAL
- **Judge:** The system answer partially matches the reference answer by mentioning some of the ongoing legal battles, but it misses the "usual and customary pricing litigation" and "PBM litigation and investigations" areas, and also does not mention the $4.3 billion and $625 million settlements related to controlled substances litigation.
- **FinanceBench gold:** Yes, CVS Health has been involved in multiple ongoing legal battles. Some notable legal dispute areas for CVS are: (1) usual and customary pricing litigation: where it's claimed that CVSâs retail pharmacies overcharged for prescription drugs; (2) PBM litigation and investigations: where it's claimed that that rebate agreements between the drug manufacturers and PBMs caused inflated prices for certain drug products; and (3) controlled substances litigation: legal matters around opioids for which CVS has agreed to pay up to $4.3 billion to claimants in remediation and $625 million to attorneys and fees
- **FinChat:** CVS Health reported the following ongoing legal battles: 
- A DEA administrative subpoena in January 2020 regarding practices with respect to prescription opioids and other controlled substances.
- A CID from the DOJ in January 2022 regarding similar subjects.
- Prescription processing litigation and investigations concerning its prescription processing practices.

CVS Health, FY2022. 
Sources:
[1] CVS Health 10-K (FY2022), 
[4] CVS Health 10-K (FY2022)

### 22. Are JnJ's FY2022 financials that of a high growth company?
- **Company / FY:** Johnson & Johnson 2022  |  **Routed to:** None  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly states that the growth rate is not explicitly stated, but it does not directly address the key fact from the reference answer that sales grew by 1.3% in FY2022.
- **FinanceBench gold:** No, JnJ's FY2022 financials are not of a high growth company as sales grew by 1.3% in FY2022.
- **FinChat:** Johnson & Johnson (JNJ) FY2022 net earnings are $20.88 billion, and sales to customers are $93.78 billion. The net profit margin is 22.3%. While the company has significant revenue and earnings, the growth rate is not explicitly stated in the provided context. However, the 5-year shareholder return performance graph shows a steady increase, but the exact growth rate is not provided.

To determine if JNJ is a high-growth company, we would need more information on the year-over-year growth rate of revenue and earnings. 

Sources:
[1] Johnson & Johnson 10-K (FY2022) - Cash Flow Statement (XBRL)
[3] Johnson & Johnson 10-K (FY2022) - Income Statement (XBRL)
[4] Johnson & Johnson 10-K (FY2022) - Key Ratios (XBRL)

### 23. Roughly how many times has JnJ sold its inventory in FY2022? Calculate inventory turnover ratio for FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- **Company / FY:** Johnson & Johnson 2022  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer correctly calculates the inventory turnover ratio and provides a close approximation of the reference answer.
- **FinanceBench gold:** JnJ sold its inventory 2.7 times in FY2022.
- **FinChat:** To calculate the inventory turnover ratio, we need the cost of goods sold and the average inventory. 

Cost of goods sold: $29.86 billion (from [6] Johnson & Johnson 10-K (FY2022) - Income Statement)
Inventory: $10.39 billion (from [2] Johnson & Johnson 10-K (FY2022) - Balance Sheet)

Inventory turnover ratio = Cost of goods sold / Inventory
= $29.86 billion / $10.39 billion
= 2.87

This means JnJ sold its inventory approximately 2.87 times in FY2022.

Conventional inventory management may not be entirely meaningful for JnJ as it is a pharmaceutical and medical devices company with a complex supply chain and a wide range of products, including prescription drugs, medical devices, and consumer products. However, based on the available data, we can still calculate the inventory turnover ratio.

Sources:
[2] Johnson & Johnson 10-K (FY2022) - Balance Sheet
[6] Johnson & Johnson 10-K (FY2022) - Income Statement

### 24. Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Nike in FY2023?
- **Company / FY:** Nike 2023  |  **Routed to:** NKE  |  **Verdict:** CORRECT
- **Judge:** The system answer agrees with the reference on the key fact that cash flow from operations was the highest for Nike in FY2023.
- **FinanceBench gold:** Among the three, cash flow from operations was the highest for Nike in FY2023.
- **FinChat:** Among operations, investing, and financing activities, operating activities brought in the most cash flow for Nike in FY2023, with $5.84 billion in cash provided by operations. 

Sources:
[1] Nike 10-K (FY2023) - Cash Flow Statement (XBRL)

### 25. Has Pepsico reported any materially important ongoing legal battles from FY2022 and FY2021?
- **Company / FY:** PepsiCo 2022  |  **Routed to:** PEP  |  **Verdict:** INCORRECT
- **Judge:** The system answer explicitly states it couldn't find the information, whereas the reference answer confirms there are no material legal battles.
- **FinanceBench gold:** No, Pepsico is not involved in material legal battles.
- **FinChat:** I couldn't find that in the filings I have.
Sources: [1] PepsiCo 10-K (FY2022) - Cash Flow Statement (XBRL), [2] PepsiCo 10-K (FY2022) - Balance Sheet (XBRL), [3] PepsiCo 10-K (FY2022) - Income Statement (XBRL)

### 26. What is the FY2022 unadjusted EBITDA less capex for PepsiCo? Define unadjusted EBITDA as unadjusted operating income + depreciation and amortization [from cash flow statement]. Answer in USD millions. Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the statement of cash flows and the income statement.
- **Company / FY:** PepsiCo 2022  |  **Routed to:** PEP  |  **Verdict:** INCORRECT
- **Judge:** The system answer incorrectly calculates the unadjusted EBITDA as $12.519 billion, whereas the reference answer is $9,068 million.
- **FinanceBench gold:** $9068.00
- **FinChat:** To calculate the unadjusted EBITDA, we need to calculate the unadjusted operating income first. However, the provided context does not directly give us the operating income. We can infer it from the net income and other items in the cash flow statement.

Net income: $8.98 billion
Gain associated with the Juice Transaction: -$3.32 billion
Impairment and other charges: $3.62 billion
Restructuring and impairment charges: $411.0 million
Acquisition and divestiture-related charges: $80.0 million
Share-based compensation expense is not directly related to operating income, but it is an operating expense. However, we do not have enough information about other operating expenses.

We can calculate the unadjusted operating income by adding back non-operating items to net income:
Unadjusted operating income = Net income + Gain associated with the Juice Transaction + Impairment and other charges + Restructuring and impairment charges + Acquisition and divestiture-related charges
Unadjusted operating income = $8.98 billion - $3.32 billion + $3.62 billion + $0.411 billion + $0.08 billion
Unadjusted operating income = $9.759 billion

Now, let's calculate the unadjusted EBITDA:
Unadjusted EBITDA = Unadjusted operating income + Depreciation and amortization
Depreciation and amortization = $2.76 billion
Unadjusted EBITDA = $9.759 billion + $2.76 billion
Unadjusted EBITDA = $12.519 billion

Capital expenditure (capex) is $5.21 billion.

Unadjusted EBITDA less capex = $12.519 billion - $5.21 billion
Unadjusted EBITDA less capex = $7.309 billion

PepsiCo (PEP) FY2022 unadjusted EBITDA less capex is $7,309 million.

Sources:
[1] PepsiCo 10-K (FY2022) - Cash Flow Statement (XBRL)

### 27. Did Pfizer grow its PPNE between FY20 and FY21?
- **Company / FY:** Pfizer 2021  |  **Routed to:** PFE  |  **Verdict:** INCORRECT
- **Judge:** The system answer explicitly states it couldn't find the information, indicating a lack of knowledge on the topic.
- **FinanceBench gold:** Yes, change in PPNE was positive year over year
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 28. What are three main companies acquired by Pfizer mentioned in this 10K report?
- **Company / FY:** Pfizer 2021  |  **Routed to:** PFE  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it cannot find the answer in the available filings.
- **FinanceBench gold:** Trillium, Array, and Therachon
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1], [2], [3], [4], [5], [6], [7], [8]

### 29. What are major acquisitions that Ulta Beauty has done in FY2023 and FY2022?
- **Company / FY:** Ulta Beauty 2023  |  **Routed to:** ULTA  |  **Verdict:** INCORRECT
- **Judge:** The system answer indicates it couldn't find the information, but the reference answer explicitly states that Ulta Beauty did not make any acquisitions in FY2023 and FY2022.
- **FinanceBench gold:** Ulta Beauty did not make any acquisitions in FY2023 and FY2022.
- **FinChat:** I couldn't find that in the filings I have. 

Sources: [1] Ulta Beauty 10-K (FY2023) - Balance Sheet (XBRL), [2] Ulta Beauty 10-K (FY2023), [3] Ulta Beauty 10-K (FY2023), [4] Ulta Beauty 10-K (FY2023) - Cash Flow Statement (XBRL), [5] Ulta Beauty 10-K (FY2023), [6] Ulta Beauty 10-K (FY2023), [7] Ulta Beauty 10-K (FY2023), [8] Ulta Beauty 10-K (FY2023)

### 30. Is Verizon a capital intensive business based on FY 2022 data?
- **Company / FY:** Verizon 2022  |  **Routed to:** VZ  |  **Verdict:** PARTIAL
- **Judge:** The system answer correctly identifies Verizon as capital-intensive but does not provide the capital intensity ratio, which is the key fact in the reference answer.
- **FinanceBench gold:** Yes. Verizon's capital intensity ratio was approximately 2.774729. This means that it took approximately $2.77 of assets to generate $1 of revenue and thus, Verizon can be considered capital intensive.
- **FinChat:** Yes, Verizon is a capital-intensive business. In FY2022, Verizon's capital expenditures were $23.09 billion. 
Sources:
[1] Verizon 10-K (FY2022) - Cash Flow Statement (XBRL)
