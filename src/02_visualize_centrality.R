# ==============================================================================
# Web User-Flow Network Centrality Visualization
# Author: Rungwit Suttinan
# Description: Reads the cleaned edge list and node centrality metrics from
#              Python and renders a circular directed network graph in R.
# ==============================================================================

library(tidyverse)
library(igraph)
library(ggraph)

# 1. Load cleaned edge list and centrality metrics exported by Python
edges <- read_csv("data/cleaned_edge_list.csv", show_col_types = FALSE) %>%
  filter(weight >= 25) # Filter low-frequency noise edges for visual clarity

nodes <- read_csv("data/node_centrality_metrics.csv", show_col_types = FALSE)

# 2. Construct directed igraph object
network_graph <- graph_from_data_frame(
  d = edges,
  vertices = nodes,
  directed = TRUE
)

# 3. Render network visualization using ggraph
set.seed(42)
plot_network <- ggraph(network_graph, layout = "linear", circular = TRUE) +
  geom_edge_arc(
    aes(width = weight, alpha = weight),
    arrow = arrow(length = unit(2.5, "mm"), type = "closed"),
    end_cap = circle(4, "mm"),
    colour = "#4A6FE3"
  ) +
  geom_node_point(
    aes(size = betweenness_centrality, color = in_degree_centrality)
  ) +
  geom_node_text(
    aes(label = name),
    repel = TRUE,
    size = 3.5,
    fontface = "bold",
    color = "#1F2937"
  ) +
  scale_edge_width(range = c(0.3, 2.2), name = "Transition Volume") +
  scale_edge_alpha(range = c(0.25, 0.85), guide = "none") +
  scale_size_continuous(range = c(4, 12), name = "Betweenness Centrality") +
  scale_color_viridis_c(option = "plasma", name = "In-Degree Centrality") +
  labs(
    title = "Web Portal User-Flow & Navigation Centrality Network",
    subtitle = "Node size = Betweenness Centrality (Bridge Pages) | Edge width = Session Transition Frequency",
    caption = "Synthetic Matomo Dataset (>4,500 Sessions, 14 Months) | Python (pandas, networkx) + R (ggraph)"
  ) +
  theme_void() +
  theme(
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5, margin = margin(t = 10, b = 4)),
    plot.subtitle = element_text(size = 10, hjust = 0.5, color = "#4B5563", margin = margin(b = 15)),
    plot.caption = element_text(size = 8, hjust = 0.5, color = "#6B7280", margin = margin(t = 15, b = 10)),
    legend.position = "right"
  )

# 4. Export high-resolution PNG
dir.create("output", showWarnings = FALSE)
ggsave(
  filename = "output/user_flow_network_centrality.png",
  plot = plot_network,
  width = 11,
  height = 8,
  dpi = 300,
  bg = "white"
)

message("Saved network plot to output/user_flow_network_centrality.png")