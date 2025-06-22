import os
import requests
from llama_api_client import LlamaAPIClient

def load_markdown(url: str) -> str:
    """Download the Markdown file from a raw GitHub URL."""
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def main():
    # Option A: set your API key here
    # os.environ["LLAMA_API_KEY"] = "sk-YOUR_REAL_KEY_HERE"

    # Option B: pass it explicitly when instantiating the client:
    api_key = os.environ.get("LLAMA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "LLAMA_API_KEY not found in environment. "
            "Set LLAMA_API_KEY or uncomment the line in this script to set it."
        )

    # Load the Markdown content
    md_url = (
        "https://raw.githubusercontent.com/"
        "Atharva2099/WikiFace/main/"
        "HF_listings/Summarization/facebook_bart-large-cnn/github_data.md"
    )
    markdown_content = load_markdown(md_url)
    print("Markdown loaded. You can now ask questions about its content.\n")

    # Initialize the Llama client
    client = LlamaAPIClient(api_key=api_key)

    # Prepare the system-level context with the markdown
    conversation = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use the following Markdown document as the knowledge source:\n\n"
                f"{markdown_content}"
            ),
        }
    ]

    # Interactive chat loop
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            # Append user message
            conversation.append({"role": "user", "content": user_input})

            # Send to Llama and stream response
            stream = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=conversation,
                stream=True,
                temperature=0.6,
                max_completion_tokens=1978,
                top_p=0.9,
                repetition_penalty=1.0,
            )

            # Print the assistant's reply as it streams in
            print("Assistant: ", end="", flush=True)
            reply_buffer = ""
            for chunk in stream:
                delta = chunk.event.delta.text or ""
                reply_buffer += delta
                print(delta, end="", flush=True)
            print("\n")

            # Append assistant reply to conversation
            conversation.append({"role": "assistant", "content": reply_buffer})

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
