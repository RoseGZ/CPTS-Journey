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

---

# Digging DNS

## Tools
| Tool | Use it for |
|---|---|
| **dig** | Go-to manual tool – any record type, detailed output, zone transfers |
| **nslookup** / **host** | Quick, simple A/AAAA/MX checks |
| **dnsenum** | Automated enum – subdomain brute-force, zone transfers |
| **fierce** | Subdomain enum with recursive search + **wildcard detection** |
| **dnsrecon** | All-in-one DNS enum, multiple output formats |
| **theHarvester** | OSINT – emails, employees, subdomains from many sources |

## dig cheat sheet
```bash
dig domain.com                 # default = A record
dig domain.com MX|NS|TXT|SOA|AAAA|CNAME
dig @1.1.1.1 domain.com        # query a specific name server
dig +trace domain.com          # full resolution path (root → TLD → auth)
dig -x 192.0.2.1           # reverse lookup (PTR) – may need @server
dig +short domain.com          # just the answer
dig +noall +answer domain.com  # only the answer section
dig domain.com ANY             # all records – often ignored (RFC 8482)
```

> ⚠️ Heavy querying can get detected/blocked – respect rate limits and scope.

## Reading dig output
- **Header** – `status: NOERROR` = success (`NXDOMAIN` = doesn't exist). Flags: `qr` response, `rd` recursion desired, `ad` authentic data. Counts of question/answer/authority/additional entries.
- `WARNING: recursion requested but not available` → server won't recurse for you.
- **Question** – what was asked (`google.com. IN A`).
- **Answer** – `name  TTL  IN  type  value` – TTL = seconds it can be cached.
- **Footer** – query time, which server answered (`IP#53`, UDP), timestamp, size.
- **OPT pseudosection** may appear → EDNS (bigger messages, DNSSEC).
