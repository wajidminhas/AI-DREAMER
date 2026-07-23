
"""
Chat API endpoint — the main entry point for agent conversations.

Receives a user message, runs it through the triage agent,
and returns the agent's response with metadata.

Why a separate endpoint file?
- Single responsibility: this file ONLY handles chat requests
- Easy to test: can test endpoint logic without running full server
- Easy to extend: add streaming, sessions, or file uploads later
"""

from fastapi import APIRouter, HTTPException

from agents import Runner

from imtiaz_mart_ai.api.v1.schemas.requests import ChatRequest
from imtiaz_mart_ai.api.v1.schemas.responses import ChatResponse
from imtiaz_mart_ai.agents.triage import triage_agent

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a user message through the agent system.
    
    Steps:
    1. Validate input (Pydantic handles this)
    2. Run triage agent with user message
    3. Return response + metadata
    """
    try:
        result = await Runner.run(
            triage_agent,
            input=request.message,
        )
        
        return ChatResponse(
            response=str(result.final_output),
            agent_used=result.last_agent.name,
        )
        
    except Exception as e:
        # TODO: Add structured logging here (Day 13)
        raise HTTPException(status_code=500, detail=str(e))