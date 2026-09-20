---
tags: [htb, cpts, pentest-path, notes, metasploit]
---

# Metasploit — Payloads

_My own condensed notes, not course text._

**Payload** = the module that rides along with an exploit and actually does something useful once the vuln lands — usually getting a shell back to us. Division of labor: the exploit's job is bypassing the target's normal behavior to get code execution; the payload's job is what runs once that happens (classically, a reverse connection + foothold).

## Three payload shapes

- **Singles** — fully self-contained, everything (exploit delivery + full shellcode) in one blob. Simple and reliable since there's nothing else to fetch, but can get large, and some exploits can't fit them. Think: "add a user," "spawn a process" — done immediately.
- **Stagers** — small, deliberately minimal first-stage shellcode. Its only job is opening a reliable channel back to us so a bigger payload (the stage) can be pulled down afterward. Metasploit auto-picks the best stager for the situation.
- **Stages** — the bigger payload the stager fetches once the channel's up — this is where Meterpreter, VNC injection, etc. live, with no real size limit.

Naming tells you which type: a `/` in the payload path means staged (stager + stage split, e.g. `windows/shell/bind_tcp`); no split (`windows/shell_bind_tcp`) means single.

## Reverse vs. bind

Reverse payloads (target connects *out* to us) tend to be more reliable in practice — they ride on outbound traffic, which networks generally trust/filter less strictly than inbound. Bind payloads make the target listen and wait for us to connect in instead. Neither is bulletproof against a well-configured environment, but reverse is the more common default.

## Meterpreter

The advanced staged payload of choice for most engagements — DLL-injection based, lives entirely in memory (no disk footprint, which makes it noticeably harder to catch with basic forensic/AV checks), supports dynamically loading extra scripts/plugins, and comes with a huge command set: credential/hash dumping, screenshots, keystroke capture, mic access, process/token manipulation, and more. Its command syntax deliberately doesn't mirror native OS commands (e.g. `getuid` instead of `whoami`) — it's its own interface, though a `shell` command drops into a real native shell on the target if that's more convenient for a specific task.

## Finding & selecting a payload

`show payloads` inside a selected exploit module lists everything compatible with that module's target OS/arch. The full list across all platforms is huge, so `grep <term> show payloads` filters it (chainable — pipe a second `grep` after the first to narrow further; `grep -c` just gives a count). Once you've got the right one, `set payload <id>` attaches it to the exploit — after that, new payload-specific options appear alongside the exploit's own (most commonly `LHOST`/`LPORT` for reverse payloads: `LHOST` = your own IP as the listener, `LPORT` = the port it listens on; `ifconfig` inside msfconsole is a quick way to check your own IP without leaving the tool).

## Common Windows payload families

Roughly: generic multi-use listeners (`generic/shell_bind_tcp`, `generic/shell_reverse_tcp`), simple single-purpose singles (`windows/x64/exec`, `loadlibrary`, `messagebox`), single vs. staged shell variants, and the big families with many transport options each — `meterpreter/*`, `powershell/*` (interactive PowerShell sessions), `vncinject/*`.

Worth knowing exist even though out of scope here: **Empire** and **Cobalt Strike** — other major payload/C2 frameworks used heavily in professional engagements. Custom payloads can also be built directly with `msfvenom` (its own topic).
