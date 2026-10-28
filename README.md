# Web Traffic & User-Flow Network Centrality Analysis

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![pandas](https://img.shields.io/badge/pandas-Data%20Cleaning-150458)
![NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Theory-orange)
![R](https://img.shields.io/badge/R-tidyverse%20%7C%20ggraph-276DC3)

> Portfolio Note & Data Privacy (DSGVO / GDPR):  
> This repository is a sanitized portfolio replication of an enterprise web analytics project completed during my IT Specialist (Fachinformatiker für Daten- und Prozessanalyse) vocational training at Heinrich-Heine-Universität Düsseldorf (ZIM). All raw logs are 100% synthetic while faithfully reproducing the data cleaning pipeline, graph-theoretic methodology, and statistical scripts used on >4,500 real user sessions across 14 months.

---

1. Project Overview & Business Goal

Standard web analytics dashboards typically report isolated page views and bounce rates, making it difficult to understand how users navigate across multi-page information portals or where they get stuck.

This project models 14 months of Matomo web traffic logs (>4,500 multi-step sessions) as a directed mathematical graph G = (V, E), where:
- Nodes (V): Individual portal pages (e.g., /home, /workshops, /training-sql).
- Directed Edges (E): Sequential page-to-page transitions within a single user session, weighted by frequency.

By combining Python (pandas, numpy, networkx) with R (tidyverse, ggraph), this pipeline identifies critical bridge pages and navigation bottlenecks.

---

2. Pipeline Architecture & Methodology

- Raw Log Ingestion & Cleaning (Python / pandas): Normalizes URL paths, filters out bot crawlers and bounce sessions, and extracts ordered transition pairs.
- Graph Centrality Modeling (Python / networkx): Computes In-Degree, Out-Degree, and Betweenness Centrality to pinpoint critical bridge pages along shortest navigation paths.
- Network Visualization (R / tidyverse & ggraph): Renders weighted directed network graphs sizing nodes by Betweenness Centrality.

---

3. Sample Centrality Results (Synthetic Portal Dataset)

| Page Node | In-Degree Centrality | Out-Degree Centrality | Betweenness Centrality | Functional Role in Portal |
| :--- | :---: | :---: | :---: | :--- |
| /home | 0.78 | 0.94 | 0.31 | Primary Entry & Distribution Hub |
| /workshops-overview | 0.72 | 0.83 | 0.44 | Key Bridge Page (Connects Landing to Courses) |
| /resources-index | 0.67 | 0.78 | 0.38 | Secondary Bridge Hub |
| /course-python-data | 0.61 | 0.44 | 0.14 | High-Engagement Content Destination |
| /course-sql-basics | 0.56 | 0.39 | 0.11 | High-Engagement Content Destination |
| /contact-support | 0.50 | 0.17 | 0.04 | Terminal Exit / Support Page |

---

4. Repository Structure

- README.md: Project documentation, methodology, and sample results
- requirements.txt: Python package dependencies
- src/01_clean_and_analyze_network.py: Synthetic log generator & NetworkX centrality pipeline
- src/02_visualize_centrality.R: R ggraph network plot script
- data/: Generated edge list and node centrality CSV outputs

---

5. How to Run

1. Install Python dependencies:
   pip install -r requirements.txt
2. Generate synthetic logs and compute centrality metrics:
   python src/01_clean_and_analyze_network.py
3. Generate the network visualization in R:
   Rscript src/02_visualize_centrality.R

