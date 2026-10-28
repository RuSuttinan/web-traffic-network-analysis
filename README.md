\# Web Traffic \& User-Flow Network Centrality Analysis



!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue)

!\[pandas](https://img.shields.io/badge/pandas-Data%20Cleaning-150458)

!\[NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Theory-orange)

!\[R](https://img.shields.io/badge/R-tidyverse%20%7C%20ggraph-276DC3)



> \*\*Portfolio Note \& Data Privacy (DSGVO / GDPR):\*\*  

> This repository is a sanitized portfolio replication of an enterprise web analytics project completed during my IT Specialist (\*Fachinformatiker für Daten- und Prozessanalyse\*) vocational training at \*\*Heinrich-Heine-Universität Düsseldorf (ZIM)\*\*. To strictly comply with institutional data protection policies, all raw logs in this repository are \*\*100% synthetic\*\* while faithfully reproducing the data cleaning pipeline, graph-theoretic methodology, and statistical scripts used on >4,500 real user sessions across 14 months.



\---



\## 1. Project Overview \& Business Goal

Standard web analytics dashboards typically report isolated page views and bounce rates, making it difficult to understand \*\*how users actually navigate across multi-page information portals\*\* or where they get stuck.



This project models 14 months of Matomo web traffic logs (>4,500 multi-step sessions) as a \*\*directed mathematical graph\*\* $G = (V, E)$, where:

\* \*\*Nodes ($V$):\*\* Individual portal pages (e.g., `/home`, `/workshops`, `/training-sql`, `/fair-data-guide`).

\* \*\*Directed Edges ($E$):\*\* Sequential page-to-page transitions $(u \\rightarrow v)$ within a single user session, weighted by transition frequency.



By combining \*\*Python (`pandas`, `numpy`, `networkx`)\*\* for log cleaning and graph modeling with \*\*R (`tidyverse`, `ggraph`)\*\* for network visualization, this pipeline identifies critical "bridge" pages and navigation bottlenecks.



\---



\## 2. Pipeline Architecture \& Methodology



1\. \*\*Raw Log Ingestion \& Cleaning (`Python / pandas`):\*\*

&#x20;  \* Normalizes URL paths (stripping tracking query strings, trailing slashes, and localized anchor tags).

&#x20;  \* Filters out automated bot crawlers, single-page bounce sessions, and consecutive page-refresh self-loops $(u \\rightarrow u)$.

&#x20;  \* Extracts ordered session transition pairs (`source\_page` $\\rightarrow$ `target\_page`) and aggregates edge weights.

2\. \*\*Graph Centrality Modeling (`Python / networkx`):\*\*

&#x20;  \* \*\*In-Degree Centrality:\*\* Identifies primary destination hubs receiving traffic from many distinct pages.

&#x20;  \* \*\*Out-Degree Centrality:\*\* Identifies directory/index hubs distributing users across the portal.

&#x20;  \* \*\*Betweenness Centrality:\*\* Pinpoints critical \*\*bridge pages\*\* that connect separate topic clusters along shortest navigation paths.

3\. \*\*Network Visualization (`R / tidyverse \& ggraph`):\*\*

&#x20;  \* Renders weighted directed network graphs sizing nodes by \*\*Betweenness Centrality\*\* and scaling edge opacity by transition volume.



\---



\## 3. Sample Centrality Results (Synthetic Portal Dataset)



| Page Node | In-Degree Centrality | Out-Degree Centrality | Betweenness Centrality | Functional Role in Portal |

| :--- | :---: | :---: | :---: | :--- |

| `/home` | 0.78 | 0.94 | 0.31 | Primary Entry \& Distribution Hub |

| `/workshops-overview` | 0.72 | 0.83 | \*\*0.44\*\* | \*\*Key Bridge Page (Connects Landing to Courses)\*\* |

| `/resources-index` | 0.67 | 0.78 | \*\*0.38\*\* | \*\*Secondary Bridge Hub\*\* |

| `/course-python-data` | 0.61 | 0.44 | 0.14 | High-Engagement Content Destination |

| `/course-sql-basics` | 0.56 | 0.39 | 0.11 | High-Engagement Content Destination |

| `/contact-support` | 0.50 | 0.17 | 0.04 | Terminal Exit / Support Page |



\---



\## 4. Repository Structure



\* `README.md` — Project documentation, methodology, and sample results

\* `requirements.txt` — Python package dependencies (`pandas`, `numpy`, `networkx`)

\* `src/01\_clean\_and\_analyze\_network.py` — Synthetic Matomo log generator, pandas cleaner \& NetworkX centrality pipeline

\* `src/02\_visualize\_centrality.R` — R (`tidyverse`, `ggraph`) circular \& directed network plot script

\* `data/` — Generated edge list and node centrality metrics CSV outputs



\---



\## 5. How to Run



1\. Install Python dependencies:

&#x20;  `pip install -r requirements.txt`

2\. Generate synthetic Matomo logs, clean transitions, and compute centrality metrics:

&#x20;  `python src/01\_clean\_and\_analyze\_network.py`

3\. Generate the network visualization in R:

&#x20;  `Rscript src/02\_visualize\_centrality.R`

