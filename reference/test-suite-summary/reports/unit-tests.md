# Unit tests (`npm run test:unit`)

Command: `mocha --require spec/config/setup --require spec/config/setup-unit spec/unit --recursive`

Location: `spec/unit/**/*.spec.js`

To regenerate this listing without running assertions:
```
npx mocha --require spec/config/setup --require spec/config/setup-unit spec/unit --recursive --dry-run --reporter spec --no-colors
```

```


  Anchor
    colWidth
      ✔ should colWidth equals 640000 when worksheet is undefined
      ✔ should colWidth equals 640000 when column has not set custom width
      ✔ should colWidth equals column width
    rowHeight
      ✔ should rowHeight equals 180000 when worksheet is undefined
      ✔ should rowHeight equals 180000 when row has not set height
      ✔ should rowHeight equals row height
    resize worksheet`s cells
      ✔ should update colWidth
      ✔ should update rowHeight
      ✔ should recalculate col
      ✔ should recalculate row
      ✔ should integer part of row and rowOff should be always equals
      ✔ should integer part of col and colOff should be always equals
      ✔ should update nativeColOff after col has been changed
      ✔ should update nativeRowOff after row has been changed

  Cell
    ✔ stores values
    ✔ validates options on construction
    ✔ merges
    ✔ upgrades from string to hyperlink
    ✔ doesn't upgrade from non-string to hyperlink
    ✔ inherits column styles
    ✔ inherits row styles
    ✔ has effective types
    ✔ shares formulas
    ✔ escapes dangerous html
    ✔ can set comment
    ✔ Cell comments supports setting margins, protection, and position properties

  Column
    ✔ creates by defn
    ✔ maintains properties
    ✔ creates model
    ✔ gets column values
    ✔ sets column values
    ✔ sets sparse column values
    ✔ sets sparse column values
    ✔ sets default column width

  DefinedNames
    ✔ adds names for cells
    ✔ removes names for cells
    ✔ gets the right ranges for a name
    ✔ splices
    ✔ creates matrix from model
    ✔ skips values with invalid range

  NumberFormatRegistry
    ✔ gets-or-creates ids, returning the same id for the same code
    ✔ does not count built-in formats against the limit
    ✔ throws NumberFormatLimitError when a new code exceeds the limit
    ✔ still returns already-registered codes for free when full
    ✔ seeds existing codes without enforcing the limit
    ✔ reports remaining budget and has()
    ✔ exposes a default limit of 206

  Workbook number formats
    ✔ defaults numFmtLimit to 206 and accepts an override
    ✔ addNumberFormat throws NumberFormatLimitError past the limit
    ✔ seeds the registry from custom formats already on cells

  Range
    ✔ has a valid default value
    ✔ constructs as expected
    ✔ expands properly
    ✔ doesn't always include the default row/col
    ✔ detects intersections
    ✔ detects containment

  Row
    ✔ stores cells
    ✔ stores values by whole row
    ✔ iterates over cells
    ✔ builds a model
    ✔ builds from model
    ✔ counts cells
    Splice
      ✔ remove only
      ✔ remove to end
      ✔ remove almost to end
      ✔ remove past end
      ✔ remove and insert fewer
      ✔ remove and insert replacements
      ✔ remove and insert more

  Workbook Writer
    ✔ returns undefined for non-existant sheet

  Workbook
    ✔ stores shared string values properly
    ✔ assigns cell types properly
    ✔ assigns rich text
    - serialises to model
    ✔ returns undefined for non-existant sheet
    ✔ returns undefined for sheet 0
    ✔ returns undefined for sheet 0 after accessing wb.worksheets or wb.eachSheet 
    duplicateRows
      ✔ inserts duplicates
      ✔ overwrites with duplicates

  Worksheet
    Table
      ✔ creates a table
      ✔ removes header
      ✔ removes totals
      ✔ moves the table
      ✔ removes a row
      ✔ adds a row
      ✔ removes a column
      ✔ adds a column
      ✔ renames a column

  Workbook Writer
    ✔ generates valid xml even when there is no data

  Worksheet
    Merge Cells
      ✔ references the same top-left value
      ✔ does not allow overlapping merges
      ✔ merges and unmerges
      ✔ does not allow overlapping merges
      ✔ merges styles
      ✔ preserves merges after row inserts

  Worksheet
    Page Breaks
      ✔ adds multiple row breaks

  Worksheet
    Shared Formulae
      ✔ Fills formula using 2D array values
      ✔ Translates formulae to slave cells
      ✔ Fills formula down using 1D array values
      ✔ Fills formula across using 1D array values
      ✔ Fills formula down and across using 1D array values
      ✔ Fills formula using function

  Worksheet
    Styles
      ✔ sets row styles
      ✔ sets col styles

  Worksheet
    Values
      ✔ stores values properly
      ✔ stores shared string values properly
      ✔ assigns cell types properly
      ✔ adds columns
      ✔ adds column headers
      ✔ adds column headers by number
      ✔ adds column headers by letter
      ✔ adds rows by object
      ✔ adds rows by contiguous array
      ✔ adds rows by sparse array
      ✔ iterates over rows
      ✔ iterates over collumn cells
      ✔ returns sheet values
      ✔ calculates rowCount and actualRowCount
      ✔ calculates columnCount and actualColumnCount
      Splice
        Rows
          ✔ Remove only
          ✔ Remove and insert fewer
          ✔ Remove and insert same
          ✔ Remove and insert more
          ✔ Remove style
          ✔ Insert style
          ✔ Replace style
          ✔ Remove defined names
          ✔ Insert defined names
          ✔ Replace defined names
        Columns
          ✔ splices columns
          ✔ Remove and insert fewer
          ✔ Remove and insert same
          ✔ Remove and insert more
          ✔ handles column keys
          ✔ Splices to end
          ✔ Splices past end
          ✔ Splices almost to end
          ✔ Remove style
          ✔ Insert style
          ✔ Replace style
          ✔ Remove defined names
          ✔ Insert defined names
          ✔ Replace defined names

  Worksheet
    Views
      ✔ adjusts collapsed property of columns
      ✔ adjusts collapsed property of row
      ✔ sets outline levels via column headers

  CellMatrix
    ✔ getCell always returns a cell
    ✔ findCell only returns known cells

  colCache
    ✔ caches values
    ✔ converts numbers to letters
    ✔ converts letters to numbers
    ✔ throws when out of bounds
    ✔ validates addresses properly
    ✔ decodes addresses
    ✔ convert [sheetName!][$]col[$]row[[$]col[$]row] into address or range structures
    ✔ gets address structures (and caches them)
    ✔ decodes addresses and ranges
    with a malformed address
      ✔ tolerates a missing row number
      ✔ tolerates a missing column number

  copyStyle
    ✔ should copy a style deeply
    ✔ should copy fill.stops deeply
    ✔ should return the argument if a falsy value passed

  shared-formula
    slideFormula
      ✔ A1+1 from A2 to A3
      ✔ A1+1 from A2 to B2
      ✔ SUM(A1:A10) from A11 to B11
      ✔ $A$1+A1 from A2 to A3
      ✔ $A$1+A1 from A2 to B2
      ✔ $A1+A1 from A2 to A3
      ✔ $A1+A1 from A2 to B2
      ✔ A$1+A1 from A2 to A3
      ✔ A$1+A1 from A2 to B2

  SharedStrings
    ✔ Stores and shares string values
    ✔ Does not escape values
    ✔ Deduplicates richText values by their XML representation
    ✔ Distinguishes richText entries that differ only in formatting

  StreamBuf
    ✔ writes strings as UTF8
    ✔ writes StringBuf chunks
    ✔ signals end
    ✔ handles buffers
    ✔ handle unsupported type of chunk

  StringBuf
    ✔ writes strings as UTF8
    ✔ grows properly
    ✔ resets

  under-dash
    isEqual
      ✔ works on simple values
      ✔ works on complex arrays
      ✔ works on complex objects

  utils
    xmlEncode
      ✔ encodes xml text
    isDateFmt
      ✔ 'yyyy-mm-dd' a date
      ✔ '' is not a date
      ✔ '[Green]#,##0 ;[Red](#,##0)' is not a date
    dateToExcel
      ✔ should convert date to excel properly
    excelToDate
      ✔ should round to the nearest millisecond when parsing excel date
      ✔ should not lost millisecond precision when parsing excel date

  XmlStream
    ✔ Writes simple XML doc
    ✔ Writes text in XML doc
    ✔ text is escaped
    ✔ attributes are escaped
    ✔ rolls back

  DefinedNameXform
    Defined Names
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Print Area
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    String with something that looks like a range
      ✔ Parse to Model

  WorkbookCalcPropertiesXform
    default
      ✔ Render to XML
      ✔ Render in Composite to XML 
    fullCalcOnLoad
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  WorkbookPropertiesXform
    default
      ✔ Render to XML
      ✔ Render in Composite to XML 
    date1904
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  WorkbookViewXform
    Normal
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Hidden
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Active Tab & First Sheet
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  WorkbookXform
    book.1
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    book.2 - no properties
      ✔ Parse to Model

  AppHeadingPairsXform
    app.01
      ✔ Render to XML
      ✔ Render in Composite to XML 
    app.02
      ✔ Render to XML
      ✔ Render in Composite to XML 

  AppTitlesOfPartsXform
    app.01
      ✔ Render to XML
      ✔ Render in Composite to XML 
    app.02
      ✔ Render to XML
      ✔ Render in Composite to XML 

  AppXform
    app.01
      ✔ Render to XML
      ✔ Render in Composite to XML 
    app.02
      ✔ Render to XML
      ✔ Render in Composite to XML 

  ContentTypesXform
    Three Sheets with shared strings
      ✔ Render to XML
    Images with shared strings
      ✔ Render to XML
    Three Sheets without shared strings
      ✔ Render to XML
    Images without shared strings
      ✔ Render to XML

  CoreXform
    core.xml
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    core.xml
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    core.xml - with cp:lastPrinted
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    core.xml - with cp:contentStatus
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    core.xml - with empty cp:version
      ✔ Parse to Model
    core.xml - without namespace for coreProperties node
      ✔ Parse to Model

  RelationshipsXform
    worksheet.rels
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  BlipFillXform
    normal
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  BlipXform
    full
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  CellPositionXform
    integers
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    halves
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  DrawingXform
    Drawing 1
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model

  TwoCellAnchorXform
    reconcile
      ✔ should not throw on null picture
      ✔ should not throw on null tl
      ✔ should not throw on null br

  ListXform
    Tagged
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Tagged and Counted
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  AutoFilterXform
    Range
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Row and Column Address
      ✔ Render to XML
      ✔ Render in Composite to XML 
    String address
      ✔ Render to XML
      ✔ Render in Composite to XML 

  CellXform
    Styled Null
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Number
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Boolean
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Error
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    String
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    String with Invalid Number
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Inline String with plain text
      ✔ Parse to Model
      ✔ Reconcile Model
    Inline String with RichText
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Shared String
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Shared String with RichText
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Date
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Hyperlink
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    String Formula
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Number Formula
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Master Shared Formula
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Shared Formula Slave
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Array Shared Formula
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model

  CfRuleXform
    Expression
      ✔ Render to XML
      ✔ Parse to Model
    Cell Is
      ✔ Render to XML
      ✔ Parse to Model
    Top 10
      ✔ Render to XML
      ✔ Parse to Model
    Top 10%
      ✔ Render to XML
      ✔ Parse to Model
    Bottom 10
      ✔ Render to XML
      ✔ Parse to Model
    Above Average
      ✔ Render to XML
      ✔ Parse to Model
    Below Average
      ✔ Render to XML
      ✔ Parse to Model
    Colour Scale
      ✔ Render to XML
      ✔ Parse to Model
    Icon Set
      ✔ Render to XML
      ✔ Parse to Model

  CfvoXform
    min
      ✔ Render to XML
      ✔ Parse to Model
    percent
      ✔ Render to XML
      ✔ Parse to Model

  ColorScaleXform
    Colour Scale
      ✔ Render to XML
      ✔ Parse to Model

  FormulaXform
    formula
      ✔ Render to XML
      ✔ Parse to Model

  IconSetXform
    Default Set
      ✔ Render to XML
      ✔ Parse to Model
    Reversed & Hide Values
      ✔ Render to XML
      ✔ Parse to Model

  CfIconExtXform
    range
      ✔ Render to XML
      ✔ Parse to Model

  CfRuleExtXform
    Icon Set
      ✔ Render to XML
      ✔ Parse to Model
    Databar
      ✔ Render to XML
      ✔ Parse to Model

  DatabarExtXform
    Default Set
      ✔ Render to XML
      ✔ Parse to Model
    Default cfvo when not specified
      ✔ Render to XML
    Non Default Set
      ✔ Render to XML
      ✔ Parse to Model

  FExtXform
    formula
      ✔ Render to XML
      ✔ Parse to Model

  IconSetExtXform
    Default Set
      ✔ Render to XML
      ✔ Parse to Model
    Reversed & Hide Values
      ✔ Render to XML
      ✔ Parse to Model

  SqrefExtXform
    range
      ✔ Render to XML
      ✔ Parse to Model

  ColXform
    Best Fit
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Outline
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  DataValidationsXform
    list type
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    whole type
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    decimal type
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    custom type
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    parse open office
      ✔ Parse to Model
    optimised
      ✔ Render to XML
      ✔ Parse to Model

  DimensionXform
    Dimension
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  HeaderFooterXform
    set oddHeader
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    set oddFooter
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    set oddHeader position
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    set firstFooter
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    set differentOddEven
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    set font style
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  HyperlinkXform
    Web Link
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Internal Link
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  MergeCellXform
    Merge
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  OutlinePropertiesXform
    empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    summaryBelow
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    summaryRight
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    summaryRight
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  PageBreaksXform
    one page break
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 

  PageMarginsXform
    normal
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  PageSetupPropertiesXform
    fitToPage
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  PageSetupXform
    normal
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    options
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    defaults
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    scale and fit
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  PrintOptionsXform
    empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    gridlines
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    headers
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    centered
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  RowXform
    Plain
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    No spans
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Styled
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model
    Outline
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
      ✔ Reconcile Model

  SheetFormatPropertiesXform
    full
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    default
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  SheetPropertiesXform
    empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    tabColor
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    pageSetup
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    outlineProperties
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    tabColor + pageSetup
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    tabColor + outlineProperties
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    pageSetup + outlineProperties
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    tabColor + outlineProperties + pageSetup
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  SheetProtectionXform
    Unprotected (Empty)
      ✔ Render to XML
      ✔ Render in Composite to XML 
    Protected (Default)
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Unprotected (All false)
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Protected (All false)
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  SheetViewXform
    Normal
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Normal Zoom
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Normal unruly noliney nohdr
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Page Break Preview
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Split
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Split Top Left
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Frozen
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    List
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Right To Left
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  WorksheetXform
    ✔ hyperlinks must be after dataValidations
    ✔ conditionalFormattings must be before dataValidations
    Sheet 1
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Parse to Model
    Sheet 2 - Data Validations
      ✔ Prepare Model
      ✔ Render to XML
    Sheet 3 - Empty Sheet
      ✔ Render to XML
    Sheet 5 - Shared Formulas
      ✔ Prepare and Render to XML
      ✔ Parse to Model
    Sheet 6 - AutoFilter
      ✔ Render to XML
      ✔ Parse to Model
    Sheet 7 - Row Breaks
      ✔ Prepare Model
      ✔ Render to XML

  BooleanXform
    true
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    false
      ✔ Render to XML
      ✔ Render in Composite to XML 
    undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 

  DateXform
    date
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    iso-date
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 
    invalid date
      ✔ Render to XML

  FloatXform
    five
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    pi
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    zero
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 

  IntegerXform
    five
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    zero
      ✔ Render to XML
      ✔ Render in Composite to XML 
    undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 

  StringXform
    hello
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 

  StaticXform
    Leaf
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Nested
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Texted
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  PhoneticTextXform
    text
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Katakana
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  SharedStringXform
    text
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    rich text
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    richText is empty
      ✔ Parse to Model
    text + phonetic
      ✔ Parse to Model
    Kanji + Katakana
      ✔ Parse to Model
    text with newline
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  SharedStringsXform
    Shared Strings
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  AlignmentXform
    Empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    Top Left
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Middle Centre
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Bottom Right
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Wrap Text
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Indent 1
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Indent 2
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 15
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 30
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 45
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 60
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 75
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate 90
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -15
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -30
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -45
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -60
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -75
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Rotate -90
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Reading Order [Left To Right]
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Reading Order [Right To Left]
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Vertical Text
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  BorderXform
    Empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Thin Red Box
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Dotted colourless Box
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Cross
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Missing Style
      ✔ Render to XML
      ✔ Render in Composite to XML 
    Missing Style
      ✔ Parse to Model

  ColorXform
    RGB
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Theme
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Theme with Tint
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Theme with Tint Zero
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Indexed
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Indexed Zero
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Undefined
      ✔ Render to XML
      ✔ Render in Composite to XML 

  FillXform
    Empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    None
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Gray 125
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Red Dark Vertical Pattern
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Red Green Dark Trellis Pattern
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Blue White Horizontal Gradient
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    RGB Path Gradient
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  FontXform
    green bold
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    rPr tag
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  NumFmtXform
    date
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    thing
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  ProtectionXform
    Empty
      ✔ Render to XML
      ✔ Render in Composite to XML 
    Locked
      ✔ Render to XML
      ✔ Render in Composite to XML 
    Unlocked
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Hidden
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Unlocked and Hidden
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  StyleXform
    Default
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Default with xfId
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Aligned
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Font
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Border
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    NumFmt
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Fill
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    Protected
      ✔ Parse to Model
      ✔ Parse within composite

  StylesXform
    Styles with fonts
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    As StyleManager
      ✔ Renders empty model

  UnderlineXform
    single
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    double
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    false
      ✔ Render to XML
      ✔ Render in Composite to XML 

  AutoFilterXform
    showing filter
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  CustomFilterXform
    custom filter
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    custom filter with operator
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  FilterColumnXform
    showing filter
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    hidden filter
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    with custom filter
      ✔ Prepare Model
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  TableColumnXform
    label
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    function
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  TableStyleInfoXform
    row
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model
    col
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model

  TableXform
    showing filter
      ✔ Render to XML
      ✔ Render in Composite to XML 
      ✔ Parse to Model


  896 passing (46ms)
  1 pending
```
