import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from trip_planner.main import run as run_trip


class PlanRequest(BaseModel):
    origin_city: str = Field(..., description="Origin city")
    month: str = Field(..., description="Trip month")
    duration_days: int = Field(..., ge=1, le=30)
    interests: list[str] = Field(default_factory=list)
    budget_usd: Optional[int] = Field(default=None, ge=0)
    model: Optional[str] = Field(default=None, description="LLM model like openai/gpt-4o-mini or groq/llama-3.3-70b-versatile")


class PlanResponse(BaseModel):
    output: str


def create_app() -> FastAPI:
    load_dotenv()
    app = FastAPI(title="Trip Planner (CrewAI)")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

    @app.post("/api/plan", response_model=PlanResponse)
    def plan(req: PlanRequest):
        if req.model:
            os.environ["TRIP_LLM_MODEL"] = req.model
        try:
            output = run_trip(
                origin_city=req.origin_city,
                month=req.month,
                duration_days=req.duration_days,
                interests_csv=", ".join(req.interests),
                budget_usd=req.budget_usd,
            )
            return PlanResponse(output=output)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


def run():
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))


app = create_app()

