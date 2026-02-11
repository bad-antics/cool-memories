# Cool Memories Documentation

## Overview

Cool Memories is a memory forensics and analysis toolkit written in Julia. Named after Baudrillard's autobiographical works, it provides tools for volatile memory analysis, process inspection, and artifact extraction.

## Capabilities

- **Memory Dump Analysis** — Parse raw memory dumps from Linux, Windows, macOS
- **Process Reconstruction** — Rebuild process state from memory
- **String Extraction** — Smart string extraction with encoding detection
- **Artifact Recovery** — Find credentials, keys, URLs, and other artifacts
- **Timeline Analysis** — Reconstruct event timelines from memory

## Usage

```julia
using CoolMemories

# Analyze a memory dump
dump = load_dump("memory.raw", os=:linux)

# Extract processes
procs = extract_processes(dump)
for p in procs
    println("PID $(p.pid): $(p.name) [$(p.state)]")
end

# Find artifacts
artifacts = find_artifacts(dump, [:credentials, :crypto_keys, :urls])
export_artifacts(artifacts, "findings.json")
```

## Part of Baudrillard Suite

Named after Jean Baudrillard's "Cool Memories" series of autobiographical fragments.
