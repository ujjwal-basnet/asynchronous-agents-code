from dataclasses import dataclass
from typing import Literal, Annotated
from loguru import logger
from transformers import AutoTokenizer
import tiktoken

# ---------- types ----------

SupportedModels = Annotated[
    Literal["gpt-4.1-mini", "tinyLlama", "gemma2b"],
    "supported text models"
]

PriceTable = Annotated[
    dict[SupportedModels, float],
    "supported model pricing table"
]

# ---------- pricing ----------

price_table: PriceTable = {
    "gpt-4.1-mini": 0.2,
    "tinyLlama": 0.0,
    "gemma2b": 0.0,
}

# ---------- data models ----------

@dataclass
class Message:
    prompt: str
    response: str
    model: SupportedModels

@dataclass
class MessageCostReport:
    req_cost: float
    res_cost: float
    total_cost: float

# ---------- tokenizer cache ----------

_TOKENIZERS = {}

def _get_tokenizer(model: SupportedModels):
    if model in _TOKENIZERS:
        return _TOKENIZERS[model]

    if model == "tinyLlama":
        tok = AutoTokenizer.from_pretrained(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    elif model == "gemma2b":
        tok = AutoTokenizer.from_pretrained(
            "google/gemma-2b"
        )

    else:
        raise ValueError("Tokenizer not required for this model")

    _TOKENIZERS[model] = tok
    return tok

# ---------- token counting ----------

def count_tokens(text: str | None, model: SupportedModels) -> int:
    if text is None:
        logger.warning("text is None; assuming 0 tokens")
        return 0

    if model == "gpt-4.1-mini":
        enc = tiktoken.encoding_for_model("gpt-4.1-mini")
        return len(enc.encode(text))

    tokenizer = _get_tokenizer(model)
    return len(tokenizer.encode(text, add_special_tokens=True))

# ---------- cost calculation ----------

def calculate_usage_cost(message: Message) -> MessageCostReport:
    if message.model not in price_table:
        raise ValueError(
            f"cost calculation not supported for {message.model}"
        )

    price = price_table[message.model]

    req_tokens = count_tokens(message.prompt, message.model) / 1_000_000 ### website price is per million token so
    res_tokens = count_tokens(message.response, message.model) / 1_000_000 

    req_cost = price * req_tokens
    res_cost = price * res_tokens

    return MessageCostReport(
        req_cost=req_cost,
        res_cost=res_cost,
        total_cost=req_cost + res_cost
    )


if __name__ == "__main__":
    msg = Message(
    prompt="Explain transformers briefly",
    response="Transformers use attention instead of recurrence.",
    model="gpt-4.1-mini")

    report = calculate_usage_cost(msg)

    print(report)
