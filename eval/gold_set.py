"""Qualitative capability gold set for FinChat (SEC EDGAR corpus).

These are document-Q&A questions (business, segments, products, geographies) --
the task FinChat is designed for -- with reference answers from the companies'
10-K filings. run_gold.py grades FinChat against them with an LLM-as-judge.

This complements run_eval.py (FinanceBench), which is dominated by numeric
financial-analysis questions that text RAG cannot compute.
"""

GOLD_SET = [
    {
        "company": "Boeing",
        "question": "What are Boeing's business segments?",
        "reference": (
            "Boeing operates through four segments: Commercial Airplanes; "
            "Defense, Space & Security; Global Services; and Boeing Capital."
        ),
    },
    {
        "company": "Microsoft",
        "question": "What are Microsoft's reportable segments?",
        "reference": (
            "Microsoft reports in three segments: Productivity and Business "
            "Processes; Intelligent Cloud; and More Personal Computing."
        ),
    },
    {
        "company": "AMD",
        "question": "What products does AMD design and sell?",
        "reference": (
            "AMD designs and sells microprocessors (CPUs), graphics processors "
            "(GPUs), accelerated processing units (APUs), adaptive/FPGA products "
            "(from Xilinx), and semi-custom System-on-Chip products. Brands "
            "include Ryzen, EPYC, Radeon, and Instinct."
        ),
    },
    {
        "company": "Verizon",
        "question": "What are Verizon's reportable segments?",
        "reference": "Verizon reports in two segments: Consumer and Business.",
    },
    {
        "company": "Nike",
        "question": "What products and brands does Nike sell?",
        "reference": (
            "Nike sells athletic footwear, apparel, equipment, and accessories. "
            "Its brands include NIKE, Jordan, and Converse."
        ),
    },
    {
        "company": "Coca-Cola",
        "question": "What is Coca-Cola's business?",
        "reference": (
            "Coca-Cola is a total beverage company that manufactures and sells "
            "nonalcoholic beverage concentrates, syrups, and finished beverages. "
            "Its brands include Coca-Cola, Sprite, and Fanta."
        ),
    },
    {
        "company": "Pfizer",
        "question": "What is Pfizer's primary business?",
        "reference": (
            "Pfizer is a research-based biopharmaceutical company that discovers, "
            "develops, manufactures, and sells medicines and vaccines, including "
            "the Comirnaty COVID-19 vaccine and Paxlovid."
        ),
    },
    {
        "company": "PepsiCo",
        "question": "What kinds of products does PepsiCo sell?",
        "reference": (
            "PepsiCo makes and sells convenient foods (snacks) and beverages. "
            "Its brands include Pepsi, Lay's, Gatorade, Quaker, and Tropicana, "
            "sold across North America and international markets."
        ),
    },
    {
        "company": "American Express",
        "question": "What is American Express's primary business?",
        "reference": (
            "American Express is a globally integrated payments company. It "
            "issues charge and credit cards and provides merchant acquiring and "
            "card-network services."
        ),
    },
    {
        "company": "Best Buy",
        "question": "What is Best Buy's business and where does it operate?",
        "reference": (
            "Best Buy is a retailer of technology products -- consumer "
            "electronics, computing, mobile phones, and appliances -- operating "
            "through a Domestic (U.S.) segment and an International (Canada) "
            "segment."
        ),
    },
    {
        "company": "Johnson & Johnson",
        "question": "What are Johnson & Johnson's business segments?",
        "reference": (
            "Johnson & Johnson operates through three segments: Consumer Health, "
            "Pharmaceutical, and MedTech (Medical Devices)."
        ),
    },
    {
        "company": "Amcor",
        "question": "What does Amcor make and what industry is it in?",
        "reference": (
            "Amcor is a global packaging company that develops and produces "
            "flexible and rigid packaging for food, beverage, pharmaceutical, "
            "medical, and home and personal care products."
        ),
    },
    {
        "company": "Apple",
        "question": "What products and services does Apple sell?",
        "reference": (
            "Apple designs and sells consumer electronics and services. Products "
            "include iPhone, Mac, iPad, and wearables/home/accessories (Apple "
            "Watch, AirPods). Services include the App Store, iCloud, Apple "
            "Music, AppleCare, and advertising."
        ),
    },
    {
        "company": "NVIDIA",
        "question": "What are NVIDIA's reportable segments?",
        "reference": (
            "NVIDIA reports in two segments: Compute & Networking and Graphics."
        ),
    },
    {
        "company": "Amazon",
        "question": "What are Amazon's reportable segments?",
        "reference": (
            "Amazon reports in three segments: North America, International, and "
            "AWS (Amazon Web Services)."
        ),
    },
]
