# FinChat Evaluation — Curated Gold Set

FinChat is graded by an LLM-as-judge against reference answers written from the 2017-2020 10-K filings in the corpus.

- **Questions:** 12
- **CORRECT:** 10   **PARTIAL:** 2   **INCORRECT:** 0
- **Score:** 11.0 / 12
- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** 92%

| # | Company | Verdict | Question |
|---|---------|---------|----------|
| 1 | AMD | CORRECT | What products does AMD design and sell? |
| 2 | AMD | CORRECT | How are AMD's products manufactured? |
| 3 | AMD | PARTIAL | What are some key risk factors AMD identifies? |
| 4 | AMD | CORRECT | Does AMD make chips for game consoles or other semi-custom customers? |
| 5 | ABT | CORRECT | What are Abbott's main business segments? |
| 6 | ABT | CORRECT | What does Abbott's diagnostics business provide? |
| 7 | APD | CORRECT | What is Air Products' primary business? |
| 8 | APD | CORRECT | Which industries or end markets does Air Products serve? |
| 9 | AIR | CORRECT | What business segments does AAR Corp operate? |
| 10 | AIR | CORRECT | What services does AAR provide to the aviation industry? |
| 11 | MATX | PARTIAL | What geographic markets does Matson's ocean transportation serve? |
| 12 | MATX | CORRECT | What does Matson's logistics business do? |

---

## Detailed results

### 1. What products does AMD design and sell?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys the key products designed and sold by AMD, with minor omissions of specific brand names.
- **Reference:** AMD is a global semiconductor company. Its products include x86 microprocessors (CPUs), accelerated processing units (APUs) that integrate CPUs with graphics, discrete graphics processing units (GPUs), and semi-custom System-on-Chip (SoC) products. Brands include Ryzen and Threadripper CPUs, EPYC server processors, and Radeon graphics.
- **FinChat:** AMD designs and sells x86 microprocessors (CPUs), accelerated processing units (APUs), discrete graphics processing units (GPUs), semi-custom System-on-Chip (SOC) products, and chipsets for the PC, gaming, datacenter, and embedded markets. 
Advanced Micro Devices Inc (2019, 2020)

Sources:
[2] ADVANCED MICRO DEVICES INC 10-K (2019) - Section 8
[6] ADVANCED MICRO DEVICES INC 10-K (2020) - Section 10

### 2. How are AMD's products manufactured?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer conveys the key fact that AMD relies on third-party foundries, including GlobalFoundries, to manufacture its products.
- **Reference:** AMD is a fabless semiconductor company and does not own the foundries that make its chips. It relies on third-party foundries, notably GlobalFoundries (with which it has a wafer supply agreement) and TSMC, to manufacture its microprocessor, APU, and GPU products.
- **FinChat:** AMD relies on third parties to manufacture its products. The company has a wafer supply agreement with GF (GlobalFoundries) to purchase all of its microprocessor and APU product requirements, and a certain portion of its GPU product requirements, manufactured at process nodes larger than 7 nanometer (nm) from GF with limited exceptions. 

Sources:
[1] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 0
[2] ADVANCED MICRO DEVICES INC 10-K (2017) - Section 0
[3] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 1

### 3. What are some key risk factors AMD identifies?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** PARTIAL
- **Judge:** The system answer captures some key risk factors, such as dependence on third-party manufacturers and the need to launch competitive products on time, but misses others like general economic and market conditions and reliance on a limited number of customers.
- **Reference:** Risks include intense competition (such as Intel in CPUs and Nvidia in GPUs), dependence on third-party foundries like GlobalFoundries and TSMC for manufacturing, the need to launch competitive products on time, reliance on a limited number of customers and third-party products, and general economic and market conditions.
- **FinChat:** AMD identifies several key risk factors, including:
1. Intel Corporation's dominance of the microprocessor market and its aggressive business practices (ADVANCED MICRO DEVICES INC 10-K (2017) - Section 1, ADVANCED MICRO DEVICES INC 10-K (2018) - Section 1)
2. Cyber-attacks, hacking, and phishing attacks (ADVANCED MICRO DEVICES INC 10-K (2018) - Section 0, ADVANCED MICRO DEVICES INC 10-K (2020) - Section 1)
3. Failure to develop and introduce new products on a timely basis (ADVANCED MICRO DEVICES INC 10-K (2018) - Section 1)
4. Dependence on third-party manufacturers and suppliers (ADVANCED MICRO DEVICES INC 10-K (2017) - Section 0)
5. Loss of a significant customer (ADVANCED MICRO DEVICES INC 10-K (2018) - Section 0)

Sources:
[1] ADVANCED MICRO DEVICES INC 10-K (2017) - Section 1
[2] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 0
[3] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 1
[4] ADVANCED MICRO DEVICES INC 10-K (2020) - Section 1
[5] ADVANCED MICRO DEVICES INC 10-K (2017) - Section 0
[6] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 0

### 4. Does AMD make chips for game consoles or other semi-custom customers?
- **Company:** AMD  |  **Routed to:** AMD  |  **Verdict:** CORRECT
- **Judge:** The system answer conveys the key fact that AMD designs and sells semi-custom SoC products for game consoles, matching the reference answer.
- **Reference:** Yes. AMD designs and sells semi-custom SoC products, including chips used in game consoles, and earns semi-custom revenue from third-party customers.
- **FinChat:** Yes, AMD makes semi-custom System-on-Chip (SoC) products for game consoles. The company's success in this area is dependent on securing customers for its semi-custom design pipeline and consumer market conditions, including the success of the Sony PlayStation and Microsoft Xbox game console systems. 
Sources:
[6] ADVANCED MICRO DEVICES INC 10-K (2018) - Section 1 
[7] ADVANCED MICRO DEVICES INC 10-K (2017) - Section 8

### 5. What are Abbott's main business segments?
- **Company:** ABT  |  **Routed to:** ABT  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately lists Abbott's four main business segments, matching the reference answer.
- **Reference:** Abbott operates through four reportable segments: Established Pharmaceutical Products, Diagnostic Products, Nutritional Products, and Medical Devices.
- **FinChat:** Abbott's main business segments are: 
1. Established Pharmaceutical Products, 
2. Diagnostic Products, 
3. Nutritional Products, and 
4. Medical Devices (previously known as Cardiovascular and Neuromodulation Products). 
Abbott Laboratories (2020)

Sources:
[1] ABBOTT LABORATORIES 10-K (2020) - Section 10
[3] ABBOTT LABORATORIES 10-K (2020) - Section 10
[5] ABBOTT LABORATORIES 10-K (2017) - Section 0
[6] ABBOTT LABORATORIES 10-K (2018) - Section 10

### 6. What does Abbott's diagnostics business provide?
- **Company:** ABT  |  **Routed to:** ABT  |  **Verdict:** CORRECT
- **Judge:** The system answer conveys the key facts of Abbott's diagnostics business, including the types of diagnostic systems and tests provided, with only minor omissions.
- **Reference:** Abbott's diagnostics business provides in vitro diagnostic systems and tests, including core laboratory diagnostics (immunoassay, clinical chemistry, hematology, and blood screening), molecular diagnostics, point-of-care, and rapid diagnostics, including its Alinity family of instruments.
- **FinChat:** Abbott's diagnostics business provides various products, including: 
- Core laboratory systems for immunoassay, clinical chemistry, hematology, and transfusion medicine, 
- Molecular diagnostics systems, 
- Rapid diagnostics products for cardiometabolic disease, infectious disease, and toxicology, 
- Informatics and automation solutions to increase efficiency in laboratories.

Abbott Laboratories (2017, 2018, 2019, 2020) 
Sources:
[1] ABBOTT LABORATORIES 10-K (2019) - Section 8
[3] ABBOTT LABORATORIES 10-K (2017) - Section 0
[6] ABBOTT LABORATORIES 10-K (2018) - Section 8
[8] ABBOTT LABORATORIES 10-K (2020) - Section 0

### 7. What is Air Products' primary business?
- **Company:** APD  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately conveys Air Products' primary business, matching the key facts of the reference answer.
- **Reference:** Air Products is a world-leading industrial gases company. It produces and sells atmospheric gases (such as oxygen, nitrogen, and argon), process and specialty gases, related equipment, and services.
- **FinChat:** Air Products' primary business is as a world-leading Industrial Gases company, providing atmospheric, process, and specialty gases, and related equipment to various industries. 
Air Products & Chemicals, Inc. (2018) 

Sources:
[2] Air Products & Chemicals, Inc. 10-K (2018) - Section 8
[3] Air Products & Chemicals, Inc. 10-K (2018) - Section 0

### 8. Which industries or end markets does Air Products serve?
- **Company:** APD  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer conveys the key facts of the reference, listing similar industries and end markets served by Air Products, with minor additions of detail.
- **Reference:** Air Products serves customers globally across the energy, electronics, chemicals, metals, and manufacturing markets.
- **FinChat:** Air Products serves various industries, including: 
- Refining 
- Chemical 
- Gasification 
- Metals 
- Electronics 
- Manufacturing 
- Food and beverage.

In later years, the company also serves energy, environment, and emerging markets.

Air Products & Chemicals, Inc. (2018, 2017, 2020) 
Sources:
[1] Air Products & Chemicals, Inc. 10-K (2018) - Section 8
[2] Air Products & Chemicals, Inc. 10-K (2017) - Section 0
[6] Air Products & Chemicals, Inc. 10-K (2020) - Section 8

### 9. What business segments does AAR Corp operate?
- **Company:** AIR  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer accurately identifies the two business segments of AAR Corp.
- **Reference:** AAR operates two reportable segments: Aviation Services and Expeditionary Services. It is a diversified provider of products and services to the worldwide commercial aviation and government and defense markets.
- **FinChat:** AAR CORP operates two business segments: Aviation Services and Expeditionary Services. 
Sources:
[3] AAR CORP 10-K (2018) - Section 0
[4] AAR CORP 10-K (2017) - Section 0

### 10. What services does AAR provide to the aviation industry?
- **Company:** AIR  |  **Routed to:** None  |  **Verdict:** CORRECT
- **Judge:** The system answer comprehensively covers the key services provided by AAR to the aviation industry, matching the reference answer's scope.
- **Reference:** AAR provides aftermarket aviation support: it sells and leases new, overhauled, and repaired engine and airframe parts and components; provides maintenance, repair and overhaul (MRO) and component inventory and repair programs; and offers supply-chain and expeditionary/airlift services to commercial and government/defense customers.
- **FinChat:** AAR CORP provides various services to the aviation industry, including: 
- Inventory management and distribution services 
- Maintenance, repair and overhaul ("MRO") 
- Engineering services 
- Customized flight hour component inventory and repair programs 
- Warranty claim management 
- Outsourcing programs for engine and airframe parts and components 
- Material planning, sourcing, logistics, information and program management, and parts and component repair and overhaul 
- Aircraft modifications 
- Aircraft and engine sales and leasing.

Sources:
[1] AAR CORP 10-K (2019) - Section 0
[5] AAR CORP 10-K (2019) - Section 0
[7] AAR CORP 10-K (2019) - Section 10
[8] AAR CORP 10-K (2020) - Section 0

### 11. What geographic markets does Matson's ocean transportation serve?
- **Company:** MATX  |  **Routed to:** MATX  |  **Verdict:** PARTIAL
- **Judge:** The system answer includes the key markets mentioned in the reference, but also adds several unrelated or unsupported markets.
- **Reference:** Matson's ocean transportation serves the domestic non-contiguous U.S. economies of Hawaii, Alaska, and Guam, other island economies in Micronesia, and provides an expedited service from China.
- **FinChat:** Matson's Ocean Transportation segment serves the following geographic markets: 
- Hawaii 
- Alaska 
- Guam 
- Micronesia 
- China 
- South Pacific islands, including Fiji, Samoa, American Samoa, the Cook Islands, Tonga, Niue, Nauru, and the Solomon Islands 
- U.S. West Coast, including California and Washington 
- Australia (east coast ports) 
- New Zealand 
- North America (through logistics services).

Matson, Inc. (2019, 2020)

### 12. What does Matson's logistics business do?
- **Company:** MATX  |  **Routed to:** MATX  |  **Verdict:** CORRECT
- **Judge:** The system answer comprehensively covers the key services provided by Matson's logistics business, matching the reference answer.
- **Reference:** Matson Logistics provides transportation brokerage, intermodal rail and highway services, less-than-container-load consolidation, freight forwarding, warehousing and distribution, and supply-chain management services.
- **FinChat:** Matson's Logistics business, conducted through Matson Logistics, Inc., provides a variety of logistics services to its customers, including: 
1. Multimodal transportation brokerage of domestic and international rail intermodal services, long-haul and regional highway trucking services, specialized hauling, flat-bed and project services, less-than-truckload services, and expedited freight services (collectively, “Transportation Brokerage” services);
2. Less-than-container load (“LCL”) consolidation and freight forwarding services (collectively, “Freight Forwarding” services);
3. Warehousing and distribution services; and 
4. Supply chain management, non-vessel operating common carrier (“NVOCC”) freight forwarding and other services.
Matson, Inc. (2020) 

Sources:
[1] Matson, Inc. 10-K (2020) - Section 10
[3] Matson, Inc. 10-K (2020) - Section 0
[7] Matson, Inc. 10-K (2020) - Section 10
