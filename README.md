# RavenChain

A modern, Python-based blockchain implementation focusing on simplicity, security, and scalability. RavenChain demonstrates core blockchain concepts while providing a foundation for building decentralized applications.

## 🚀 Features

### Current Features
- ✅ Core blockchain implementation with proof-of-work mining
- ✅ Secure wallet management with ECDSA cryptography
- ✅ Transaction system with digital signatures
- ✅ Bitcoin-style address generation
- ✅ Interactive command-line interface
- ✅ Persistent wallet storage
- ✅ Chain validation and integrity checking
- ✅ Mining rewards system

### Planned Features
- 🔄 Peer-to-peer networking
- 🌐 FastAPI-based REST API
- 📊 Block explorer web interface
- 📜 Smart contract support
- 💾 Database persistence
- 🔍 UTXO model implementation
- 🔒 Enhanced security features
- ⚡ Performance optimizations

## 🛠 Technology Stack

- **Language**: Python 3.13+
- **Cryptography**: `ecdsa`, `hashlib`
- **Storage**: File-based (to be upgraded to LevelDB)
- **Future Stack**:
  - FastAPI for REST API
  - SQLAlchemy for database management
  - WebSocket for real-time updates
  - Vue.js for block explorer frontend

## 🏗 Project Structure

```
ravenchain/
├── ravenchain/              # Core package
│   ├── __init__.py
│   ├── block.py            # Block implementation
│   ├── blockchain.py       # Main blockchain logic
│   ├── transaction.py      # Transaction handling
│   └── wallet.py           # Wallet management
├── config/                  # Configuration
│   └── settings.py         # Global settings
├── tests/                  # Test suite
├── utils/                  # Utility functions
├── scripts/                # Maintenance scripts
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

OR

- Docker
- Docker Compose

### Installation

#### Using Python (Traditional Setup)

```bash
# Clone the repository
git clone https://github.com/yourusername/ravenchain.git
cd ravenchain

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

#### Using Docker 🐳

```bash
# Clone the repository
git clone https://github.com/yourusername/ravenchain.git
cd ravenchain

# Build and start the containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

The Docker setup provides:
- Isolated development environment
- Consistent dependencies across platforms
- Easy setup for future features (API, database)
- Production-ready container configuration

### Running Tests with Docker

```bash
# Run tests in a new container
docker-compose run --rm ravenchain pytest

# Run tests with coverage
docker-compose run --rm ravenchain pytest --cov=ravenchain
```

## 🎯 Roadmap

### Phase 1: Core Infrastructure Enhancement (Current)
- [x] Basic blockchain implementation
- [x] Wallet management system
- [x] Command-line interface
- [x] Transaction handling
- [ ] Unit test coverage
- [ ] Documentation improvements

### Phase 2: Data Persistence & API (Next)
- [ ] Implement LevelDB for blockchain storage
- [ ] Design and implement FastAPI REST API
  - [ ] Block endpoints
  - [ ] Transaction endpoints
  - [ ] Wallet endpoints
  - [ ] Mining endpoints
- [ ] API documentation with Swagger/OpenAPI
- [ ] Request rate limiting
- [ ] API authentication system

### Phase 3: Networking & Distribution
- [ ] P2P network implementation
  - [ ] Node discovery protocol
  - [ ] Block synchronization
  - [ ] Transaction broadcasting
- [ ] Consensus mechanism improvements
- [ ] Network state management
- [ ] Peer management system

### Phase 4: Smart Contracts & Advanced Features
- [ ] Basic smart contract engine
- [ ] Contract deployment system
- [ ] Standard contract templates
- [ ] Contract execution environment
- [ ] Gas fee implementation

### Phase 5: Performance & Security
- [ ] UTXO model implementation
- [ ] Merkle tree optimization
- [ ] Chain pruning
- [ ] Advanced security features
  - [ ] Double-spend protection
  - [ ] Sybil attack prevention
  - [ ] DDoS mitigation
- [ ] Performance benchmarking

### Phase 6: User Interface & Tools
- [ ] Block explorer web interface
- [ ] Wallet GUI application
- [ ] Network monitoring tools
- [ ] Development tools and SDKs

## 🧪 Testing

```bash
pytest tests/
```

## 📖 API Documentation (Planned)

The REST API will provide the following endpoints:

```
GET    /api/v1/blocks              # List blocks
GET    /api/v1/blocks/{hash}       # Get block details
GET    /api/v1/transactions        # List transactions
POST   /api/v1/transactions        # Create transaction
GET    /api/v1/wallets/{address}   # Get wallet info
POST   /api/v1/mine                # Mine new block
```

Detailed API documentation will be available via Swagger UI at `/docs`.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's cryptographic libraries
- Inspired by blockchain technology principles
- Community contributions and feedback

## 📞 Contact

Ray Thurman - [@raythurman2386](https://github.com/raythurman2386)

Project Link: [https://github.com/raythurman2386/ravenchain](https://github.com/raythurman2386/ravenchain)
