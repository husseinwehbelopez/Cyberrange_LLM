import logging
import os
from datetime import datetime

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

# --------------------------------------------------------------------
# Config from environment
# --------------------------------------------------------------------
SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")
SYSTEM_PROMPT = os.getenv("LLM_SYSTEM_PROMPT", "You are a helpful assistant.")
ALLOW_OVERRIDE = os.getenv("ALLOW_SYSTEM_OVERRIDE", "false").lower() == "true"


# --------------------------------------------------------------------
# Splunk HEC logging handler - sends proper JSON
# --------------------------------------------------------------------
class SplunkHECHandler(logging.Handler):
    def __init__(self, url: str, token: str):
        super().__init__()
        self.url = url
        self.headers = {"Authorization": f"Splunk {token}"}

    def emit(self, record: logging.LogRecord) -> None:
        try:
            # We expect logger.info(<dict>) from the app code
            event = record.msg
            if not isinstance(event, dict):
                # Fallback: wrap as message string
                event = {"message": self.format(record)}

            payload = {
                "time": datetime.utcnow().timestamp(),
                "sourcetype": "llm_app",
                "index": "main",
                "event": event,
            }

            requests.post(
                self.url,
                headers=self.headers,
                json=payload,  # send as JSON
                timeout=2,
            )
        except Exception:
            # In a lab we silently swallow logging errors
            pass


# --------------------------------------------------------------------
# Logger setup
# --------------------------------------------------------------------
logger = logging.getLogger("llm_app")
logger.setLevel(logging.INFO)
logger.propagate = False

# HEC handler (only if env vars are set)
if SPLUNK_HEC_URL and SPLUNK_HEC_TOKEN:
    hec_handler = SplunkHECHandler(SPLUNK_HEC_URL, SPLUNK_HEC_TOKEN)
    hec_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(hec_handler)

# Console handler (docker logs)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(console)


# --------------------------------------------------------------------
# Trivial LLM stub (replace with real model later if you want)
# --------------------------------------------------------------------
def trivial_llm(system_prompt: str, user_prompt: str) -> str:
    return (
        f"[SYSTEM]: {system_prompt}\n"
        f"[USER]: {user_prompt}\n"
        f"[LLM]: (stubbed response for training)"
    )


# --------------------------------------------------------------------
# FastAPI app
# --------------------------------------------------------------------
app = FastAPI(title="Vulnerable LLM Lab App")


class ChatRequest(BaseModel):
    user_id: str
    message: str
    system_override: str | None = None


@app.post("/chat")
async def chat(req: ChatRequest, request: Request):
    client_host = request.client.host if request.client else "unknown"

    # Vulnerability: allow user to override system prompt
    effective_system_prompt = SYSTEM_PROMPT
    overridden = False
    if ALLOW_OVERRIDE and req.system_override:
        effective_system_prompt = req.system_override
        overridden = True

    llm_response = trivial_llm(effective_system_prompt, req.message)

    # Structured log event (will be sent to Splunk as JSON)
    log_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": req.user_id,
        "client_ip": client_host,
        "message": req.message,
        "system_override": req.system_override,
        "system_override_used": overridden,
        "response_preview": llm_response[:200],
        "labels": [],
    }

    # Naive detection tags
    lower_msg = req.message.lower()
    suspicious_keywords = [
        "ignore previous instructions",
        "override",
        "exfiltrate",
        "bypass",
        "prompt injection",
    ]
    if any(k in lower_msg for k in suspicious_keywords):
        log_event["labels"].append("possible_prompt_injection")

    # This should NOT raise now
    logger.info(log_event)

    return {
        "system_prompt_effective": effective_system_prompt,
        "response": llm_response,
        "warning": "Lab system, not for production. Logs are sent to Splunk.",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
