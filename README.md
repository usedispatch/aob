# AOC CLI

A command-line interface tool for scaffolding, deploying, and managing AO applications.

## Installation

```bash
pip install aoc
```

## Commands

### Initialize Project

```bash
aoc init
```

Clones and sets up a new AO Counter project in the current directory. Optionally specify a custom installation path.

### Build Components

```bash
aoc build <component>
```

Build AO Counter components:

- `aoc build process` - Build the AO process
- `aoc build frontend` - Build the frontend application

### Development Mode

```bash
aoc dev frontend
```

Start the frontend development server.

### Deploy Components

```bash
aoc deploy <component>
```

Deploy AO Counter components:

- `aoc deploy process` - Deploy the AO process

### Run Tests

```bash
aoc test process
```

Run tests for the AO process component.

### Version

```bash
aoc version
```

Display the current version of AOX CLI.

## Options

- `--verbose, -v`: Enable verbose output logging
- `--help`: Show help message and available commands

## License

[MIT License](LICENSE)
