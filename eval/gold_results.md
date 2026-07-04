# FinChat Evaluation — Qualitative Capability Gold Set

FinChat is graded by an LLM-as-judge on document-Q&A questions (business, segments, products) across the 18-company corpus -- the task it is designed for. Reference answers are drawn from the 10-K filings.

- **Questions:** 15
- **CORRECT:** 13   **PARTIAL:** 2   **INCORRECT:** 0
- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** 93%

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
| 10 | Best Buy | PARTIAL | What is Best Buy's business and where does it operate? |
| 11 | Johnson & Johnson | CORRECT | What are Johnson & Johnson's business segments? |
| 12 | Amcor | CORRECT | What does Amcor make and what industry is it in? |
| 13 | Apple | PARTIAL | What products and services does Apple sell? |
| 14 | NVIDIA | CORRECT | What are NVIDIA's reportable segments? |
| 15 | Amazon | CORRECT | What are Amazon's reportable segments? |

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
[6] Boeing 10-K (FY2022)

### 2. What are Microsoft's reportable segments?
- **Company:** Microsoft  |  **Routed to:** MSFT  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the segment names and the source.
- **Reference:** Microsoft reports in three segments: Productivity and Business Processes; Intelligent Cloud; and More Personal Computing.
- **FinChat:** Microsoft's reportable segments are: 
1. Productivity and Business Processes, 
2. Intelligent Cloud, and 
3. More Personal Computing. 
Microsoft, FY2023.
Sources:
[1] Microsoft 10-K (FY2023), 
[2] Microsoft 10-K (FY2023)

### 3. What products does AMD design and sell?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately lists and describes the various products designed and sold by AMD, including CPUs, GPUs, APUs, and semi-custom SoCs, matching the key facts of the reference answer.
- **Reference:** AMD designs and sells microprocessors (CPUs), graphics processors (GPUs), accelerated processing units (APUs), adaptive/FPGA products (from Xilinx), and semi-custom System-on-Chip products. Brands include Ryzen, EPYC, Radeon, and Instinct.
- **FinChat:** Advanced Micro Devices (FY2022) designs and sells a variety of products, including: 
- Client processors (e.g. AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series)
- Graphics products (e.g. AMD Radeon graphics, AMD Embedded Radeon graphics, AMD Radeon PRO graphics)
- Professional graphics products (e.g. AMD Radeon PRO graphics)
- Data center graphics (e.g. Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers)
- Server microprocessors (e.g. AMD EPYC processors)
- Embedded processor solutions (e.g. low-power versions of AMD Athlon, AMD Geode, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors)
- FPGA products (e.g. Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and Spartan-7)
- Adaptive SoCs (e.g. Zynq-7000, Zynq UltraScale+ MPSoC, Zynq UltraScale+ RFSoCs, Versal HBM, Versal Premium, Versal Prime, Versal AI Core, Versal AI Edge, Vitis and Vivado)
- Commercial CPUs (e.g. AMD PRO Mobile and AMD PRO desktop processors with Radeon graphics)
- Professional GPUs (e.g. AMD Radeon PRO family of professional graphics products)
- Discrete Desktop and Notebook GPUs (e.g. AMD Radeon series discrete GPU processors)

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
- **FinChat:** Verizon has two reportable segments. 
Verizon Communications Inc. (FY2022)

Sources:
[4] Verizon 10-K (FY2022)

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
- **FinChat:** Coca-Cola is a total beverage company. They own or license and market numerous beverage brands, which are grouped into categories including: Trademark Coca-Cola; sparkling flavors; water, sports, coffee and tea; juice, value-added dairy and plant-based beverages; and emerging beverages. 
The Coca-Cola Company, FY2022.
Sources:
[1] Coca-Cola 10-K (FY2022)
[2] Coca-Cola 10-K (FY2022)
[4] Coca-Cola 10-K (FY2022)

### 7. What is Pfizer's primary business?
- **Company:** Pfizer  |  **Routed to:** PFE  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys Pfizer's primary business as a research-based biopharmaceutical company, including its key activities of discovery, development, and distribution of medicines and vaccines.
- **Reference:** Pfizer is a research-based biopharmaceutical company that discovers, develops, manufactures, and sells medicines and vaccines, including the Comirnaty COVID-19 vaccine and Paxlovid.
- **FinChat:** Pfizer Inc. is a research-based, global biopharmaceutical company that applies science and global resources to bring therapies to people through the discovery, development, manufacture, marketing, sale, and distribution of biopharmaceutical products worldwide. 
Pfizer, FY2021
Sources:
[1] Pfizer 10-K (FY2021)

### 8. What kinds of products does PepsiCo sell?
- **Company:** PepsiCo  |  **Routed to:** PEP  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the types of products PepsiCo sells (beverages and convenient foods) and some of its notable brands.
- **Reference:** PepsiCo makes and sells convenient foods (snacks) and beverages. Its brands include Pepsi, Lay's, Gatorade, Quaker, and Tropicana, sold across North America and international markets.
- **FinChat:** PepsiCo sells a wide variety of beverages and convenient foods, including brands such as Lay’s, Doritos, Cheetos, Gatorade, Pepsi-Cola, Mountain Dew, Quaker, and SodaStream. Specifically, their beverage brands include 7UP, Diet Pepsi, Pepsi, and Pepsi Max, among others. They also sell sparkling water makers and related products through SodaStream. Additionally, their food brands include PopCorners, Quaker Chewy, Ruffles, and SunChips, among others. 
PepsiCo, FY2022
Sources:
[1] PepsiCo 10-K (FY2022)
[2] PepsiCo 10-K (FY2022)
[5] PepsiCo 10-K (FY2022)

### 9. What is American Express's primary business?
- **Company:** American Express  |  **Routed to:** AXP  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys American Express's primary business as a globally integrated payments company, including its issuance of credit and charge cards and provision of merchant acquiring and card-network services.
- **Reference:** American Express is a globally integrated payments company. It issues charge and credit cards and provides merchant acquiring and card-network services.
- **FinChat:** American Express is a globally integrated payments company, providing customers with access to products, insights, and experiences, and is a leader in providing credit and charge cards to consumers, small businesses, mid-sized companies, and large corporations around the world. 
Sources:
[1] American Express 10-K (FY2022)

### 10. What is Best Buy's business and where does it operate?
- **Company:** Best Buy  |  **Routed to:** BBY  |  **Verdict:** PARTIAL
- **Judge:** The system answer captures the geographic scope of Best Buy's operations but misses the key fact that it is a retailer of technology products.
- **Reference:** Best Buy is a retailer of technology products -- consumer electronics, computing, mobile phones, and appliances -- operating through a Domestic (U.S.) segment and an International (Canada) segment.
- **FinChat:** Best Buy's business is driven by its purpose to enrich lives through technology and its vision to personalize and humanize technology solutions for every stage of life. The company operates in the U.S. and Canada. 

Best Buy Co., Inc. (FY2023)
Sources:
[1] Best Buy 10-K (FY2023), [3] Best Buy 10-K (FY2023)

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

### 13. What products and services does Apple sell?
- **Company:** Apple  |  **Routed to:** AAPL  |  **Verdict:** PARTIAL
- **Judge:** The system answer captures some products and services but misses others, such as the App Store, Apple Music, and iCloud, and includes some products not mentioned in the reference answer, like Apple TV and HomePod.
- **Reference:** Apple designs and sells consumer electronics and services. Products include iPhone, Mac, iPad, and wearables/home/accessories (Apple Watch, AirPods). Services include the App Store, iCloud, Apple Music, AppleCare, and advertising.
- **FinChat:** Apple sells the following products: 
- iPhone 
- Mac (including laptops MacBook Air and MacBook Pro, and desktops iMac, Mac mini, Mac Studio, and Mac Pro) 
- iPad (including iPad Pro, iPad Air, iPad, and iPad mini) 
- Wearables (including Apple Watch and wireless headphones such as AirPods) 
- Home products (including Apple TV, HomePod, and HomePod mini) 
- Accessories (including Apple-branded and third-party accessories).

Apple also sells the following services: 
- Advertising 
- AppleCare (fee-based service and support products) 
- Cloud Services 
- Digital Content.

Apple Inc. (FY2023) 
Sources: 
[1] Apple 10-K (FY2023) 
[2] Apple 10-K (FY2023) 
[5] Apple 10-K (FY2023)

### 14. What are NVIDIA's reportable segments?
- **Company:** NVIDIA  |  **Routed to:** NVDA  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the two reportable segments and the source.
- **Reference:** NVIDIA reports in two segments: Compute & Networking and Graphics.
- **FinChat:** NVIDIA's reportable segments are "Compute & Networking" and "Graphics" (NVIDIA, FY2024).

Sources:
[1] NVIDIA 10-K (FY2024)
[4] NVIDIA 10-K (FY2024)
[7] NVIDIA 10-K (FY2024)

### 15. What are Amazon's reportable segments?
- **Company:** Amazon  |  **Routed to:** AMZN  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key facts of the reference, including the segment names and the source of the information.
- **Reference:** Amazon reports in three segments: North America, International, and AWS (Amazon Web Services).
- **FinChat:** Amazon's reportable segments are: 
1. North America, 
2. International, and 
3. Amazon Web Services (“AWS”). 
Amazon (FY2023)

Sources:
[2] Amazon 10-K (FY2023)
[3] Amazon 10-K (FY2023)
