---
tags: [htb, cpts, pentest-path, notes, dns]
---

# DNS

_My own condensed notes, not course text._

Related: [[information-gathering]]

**What it does:** translates domain names → IP addresses (e.g. `www.example.com` → `192.0.2.1`).

## Resolution flow
1. **Local cache** – the host checks its own cache first.
2. **Resolver** (usually ISP, or public like `8.8.8.8`) – checks its cache, otherwise does a **recursive lookup**:
3. **Root server** → points to the right TLD server (13 root servers, `a`–`m.root-servers.net`)
4. **TLD server** (`.com`, `.org`…) → points to the domain's authoritative server
5. **Authoritative server** → returns the actual IP
6. Resolver caches the answer (for the TTL) and returns it → client connects

## Hosts file
Local, manual name→IP mapping that **overrides DNS**. Changes apply immediately.
- Linux/macOS: `/etc/hosts`
- Windows: `C:\Windows\System32\drivers\etc\hosts`
- Format: `<IP>  <hostname> [aliases]`
- Uses: point a vhost to a target box (very common in HTB labs), local dev, block sites (`0.0.0.0 site.com`)

```bash
echo "10.129.x.x  target.htb" | sudo tee -a /etc/hosts
```

## Zones
- **Zone** = part of the namespace managed by one admin (e.g. `example.com` + its subdomains)
- **Zone file** = text file on the authoritative server holding the zone's records
- `IN` in records = Internet class (practically always IN)

## Record types
| Type | Purpose |
|---|---|
| **A** | hostname → IPv4 |
| **AAAA** | hostname → IPv6 |
| **CNAME** | alias → another hostname |
| **MX** | mail servers (with priority) |
| **NS** | authoritative name servers for the zone |
| **TXT** | free text – SPF, domain verification, etc. |
| **SOA** | zone admin info (primary NS, admin email, serial, timers) |
| **SRV** | host + port for a specific service |
| **PTR** | reverse lookup: IP → hostname |

## Why it matters for recon
- **Asset discovery** – subdomains, mail servers, name servers. A CNAME to an old/forgotten server = possible weak target.
- **Infrastructure mapping** – NS records hint at the hosting provider; names like `loadbalancer.` or `vpn.` reveal architecture and entry points.
- **Change monitoring** – new subdomains = new attack surface.
- **TXT records leak tooling** – verification tokens (e.g. `_1password=...`) reveal SaaS in use → useful for phishing/social engineering.
