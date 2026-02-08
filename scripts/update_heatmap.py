import requests, datetime, json
import matplotlib.pyplot as plt
import seaborn as sns

today = datetime.date.today().isoformat()

# Load existing progress
try:
    with open("progress.json") as f:
        progress = json.load(f)
except FileNotFoundError:
    progress = {}

progress[today] = {}

# Example: Codeforces submissions
cf_user = "Vansh1947"
cf_api = f"https://codeforces.com/api/user.status?handle={cf_user}"
resp = requests.get(cf_api).json()
submissions_today = [
    s for s in resp['result']
    if datetime.date.fromtimestamp(s['creationTimeSeconds']).isoformat() == today
]
progress[today]['codeforces'] = len(submissions_today)

# TODO: Add LeetCode, CodeChef, AtCoder, HackerRank, GFG fetchers

# Save progress
with open("progress.json", "w") as f:
    json.dump(progress, f, indent=2)

# Generate heatmap
dates = list(progress.keys())
counts = [sum(progress[d].values()) for d in dates]

plt.figure(figsize=(12, 4))
sns.heatmap([counts], cmap="YlGnBu", cbar=True)
plt.title("Competitive Programming Heatmap")
plt.savefig("heatmap.png")