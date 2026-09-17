# Integration tests (`npm run test:integration`)

Command: `mocha --require spec/config/setup spec/integration --recursive`

Location: `spec/integration/**/*.spec.js (uses real fixture files under spec/integration/data/)`

To regenerate this listing without running assertions:
```
npx mocha --require spec/config/setup spec/integration --recursive --dry-run --reporter spec --no-colors
```

```


  Gold Book
    Read
      ✔ Values
      ✔ Styles

  github issues
    ✔ issue 1027 - Broken due to Cannot set property 'marked' of undefined error

  github issues: Date field with cache style
    ✔ issue 1328 - should emit row with Date Object

  github issues
    ✔ issue 1339 - Special cell value results invalid file

  github issues
    ✔ issue 1364 - Incorrect Worksheet Name on Streaming XLSX Reader

  github issues
    ✔ issue 163 - Error while using xslx readFile method

  github issues
    ✔ issue 1669 - optional autofilter and custom autofilter on tables

  github issues
    ✔ issue 176 - Unexpected xml node in parseOpen

  github issues
    ✔ issue 1804 - wrong image when reusing same image multiple times

  github issues
    issue 1842 - Memory overload when unnecessary dataValidations apply
      ✔ when using readFile
      ✔ when loading an in memory buffer

  github issues
    ✔ issue 2125 - spliceRows remove last row

  github issues
    issue 219 - 1904 dates not supported
      ✔ Reading 1904.xlsx
      ✔ Writing and Reading

  github issues
    ✔ issue 234 - Broken XLSX because of "vertical tab" ascii character in a cell

  github issues
    ✔ issue 257 - worksheet order is not respected

  github issues
    ✔ issue 275 - hyperlink with query arguments corrupts workbook

  github issues
    issue 539 - <contentType /> element
      ✔ Reading 1904.xlsx

  github issues
    ✔ issue 623 - Issue with borders for merged cell when rewriting an excel workbook

  github issues
    ✔ issue 703 - Special cell value results invalid file

  github issues
    ✔ issue 771 - Issue with dataValidation without type and with formula1 or formula2

  github issues
    ✔ issue 877 - hyperlink without text crashes on write

  github issues
    ✔ issue 880 - malformed comment crashes on write

  github issues
    ✔ issue 988 - table without autofilter model

  github issues
    ✔ issue 991 - differentiates between strings with leading numbers and dates when reading csv files

  github issues
    ✔ issue 995 - encoding option works fine

  github issues
    Shared Formulas
      issue xyz - cells copied as a block treat formulas as values
        ✔ copied cells should have the right formulas
        ✔ copied cells should have the right types
        ✔ copied cells should have the same fields

  pr related issues
    pr 896 add xml:space="preserve" for all whitespaces
      ✔ should store cell text and comment with leading new line

  github issues
    ✔ pull request 1204 - Read and write data validation should be successful

  github issues
    ✔ pull request 1220 - The worksheet should not be undefined

  github issues
    ✔ pull request 1262 - protect should work with streaming workbook writer

  github issues
    ✔ pull request 1334 - Fix the error that comment does not delete at spliceColumn

  github issues
    ✔ pull request 1431 - streaming reader should handle rich text within shared strings

  github issues
    pull request 1487 - lastColumn with an empty column
      ✔ Reading 1904.xlsx

  github issues
    pull request 1576 - inlineStr cell type support
      ✔ Reading test-issue-1575.xlsx

  pull request  2244
    ✔ pull request 2244- Fix xlsx.writeFile() not catching error when error occurs

  pr related issues
    pr 5676 whole column defined names
      ✔ Should be able to read this file

  github issues
    ✔ pull request 728 - Read worksheet hidden state

  pr related issues
    pr 896 leading and trailing whitespace
      ✔ Should preserve leading and trailing whitespace
      ✔ Should preserve newlines

  Workbook
    Images
      ✔ stores background image
      ✔ stores embedded image and hyperlink
      ✔ stores embedded image with oneCell
      ✔ stores embedded image with one-cell-anchor
      ✔ stores embedded image with hyperlinks
      ✔ image extensions should not be case sensitive

  Workbook
    Pivot Tables with count
      ✔ if pivot table added, then certain xml and rels files are added
      ✔ if pivot table NOT added, then certain xml and rels files are not added

  Workbook
    Pivot Tables
      ✔ if pivot table added, then certain xml and rels files are added
      ✔ if pivot table NOT added, then certain xml and rels files are not added

  Workbook
    Styles
      ✔ row styles and columns properly
      ✔ in-cell formats properly in xlsx file
      ✔ null cells retain style
      ✔ sets row styles
      ✔ sets col styles

  Workbook
    ✔ spliced meat and ham
    ✔ throws an error when xlsx file not found
    ✔ throws an error when csv file not found
    ✔ throw an error for wrong data type
    Serialise
      ✔ xlsx file
      ✔ sheets with correct names
      ✔ creator, lastModifiedBy, etc
      ✔ printTitlesRow
      ✔ printTitlesColumn
      ✔ printTitlesRowAndColumn
      ✔ shared formula
      ✔ auto filter
      ✔ company, manager, etc
      ✔ title, subject, etc
      ✔ language, revision and contentStatus
      ✔ empty strings
      ✔ dataValidations
      ✔ empty string
      ✔ a lot of sheets to xlsx file
      ✔ csv file
      ✔ CSV file and its configuration
      ✔ defined names
      Xlsx Zip Compression
        ✔ xlsx file with best compression
        ✔ xlsx file with default compression
        ✔ xlsx file with fast compression
        ✔ xlsx file with no compression
      Duplicate Rows
        ✔ Duplicate rows with styles properly
        ✔ Duplicate rows replacing properly
        ✔ Duplicate rows shifting properly
        ✔ Duplicate rows with height properly
      Merge Cells
        ✔ serialises and deserialises properly
        ✔ styles
    Sheet Views
      ✔ frozen panes
      ✔ serialises split panes
      ✔ multiple book views

  WorkbookReader
    Serialise
      ✔ xlsx file
    #readFile
      Row limit
        ✔ should bail out if the file contains more rows than the limit
        ✔ should fail fast on a huge file
        ✔ should parse fine if the limit is not exceeded
      Column limit
        ✔ should bail out if the file contains more cells than the limit
        ✔ should fail fast on a huge file
        ✔ should parse fine if the limit is not exceeded
    #read
      Row limit
        ✔ should bail out if the file contains more rows than the limit
        ✔ should parse fine if the limit is not exceeded
    edit styles in existing file
      ✔ edit styles of single row instead of all
    with a spreadsheet that contains formulas
      with a cell that contains a regular formula
        ✔ should be classified as a formula cell
        ✔ should have text corresponding to the evaluated formula result
        ✔ should have the formula source
      with a cell that contains a hyperlinked formula
        ✔ should be classified as a formula cell
        ✔ should have text corresponding to the evaluated formula result
        ✔ should have the formula source
        ✔ should contain the linked url
    with a spreadsheet that contains a shared string with an escaped underscore
      ✔ should decode the underscore
    with a spreadsheet that has an XML parse error in a worksheet
      ✔ should reject the promise with the sax error
    with a spreadsheet that is missing some files in the zip container
      ✔ should not break
    with a spreadsheet that contains images
      with image`s tl anchor
        ✔ Should integer part of col equals nativeCol
        ✔ Should integer part of row equals nativeRow
        ✔ Should anchor width equals to column width when custom
        ✔ Should anchor height equals to row height
      with image`s br anchor
        ✔ Should integer part of col equals nativeCol
        ✔ Should integer part of row equals nativeRow
        ✔ Should anchor width equals to column width when custom
        ✔ Should anchor height equals to row height
    with a spreadsheet containing a defined name that kinda looks like it contains a range
      ✔ should not crash
    HAN CELL compatibility
      ✔ should read files created by HAN CELL (Korean spreadsheet software)

  WorkbookWriter
    ✔ creates sheets with correct names
    Serialise
      ✔ xlsx file
      ✔ shared formula
      ✔ auto filter
      ✔ Without styles
      ✔ serializes row styles and columns properly
      ✔ rich text
      ✔ A lot of sheets
      ✔ addRow
      ✔ defined names
      ✔ does not escape special xml characters
      ✔ serializes and deserializes dataValidations
      ✔ with zip compression option
      ✔ writes notes
      ✔ Cell annotation supports setting margins and protection properties
      ✔ with background image
      ✔ with background image where worksheet is commited in advance
      ✔ with conditional formatting
      ✔ with conditional formatting that contains numFmt (#1814)
      ✔ with data bar conditional formatting using minimal options (#3015)

  WorksheetWriter
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
      ✔ sets row styles
      ✔ sets col styles
    Merge Cells
      ✔ references the same top-left value
      ✔ does not allow overlapping merges
    Page Breaks
      ✔ adds multiple row breaks

  Worksheet
    ✔ returns sheet values
    ✔ sets row styles
    ✔ sets col styles
    ✔ puts the lotion in the basket
    ✔ Should not break when importing an Excel file that contains a chartsheet
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
      ✔ adds rows with style option
      ✔ inserts rows by object
      ✔ inserts rows by contiguous array
      ✔ inserts rows by sparse array
      ✔ inserts rows with style option
      ✔ should style of the inserted row with inherited style be mutable
      ✔ iterates over rows
      ✔ iterates over collumn cells
      ✔ returns undefined when row range is less than 1
      when worksheet name is less than or equal 31
        ✔ save the original name
      name is be not empty string
        ✔ when empty should thrown an error
        ✔ when isn't string should thrown an error
      when worksheet name is `History`
        ✔ thrown an error
      when worksheet name is longer than 31
        ✔ keep first 31 characters
      when the worksheet name contains illegal characters
        ✔ throws an error
        ✔ throws an error
      when worksheet name already exists
        ✔ throws an error
        ✔ throws an error
    Merge Cells
      ✔ references the same top-left value
      ✔ does not allow overlapping merges
      ✔ merges and unmerges
      ✔ does not allow overlapping merges
      ✔ merges styles
    When passed a non-Excel file
      ✔ Should not break when importing a .numbers file
    Hidden
      ✔ Should set hidden attribute correctly (google-sheets)
      ✔ Should set hidden attribute correctly (libre-calc-as-excel-2007-365)
      ✔ Should set hidden attribute correctly (libre-calc-as-office-open-xml-spreadsheet)


  200 passing (12ms)
```
