#!/usr/bin/env python3
"""
Jules Telemetry Auditor
Usage:
  python infra/telemetry/jules_audit.py --input telemetry.csv [--dry-run] [--canary] [--auto-remediate] [--backup]
"""
import argparse
import pandas as pd
import os
import sys
import json
from collections import Counter
import logging
import hashlib
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def ewma(series, alpha=0.3):
    s = []
    prev = None
    for v in series:
        if prev is None:
            prev = v
        else:
            prev = alpha * v + (1 - alpha) * prev
        s.append(prev)
    return s

def fingerprint(row, keys):
    s = "|".join(str(row[k]) for k in keys if k in row)
    return hashlib.sha1(s.encode()).hexdigest()

def load_df(path):
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.json'):
        return pd.read_json(path, lines=True)
    else:
        raise RuntimeError("Unsupported format")

def dedupe(df):
    if 'bugid' in df.columns:
        df_unique = df.drop_duplicates(subset=['bugid'])
    elif 'bug_id' in df.columns:
        df_unique = df.drop_duplicates(subset=['bug_id'])
    else:
        df['fingerprint'] = df.apply(lambda r: fingerprint(r, ['bugtype','detectedby','timestamp','payload_hash']), axis=1)
        df_unique = df.drop_duplicates(subset=['fingerprint'])
    return df_unique

def summarize(df):
    counts = df['bugtype'].value_counts().to_dict()
    total = len(df)
    return total, counts

def sample_precision(df, sample_n=1000):
    if 'istruebug' not in df.columns:
        return None, None
    sample = df.sample(n=min(sample_n, len(df)), random_state=42)
    precision = sample['istruebug'].mean()
    return precision, len(sample)

def backup_state(backupdir='backups'):
    os.makedirs(backupdir, exist_ok=True)
    ts = int(time.time())
    fname = os.path.join(backupdir, f"telemetry_backup_{ts}.json")
    logging.info("Creating backup %s", fname)
    with open(fname, 'w') as f:
        f.write(json.dumps({'ts': ts}))
    return fname

def plan_remediation(df, conf_low=0.5, conf_high=0.99):
    actions = []
    for _, row in df.iterrows():
        conf = float(row.get('confidence', 0.0))
        bugid = row.get('bugid') or row.get('fingerprint')
        if conf < conf_low:
            actions.append({'bugid': bugid, 'action': 'quarantine', 'reason': 'low_confidence'})
        elif conf >= conf_high:
            actions.append({'bugid': bugid, 'action': 'schedule_terminate', 'reason': 'high_confidence'})
    return actions

def autoremediate(actions, dry_run=True, canary=True):
    logging.info("Planned remediation actions: %d", len(actions))
    if dry_run:
        return actions
    executed = []
    for a in actions:
        if canary:
            logging.info("CANARY mode: not executing destructive action %s for %s", a['action'], a['bugid'])
            executed.append({'bugid': a['bugid'], 'status': 'planned'})
        else:
            logging.info("Executing action %s for %s", a['action'], a['bugid'])
            executed.append({'bugid': a['bugid'], 'status': 'executed'})
    return executed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--canary', action='store_true')
    parser.add_argument('--auto-remediate', action='store_true')
    parser.add_argument('--backup', action='store_true')
    parser.add_argument('--sample-n', type=int, default=1000)
    args = parser.parse_args()

    if args.backup:
        backup_state()

    df = load_df(args.input)
    df_unique = dedupe(df)
    total, counts = summarize(df_unique)
    logging.info("Total unique bugs: %d", total)
    logging.info("Counts by type: %s", counts)

    precision, samplen = sample_precision(df_unique, sample_n=args.sample_n)
    if precision is not None:
        logging.info("Sample precision on %d items: %.3f", samplen, precision)

    if 'relaylatencyms' in df_unique.columns:
        lat_series = df_unique['relaylatencyms'].fillna(0).tolist()
        filtered = ewma(lat_series, alpha=0.2)
        df_unique['latewma'] = filtered
        median = pd.Series(filtered).median()
        spikes = (pd.Series(filtered) > median * 3).sum()
        logging.info("Detected latency spikes: %d", int(spikes))

    planned_actions = []
    if args.auto_remediate:
        planned_actions = plan_remediation(df_unique)
        executed = autoremediate(planned_actions, dry_run=args.dry_run, canary=args.canary)
        logging.info("Auto-remediate returned %d planned/executed actions", len(executed))

    out = {
        'total_unique': total,
        'counts': counts,
        'planned_actions': len(planned_actions)
    }
    print(json.dumps(out))

if __name__ == "__main__":
    main()
