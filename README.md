# AOX CLI

A command-line interface tool for scaffolding, deploying, and managing AO Counter applications.

## Installation

```bash
pip install aox
```

## Commands

### Initialize Project

```bash
aox init
```

Clones and sets up a new AO Counter project in the current directory. Optionally specify a custom installation path.

### Build Components

```bash
aox build <component>
```

Build AO Counter components:

- `aox build process` - Build the AO process
- `aox build frontend` - Build the frontend application

### Development Mode

```bash
aox dev frontend
```

Start the frontend development server.

### Deploy Components

```bash
aox deploy <component>
```

Deploy AO Counter components:

- `aox deploy process` - Deploy the AO process

### Run Tests

```bash
aox test process
```

Run tests for the AO process component.

### Version

```bash
aox version
```

Display the current version of AOX CLI.

## Options

- `--verbose, -v`: Enable verbose output logging
- `--help`: Show help message and available commands

## License

[MIT License](LICENSE)
