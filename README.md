# Checkers Bot

This is a Python implementation of a Checkers bot that utilizes the Alpha-Beta Pruning algorithm for decision making. You can play against a bot or another human player

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/adityak1429/checkers-bot.git
    ```

2. Install the required dependencies:
    ```
    pip install pygame
    ```

## Usage

To play against the bot, run the `layout.py` file with the `bot` argument:
```
python layout.py bot
```

To play against another human player, simply run the `layout.py` file without any arguments:
```
python layout.py
```

## Gameplay

The game is visualized using the Pygame library, providing an interactive and user-friendly interface. Players take turns making moves by selecting their pieces and choosing valid destinations.

The bot's moves are determined using the Alpha-Beta Pruning algorithm, which allows it to make intelligent decisions based on the current state of the game.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
