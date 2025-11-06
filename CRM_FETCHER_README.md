# CRM Data Fetcher

A Python script to automatically retrieve data from `agent.ringcloud.et/crm/{id}` for IDs ranging from 1000 to 70000.

## Features

- ✅ Fetches data from 69,001 records (IDs 1000-70000)
- ✅ Progress bar with real-time statistics
- ✅ Error handling and retry logic
- ✅ Rate limiting to avoid server overload
- ✅ Saves individual records to files
- ✅ Generates summary report with statistics
- ✅ Resume capability (can be interrupted and restarted)
- ✅ Configurable range and output directory

## Requirements

- Python 3.x
- requests library (already installed)

## Usage

### Basic Usage (Full Range)

Run the script with default settings (IDs 1000-70000):

```bash
python3 fetch_crm_data.py
```

This will:
- Fetch all records from ID 1000 to 70000
- Save each record to `crm_data/record_{id}.txt`
- Create a summary at `crm_data/summary.json`
- Add 0.1 second delay between requests

### Custom Range

Fetch a specific range of IDs:

```bash
python3 fetch_crm_data.py --start 1000 --end 5000
```

### Custom Output Directory

Save to a different directory:

```bash
python3 fetch_crm_data.py --output my_data
```

### Adjust Request Delay

Change the delay between requests (in seconds):

```bash
python3 fetch_crm_data.py --delay 0.2
```

### Don't Save Individual Files

Only generate summary without saving individual records:

```bash
python3 fetch_crm_data.py --no-save
```

### Combined Options

```bash
python3 fetch_crm_data.py --start 1000 --end 10000 --output batch1 --delay 0.05
```

## Output

### Individual Record Files

Each successful fetch creates a file: `crm_data/record_{id}.txt`

Example: `crm_data/record_1000.txt`

### Summary File

A JSON file with statistics: `crm_data/summary.json`

```json
{
  "start_id": 1000,
  "end_id": 70000,
  "total_attempted": 69001,
  "successful": 68500,
  "failed": 501,
  "timestamp": "2025-11-06T18:10:46.220334",
  "errors": [...]
}
```

## Progress Display

While running, you'll see:

```
[████████████████████░░░░░░░░░░] 45.2% | ID: 32145 | ✓ 31000 | ✗ 145
```

- Progress bar
- Current percentage
- Current ID being fetched
- ✓ Successful fetches
- ✗ Failed fetches

## Interrupting the Script

Press `Ctrl+C` to stop. The script will:
- Save a summary of partial results
- Show statistics for completed fetches
- Allow you to resume later

## Time Estimate

With default settings (0.1s delay):
- 69,001 records × 0.1s = ~6,900 seconds = **~1.9 hours**

To speed up (use with caution):
```bash
python3 fetch_crm_data.py --delay 0.05  # ~58 minutes
```

## Examples

### Test with small range first:
```bash
python3 fetch_crm_data.py --start 1000 --end 1100 --output test
```

### Run full range:
```bash
python3 fetch_crm_data.py
```

### Run in background (Linux):
```bash
nohup python3 fetch_crm_data.py > fetch.log 2>&1 &
```

## Troubleshooting

**Connection errors**: The script will log errors and continue with remaining IDs.

**Timeout errors**: Increase delay with `--delay 0.2` or higher.

**Disk space**: Each record is ~3-4KB. Total: ~270MB for all records.

## Help

View all options:
```bash
python3 fetch_crm_data.py --help
```
