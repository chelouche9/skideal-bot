# Shlomo Sixt Car Sales Bot 🚗

A warm, professional Hebrew-speaking AI car sales agent powered by **Claude Sonnet 4.5** and **LangChain v1**. This bot helps Israeli customers find the perfect vehicle from Shlomo Sixt's inventory.

## Features

- 🤖 **Claude Sonnet 4.5** - Latest AI model for natural Hebrew conversations
- 🇮🇱 **Hebrew-only** - Professional Hebrew communication
- 🔧 **Real-time Data** - Live integration with Shlomo Sixt APIs
- 🎯 **Smart Recommendations** - Suggests 3-5 relevant vehicles based on customer needs
- 📊 **Multiple Options** - Shows Zero Kilometer, First-hand, and Second-hand vehicles
- 💬 **Conversational** - Warm, persuasive, and customer-focused

## Agent Capabilities

The agent can:

- Browse all available car models (first-hand)
- Search zero kilometer (brand new) vehicles
- Get detailed specifications and pricing for specific cars
- Tailor recommendations based on customer personas:
  - **Family**: Budget-conscious, needs space and reliability
  - **Young**: First car, affordable, economical
  - **Luxury**: Performance, design, prestige

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

- `langchain>=1.0.0` - Modern LangChain v1 API
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
LANGSMITH_PROJECT=shlomo-bot
```

**Get your Anthropic API key**: https://console.anthropic.com/

### 4. Start the LangGraph server

```bash
langgraph dev
```

The server will start on `http://localhost:2024` with hot reload enabled.

## Architecture

### LangChain v1 Agent

The agent is built using LangChain v1's `create_agent` API, which provides:

- Simple, modern interface
- Middleware support for customization
- Native tool calling with Claude
- Streaming responses
- Built-in error handling

### Tools (API Integration)

The agent has access to 4 real-time tools:

1. **`get_available_models`** - Lists all first-hand cars in inventory
2. **`get_zero_km_cars`** - Lists all brand new (0 km) vehicles
3. **`get_first_hand_car_details(importer_model)`** - Gets detailed specs for a first-hand car
4. **`get_zero_km_car_details(car_id)`** - Gets detailed specs for a zero km car

All tools connect to Shlomo Sixt's production APIs:

- Base URL: `https://sales-backend-prod.shlomo.co.il/api/shlomo/`

### System Prompt

The agent operates with a comprehensive Hebrew system prompt that:

- Enforces Hebrew-only communication
- Maintains warm, professional car sales persona
- Never breaks character or admits being AI
- Always uses real data (never guesses or fabricates)
- Provides 3-5 targeted recommendations
- Ends with strong CTAs

## Usage Examples

### Via LangGraph Studio

Open LangGraph Studio (automatically opens when running `langgraph dev`) and start chatting:

**Example 1: Family Car**

```
User: שלום, אני מחפש רכב משפחתי מרווח עם תא מטען גדול, תקציב 150,000 ש"ח
Agent: [Uses get_available_models and get_first_hand_car_details to suggest 3-5 suitable family cars]
```

**Example 2: First Car for Young Adult**

```
User: סיימתי צבא לאחרונה, צריך רכב ראשון חסכוני ובמחיר נגיש
Agent: [Suggests economical options from both first-hand and zero km inventory]
```

**Example 3: Luxury Car**

```
User: מעוניין ברכב יוקרה עם ביצועים גבוהים, עיצוב מרשים
Agent: [Focuses on premium models with performance and design highlights]
```

### Via API

```python
import requests

response = requests.post(
    "http://localhost:2024/runs/stream",
    json={
        "assistant_id": "agent",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": "שלום, אני מחפש רכב משפחתי"
                }
            ]
        }
    },
    headers={"Content-Type": "application/json"},
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

## Development

### Project Structure

```
shlomo-bot/
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

### Key Files

- **`src/agent/graph.py`** - Main agent implementation

  - System prompt in Hebrew
  - 4 async tools for API integration
  - LangChain v1 `create_agent` setup

- **`pyproject.toml`** - Dependencies (LangChain v1, Anthropic, etc.)

- **`langgraph.json`** - Server configuration

### Testing

Run tests:

```bash
pytest tests/
```

### Hot Reload

When running `langgraph dev`, any changes to `src/agent/graph.py` will automatically reload - no need to restart the server!

## API Endpoints Reference

### Shlomo Sixt APIs

The agent integrates with these production endpoints:

| Endpoint                                       | Method | Description                         |
| ---------------------------------------------- | ------ | ----------------------------------- |
| `/api/shlomo/models`                           | GET    | All first-hand models               |
| `/api/shlomo/zero-km-cars`                     | GET    | All zero km cars                    |
| `/api/shlomo/first-hand-cars/{importer_model}` | GET    | Details for specific first-hand car |
| `/api/shlomo/zero-km-cars/{car_id}`            | GET    | Details for specific zero km car    |

## Debugging with LangSmith

To enable LangSmith tracing for debugging:

1. Set environment variables in `.env`:

```bash
LANGSMITH_API_KEY=lsv2_your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=shlomo-bot
```

2. View traces at https://smith.langchain.com/

You'll see:

- Agent reasoning steps
- Tool calls and responses
- Token usage
- Latency metrics
- Error traces

## Why LangChain v1?

This project uses **LangChain v1** (the newest version) with the modern `create_agent` API because:

✅ **Simpler**: Less boilerplate than older APIs
✅ **More powerful**: Built-in middleware support
✅ **Better streaming**: Native streaming with SSE
✅ **Future-proof**: Latest LangChain architecture
✅ **Model-agnostic**: Easy to switch between Claude, GPT, etc.

## Model: Claude Sonnet 4.5

We use `claude-sonnet-4-20250514` because:

- 🧠 **Most capable** - Best reasoning and Hebrew language skills
- 🚀 **Fast** - Low latency for conversational experience
- 💰 **Cost-effective** - Balanced performance/price
- 🔧 **Tool use** - Excellent at deciding when to use which tool
- 🇮🇱 **Hebrew fluency** - Native-level Hebrew comprehension

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

### API timeouts

The tools have 30-second timeouts. If Shlomo Sixt APIs are slow, you may need to adjust:

```python
async with httpx.AsyncClient(timeout=30.0) as client:
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

## Support

For issues with:

- **The agent/bot**: Open an issue in this repo
- **Shlomo Sixt APIs**: Contact Shlomo Sixt IT support
- **LangChain/LangGraph**: Check [LangChain docs](https://docs.langchain.com/)
- **Anthropic/Claude**: Check [Anthropic docs](https://docs.anthropic.com/)

---

Built with ❤️ using Claude Sonnet 4.5 and LangChain v1
