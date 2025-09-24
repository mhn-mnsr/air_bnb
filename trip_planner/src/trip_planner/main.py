import os
from typing import Optional

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process


def create_agents() -> tuple[Agent, Agent, Agent]:
    destination_researcher = Agent(
        role="Destination Researcher",
        goal=(
            "Identify destinations that best match user constraints: month, duration, budget, interests, and origin."
        ),
        backstory=(
            "Seasoned travel analyst with a deep understanding of seasonal patterns, safety, and cost trends."
        ),
        allow_delegation=False,
        verbose=True,
    )

    itinerary_planner = Agent(
        role="Itinerary Planner",
        goal=(
            "Craft a balanced day-by-day itinerary optimizing travel time, activities, and rest."
        ),
        backstory=(
            "Expert itinerary designer focused on logistics, locality clustering, and memorable experiences."
        ),
        allow_delegation=False,
        verbose=True,
    )

    budget_manager = Agent(
        role="Budget Manager",
        goal=(
            "Estimate costs and ensure the plan fits within budget; propose tradeoffs if needed."
        ),
        backstory=(
            "Financial planner adept at pricing flights, lodging, activities, food, and transport."
        ),
        allow_delegation=False,
        verbose=True,
    )

    return destination_researcher, itinerary_planner, budget_manager


def create_tasks(
    researcher: Agent,
    planner: Agent,
    budgeter: Agent,
    *,
    origin_city: str,
    month: str,
    duration_days: int,
    interests: list[str],
    budget_usd: Optional[int],
) -> list[Task]:
    preferences_block = (
        f"Origin: {origin_city}\nMonth: {month}\nDuration: {duration_days} days\n"
        f"Interests: {', '.join(interests) if interests else 'general sightseeing'}\n"
        f"Budget: ${budget_usd if budget_usd is not None else 'unspecified'}\n"
    )

    research_description = (
        "Given the user preferences, shortlist 3 destination options with rationale, expected weather,\n"
        "visa/safety notes, approximate flight duration, and indicative cost level (low/med/high).\n"
        "Return as a concise table and a brief recommendation paragraph.\n\n"
        f"Preferences:\n{preferences_block}"
    )

    plan_description = (
        "From the recommended destination, produce a day-by-day plan including clusters of activities,\n"
        "must-see highlights, travel logistics, and dining suggestions. Include realistic time blocks\n"
        "and fallback options for bad weather.\n\n"
        f"Preferences:\n{preferences_block}"
    )

    budget_description = (
        "Estimate total trip cost broken down by flights, lodging (per night), activities, local transport,\n"
        "and food. Validate against budget; if over, suggest concrete tradeoffs (e.g., different area,\n"
        "shorter stay, alternative activity). Output a summary table plus notes.\n\n"
        f"Preferences:\n{preferences_block}"
    )

    task_research = Task(
        description=research_description,
        expected_output=(
            "Table of 3 destinations with pros/cons, then a short recommendation paragraph."
        ),
        agent=researcher,
    )

    task_plan = Task(
        description=plan_description,
        expected_output=(
            "Daily itinerary with time blocks, activity clusters, logistics notes, and dining suggestions."
        ),
        agent=planner,
        context=[task_research],
    )

    task_budget = Task(
        description=budget_description,
        expected_output=(
            "Itemized cost estimate and recommendation to fit budget, including tradeoffs if needed."
        ),
        agent=budgeter,
        context=[task_plan],
    )

    return [task_research, task_plan, task_budget]


def run(
    origin_city: str | None = None,
    month: str | None = None,
    duration_days: int | None = None,
    interests_csv: str | None = None,
    budget_usd: Optional[int] = None,
) -> str:
    load_dotenv()
    # Allow options to be sourced from env for quick testing
    origin_city = origin_city or os.getenv("TRIP_ORIGIN", "San Francisco")
    month = month or os.getenv("TRIP_MONTH", "June")
    duration_days = duration_days or int(os.getenv("TRIP_DAYS", "7"))
    interests_csv = interests_csv or os.getenv("TRIP_INTERESTS", "food, museums, nature")
    interests = [s.strip() for s in interests_csv.split(",") if s.strip()]
    budget_env = os.getenv("TRIP_BUDGET_USD")
    budget_usd = budget_usd if budget_usd is not None else (int(budget_env) if budget_env else None)

    a_research, a_plan, a_budget = create_agents()
    tasks = create_tasks(
        a_research,
        a_plan,
        a_budget,
        origin_city=origin_city,
        month=month,
        duration_days=duration_days,
        interests=interests,
        budget_usd=budget_usd,
    )

    crew = Crew(
        agents=[a_research, a_plan, a_budget],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    if hasattr(result, "raw"):
        return str(result.raw)
    return str(result)


if __name__ == "__main__":
    print(run())

