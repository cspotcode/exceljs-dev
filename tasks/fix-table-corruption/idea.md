There is a bug when using this library, reproducible as follows:

In Excel desktop, create a sheet with a table.
Save it.
Open that workbook in this library.
Save that workbook using this library.
Attempt to open the saved .xlsx in Excel.
Get an error about the table having been corrupted.

Somewhere along the line, this library is corrupting the table, likely not parsing it correctly.

We need to fix that bug.
