# FinChat Evaluation — Qualitative Capability Gold Set

FinChat is graded by an LLM-as-judge on document-Q&A questions (business, segments, products) across the 18-company corpus -- the task it is designed for. Reference answers are drawn from the 10-K filings.

- **Questions:** 12
- **CORRECT:** 12   **PARTIAL:** 0   **INCORRECT:** 0
- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** 100%

| # | Company | Verdict | Question |
|---|---------|---------|----------|
| 1 | Boeing | CORRECT | What are Boeing's business segments? |
| 2 | Microsoft | CORRECT | What are Microsoft's reportable segments? |
| 3 | AMD | CORRECT | What products does AMD design and sell? |
| 4 | Verizon | CORRECT | What are Verizon's reportable segments? |
| 5 | Nike | CORRECT | What products and brands does Nike sell? |
| 6 | Coca-Cola | CORRECT | What is Coca-Cola's business? |
| 7 | Pfizer | CORRECT | What is Pfizer's primary business? |
| 8 | PepsiCo | CORRECT | What kinds of products does PepsiCo sell? |
| 9 | American Express | CORRECT | What is American Express's primary business? |
| 10 | Best Buy | CORRECT | What is Best Buy's business and where does it operate? |
| 11 | Johnson & Johnson | CORRECT | What are Johnson & Johnson's business segments? |
| 12 | Amcor | CORRECT | What does Amcor make and what industry is it in? |

---

## Detailed results

### 1. What are Boeing's business segments?
- **Company:** Boeing  |  **Routed to:** BA  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately lists Boeing's four business segments with their respective abbreviations, matching the reference answer.
- **Reference:** Boeing operates through four segments: Commercial Airplanes; Defense, Space & Security; Global Services; and Boeing Capital.
- **FinChat:** Boeing's business segments are: 
1. Commercial Airplanes (BCA)
2. Defense, Space & Security (BDS)
3. Global Services (BGS)
4. Boeing Capital (BCC)
Boeing (FY2022)
Sources: 
[1] Boeing 10-K (FY2022)
[5] Boeing 10-K (FY2022)

### 2. What are Microsoft's reportable segments?
- **Company:** Microsoft  |  **Routed to:** MSFT  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the segment names and the source (Microsoft 10-K FY2023).
- **Reference:** Microsoft reports in three segments: Productivity and Business Processes; Intelligent Cloud; and More Personal Computing.
- **FinChat:** Microsoft's reportable segments are: 
1. Productivity and Business Processes, 
2. Intelligent Cloud, and 
3. More Personal Computing. 
Microsoft, FY2023.
Sources:
[1] Microsoft 10-K (FY2023), 
[2] Microsoft 10-K (FY2023), 
[4] Microsoft 10-K (FY2023)

### 3. What products does AMD design and sell?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key products designed and sold by AMD, including CPUs, GPUs, APUs, and semi-custom SoCs, with specific product lines and brands mentioned.
- **Reference:** AMD designs and sells microprocessors (CPUs), graphics processors (GPUs), accelerated processing units (APUs), adaptive/FPGA products (from Xilinx), and semi-custom System-on-Chip products. Brands include Ryzen, EPYC, Radeon, and Instinct.
- **FinChat:** Advanced Micro Devices (FY2022) designs and sells a variety of products, including: 
- Client processors (e.g. AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series)
- Graphics products (e.g. AMD Radeon graphics, AMD Radeon PRO graphics, Radeon Instinct, Radeon PRO V-series)
- Server microprocessors (e.g. AMD EPYC processors)
- Embedded processor solutions (e.g. low-power versions of AMD Athlon, AMD Geode, AMD Ryzen, AMD EPYC)
- FPGA products (e.g. Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale)
- Adaptive SoCs (e.g. Zynq-7000, Zynq UltraScale+ MPSoC, Versal HBM, Versal Premium)
- Commercial CPUs (e.g. AMD PRO Mobile, AMD PRO desktop processors with Radeon graphics)
- Professional GPUs (e.g. AMD Radeon PRO family)
- Discrete Desktop and Notebook GPUs (e.g. AMD Radeon series)

Sources:
[1] Advanced Micro Devices 10-K (FY2022)
[2] Advanced Micro Devices 10-K (FY2022)
[4] Advanced Micro Devices 10-K (FY2022)
[5] Advanced Micro Devices 10-K (FY2022)
[6] Advanced Micro Devices 10-K (FY2022)
[7] Advanced Micro Devices 10-K (FY2022)
[8] Advanced Micro Devices 10-K (FY2022)

### 4. What are Verizon's reportable segments?
- **Company:** Verizon  |  **Routed to:** VZ  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the number and names of Verizon's reportable segments.
- **Reference:** Verizon reports in two segments: Consumer and Business.
- **FinChat:** Verizon has two reportable segments. According to Note 13, the segments are: 
1. Verizon Consumer Group 
2. Verizon Business segment.

Sources:
[4] Verizon 10-K (FY2022)
[2] Verizon 10-K (FY2022)
[5] Verizon 10-K (FY2022)

### 5. What products and brands does Nike sell?
- **Company:** Nike  |  **Routed to:** NKE  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the types of products and brands sold by Nike.
- **Reference:** Nike sells athletic footwear, apparel, equipment, and accessories. Its brands include NIKE, Jordan, and Converse.
- **FinChat:** Nike sells athletic footwear, apparel, equipment, accessories, and services under the NIKE Brand, Jordan Brand, and Converse. Specifically, their products include:

- Performance athletic footwear, apparel, equipment, and accessories
- Sport-inspired lifestyle products
- Bags, socks, sport balls, eyewear, timepieces, digital devices, bats, gloves, and protective equipment
- Jordan Brand products focused on basketball performance and culture

Company: Nike, Fiscal Year: 2023
Sources:
[1] Nike 10-K (FY2023)
[2] Nike 10-K (FY2023)
[5] Nike 10-K (FY2023)

### 6. What is Coca-Cola's business?
- **Company:** Coca-Cola  |  **Routed to:** KO  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of Coca-Cola's business as a total beverage company with various beverage categories.
- **Reference:** Coca-Cola is a total beverage company that manufactures and sells nonalcoholic beverage concentrates, syrups, and finished beverages. Its brands include Coca-Cola, Sprite, and Fanta.
- **FinChat:** The Coca-Cola Company is a total beverage company, owning or licensing and marketing numerous beverage brands, grouped into categories such as Trademark Coca-Cola, sparkling flavors, water, sports, coffee and tea, juice, value-added dairy and plant-based beverages, and emerging beverages. 
Coca-Cola, FY2022
Sources:
[1] Coca-Cola 10-K (FY2022)
[2] Coca-Cola 10-K (FY2022)
[4] Coca-Cola 10-K (FY2022)

### 7. What is Pfizer's primary business?
- **Company:** Pfizer  |  **Routed to:** PFE  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys Pfizer's primary business as a research-based biopharmaceutical company, including its key activities of discovery, development, and distribution of medicines and vaccines.
- **Reference:** Pfizer is a research-based biopharmaceutical company that discovers, develops, manufactures, and sells medicines and vaccines, including the Comirnaty COVID-19 vaccine and Paxlovid.
- **FinChat:** Pfizer Inc. is a research-based, global biopharmaceutical company that applies science and global resources to bring therapies to people, through the discovery, development, manufacture, marketing, sale, and distribution of biopharmaceutical products worldwide. 
Pfizer, FY2021
Sources:
[1] Pfizer 10-K (FY2021)

### 8. What kinds of products does PepsiCo sell?
- **Company:** PepsiCo  |  **Routed to:** PEP  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the types of products PepsiCo sells (beverages and convenient foods) and some of its notable brands.
- **Reference:** PepsiCo makes and sells convenient foods (snacks) and beverages. Its brands include Pepsi, Lay's, Gatorade, Quaker, and Tropicana, sold across North America and international markets.
- **FinChat:** PepsiCo sells a wide variety of beverages and convenient foods, including brands such as Lay’s, Doritos, Cheetos, Gatorade, Pepsi-Cola, Mountain Dew, Quaker, and SodaStream. Specifically, their beverage brands include 7UP, Diet Pepsi, Pepsi, and Pepsi Max, among others. They also sell snack foods like PopCorners, Ruffles, and SunChips, as well as other products like Rice-A-Roni and Quaker oats. 
PepsiCo, FY2022
Sources:
[1] PepsiCo 10-K (FY2022)
[2] PepsiCo 10-K (FY2022)
[5] PepsiCo 10-K (FY2022)
[8] PepsiCo 10-K (FY2022)

### 9. What is American Express's primary business?
- **Company:** American Express  |  **Routed to:** AXP  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys American Express's primary business as a globally integrated payments company, including its issuance of credit and charge cards and provision of merchant acquiring and card-network services.
- **Reference:** American Express is a globally integrated payments company. It issues charge and credit cards and provides merchant acquiring and card-network services.
- **FinChat:** American Express is a globally integrated payments company, providing customers with access to products, insights, and experiences, and is a leader in providing credit and charge cards to consumers, small businesses, mid-sized companies, and large corporations. 
Company: American Express, Fiscal Year: 2022
Sources:
[1] American Express 10-K (FY2022)

### 10. What is Best Buy's business and where does it operate?
- **Company:** Best Buy  |  **Routed to:** BBY  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of Best Buy's business and its operating segments, matching the reference answer.
- **Reference:** Best Buy is a retailer of technology products -- consumer electronics, computing, mobile phones, and appliances -- operating through a Domestic (U.S.) segment and an International (Canada) segment.
- **FinChat:** Best Buy's business is driven by its purpose to enrich lives through technology, and it operates in the U.S. and Canada. The company is comprised of two reportable segments: Domestic (U.S. and Best Buy Health) and International (Canada). 

Sources:
[1] Best Buy 10-K (FY2023)
[3] Best Buy 10-K (FY2023)
[4] Best Buy 10-K (FY2023)
[5] Best Buy 10-K (FY2023)

### 11. What are Johnson & Johnson's business segments?
- **Company:** Johnson & Johnson  |  **Routed to:** JNJ  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the three business segments and the source.
- **Reference:** Johnson & Johnson operates through three segments: Consumer Health, Pharmaceutical, and MedTech (Medical Devices).
- **FinChat:** Johnson & Johnson's business segments are: 
1. Consumer Health, 
2. Pharmaceutical, and 
3. Medical Devices. 
Johnson & Johnson (FY2022)

Sources:
[4] Johnson & Johnson 10-K (FY2022)

### 12. What does Amcor make and what industry is it in?
- **Company:** Amcor  |  **Routed to:** AMCR  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the types of products Amcor makes and the industry it is in.
- **Reference:** Amcor is a global packaging company that develops and produces flexible and rigid packaging for food, beverage, pharmaceutical, medical, and home and personal care products.
- **FinChat:** Amcor makes responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets. It is in the packaging industry. 
Amcor plc (FY2023)
Sources: 
[1] Amcor 10-K (FY2023)
[2] Amcor 10-K (FY2023)
[3] Amcor 10-K (FY2023)
