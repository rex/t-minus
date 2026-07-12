# Changelog

## [0.3.0] — 2026-07-10

- Multi-tab singleton: only one tab speaks. Opening the app in a second tab broadcasts a claim (BroadcastChannel); older tabs mute all announcements, stop writing to storage, and show a "MUTED — ACTIVE IN ANOTHER TAB · CLICK TO TAKE OVER" badge. Clicking a muted tab takes the voice back and silences the others. Muted tabs stay live as read-only mirrors, syncing display from storage events. Fixes double/overlapping voices from duplicate tabs
- Makefile: `make run` (serve with native say), `make open` (open the browser), `make stop` (kill anything on port 4173)

## [0.2.0] — 2026-07-10

- Native macOS `say` voice: new `serve.py` (stdlib-only) serves the app and pipes announcements through the real `say` command with no voice flag — the true system default voice, queued so announcements never overlap. Browser voices remain as fallback (file:// or plain static hosting)
- PAUSE / RESUME: freezes the countdown; on resume every remaining boundary shifts by the exact pause duration, so wall clock, ENDS, and T-ZERO/DEADLINE times stay locked to reality (deadline drift keeps counting against you while paused)
- DEFER ▸▸ : push the current task's remaining time to the end of the queue and start the next task immediately; task list reorders to match
- Live editing: task renames, duration changes, buffer changes, reorders, adds, and deletes apply to the running schedule instantly — no relaunch. Deadline time edits retarget a live session too
- Setup panel dismissible via ✕, click outside, or Esc; new keyboard shortcuts D (defer) and P / Space (pause)

## [0.1.0] — 2026-07-10

Initial build of T-MINUS, an ADHD time-blindness tracker.

- Single-file web app (`index.html`), zero dependencies, zero build step
- Task queue with per-task minutes, per-task buffer override, reorder, live "T-ZERO ≈" / "LAUNCH BY" schedule preview
- Two modes: START NOW (forward from this moment) and BY DEADLINE (schedule anchored backward from a wall-clock deadline, with a violet T-MINUS countdown state before launch and live over/spare drift readout)
- Spoken announcements via macOS system voices (Web Speech API): task start, configurable warning threshold (% or minutes), final-stretch threshold, buffer transitions with what's next, all-clear, and the time every :00/:30 — with an attention chime before each
- Seven full-bleed gradient states: idle, running (emerald), warning (amber), critical (crimson, pulsing), buffer (cyan), waiting (violet), done (gold) — animated glow orbs, grain, vignette
- Giant Space Grotesk task name, colossal JetBrains Mono countdown, across-the-room wall clock, up-next on top, previous task bleeding off the bottom of the screen
- Proportional session timeline map along the bottom edge with live fill
- Controls: COMPLETE/SKIP, +5 MIN, two-tap END, keyboard (Esc / N / +)
- Everything persists in localStorage — refresh resumes mid-second with no repeated announcements
- Screen wake lock while a session is live
