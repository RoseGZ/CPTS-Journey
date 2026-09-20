---
tags: [htb, cpts, pentest-path, notes, metasploit]
---

# Metasploit — Targets

_My own condensed notes, not course text._

**Targets** = OS/version-specific identifiers that tell an exploit module how to adapt itself to the specific build it's attacking (service pack, OS version, even language pack — these all shift memory/return addresses the exploit relies on).

- `show targets` only works *inside* a selected exploit module (`use <module>`). Run at the root msfconsole prompt with nothing selected, it just errors that no module is chosen.
- Many exploits only have one generic "Automatic" target. Others (e.g. old IE/browser exploits) list out specific combinations — browser version + OS + service pack — each as its own numbered target.
- `set target <id>` picks one explicitly. Leaving it on **Automatic** (id 0) tells msfconsole to fingerprint/service-detect the target first before firing.
- `info` on a module is worth running before anything else — shows what the vulnerability actually is, its disclosure date, references (CVE etc.), and module options. Good habit generally: understand what a module/payload actually does before running it, both for safety and to avoid surprises.

**Why targets differ under the hood:** different builds → different return addresses needed for the exploit to hijack execution reliably (things like `jmp esp`, a register jump, or `pop/pop/ret` gadgets). To identify the right target for something novel: get a copy of the actual target binary and use `msfpescan` to find a usable return address in it. (Deeper dive on this lives in the Windows x86 stack buffer overflow material — separate topic.)
