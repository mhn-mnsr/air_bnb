## Trip Planner (CrewAI)

Minimal CrewAI workflow to research destinations, plan an itinerary, and check budget.

### Setup

1. Install Python 3.10+.
2. Install deps (user site packages):
   ```bash
   python3 -m pip install --user crewai python-dotenv openai
   ```
3. Configure env:
   ```bash
   cp .env.example .env
   # edit .env and set OPENAI_API_KEY
   ```

### Run

```bash
python3 -m trip_planner.main
```

Or customize via function params in `trip_planner/main.py`.

### Notes

- Uses `Process.sequential`: research -> itinerary -> budget.
- Set `TRIP_*` vars in `.env` to control defaults.
