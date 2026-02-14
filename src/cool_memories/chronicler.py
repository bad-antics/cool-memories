"""Cool Memories — Forensic Event Chronicler.

Immutable forensic logging with Baudrillard's fragmentary style.
Each log entry is a 'cool memory' — a crystallized moment that
resists the entropy of information overload.
"""

import os
import json
import hashlib
import time
from datetime import datetime
from collections import OrderedDict


class ForensicChronicler:
    """Create immutable, chain-linked forensic logs.

    Each entry is hashed and linked to the previous, forming
    an evidence chain that cannot be silently altered.
    """

    def __init__(self, log_dir="cool_memories_log"):
        self.log_dir = log_dir
        self.chain = []
        self.genesis_hash = hashlib.sha256(b"In the beginning was the simulacrum").hexdigest()
        os.makedirs(log_dir, exist_ok=True)
        self._load_chain()

    def _load_chain(self):
        """Load existing chain from disk."""
        chain_file = os.path.join(self.log_dir, "chain.json")
        if os.path.exists(chain_file):
            with open(chain_file, "r") as f:
                self.chain = json.load(f)

    def _save_chain(self):
        """Persist chain to disk."""
        chain_file = os.path.join(self.log_dir, "chain.json")
        with open(chain_file, "w") as f:
            json.dump(self.chain, f, indent=2)

    def _compute_hash(self, entry):
        """Compute hash for a chain entry."""
        content = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def record(self, event_type, description, evidence=None, severity="INFO"):
        """Record a forensic event as an immutable chain entry."""
        prev_hash = self.chain[-1]["hash"] if self.chain else self.genesis_hash

        entry = OrderedDict([
            ("index", len(self.chain)),
            ("timestamp", datetime.utcnow().isoformat() + "Z"),
            ("epoch", time.time()),
            ("event_type", event_type),
            ("severity", severity),
            ("description", description),
            ("evidence", evidence or {}),
            ("previous_hash", prev_hash),
        ])

        entry["hash"] = self._compute_hash(dict(entry))
        self.chain.append(dict(entry))
        self._save_chain()

        # Also write individual entry file
        entry_file = os.path.join(
            self.log_dir,
            f"entry_{entry['index']:06d}_{entry['hash'][:8]}.json"
        )
        with open(entry_file, "w") as f:
            json.dump(dict(entry), f, indent=2)

        return dict(entry)

    def verify_chain(self):
        """Verify the integrity of the entire evidence chain."""
        if not self.chain:
            return {"valid": True, "message": "Empty chain", "entries": 0}

        errors = []

        # Check genesis
        if self.chain[0]["previous_hash"] != self.genesis_hash:
            errors.append({
                "index": 0,
                "type": "GENESIS_MISMATCH",
                "detail": "First entry does not reference genesis hash",
            })

        for i, entry in enumerate(self.chain):
            # Verify hash
            entry_copy = dict(entry)
            stored_hash = entry_copy.pop("hash")
            computed_hash = self._compute_hash(entry_copy)
            if computed_hash != stored_hash:
                errors.append({
                    "index": i,
                    "type": "HASH_MISMATCH",
                    "detail": f"Stored: {stored_hash[:16]}... Computed: {computed_hash[:16]}...",
                })

            # Verify chain link
            if i > 0:
                if entry["previous_hash"] != self.chain[i - 1]["hash"]:
                    errors.append({
                        "index": i,
                        "type": "CHAIN_BREAK",
                        "detail": f"Entry {i} does not link to entry {i-1}",
                    })

            # Verify temporal order
            if i > 0:
                if entry["epoch"] < self.chain[i - 1]["epoch"]:
                    errors.append({
                        "index": i,
                        "type": "TEMPORAL_ANOMALY",
                        "detail": "Entry timestamp precedes previous entry",
                    })

        return {
            "valid": len(errors) == 0,
            "entries": len(self.chain),
            "errors": errors,
            "chain_hash": self.chain[-1]["hash"] if self.chain else self.genesis_hash,
        }

    def search(self, event_type=None, severity=None, keyword=None, limit=50):
        """Search the chronicle for matching entries."""
        results = []
        for entry in reversed(self.chain):
            if event_type and entry["event_type"] != event_type:
                continue
            if severity and entry["severity"] != severity:
                continue
            if keyword and keyword.lower() not in json.dumps(entry).lower():
                continue
            results.append(entry)
            if len(results) >= limit:
                break
        return results

    def export_timeline(self, output_format="json"):
        """Export the full timeline."""
        if output_format == "json":
            return json.dumps(self.chain, indent=2)
        elif output_format == "csv":
            lines = ["index,timestamp,event_type,severity,description,hash"]
            for entry in self.chain:
                lines.append(
                    f"{entry['index']},{entry['timestamp']},{entry['event_type']},"
                    f"{entry['severity']},\"{entry['description']}\",{entry['hash'][:16]}"
                )
            return "\n".join(lines)
        else:
            return str(self.chain)


class IncidentRecorder:
    """High-level incident recording with automatic evidence collection."""

    def __init__(self, chronicler=None):
        self.chronicler = chronicler or ForensicChronicler()

    def record_file_event(self, filepath, action="ACCESSED"):
        """Record a file access/modification event."""
        evidence = {"filepath": filepath, "action": action}
        try:
            st = os.stat(filepath)
            evidence.update({
                "size": st.st_size,
                "mode": oct(st.st_mode),
                "uid": st.st_uid,
                "gid": st.st_gid,
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(),
                "atime": datetime.fromtimestamp(st.st_atime).isoformat(),
            })
            with open(filepath, "rb") as f:
                content = f.read(8192)
                evidence["hash_sha256"] = hashlib.sha256(content).hexdigest()
                evidence["partial"] = len(content) < st.st_size
        except (OSError, PermissionError) as e:
            evidence["error"] = str(e)

        return self.chronicler.record(
            event_type="FILE_EVENT",
            description=f"{action}: {filepath}",
            evidence=evidence,
            severity="INFO" if action == "ACCESSED" else "WARNING",
        )

    def record_network_event(self, src, dst, port, protocol="TCP", detail=""):
        """Record a network connection event."""
        return self.chronicler.record(
            event_type="NETWORK_EVENT",
            description=f"{protocol} {src} → {dst}:{port} {detail}",
            evidence={
                "source": src,
                "destination": dst,
                "port": port,
                "protocol": protocol,
                "detail": detail,
            },
            severity="INFO",
        )

    def record_process_event(self, pid, name, action="STARTED", detail=""):
        """Record a process lifecycle event."""
        severity = "INFO"
        if action in ("KILLED", "CRASHED"):
            severity = "WARNING"
        elif action in ("INJECTED", "HOLLOWED"):
            severity = "CRITICAL"

        return self.chronicler.record(
            event_type="PROCESS_EVENT",
            description=f"Process {name} (PID {pid}) {action}",
            evidence={
                "pid": pid,
                "name": name,
                "action": action,
                "detail": detail,
            },
            severity=severity,
        )

    def record_anomaly(self, category, description, evidence=None):
        """Record a detected anomaly."""
        return self.chronicler.record(
            event_type="ANOMALY",
            description=description,
            evidence=evidence or {"category": category},
            severity="WARNING",
        )

    def generate_report(self):
        """Generate a summary forensic report."""
        chain = self.chronicler.chain
        if not chain:
            return {"status": "No events recorded"}

        event_counts = {}
        severity_counts = {}
        for entry in chain:
            et = entry["event_type"]
            sv = entry["severity"]
            event_counts[et] = event_counts.get(et, 0) + 1
            severity_counts[sv] = severity_counts.get(sv, 0) + 1

        verification = self.chronicler.verify_chain()

        return {
            "report_time": datetime.utcnow().isoformat(),
            "total_events": len(chain),
            "time_span": {
                "first": chain[0]["timestamp"],
                "last": chain[-1]["timestamp"],
            },
            "event_breakdown": event_counts,
            "severity_breakdown": severity_counts,
            "chain_integrity": verification,
            "critical_events": [
                e for e in chain if e["severity"] == "CRITICAL"
            ],
        }
