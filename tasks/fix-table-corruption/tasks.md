Start by creating a temporary test for reproducing this bug.

I've already created a sheet -- BookWithTable.xlsx
You can copy, rename, and use this sheet for tests

We can also use the new excel-validator test suite and utils to automatically test code changes against excel. (albeit on windows only)
Write a temporary test case for our BookWithTable.xlsx, then you can call it directly (only that one test case, cuz the full suite is slow)

Later, once we're confidence we've implemented a robust fix, we can look at existing integration and unit tests and decide how to write
automated tests/assertions that can run on CI.

---

Plan talks about a previous code change that sets rows = [] when it loads a table.

This confuses me, because tables shouldn't have rows within (as far as I understand.)

Where does excel store the contents of a table in its own data model? In the sheet?
How should addRow behave in that case?

How does exceljs serialize a table with rows in it? Does exceljs store the rows as an array on the table, but then it has
to copy all those values over to the sheet for serialization?