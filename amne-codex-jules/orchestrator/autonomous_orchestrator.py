import os
import requests

class AutonomousOrchestrator:
    def __init__(self):
        self.active_agents = 0
        # Trigger lock to ensure alert is sent only once when crossing the threshold
        self.alert_500_sent = False

    def send_whatsapp_alert(self, message: str):
        """
        Sends a high-priority alert directly to the Admiral's WhatsApp.
        """
        # Retrieve encrypted data from environment variables (GitHub Secrets / Env)
        phone = os.getenv("WHATSAPP_PHONE")      # Your phone number (with country code, e.g., +972...)
        api_key = os.getenv("WHATSAPP_API_KEY")  # The API Key from CallMeBot

        if not phone or not api_key:
            print("[WARNING] WhatsApp API credentials missing. Authorize API to receive alerts.")
            return

        # Using CallMeBot's fast bridge for system messages to WhatsApp
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey={api_key}"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"[SUCCESS] WhatsApp Alert sent to Admiral: {message}")
            else:
                print(f"[ERROR] Failed to send WhatsApp alert. Status: {response.status_code}")
        except Exception as e:
            print(f"[CRITICAL] WhatsApp Bridge Connection Error: {e}")

    def monitor_swarm(self, current_agent_count: int):
        """
        Continuous monitoring loop that tracks agent count and triggers threshold alerts.
        """
        self.active_agents = current_agent_count

        # Check Sovereign Territory boundary (500 agents)
        if self.active_agents >= 500 and not self.alert_500_sent:
            alert_msg = f"🚨 [SYSTEM IGNITION] Admiral, the 500 agent threshold has been successfully crossed! The swarm now counts {self.active_agents} active units in parallel."
            self.send_whatsapp_alert(alert_msg)

            # Lock the trigger to prevent duplicate messages
            self.alert_500_sent = True

        # Optional: Reset the lock if agent count drops below threshold (for re-triggering on subsequent crossings)
        elif self.active_agents < 500 and self.alert_500_sent:
            self.alert_500_sent = False
