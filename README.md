# Ravenchain

A lightweight blockchain implementation in Python that demonstrates the core concepts of blockchain technology.

## Features

- Basic blockchain structure with block creation and linking
- SHA-256 cryptographic hashing
- Chain validation and integrity checking
- Interactive command-line interface
- Genesis block creation
- Timestamp-based block recording

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/raythurman2386/ravenchain.git
cd ravenchain
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the blockchain application:
```bash
python main.py
```

The interactive menu provides the following options:
1. Add a message to the blockchain
2. View the blockchain
3. Check blockchain validity
4. Exit

## Project Structure

```
ravenchain/
├── main.py         # Main blockchain implementation
├── requirements.txt # Project dependencies
├── .gitignore      # Git ignore file
└── README.md       # Project documentation
```

## How It Works

- Each block contains:
  - Index
  - Timestamp
  - Data (message)
  - Previous block's hash
  - Current block's hash

- The blockchain maintains integrity through:
  - Linking blocks using cryptographic hashes
  - Validating the entire chain
  - Ensuring immutability of historical data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python's hashlib for SHA-256 cryptographic hashing
- Inspired by the fundamental principles of blockchain technology
