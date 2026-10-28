"""
Web Traffic Log Cleaning & Graph Network Centrality Pipeline
Author: Rungwit Suttinan
Description:
    1. Generates a synthetic 14-month Matomo web session log dataset (>4,500 sessions)
       for portfolio reproducibility.
    2. Cleans URLs, filters bot/bounce noise, and removes self-loop refreshes using pandas.
    3. Builds a weighted directed graph in NetworkX and computes In-Degree, Out-Degree,
       and Betweenness Centrality metrics.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx


def generate_synthetic_matomo_logs(num_sessions: int = 4650, seed: int = 42) -> pd.DataFrame:
    """Generates realistic synthetic Matomo session logs spanning 14 months."""
    rng = np.random.default_rng(seed)

    portal_pages = [
        "/home",
        "/about-project",
        "/workshops-overview",
        "/course-python-data",
        "/course-sql-basics",
        "/course-git-ci",
        "/course-unix-shell",
        "/resources-index",
        "/fair-data-guide",
        "/wikidata-intro",
        "/faq",
        "/contact-support",
        "/registration-form",
        "/downloads-templates",
    ]

    # Realistic transition probabilities favouring hub-and-bridge navigation
    hub_weights = np.array([0.18, 0.06, 0.15, 0.08, 0.07, 0.06, 0.05, 0.11, 0.06, 0.04, 0.04, 0.03, 0.04, 0.03])
    hub_weights = hub_weights / hub_weights.sum()

    start_ts = pd.Timestamp("2024-11-01")
    end_ts = pd.Timestamp("2025-12-31")
    total_seconds = int((end_ts - start_ts).total_seconds())

    records = []
    for session_idx in range(1, num_sessions + 1):
        session_id = f"SES-{session_idx:05d}"
        session_start = start_ts + pd.Timedelta(seconds=int(rng.integers(0, total_seconds)))

        # Simulate session length (1 to 7 page views; 1 = bounce)
        n_steps = int(rng.choice([1, 2, 3, 4, 5, 6, 7], p=[0.12, 0.24, 0.26, 0.18, 0.10, 0.06, 0.04]))
        current_time = session_start

        for step in range(n_steps):
            if step == 0:
                page = rng.choice(["/home", "/workshops-overview", "/resources-index"], p=[0.65, 0.20, 0.15])
            else:
                page = rng.choice(portal_pages, p=hub_weights)

            # Inject realistic raw URL noise (query strings, trailing slashes)
            noisy_suffix = rng.choice(["", "/", "?mtm_campaign=newsletter", "?lang=de", "#top"], p=[0.65, 0.15, 0.08, 0.07, 0.05])
            user_agent_type = rng.choice(["human", "bot"], p=[0.96, 0.04])

            records.append(
                {
                    "session_id": session_id,
                    "timestamp": current_time,
                    "raw_url": f"https://portal.example-uni.de{page}{noisy_suffix}",
                    "visitor_type": user_agent_type,
                }
            )
            current_time += pd.Timedelta(seconds=int(rng.integers(15, 240)))

    return pd.DataFrame(records)


def clean_matomo_logs(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Cleans raw session logs and extracts sequential (source -> target) page transitions."""
    df = df_raw.copy()

    # 1. Remove automated bot traffic
    df = df[df["visitor_type"] == "human"].copy()

    # 2. Normalize URLs: strip domain, query parameters, anchors, and trailing slashes
    df["clean_page"] = (
        df["raw_url"]
        .str.replace(r"^https?://[^/]+", "", regex=True)
        .str.replace(r"[\?#].*$", "", regex=True)
        .str.rstrip("/")
    )
    df.loc[df["clean_page"] == "", "clean_page"] = "/home"

    # 3. Sort chronologically within each session
    df = df.sort_values(["session_id", "timestamp"]).reset_index(drop=True)

    # 4. Create sequential transition pairs (u -> v) within the same session
    df["target_page"] = df.groupby("session_id")["clean_page"].shift(-1)
    transitions = df.dropna(subset=["target_page"]).copy()
    transitions = transitions.rename(columns={"clean_page": "source_page"})

    # 5. Remove immediate page-refresh self-loops (source_page == target_page)
    transitions = transitions[transitions["source_page"] != transitions["target_page"]].copy()

    # 6. Aggregate weighted edge list
    edge_list = (
        transitions.groupby(["source_page", "target_page"], as_index=False)
        .size()
        .rename(columns={"size": "weight"})
        .sort_values("weight", ascending=False)
        .reset_index(drop=True)
    )
    return edge_list


def compute_centrality_metrics(edge_list: pd.DataFrame) -> pd.DataFrame:
    """Builds a directed NetworkX graph and computes key centrality metrics."""
    G = nx.DiGraph()
    for _, row in edge_list.iterrows():
        G.add_edge(row["source_page"], row["target_page"], weight=int(row["weight"]))

    in_deg = nx.in_degree_centrality(G)
    out_deg = nx.out_degree_centrality(G)
    betweenness = nx.betweenness_centrality(G, normalized=True)

    # Total inbound and outbound transition volumes
    weighted_in = dict(G.in_degree(weight="weight"))
    weighted_out = dict(G.out_degree(weight="weight"))

    metrics_df = pd.DataFrame(
        {
            "page": list(G.nodes()),
            "in_degree_centrality": [round(in_deg[n], 4) for n in G.nodes()],
            "out_degree_centrality": [round(out_deg[n], 4) for n in G.nodes()],
            "betweenness_centrality": [round(betweenness[n], 4) for n in G.nodes()],
            "inbound_transitions": [weighted_in[n] for n in G.nodes()],
            "outbound_transitions": [weighted_out[n] for n in G.nodes()],
        }
    ).sort_values("betweenness_centrality", ascending=False).reset_index(drop=True)

    return metrics_df


def main() -> None:
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    print("[1/3] Generating synthetic 14-month Matomo dataset (>4,500 sessions)...")
    df_raw = generate_synthetic_matomo_logs(num_sessions=4650)

    print("[2/3] Cleaning URLs, filtering bounces/bots, and building transition edge list...")
    edge_list = clean_matomo_logs(df_raw)
    edge_list.to_csv(output_dir / "cleaned_edge_list.csv", index=False)

    print("[3/3] Computing NetworkX graph centrality metrics...")
    metrics_df = compute_centrality_metrics(edge_list)
    metrics_df.to_csv(output_dir / "node_centrality_metrics.csv", index=False)

    print("\nTop Pages by Betweenness Centrality:")
    print(metrics_df.head(8).to_string(index=False))


if __name__ == "__main__":
    main()