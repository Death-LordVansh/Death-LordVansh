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

# --- Codeforces API ---
cf_user = "Vansh1947"
cf_api = f"https://codeforces.com/api/user.status?handle={cf_user}"
resp = requests.get(cf_api).json()
submissions_today = [
    s for s in resp['result']
    if datetime.date.fromtimestamp(s['creationTimeSeconds']).isoformat() == today
]
progress[today]['codeforces'] = len(submissions_today)

# --- LeetCode API (GraphQL) ---
# Example query: number of submissions today
leetcode_user = "Death_lord"
query = """
{
  matchedUser(username: "%s") {
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
""" % leetcode_user

resp = requests.post("https://leetcode.com/graphql", json={"query": query}).json()
total_solved = sum(item["count"] for item in resp["data"]["matchedUser"]["submitStats"]["acSubmissionNum"])
progress[today]['leetcode'] = total_solved  # You can refine to daily submissions

# TODO: Add CodeChef, AtCoder, HackerRank, GFG integrations

# Save progress
with open("progress.json", "w") as f:
    json.dump(progress, f, indent=2)

# --- Generate Heatmap ---
dates = list(progress.keys())
counts = [sum(progress[d].values()) for d in dates]

plt.figure(figsize=(12, 4))
sns.heatmap([counts], cmap="YlGnBu", cbar=True)
plt.title("Unified CP Heatmap (LeetCode + Codeforces)")
plt.savefig("heatmap.png")