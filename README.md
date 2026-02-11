# Startup Tracker Dashboard

A daily tracker for trending and failed startups that monitors TechCrunch, Product Hunt, and startup news sources.

## Features

- **Trending Startups**: Track newly funded startups, product launches, and emerging companies
- **Failed Startups**: Monitor startup shutdowns and failures to learn from their experiences
- **Daily Updates**: Automated data refresh to keep information current
- **Responsive Design**: Modern dark-themed UI that works on all devices
- **REST API**: FastAPI backend with documented endpoints

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Data Sources**: TechCrunch, Product Hunt, startup news aggregators
- **Deployment**: Render.com (Free tier)

## API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/dashboard` - Get all dashboard data (trending + failed startups)
- `GET /api/trending` - Get trending startups only
- `GET /api/failed` - Get failed startups only
- `POST /api/refresh` - Manually trigger data refresh
- `GET /health` - Health check endpoint

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Access the dashboard
open http://localhost:8000
```

## Deployment on Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Select this repository
5. Render will automatically detect the `render.yaml` configuration
6. Deploy!

The app will be available at: `https://startup-tracker-<random>.onrender.com`

## Data Sources

- **TechCrunch**: Funding announcements and startup news
- **Product Hunt**: New product launches and trending startups
- **Twitter/X**: Startup community discussions and announcements
- **Crunchbase**: Funding rounds and company data
- **Autopsy.io**: Failed startup case studies

## Automation

The dashboard includes built-in data refresh capabilities:
- Manual refresh via `/api/refresh` endpoint
- Can be automated with cron jobs or scheduled tasks
- Daily updates recommended for fresh data

## License

MIT License - feel free to use and modify!

## Author

Gaurav Rodrigues

---

**Note**: This tracker uses publicly available data sources. For production use, consider implementing proper API integrations with rate limiting and caching.