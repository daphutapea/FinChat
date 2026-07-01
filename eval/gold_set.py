"""Curated evaluation set for FinChat.

Each item is a question plus a concise REFERENCE answer written from the actual
2017-2020 10-K filings in the corpus (verified against retrieved passages).
run_eval.py runs FinChat on each question and grades its answer against the
reference with an LLM-as-judge.

This exists because the corpus ends in 2020, while the FinanceBench benchmark
targets 2018-2023 filings -- so a corpus-aligned gold set gives a fair,
meaningful accuracy number.
"""

GOLD_SET = [
    {
        "company": "AMD",
        "question": "What products does AMD design and sell?",
        "reference": (
            "AMD is a global semiconductor company. Its products include x86 "
            "microprocessors (CPUs), accelerated processing units (APUs) that "
            "integrate CPUs with graphics, discrete graphics processing units "
            "(GPUs), and semi-custom System-on-Chip (SoC) products. Brands "
            "include Ryzen and Threadripper CPUs, EPYC server processors, and "
            "Radeon graphics."
        ),
    },
    {
        "company": "AMD",
        "question": "How are AMD's products manufactured?",
        "reference": (
            "AMD is a fabless semiconductor company and does not own the "
            "foundries that make its chips. It relies on third-party foundries, "
            "notably GlobalFoundries (with which it has a wafer supply "
            "agreement) and TSMC, to manufacture its microprocessor, APU, and "
            "GPU products."
        ),
    },
    {
        "company": "AMD",
        "question": "What are some key risk factors AMD identifies?",
        "reference": (
            "Risks include intense competition (such as Intel in CPUs and "
            "Nvidia in GPUs), dependence on third-party foundries like "
            "GlobalFoundries and TSMC for manufacturing, the need to launch "
            "competitive products on time, reliance on a limited number of "
            "customers and third-party products, and general economic and "
            "market conditions."
        ),
    },
    {
        "company": "AMD",
        "question": "Does AMD make chips for game consoles or other semi-custom customers?",
        "reference": (
            "Yes. AMD designs and sells semi-custom SoC products, including "
            "chips used in game consoles, and earns semi-custom revenue from "
            "third-party customers."
        ),
    },
    {
        "company": "ABT",
        "question": "What are Abbott's main business segments?",
        "reference": (
            "Abbott operates through four reportable segments: Established "
            "Pharmaceutical Products, Diagnostic Products, Nutritional "
            "Products, and Medical Devices."
        ),
    },
    {
        "company": "ABT",
        "question": "What does Abbott's diagnostics business provide?",
        "reference": (
            "Abbott's diagnostics business provides in vitro diagnostic systems "
            "and tests, including core laboratory diagnostics (immunoassay, "
            "clinical chemistry, hematology, and blood screening), molecular "
            "diagnostics, point-of-care, and rapid diagnostics, including its "
            "Alinity family of instruments."
        ),
    },
    {
        "company": "APD",
        "question": "What is Air Products' primary business?",
        "reference": (
            "Air Products is a world-leading industrial gases company. It "
            "produces and sells atmospheric gases (such as oxygen, nitrogen, "
            "and argon), process and specialty gases, related equipment, and "
            "services."
        ),
    },
    {
        "company": "APD",
        "question": "Which industries or end markets does Air Products serve?",
        "reference": (
            "Air Products serves customers globally across the energy, "
            "electronics, chemicals, metals, and manufacturing markets."
        ),
    },
    {
        "company": "AIR",
        "question": "What business segments does AAR Corp operate?",
        "reference": (
            "AAR operates two reportable segments: Aviation Services and "
            "Expeditionary Services. It is a diversified provider of products "
            "and services to the worldwide commercial aviation and government "
            "and defense markets."
        ),
    },
    {
        "company": "AIR",
        "question": "What services does AAR provide to the aviation industry?",
        "reference": (
            "AAR provides aftermarket aviation support: it sells and leases "
            "new, overhauled, and repaired engine and airframe parts and "
            "components; provides maintenance, repair and overhaul (MRO) and "
            "component inventory and repair programs; and offers supply-chain "
            "and expeditionary/airlift services to commercial and "
            "government/defense customers."
        ),
    },
    {
        "company": "MATX",
        "question": "What geographic markets does Matson's ocean transportation serve?",
        "reference": (
            "Matson's ocean transportation serves the domestic non-contiguous "
            "U.S. economies of Hawaii, Alaska, and Guam, other island economies "
            "in Micronesia, and provides an expedited service from China."
        ),
    },
    {
        "company": "MATX",
        "question": "What does Matson's logistics business do?",
        "reference": (
            "Matson Logistics provides transportation brokerage, intermodal "
            "rail and highway services, less-than-container-load consolidation, "
            "freight forwarding, warehousing and distribution, and supply-chain "
            "management services."
        ),
    },
]
