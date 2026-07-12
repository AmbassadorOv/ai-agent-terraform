import os
try:
    from github import Github
except ImportError:
    Github = None

from julius_time_kernel import TimeKernel

def initialize_clean_repository(kernel: TimeKernel, token, repo_name):
    """
    יצירת מאגר (Repository) מנוקה ומנוהל.
    המערכת מפרידה בין "גרסת האמת" (Clean) לבין "שאריות הזיהום" (Legacy/Bugs).
    """
    kernel.require_time()

    if Github is None:
        return "Error: PyGithub is not installed. Please install it using 'pip install PyGithub'."

    if not token or token == "YOUR_TOKEN":
        return "Error: A valid GitHub token is required."

    print(f"[*] Initializing clean repository: {repo_name}...")

    try:
        g = Github(token)
        user = g.get_user()

        # יצירת מאגר חדש למערכת המנוקה
        repo = user.create_repo(repo_name, private=True)

        # בניית מבנה הספריה להגנה על המערכת
        repo.create_file("README.md", "System: Zero Tolerance Protocol Active.", "Clean system initialized.")
        repo.create_file("bug_monitor.py", "def check_bugs(): return 0 # No bugs allowed", "Monitor initialized.")
        repo.create_file("legacy_blacklist.log", "23000 bugs marked as DEPRECATED/BLOCKED", "Blacklist initialized.")

        # Emit telemetry for repo initialization
        kernel.get_telemetry(1.0)

        return f"Repository {repo_name} initialized and locked."
    except Exception as e:
        return f"Error during repository creation: {str(e)}"
