Using the C# .exe we created in dev/tasks/excel-com-repair-check,
Write a new test suite that is only run manually on Windows.
It should attempt to parse all the XLSX files in this repo, reporting which ones require "repair" or "data recovery" modes.

You can write it for mocha, so it can be run using the same reporting tools as the other suites.
Make the list of .xlsx files explicit -- explicitly declared it() calls in mocha -- but generate / derive it from scanning for .xlsx files in this repo.

Will need some new helpers to run the .exe, plus a new package.json script to build the .exe

While we're at it:
- move the C# .exe & source into a subdirectory of spec/utils
- refactor so that C# code is minimal. Move all the error log discovery logic out of C#, into JS. This is a JS project, after all, and we don't want maintainers touching more C# than is necessary. The C# should handle solely making the COM calls and reporting the result of those calls: successful return or error.

When writing the new mocha suite, be sure to match code style from other suites and test helpers.