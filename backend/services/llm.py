from openai import Client

from backend.models.llm import LLMRequest, LLMResponse


def prompt(client: Client, prompt: LLMRequest, llm_model: str) -> LLMResponse:
    completion = client.beta.chat.completions.parse(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": "You are a careful eligibility classifier for scholarship pages.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=...,
        temperature=0,
    )

    return completion.choices[0].message.parsed
