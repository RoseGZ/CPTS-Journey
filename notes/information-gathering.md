---
tags: [htb, cpts, pentest-path, notes]
---

# Information Gathering

_My own condensed notes, not course text._

Foundation of the whole test — every engagement should cover all four angles below.

## 1. OSINT

Publicly available info about the company/people: social media, job postings, public meetings, org structure, dependencies. People sharing it usually don't realize how exposed it is.

Big one: secrets leaking through misconfigured public repos or code shared on dev sites (Stack Overflow etc.) — private keys, hashes, tokens, passwords sitting in the open. If something critical turns up this early, follow whatever the RoE's incident-handling section says for reporting it — the client needs to know and fix it, ideally before testing even continues.

## 2. Infrastructure Enumeration

Map the company's internet + intranet footprint: OSINT + DNS + first active scans → nameservers, mail servers, web servers, cloud instances. Build a host/IP list and check it against scope.

Also a chance to gauge their defenses (firewalls, WAFs) — the clearer that picture, the easier it is to plan around detection (evasive testing) later. Doesn't matter if this is done from outside or inside; internal enumeration is also what feeds a **password spraying** target list (one password, many usernames, hoping for one hit).

## 3. Service Enumeration

What's actually running and reachable (network or local): service + version + purpose. Version info often reveals whether something's patched — orgs frequently leave known-vulnerable versions running because they're scared changing them will break things.

## 4. Host Enumeration

Deep dive per host: OS, services, versions, config — active scanning + OSINT. Old/unsupported systems often linger with known vulns nobody's tracking anymore.

Internal-perspective hosts are often assumed "safe" by admins just because they're not internet-facing — that assumption is exactly where misconfigs tend to hide. Post-exploitation, this continues as an internal deep-dive (files, local services, scripts, apps) — part of what feeds privesc.

## Pillaging (quick definition)

Collecting sensitive info that's local to an already-exploited host (names, customer data, etc.) — not treated as its own separate module in the HTB path, more a thread that runs through info-gathering and privesc across many modules. Covered in more depth in my post-exploitation notes.
