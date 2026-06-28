# Jules Telemetry Auditor

מיקום: infra/telemetry/jules_audit.py

מטרה: דדופינג, סיכום, דגימת precision, גילוי spike ב‑relay latency ותכנון פעולות remediation מבוקרות.

הרצה מהירה:
```bash
python infra/telemetry/jules_audit.py --input infra/telemetry/sample_telemetry.csv --dry-run --canary --backup
```

דגלים חשובים:
--dry-run  : לא מבצע פעולות משנות מצב
--canary   : מגביל פעולות ל‑canary targets
--auto-remediate : מחשב פעולות remediation מתוכננות
--backup   : יוצר snapshot בסיסי לפני פעולות

אבטחה: יש להריץ תחת service account עם RBAC מוגבל. אין להריץ --auto-remediate ללא dry-run ובלי אישור SRE.
