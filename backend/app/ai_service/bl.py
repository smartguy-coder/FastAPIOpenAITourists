import logging
from fastapi import HTTPException, status

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from apps.tourism.schemas import ResponseTourismDestinationSchema


async def get_ai_tourism_info(
    user_request: str, system_prompt: str, model: str = "gpt-3.5-turbo-1106"
) -> list[ResponseTourismDestinationSchema]:
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        output_type=list[ResponseTourismDestinationSchema],
        output_retries=5,
        model_settings=ModelSettings(timeout=25)
    )

    try:
        result = await agent.run(user_request)
        return result.output
    except Exception as e:
        logging.error(f"Error in get_ai_tourism_info: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request to AI agent timed out or failed."
        )
