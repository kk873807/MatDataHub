# MatDataHub

**Engineering Material Properties Database** — Search, filter, and compare 500+ engineering materials.

A subscription data platform for engineers, researchers, and procurement teams.

## Features

- Searchable database of engineering materials (metals, polymers, ceramics, composites)
- Filter by category, tensile strength, cost, thermal conductivity
- Full-text search across name, grade, standard, and applications
- REST API with auto-generated documentation (Swagger UI)
- Streamlit frontend for easy browsing

## Tech Stack

| Layer | Tool |
|-------|------|
| Backend API | FastAPI |
| Database | PostgreSQL (Supabase) / SQLite (dev) |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Scraping | Scrapy + BeautifulSoup |
| Hosting | Render.com + Streamlit Cloud |

## Local Development

```bash
# 1. Clone and setup
git clone https://github.com/YOUR_USERNAME/MatDataHub.git
cd MatDataHub
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Initialize database
python init_db.py
python -m scraper.seed_data

# 3. Start API server
uvicorn app.main:app --reload

# 4. Start frontend (new terminal)
streamlit run frontend/app.py
```

- API: http://127.0.0.1:8000/docs
- Frontend: http://localhost:8501

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/v1/materials/` | List all materials (with filters) |
| GET | `/api/v1/materials/search?q=stainless` | Search by keyword |
| GET | `/api/v1/materials/{id}` | Get material by ID |
| POST | `/api/v1/materials/` | Add a new material |

## License

MIT
