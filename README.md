# API Reliability Monitor

A Python command-line project that checks HTTP endpoints and tracks their reliability across runs. It reports HTTP status codes, timeouts, connection failures, and how long each check took.

## Quick start

Requires Python 3.12 or later. The project uses only the Python standard library.

From the project folder, run the checker first:

```powershell
python check_endpoint.py
```

The default URLs demonstrate three outcomes: a successful response, a DNS lookup failure, and a `404 Not Found`. To check different endpoints, edit `url_list` in `check_endpoint.py`.

After at least one run, open the history report:

```powershell
python read_history.py
```

Choose a URL by number to see how many checks succeeded, the success rate, and the average duration of successful checks.

## Output files

- `latest_run.json` contains the results from the most recent run.
- `run_history.jsonl` keeps past results, with one line per run.

Both files are generated locally and ignored by Git.