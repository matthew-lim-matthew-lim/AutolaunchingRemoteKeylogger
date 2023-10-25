# AutolaunchingRemoteKeylogger
A suite of 3 programs:
1. A keylogger (`windowsProcess.py`) packaged into an `.exe` (`dist/windowsProcess.exe`). When opened, copies itself to Windows starting directory so it automatically launches each startup. Logs keys until user stops typing, then sends logged keys and a screenshot to a target email.
2. An extractor for emailed key-logs (`keylogExtractor.py`). Extracts the emailed logged keys and saves them into files based on source computer.
  - The fully concatenated file format is suitable for the 3rd program, which searches for common strings.
  - The timestamp-seperated file format is suitable for discerning seperate user sessions or spurts of usage.
3. A common-string searcher (`stringExtractor.py`), which outputs a file with complex formatting and keywords removed for easier manual analysis. Also allows user to input parameters for automatic common-string searching.
- First argument is the source file (which must be a fully concatenated file).
- Second argument is the minimum number of characters each subject string should have.
- Third argument is the number of search results to display.

These programs are for educational purposes only. They must not be used with malicious intent. Only use these programs on devices you own.
