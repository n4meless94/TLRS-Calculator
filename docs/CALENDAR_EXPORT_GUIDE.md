# TLRS Calculator - Calendar Export Guide

## Overview

The TLRS Calculator now exports to Excel with a professional calendar grid view, perfect for claim submissions and record-keeping.

## Excel Workbook Structure

### Sheet 1: Calendar (Primary)

The main sheet displays a true monthly calendar grid styled like a wall calendar.

**Layout:**
- **Page Setup**: A4 Landscape, fits on 1 page
- **Title**: Large month/year header (e.g., "MARCH 2025")
- **Day Headers**: Sunday through Saturday with dark blue background
- **Calendar Grid**: 6 weeks × 7 days (always 6 rows for consistency)
- **Cell Height**: 80 pixels for readability

**Cell Content:**
Each date cell contains:
- **Day Number** (top-left, bold, large font)
- **Status Marker** (in brackets):
  - `[WD]` = Working Day (eligible for reimbursement)
  - `[WE]` = Weekend (Saturday/Sunday)
  - `[PH]` = Public Holiday
  - `[PL]` = Personal Leave
- **Holiday Name** (if applicable, in red italic text)
- **"Personal Leave"** label (if applicable, in yellow highlight)

**Visual Styling:**
- **Weekends**: Light blue background (Sunday and Saturday columns)
- **Public Holidays**: Holiday name displayed in red
- **Personal Leave**: Yellow background highlight
- **Working Days**: Clean white cells with `[WD]` marker
- **Outside Month**: Blank cells (dates before/after the month)

**Monthly Summary (Bottom-Right):**
```
X Working Days

JGA:      RM X,XXX.00
JG8/JGB:  RM X,XXX.00
JG7:      RM X,XXX.00
JG6:      RM X,XXX.00
JG5:      RM X,XXX.00
```

- Shows working days count
- Lists reimbursement amounts for all grades
- Selected grade is highlighted in red and bold
- Currency formatted with RM prefix and 2 decimal places

### Sheet 2: Details (Secondary)

Traditional table format for audit and verification purposes.

**Columns:**
1. **Date** (dd/mm/yyyy format)
2. **Day** (Monday, Tuesday, etc.)
3. **Status** (Weekend, Public Holiday, Personal Leave, Working Day)
4. **Holiday/Leave Name** (actual holiday name or "Personal Leave")
5. **Remarks** (Eligible or Excluded)

**Color Coding:**
- Weekends: Light blue row
- Public Holidays: Light yellow row
- Personal Leave: Light yellow row
- Working Days: White row

**Summary Section:**
- Total Calendar Days
- Weekend Days
- Public Holidays
- Personal Leave Days
- Working Days Eligible
- Total Reimbursement (for selected grade)

## How to Use

### Generating the Calendar Export

1. **Open TLRS Calculator** (`dist/tlrs.exe`)
2. **Select Grade** (JG5–JGA)
3. **Choose Month and Year**
4. **(Optional) Add Personal Leave Dates**
5. **Click "Calculate Reimbursement"**
6. **Click "📊 Export Excel"**
7. **Choose save location** (default filename includes year, month, and grade)

### Printing the Calendar

**For Best Results:**
1. Open the exported Excel file
2. Go to the **Calendar** sheet
3. **File → Print** (or Ctrl+P)
4. **Settings:**
   - Paper: A4
   - Orientation: Landscape
   - Margins: Narrow
   - Fit to: 1 page wide × 1 page tall
5. **Print**

The calendar will print on a single page, suitable for attaching to claim forms.

### Using the Details Sheet

The Details sheet provides:
- **Audit Trail**: Complete record of all dates and their status
- **Verification**: Easy to cross-check with claim requirements
- **Record-Keeping**: Suitable for filing with claim documentation

## Example Output

### Calendar Sheet Example (March 2026)

```
                    MARCH  2026

Sunday    Monday    Tuesday   Wednesday  Thursday  Friday    Saturday
                                                              1 [WD]
2 [WE]    3 [WD]    4 [WD]    5 [WD]    6 [WD]    7 [WD]    8 [WE]
9 [WE]    10 [WD]   11 [WD]   12 [WD]   13 [WD]   14 [WD]   15 [WE]
16 [WE]   17 [WD]   18 [WD]   19 [WD]   20 [WD]   21 [PH]   22 [WE]
           Hari Raya Puasa
23 [WE]   24 [WD]   25 [WD]   26 [WD]   27 [WD]   28 [WD]   29 [WE]
30 [PH]   31 [WD]
Hari Jadi Yang di-Pertua Negeri Sabah

                    21 Working Days

JGA:      RM 5,250.00
JG8/JGB:  RM 4,200.00
JG7:      RM 3,150.00
JG6:      RM 2,100.00
JG5:      RM 1,050.00
```

## Features

✅ **Professional Appearance** - Suitable for claim submissions
✅ **Print-Ready** - Fits on single A4 page in landscape
✅ **Clear Status Markers** - Easy to identify working days vs. excluded days
✅ **Holiday Names** - Shows actual Sabah public holiday names
✅ **All Grades** - Displays reimbursement for all grade levels
✅ **Audit Trail** - Details sheet for verification
✅ **Color-Coded** - Visual distinction between day types
✅ **Offline Support** - Works with cached holidays or offline mode

## Troubleshooting

### Calendar Not Printing Correctly

**Issue**: Calendar doesn't fit on one page
**Solution**: 
- Ensure "Fit to 1 page" is selected in print settings
- Use narrow margins
- Landscape orientation

### Holiday Names Not Showing

**Issue**: Holidays show as blank or "Public Holiday"
**Solution**:
- Click "Refresh Holidays" to fetch latest data
- Ensure internet connection is available
- Check that offline mode is not enabled

### Dates Appear in Wrong Month

**Issue**: Dates from previous/next month showing
**Solution**:
- This is normal - the calendar grid always shows 6 weeks
- Dates outside the selected month appear blank
- Check the Details sheet for clarification

## Technical Details

- **File Format**: .xlsx (Excel 2007+)
- **Sheets**: 2 (Calendar + Details)
- **Page Setup**: A4 Landscape, 1 page
- **Fonts**: Calibri (standard)
- **Colors**: Professional blue/yellow/light blue scheme
- **Date Format**: dd/mm/yyyy

## Support

For issues or questions:
1. Check the Details sheet for complete date breakdown
2. Verify holiday data by clicking "Refresh Holidays"
3. Ensure all dates are within the selected month
4. Check that personal leave dates are in correct format (dd/mm/yyyy)
