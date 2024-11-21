# Fantasy Football Tiers (inspired by borischen.co)

Python implementation of the borischen.co fantasy football tiers, using sklearn and data from FantasyPros.

## Usage

Install the dependencies and project using `poetry`:

```bash
poetry install
```

Python:
```python
from ff_tiers.clustering import TierAnalyzer
from ff_tiers.download import get_ranking_data, fetch_all_rankings

# Get tier data for a given week (returns a Pandas DataFrame):
rankings_df = fetch_all_rankings(week=12)

# Plot the tiers:
analyzer = TierAnalyzer(rankings_df)
analyzer.plot_tiers("WR", week=12)

# Get position-specific tier data:
pos_tiers = analyzer.create_tiers("WR")

# Inspect the tiers:
max_tier = int(pos_tiers["tier"].max())
for i in range(1, max_tier):
    sub_pos_df = pos_tiers[pos_tiers['tier'] == i]
    print(f"Tier {i}: {', '.join(sub_pos_df['name'].tolist())}\n")
```