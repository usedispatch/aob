# AOB CLI

[![Status](https://img.shields.io/badge/Status-Alpha-yellow.svg)]()

A command-line interface tool for scaffolding, deploying, and managing AO applications.

> **Note**: This CLI is currently in alpha stage and under active development. Features may change or break between versions.

## Installation

```bash
pip install aob
```

## Commands

### Initialize Project

```bash
aob init [--sqlite]
```

Clones and sets up a new AO Counter project in the current directory. Optionally specify a custom installation path.

Options:

- `--sqlite`: Initialize project with SQLite database template instead of default counter template

### Build Components

```bash
aob build <component>
```

Build AO application components:

- `aoc build process` - Build the AO process
- `aoc build frontend` - Build the frontend application

### Development Mode

```bash
aob dev frontend
```

Start the frontend development server.

### Deploy Components

```bash
# First, set your wallet environment variable
export WALLET_JSON="$(cat ~/.aos.json)"
# Then deploy process
aob deploy <component>
```

Deploy AO application components:

- `aoc deploy process` - Deploy the AO process

### Run Tests

```bash
aob test process
```

Run tests for the AO process component.

### Generate Tests

```bash
# First, set the model api key
export ANTHROPIC_API_KEY=<key>
# Then generate tests
aob generate test [--model MODEL]
```

Generate test code for AO application components:

- Currently supports test generation only
- Optional `--model` or `-m` flag to specify the AI model:
  - `anthropic` - Use Anthropic's Claude model
  - `openai` - Use OpenAI's GPT model
  - `auto` (default) - Automatically selects based on available API keys

Requires either `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` environment variable to be set.

You can set the env using `export ANTHROPIC_API_KEY=<key>` or `export OPENAI_API_KEY=<key>`.

### Version

```bash
aob version
```

Display the current version of AOX CLI.

## Options

- `--verbose, -v`: Enable verbose output logging
- `--help`: Show help message and available commands

## License

[MIT License](LICENSE.md)
