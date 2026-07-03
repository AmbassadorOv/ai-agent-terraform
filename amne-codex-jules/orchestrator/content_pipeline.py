import re
import hashlib
import json

class ContentPipeline:
    """Processes incoming content from various sources (Drive, Gemini, GitHub) into clean ontological data."""
    def __init__(self):
        self.registry = []

    def ingest_url(self, url: str, source_type: str):
        print(f"[*] INGESTING {source_type.upper()}: {url}")
        content_id = hashlib.sha256(url.encode()).hexdigest()[:12]
        self.registry.append({"id": content_id, "url": url, "source": source_type, "status": "queued"})
        return content_id

    def filter_and_clean(self, raw_text: str):
        # Remove noisy characters, HTML tags (if any), and normalize
        clean_text = re.sub(r'<[^>]*>', '', raw_text)
        clean_text = re.sub(r'[^a-zA-Z0-9\s\u0590-\u05FF]', '', clean_text) # Keep Hebrew
        return clean_text.strip()

    def create_atomic_config_parts(self, clean_text: str):
        # Split into small logical segments (particles)
        words = clean_text.split()
        particles = []
        for i in range(0, len(words), 5):
            particle = " ".join(words[i:i+5])
            if particle:
                particles.append({
                    "particle_id": hashlib.md5(particle.encode()).hexdigest()[:8],
                    "logic_unit": particle,
                    "entropy": len(set(particle)) / len(particle) if len(particle) > 0 else 0
                })
        return particles

if __name__ == "__main__":
    pipeline = ContentPipeline()
    pipeline.ingest_url("https://g.co/gemini/share/059c9159a1bd", "gemini")
    mock_content = "מערכת אופטימיזציה אטומיסטית עבור רשת סוכנים אוטונומית"
    clean = pipeline.filter_and_clean(mock_content)
    parts = pipeline.create_atomic_config_parts(clean)
    print(f"[*] EXTRACTED {len(parts)} ATOMIC PARTICLES.")
    print(json.dumps(parts[0], indent=2, ensure_ascii=False))
