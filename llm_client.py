import json
import sys
import requests

LLM_URL = "http://localhost:5000/chat"  # change to http://SERVER_IP:5000 if remote
USER_ID = "human_cli"

def main():
    print(f"Talking to LLM at {LLM_URL} as user_id={USER_ID}")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            msg = input("You> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if msg.strip().lower() in {"exit", "quit"}:
            print("Bye.")
            break

        payload = {
            "user_id": USER_ID,
            "message": msg,
            "system_override": None,  # you can set a string here to simulate override
        }

        try:
            r = requests.post(LLM_URL, json=payload, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"[error] {e}")
            continue

        try:
            data = r.json()
        except json.JSONDecodeError:
            print("Raw response:", r.text)
            continue

        print("LLM>\n", data.get("response", "(no response)"))
        print("---\n")

if __name__ == "__main__":
    main()

