# Velarium Bot

A Discord bot with AFK status tracking functionality.

## Features

- **AFK Command**: Set yourself as AFK with an optional reason
- **Slash Command Support**: Use `/afk` for the slash command version
- **Mention Tracking**: Tracks who mentions you while you're AFK
- **Auto-Removal**: Automatically removes AFK status when you send a message
- **Welcome Back Message**: Shows AFK duration and mention count when you return

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- A Discord bot token (get one from [Discord Developer Portal](https://discord.com/developers/applications))

### 2. Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Rename `.env.example` to `.env`
2. Add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

### 4. Running the Bot

```bash
python main.py
```

## Usage

### Text Command
```
,afk [reason]
```

Example:
```
,afk Getting coffee, be back in 5 mins
,afk  (uses default "AFK" reason)
```

### Slash Command
```
/afk [reason]
```

## How It Works

- **Setting AFK**: Use `!afk` or `,afk` with an optional reason
- **Getting Pinged**: When someone mentions you while AFK, a notice is sent and the mention is recorded
- **Returning**: When you send any message (except the AFK command), you're automatically removed from AFK with a summary
- **Mention Summary**: Shows the last 10 pings if you got more than that

## Bot Permissions Required

- Send Messages
- Embed Links
- Read Message History

## File Structure

```
Velarium Bot/
├── main.py              # Main bot file
├── cogs/
│   └── afk.py          # AFK cog with all functionality
├── requirements.txt     # Python dependencies
├── .env                # Bot token (create from .env.example)
├── .env.example        # Example configuration
└── README.md           # This file
```
