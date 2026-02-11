# Startup Tracker Dashboard

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

A daily tracker for trending and failed startups that monitors TechCrunch, Product Hunt, and startup news sources.

🔗 **Live Demo**: [Coming Soon]
📚 **[Automation Setup Guide](AUTOMATION-SETUP.md)** - Set up daily automated data refresh

## Features

- ✅ **Trending Startups**: Track newly funded startups, product launches, and emerging companies
- ✅ **Failed Startups**: Monitor startup shutdowns and failures to learn from their experiences
- ✅ **Daily Updates**: Automated data refresh to keep information current
- ✅ **Responsive Design**: Modern dark-themed UI that works on all devices
- ✅ **REST API**: FastAPI backend with documented endpoints
- ✅ **GitHub Actions Ready**: Automated workflows included

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Data Sources**: TechCrunch, Product Hunt, startup news aggregators
- **Deployment**: Render.com (Free tier compatible)
- **Automation**: GitHub Actions / Cron jobs

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/gauravrodrigues/startup-tracker.git
cd startup-tracker

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Access the dashboard
open http://localhost:8000
```

## API Endpoints

- `GET /` - Dashboard homepage with live UI
- `GET /api/dashboard` - Get all dashboard data (trending + failed startups)
- `GET /api/trending` - Get trending startups only
- `GET /api/failed` - Get failed startups only
- `POST /api/refresh` - Manually trigger data refresh
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (FastAPI Swagger UI)

## Deployment

### Option 1: Deploy to Render (Recommended)

1. **Fork this repository** to your GitHub account

2. **Sign up at [Render.com](https://render.com)** and connect your GitHub account

3. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Select this repository
   - Name: `startup-tracker`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy!** - Render will automatically deploy your app

5. **Set up automation** - Follow the [Automation Setup Guide](AUTOMATION-SETUP.md)

Your app will be available at: `https://startup-tracker-<random>.onrender.com`

### Option 2: Deploy to Other Platforms

The app is compatible with:
- **Railway**: One-click deploy with `railway up`
- **Fly.io**: Deploy with `flyctl launch`
- **Heroku**: Use the included `render.yaml` as reference for Procfile
- **DigitalOcean App Platform**: Connect repo and deploy

## Automation Setup

See the comprehensive **[Automation Setup Guide](AUTOMATION-SETUP.md)** for:
- ✅ GitHub Actions daily refresh workflow
- ✅ Render cron jobs configuration
- ✅ External cron service integration
- ✅ Troubleshooting and monitoring

## Data Sources

### Trending Startups
- **TechCrunch**: Funding announcements and startup news
- **Product Hunt**: New product launches and trending startups
- **Twitter/X**: Startup community discussions and announcements
- **Crunchbase**: Funding rounds and company data

### Failed Startups
- **Autopsy.io**: Failed startup case studies
- **FailCon**: Startup failure analysis
- **Startup Graveyard**: Shutdown announcements
- **Twitter/X**: Real-time shutdown announcements

## Project Structure

```
startup-tracker/
├── main.py                 # FastAPI backend with all endpoints
├── index.html              # Frontend dashboard UI
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── python-version.txt     # Python version specification
├── AUTOMATION-SETUP.md    # Automation configuration guide
└── README.md              # This file
```

## Development Roadmap

- [x] Basic dashboard with trending/failed sections
- [x] REST API with FastAPI
- [x] Responsive dark-themed UI
- [x] Deployment configuration
- [x] Automation setup guide
- [ ] Real-time data source integrations
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication
- [ ] Saved searches and alerts
- [ ] Export to CSV/JSON
- [ ] Analytics dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - feel free to use and modify!

## Author

**Gaurav Rodrigues**
- GitHub: [@gauravrodrigues](https://github.com/gauravrodrigues)

## Acknowledgments

- Data sources: TechCrunch, Product Hunt, Crunchbase, and the startup community
- Inspiration: The need to track both successful and failed startups for learning

---

⭐ **Star this repo** if you find it useful!

**Note**: This tracker uses publicly available data sources. For production use with high traffic, consider implementing proper API integrations with authentication, rate limiting, and caching.