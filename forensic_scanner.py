import os
import subprocess
import json
from datetime import datetime

TERMS = [
    "algorithmic governance", "algorithmic government", "algorithmic world government",
    "global algorithmic governance", "global governance", "world government",
    "world governance", "algorithmic state", "algorithmic constitution",
    "algorithmic referendum", "algorithmic democracy", "AI governance",
    "computational governance", "AI government"
]

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

def main():
    # דורש GitHub CLI (gh) מותקן ומחובר: gh auth login
    repos_json = run('gh repo list --all --limit 1000 --json nameWithOwner,sshUrl')

    try:
        repos = json.loads(repos_json)
    except Exception:
        print("Error: Could not fetch repositories. Run 'gh auth login' first.")
        return

    workspace = "forensic_workspace"
    os.makedirs(workspace, exist_ok=True)
    findings = []

    for repo in repos:
        name = repo['nameWithOwner']
        url = repo['sshUrl']
        repo_path = os.path.join(workspace, name.replace("/", "_"))

        # שכפול בגרסת Bare לביצועים מקסימליים וסריקת כל ה-Branches
        if not os.path.exists(repo_path):
            run(f'git clone --bare {url} {repo_path}')
        else:
            run('git fetch --all', cwd=repo_path)

        for term in TERMS:
            log_cmd = f'git log --all -p -i -S"{term}" --format="COMMIT_INFO:%H|%an|%ad|%s" --date=iso'
            output = run(log_cmd, cwd=repo_path)

            if not output: continue

            commits = output.split("COMMIT_INFO:")
            for commit_data in commits[1:]:
                lines = commit_data.strip().split('\n')
                if not lines or len(lines[0].split('|')) < 4: continue

                meta = lines[0].split('|')
                commit_hash, author, date_str, title = meta[0], meta[1], meta[2], meta[3]

                try:
                    date_obj = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
                except:
                    continue

                current_file = ""
                excerpt = []

                for line in lines[1:]:
                    if line.startswith("+++ b/"):
                        current_file = line[6:]
                    elif term.lower() in line.lower() and (line.startswith("+") or line.startswith("-")):
                        excerpt.append(line.strip())

                if current_file and excerpt:
                    findings.append({
                        "repo": name,
                        "file": current_file,
                        "commit": commit_hash,
                        "author": author,
                        "date": date_obj,
                        "title": title,
                        "excerpt": " ".join(excerpt)[:500].replace('\n', ' '),
                        "term": term
                    })

    # חיפוש גם ב-Issues וב-PRs באמצעות GitHub CLI
    for term in TERMS:
        issues_json = run(f'gh search issues "{term}" --author="@me" --json repository,title,url,createdAt,body --limit 100')
        if issues_json:
            try:
                issues = json.loads(issues_json)
                for issue in issues:
                    date_obj = datetime.strptime(issue['createdAt'][:19], "%Y-%m-%dT%H:%M:%S")
                    findings.append({
                        "repo": issue['repository']['nameWithOwner'],
                        "file": "Issue/PR",
                        "commit": issue['url'].split('/')[-1],
                        "author": "User",
                        "date": date_obj,
                        "title": issue['title'],
                        "excerpt": issue['body'][:500].replace('\n', ' ') if issue['body'] else "",
                        "term": term,
                        "url": issue['url']
                    })
            except:
                pass

    findings.sort(key=lambda x: x["date"])

    with open("forensic_report.md", "w", encoding="utf-8") as f:
        if not findings:
            f.write("לא נמצאו תוצאות.\n")
            return

        for item in findings:
            url = item.get("url", f"https://github.com/{item['repo']}/commit/{item['commit']}")
            f.write(f"Repository: {item['repo']}\n")
            f.write(f"Path/File: {item['file']}\n")
            f.write(f"Commit/Issue/PR: {item['commit']}\n")
            f.write(f"Author: {item['author']}\n")
            f.write(f"Original date: {item['date'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Last relevant modification: [ראה תאריך מקורי]\n")
            f.write(f"Exact title/name: {item['title']}\n")
            f.write(f"Relevant excerpt: {item['excerpt']}\n")
            f.write("What the material appears to establish: \n")
            f.write(f"Evidence URL: {url}\n")
            f.write(f"Confidence: High ({item['term']})\n\n---\n\n")

        f.write("\n## Timeline\n")
        for item in findings:
            year = item['date'].year
            url = item.get("url", f"https://github.com/{item['repo']}/commit/{item['commit']}")
            f.write(f"{year} -> {item['repo']} -> {item['commit'][:7]} -> {item['term']} -> {url}\n")

if __name__ == "__main__":
    main()
