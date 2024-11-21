import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator


class TierAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def find_optimal_k(self, X: np.ndarray) -> int:
        inertias = [
            KMeans(n_clusters=k, random_state=42).fit(X).inertia_ for k in range(7, 14)
        ]
        k = (
            KneeLocator(
                range(7, 14), inertias, curve="convex", direction="decreasing"
            ).elbow
            or 10
        )
        return k

    def create_tiers(self, position: str) -> pd.DataFrame:
        pos_df = self.df[self.df["position"] == position].sort_values("rank_ecr").copy()
        X = StandardScaler().fit_transform(
            pos_df[["rank_ecr", "rank_ave"]].astype(float)
        )

        kmeans = KMeans(n_clusters=self.find_optimal_k(X), random_state=42)
        centroids = kmeans.fit(X)

        centroid_ranks = {i: c[0] for i, c in enumerate(centroids.cluster_centers_)}
        tier_mapping = {
            c: i + 1
            for i, c in enumerate(sorted(centroid_ranks, key=centroid_ranks.get))
        }
        pos_df["tier"] = [tier_mapping[c] for c in kmeans.labels_]

        return pos_df

    def plot_tiers(self, position: str, week: int = None):
        plt.clf()  # Clear any existing plots
        df = self.create_tiers(position)

        fig, ax = plt.subplots(figsize=(15, 12))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(df["tier"].unique())))

        for tier, data in df.groupby("tier"):
            color = colors[tier - 1]
            ax.errorbar(
                x=data["rank_ave"].astype(float),
                y=-data["rank_ecr"].astype(float),
                xerr=data["rank_std"].astype(float),
                fmt="o",
                markersize=4,
                color=color,
                ecolor=color,
                label=f"Tier {tier}",
            )

            for _, p in data.iterrows():
                ax.text(
                    float(p["rank_ave"]),
                    -float(p["rank_ecr"]),
                    f" {p['name']}",
                    color=color,
                    fontsize=8,
                    va="center",
                )

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(-y)}"))
        ax.set_xlabel("Average Expert Rank")
        ax.set_ylabel("Expert Consensus Rank")
        ax.set_title(f"Week {week} - {position} Tiers" if week else f"{position} Tiers")
        ax.legend(title="Tier", bbox_to_anchor=(1.02, 1))
        plt.tight_layout()
        plt.show()
