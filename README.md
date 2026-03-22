# ![](app/static/images/Open-RAG_ico.svg) OpenRAG Playground

A demo interface for [Open-RAG.ai](https://open-rag.ai), purpose-built for smooth, impressive client demos. Operators run demos using persona logins, each backed by a real OpenRAG API token.

**Built by [LINAGORA](https://linagora.com)** | **License: AGPL-3.0**

## Features

- **Persona-based login** — fake user profiles backed by real OpenRAG tokens
- **Streaming chat** — SSE-based token streaming with source citations
- **Partition tree** — browse partitions, view files and chunks
- **File upload** — upload documents to partitions with indexing status
- **Prompt suggestions** — type `/` to pick from pre-configured prompts
- **Admin panel** — manage groups, users, and prompts
- **i18n** — English and French, auto-detected from browser
- **Dark/Light themes**
- **GDPR compliant** — zero external requests, all assets self-hosted
- **AI Act transparency** — built-in compliance notices

## Quick Start

### Requirements

- Python 3.11+
- pip

### Install

```bash
pip install -r requirements.txt
```

### Run (development)

```bash
flask run --debug
```

Visit `http://localhost:5000`. On first run, a setup wizard will prompt you to create a master password. Then use `/admin` to configure groups, users, and prompts.

### Run (production)

```bash
FLASK_SECRET_KEY=your-secret-key docker compose up -d
```

## Configuration

All configuration is stored in `config.yaml` (gitignored). Delete it to reset and trigger the setup wizard.

```yaml
password_hash: "$2b$12$..."
groups:
  - id: legal
    label: Legal Department
    color: "#4F6EF7"
    icon: scale
demo_users:
  - id: alice-martin
    name: Alice Martin
    title: Legal Counsel
    group: legal
    genre: female
    avatar_color: "#E85D9A"
    api_url: https://demo.open-rag.ai
    token: "enc:v1:..."
demo_prompts:
  - scope: global
    prompt: Summarize the key terms from the latest contract.
```

API tokens are AES-256-GCM encrypted with a key derived from the master password.

## Tech Stack

| Layer | Choice |
|---|---|
| Runtime | Python 3.11+ |
| Web framework | Flask |
| Templates | Jinja2 |
| Interactivity | HTMX |
| Chat streaming | SSE (HTMX SSE extension) |
| Styling | Tailwind CSS |
| Icons | Lucide |
| Charts | Datatype variable font |
| Config storage | YAML |
| Password hashing | bcrypt |
| Token encryption | AES-256-GCM (cryptography) |
| HTTP client | httpx |

## Security

- Master password gate on all routes (bcrypt + session cookie)
- API tokens encrypted at rest (AES-256-GCM + PBKDF2)
- Plaintext tokens never sent to browser
- All OpenRAG API calls are server-side
- Zero external requests — all assets vendored locally
- 24h session expiry

## Project Structure

```
openrag-playground/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── auth.py              # Session middleware
│   ├── config.py            # Config path
│   ├── crypto.py            # bcrypt + AES-256-GCM
│   ├── i18n.py              # Translations EN/FR
│   ├── yaml_store.py        # Config read/write
│   ├── routes/
│   │   ├── admin.py         # Admin CRUD
│   │   ├── auth.py          # /unlock
│   │   ├── chat.py          # Chat, streaming, files
│   │   ├── demo.py          # Persona login
│   │   ├── pages.py         # Footer modals
│   │   └── setup.py         # First-run wizard
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, fonts, images
├── tests/
├── config.example.yaml
├── requirements.txt
├── pyproject.toml
└── run.py
```

## License

Copyright 2026 LINAGORA. Published under [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html).

![](app/static/images/LINAGORA.svg)