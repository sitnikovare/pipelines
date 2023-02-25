# MeetDagster project

## How to run:

1. Init poetry
2. Go to directory
```
pipelines\MeetDagster\meetdagster
```

3. Run command
```
dagit -f run_dagster.py
```
you should see something like
```
2023-02-25 07:01:20 +0200 - dagit - INFO - Serving dagit on http://127.0.0.1:3000 in process 13225
```

4. Go to link http://127.0.0.1:300
5. Navigate to tab Launchpad at dagit interface
6. Click the "Launch Run" button

### Result
You should see 'Success' status of job and new files:
```
pipelines\MeetDagster\DATA\result_asset.csv
pipelines\MeetDagster\DATA\result_operation.csv
```