# SkiDeal Bot ⛷️

A friendly, professional AI assistant powered by **Claude Sonnet 4.5** and **LangGraph**. This bot helps customers find and book the perfect ski trip packages.

## Features

- 🤖 **Claude Sonnet 4.5** - Latest AI model for natural conversations
- 🏔️ **Ski Trip Packages** - Browse and compare ski destinations
- 🎿 **Smart Recommendations** - Personalized trip suggestions based on preferences
- 💬 **Conversational** - Friendly, helpful, and customer-focused

## Getting Started

### 1. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -e . "langgraph-cli[inmem]"
```

This installs:

- `langchain>=1.0.0` - Modern LangChain API
- `langgraph>=1.0.0` - Agent orchestration framework
- `langchain-anthropic` - Claude Sonnet 4.5 integration
- `httpx` - Async HTTP client for API calls
- `python-dotenv` - Environment variable management

### 3. Set up environment variables

Create a `.env` file in the project root:

```bash
# Required: Anthropic API Key for Claude Sonnet 4.5
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Optional: LangSmith for tracing and debugging
LANGSMITH_API_KEY=lsv2...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=skideal-bot
```

**Get your Anthropic API key**: https://console.anthropic.com/

### 4. Start the LangGraph server

```bash
langgraph dev
```

The server will start on `http://localhost:2024` with hot reload enabled.

## Development

### Project Structure

```
skideal-bot/
├── src/
│   └── agent/
│       ├── __init__.py
│       └── graph.py          # Main agent with tools and system prompt
├── tests/
│   ├── integration_tests/
│   └── unit_tests/
├── .env                      # Your API keys (create this)
├── langgraph.json            # LangGraph configuration
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

### Testing

Run tests:

```bash
pytest tests/
```

### Hot Reload

When running `langgraph dev`, any changes to `src/agent/graph.py` will automatically reload - no need to restart the server!

## Debugging with LangSmith

To enable LangSmith tracing for debugging:

1. Set environment variables in `.env`:

```bash
LANGSMITH_API_KEY=lsv2_your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=skideal-bot
```

2. View traces at https://smith.langchain.com/

## Troubleshooting

### "Module not found" errors

```bash
pip install -e . "langgraph-cli[inmem]"
```

### "ANTHROPIC_API_KEY not set"

Make sure you have a `.env` file with:

```
ANTHROPIC_API_KEY=your-key-here
```

### Port 2024 already in use

```bash
langgraph dev --port 8000
```

## Contributing

1. Make changes to `src/agent/graph.py`
2. Test locally with `langgraph dev`
3. Run tests: `pytest tests/`
4. Check linting: `ruff check .`

## License

MIT

---

Built with ❤️ using Claude Sonnet 4.5 and LangGraph
