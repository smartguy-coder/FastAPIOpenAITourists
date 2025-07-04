from pydantic_ai import Agent

from apps.tourism.schemas import ResponseTourismDestinationSchema


async def get_ai_tourism_info(
    user_request: str, system_prompt: str, model: str = "gpt-3.5-turbo-1106"
) -> list[ResponseTourismDestinationSchema]:
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        output_type=list[ResponseTourismDestinationSchema],
        output_retries=5
    )

    result = await agent.run(user_request)
    return result.output
