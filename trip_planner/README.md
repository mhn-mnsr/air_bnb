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
   # edit .env and set the provider API key and TRIP_LLM_MODEL
   ```

### Run

```bash
python3 -m trip_planner.main
```

Or customize via function params in `trip_planner/main.py`.

### Switch LLM Provider

Set `TRIP_LLM_MODEL` and the matching API key:

- OpenAI: `TRIP_LLM_MODEL=openai/gpt-4o-mini`, set `OPENAI_API_KEY`
- Groq: `TRIP_LLM_MODEL=groq/llama-3.3-70b-versatile`, set `GROQ_API_KEY`
- Anthropic: `TRIP_LLM_MODEL=anthropic/claude-3-5-sonnet-latest`, set `ANTHROPIC_API_KEY`

### Notes

- Uses `Process.sequential`: research -> itinerary -> budget.
- Set `TRIP_*` vars in `.env` to control defaults.
