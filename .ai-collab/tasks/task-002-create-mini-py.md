# Task 002 — create-mini-py

## Goal
Create `mini.py` at the repository root. The script uses `matplotlib` (and/or `matplotlib.patches`) to draw a classic Mickey Mouse head (three filled circles) and save/display the result.

## Status
`todo`

## Assigned to
codex

## Target paths
- `mini.py`

## Instructions
1. Create a new file `mini.py` at `C:\Users\X\Desktop\test_of_multi_agent\mini.py`.
2. Use `matplotlib` and `matplotlib.patches` — **no external image assets**.
3. The drawing must include:
   - A large filled black circle for the head.
   - Two smaller filled black circles for the ears (upper-left and upper-right).
   - A skin-colored (peach/tan) filled ellipse for the face area.
   - Two white eyes with black pupils.
   - A nose (small black ellipse).
   - A smiling mouth (arc).
   - Optional: red shorts outline or other iconic details if space allows.
4. The script must call `plt.savefig("mini.png")` to save the output image, then `plt.show()`.
5. The script must be runnable with `python mini.py` (only stdlib + matplotlib required).

## Acceptance criteria
- `mini.py` exists at the repo root.
- Running `python mini.py` produces `mini.png` without errors.
- `mini.png` visually resembles a Mickey Mouse face.

## Depends on
*(none)*

## Updated
2026-03-18
