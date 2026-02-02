# Master Changelog

## Session Entry: 2026-02-02 (PC)
- **Goal**: Assess progress and create changelog.
- **Branch**: main (assumed)
- **Device**: PC
- **Status**: Deployment Ready (v2.2)

## Next Actions (Pick One)
- [ ] Test the installed application
- [ ] Distribute to pilot users

## Blocked
- None

## Session Entry: 2026-02-03 (PC)
- **Goal**: Revamp GUI (UI/UX, Features, Refactoring)
- **Branch**: main (assumed)
- **Device**: PC
- **Status**: ✅ RELEASED - Version 1.0

## Next Actions (Pick One)
- [ ] Distribute v2.0 to users
- [ ] Gather feedback on new UI

## Done
- [x] **Refactoring**: Split monolithic code into `domain/`, `services/`, `ui/`, `exporters/`.
- [x] **UI/UX**: Implemented Tkinter GUI with Hero Display, Key-Value Grid, and modern components.
- [x] **Features**:
    - [x] Async Holiday Fetching (Threaded + Queue).
    - [x] Caching with JSON schema and versioning.
    - [x] Excel/CSV Export with clean auditing.
    - [x] Personal Leave improvements (flexible parsing).
- [x] **Verification**:
    - [x] Unit Tests: `domain/tests/test_calculator.py` (Passed).
    - [x] Logic Verification: `verify_logic.py` (Export & Cache logic passed).
    - [x] Entry Point: `main.py` runs successfully.
    - [x] **Bug Fixes**:
        - [x] Added missing `ignored_leave_count` property to domain model.
        - [x] Fixed holiday name parsing (ignoring "30 May" date text).
        - [x] Updated UI to display dates in DD/MM/YYYY format.
        - [x] Resolved IndentationError and NameError in `main_window.py`.
    - [x] **New Feature**: Added "Logs (Debug)" tab for internal diagnostics.
    - [x] **New Feature**: Implemented PDF Export with "Modern Card UI" (Rounded corners, Pills, Stat Cards) matching user design.
    - [x] **Refinement**: Optimized PDF for Print/Grayscale (2x2 Summary Grid, Fixed Layout, Borders, Legends).
    - [x] **New Feature**: Added "PDF Preview" tab for instant feedback within the app.
    - [x] **Improvement**: PDF Preview now automatically "Fits to Window" (Display Full) for better visibility.
    - [x] **Improvement**: PDF Preview updates in real-time when clicking "Calculate" (if tab is active).
    - [x] **Bug Fix**: Dynamic layout adjustment for months with 6 weeks (e.g., March, Aug) to prevent footer overlap.
    - [x] **Refinement**: Switched Summary Cards specific layout to **4 Columns (1 Row)** as requested.
    - [x] **Improvement**: Added **Previous (<) / Next (>)** buttons for 1-click month navigation.
    - [x] **New Feature**: Added **Settings Tab** with useful configurations:
        - **Default Grade**: Set your preferred grade to load on startup.
        - **Auto-Open Export**: Automatically open Excel/PDF files after saving.
        - **Clear Cache**: Reset holiday data if issues arise.
        - *(Changes are saved automatically)*
    - [x] **New Feature**: Replaced native confirmation boxes with **Modern UI Dialogs** (Flat design, branded colors).
    - [x] **Improvement**: Enabled Mousewheel support and Drag-to-Scroll (Panning) for the PDF Preview canvas.
    - [x] **Polish**: Implemented specific PDF feedback (Renamed labels, uniform status codes, footer metadata).
    - [x] **Polish**: Implemented specific PDF feedback (Renamed labels, uniform status codes, footer metadata).
    - [x] **Bug Fix**: Restored missing "Settings" and "About" tabs in UI.
    - [x] **Bug Fix**: Restored missing "Settings" and "About" tabs in UI.
    - [x] **Improvement**: Enhanced Excel Export aesthetics (cleaner fonts, borders, layout).
    - [x] **Refinement**: Replicated exact Excel Styles from template `QSB_WORKING_CALENDAR_2026_01_JG5.xlsx` (Fonts: Calibri 9/11/22, Left Alignment, F0F0F0 padding).
    - [x] **Bug Fix**: Resolved `AttributeError` in Excel Class caused by missing method definition.

