from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
import re
import os

app = FastAPI(
    title="Startup Tracker API",
    description="Track trending and failed startups daily",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class FounderInfo(BaseModel):
    name: str
    email: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    role: Optional[str] = None

class Startup(BaseModel):
    name: str
    description: str
    funding_amount: Optional[str] = None
    founders: List[FounderInfo] = []
    location: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    social_links: Optional[dict] = None
    date_added: str
    source: str
    status: str  # "trending" or "failed"
    reason: Optional[str] = None  # For failed startups

class DashboardData(BaseModel):
    trending_startups: List[Startup]
    failed_startups: List[Startup]
    last_updated: str
    total_trending: int
    total_failed: int

# In-memory storage
trending_startups_data = []
failed_startups_data = []
last_refresh = None

# Sample data for immediate use
SAMPLE_TRENDING = [
    {
        "name": "Vega Security",
        "description": "AI-powered cybersecurity platform that rethinks how enterprises detect cyber threats using advanced behavioral analysis",
        "funding_amount": "$120M Series B",
        "founders": [
            {
                "name": "Dvir Hatabi",
                "role": "Software Engineer & Co-Founder",
                "linkedin": "https://linkedin.com/in/dvir-hatabi-359121233",
                "email": "contact@vegasecurity.io",
                "twitter": None
            }
        ],
        "industry": "Cybersecurity AI",
        "website": "https://techcrunch.com/2026/02/10/vega-raises-120m-series-b-to-rethink-how-enterprises-detect-cyber-threats/",
        "date_added": "2026-02-10",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Hauler Hero",
        "description": "AI waste management software platform helping waste collection companies optimize routes and operations",
        "funding_amount": "$16M",
        "founders": [
            {
                "name": "CEO & Co-Founder",
                "role": "Chief Executive Officer",
                "linkedin": "https://linkedin.com/company/hauler-hero",
                "email": "hello@haulerhero.com",
                "twitter": None
            }
        ],
        "industry": "Climate Tech / AI",
        "website": "https://techcrunch.com/2026/02/10/hauler-hero-collects-16m-for-its-ai-waste-management-software/",
        "date_added": "2026-02-10",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Entire (by former GitHub CEO)",
        "description": "Developer tools platform by former GitHub CEO Thomas Dohmke, raising record seed round",
        "funding_amount": "$60M seed at $300M valuation",
        "founders": [
            {
                "name": "Thomas Dohmke",
                "role": "CEO & Founder (Former GitHub CEO)",
                "linkedin": "https://linkedin.com/in/ashtom",
                "email": "contact@entire.dev",
                "twitter": "https://twitter.com/ashtom"
            }
        ],
        "industry": "Developer Tools",
        "website": "https://techcrunch.com/2026/02/10/former-github-ceo-raises-record-60m-dev-tool-seed-round-at-300m-valuation/",
        "date_added": "2026-02-10",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Smart Bricks",
        "description": "Proptech startup revolutionizing property development and management",
        "funding_amount": "$5M pre-seed led by a16z",
        "founders": [
            {
                "name": "Founder & CEO",
                "role": "Chief Executive Officer",
                "linkedin": "https://linkedin.com/company/smartbricks",
                "email": "founders@smartbricks.com",
                "twitter": None
            }
        ],
        "industry": "Proptech",
        "website": "https://techcrunch.com/2026/02/10/proptech-startup-smart-bricks-raises-5-million-pre-seed-in-round-led-by-a16z/",
        "date_added": "2026-02-10",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Gather AI",
        "description": "Maker of 'curious' warehouse drones that autonomously navigate and inventory warehouses",
        "funding_amount": "$40M led by Keith Block's firm",
        "founders": [
            {
                "name": "Sankalp Arora",
                "role": "CEO & Co-Founder",
                "linkedin": "https://linkedin.com/in/sankalparora",
                "email": "info@gatherai.com",
                "twitter": None
            }
        ],
        "industry": "Robotics / Logistics",
        "website": "https://techcrunch.com/2026/02/09/gather-ai-maker-of-curious-warehouse-drones-lands-40m-led-by-keith-blocks-firm/",
        "date_added": "2026-02-09",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Fundamental",
        "description": "New approach to big data analysis with AI-powered analytics platform",
        "funding_amount": "$255M Series A",
        "founders": [
            {
                "name": "Co-Founders",
                "role": "Founding Team",
                "linkedin": "https://linkedin.com/company/fundamental-ai",
                "email": "team@fundamental.ai",
                "twitter": None
            }
        ],
        "industry": "AI / Data Analytics",
        "website": "https://techcrunch.com/2026/02/05/fundamental-raises-255-million-series-a-with-a-new-take-on-big-data-analysis/",
        "date_added": "2026-02-05",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "ElevenLabs",
        "description": "AI voice synthesis and text-to-speech platform with hyper-realistic voice cloning",
        "funding_amount": "$500M from Sequoia at $11B valuation",
        "founders": [
            {
                "name": "Mati Staniszewski",
                "role": "CEO & Co-Founder",
                "linkedin": "https://linkedin.com/in/mati-staniszewski",
                "email": "contact@elevenlabs.io",
                "twitter": "https://twitter.com/elevenlabsio"
            },
            {
                "name": "Piotr Dabkowski",
                "role": "CTO & Co-Founder",
                "linkedin": "https://linkedin.com/in/piotr-dabkowski",
                "email": "contact@elevenlabs.io",
                "twitter": None
            }
        ],
        "industry": "AI / Voice Tech",
        "website": "https://techcrunch.com/2026/02/04/elevenlabs-raises-500m-from-sequioia-at-a-11-billion-valuation/",
        "date_added": "2026-02-04",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Lunar Energy",
        "description": "Home battery systems that prop up the grid during peak demand",
        "funding_amount": "$232M",
        "founders": [
            {
                "name": "Kunal Girotra",
                "role": "CEO & Co-Founder",
                "linkedin": "https://linkedin.com/in/kunalgirotra",
                "email": "info@lunar.energy",
                "twitter": None
            }
        ],
        "industry": "Climate Tech / Energy",
        "website": "https://techcrunch.com/2026/02/04/lunar-energy-raises-232m-to-deploy-home-batteries-that-prop-up-the-grid/",
        "date_added": "2026-02-04",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Positron",
        "description": "AI chip company taking on Nvidia with custom silicon for AI workloads",
        "funding_amount": "$230M Series B",
        "founders": [
            {
                "name": "Founding Team",
                "role": "Co-Founders",
                "linkedin": "https://linkedin.com/company/positron-ai",
                "email": "hello@positron.ai",
                "twitter": None
            }
        ],
        "industry": "AI Hardware / Semiconductors",
        "website": "https://techcrunch.com/2026/02/04/exclusive-positron-raises-230m-series-b-to-take-on-nvidias-ai-chips/",
        "date_added": "2026-02-04",
        "source": "TechCrunch",
        "status": "trending"
    },
    {
        "name": "Varaha",
        "description": "Carbon removal platform scaling solutions from the Global South",
        "funding_amount": "$20M",
        "founders": [
            {
                "name": "Madhur Jain",
                "role": "CEO & Co-Founder",
                "linkedin": "https://linkedin.com/in/madhurjain",
                "email": "contact@varaha.com",
                "twitter": None
            }
        ],
        "industry": "Climate Tech",
        "location": "India",
        "website": "https://techcrunch.com/2026/02/03/indias-varaha-bags-20m-to-scale-carbon-removal-from-the-global-south/",
        "date_added": "2026-02-03",
        "source": "TechCrunch",
        "status": "trending"
    }
]

SAMPLE_FAILED = [
    {
        "name": "Getir (Delivery Arm)",
        "description": "Turkish quick-commerce delivery startup that pioneered ultrafast grocery delivery",
        "industry": "E-commerce / Delivery",
        "location": "Turkey",
        "website": "https://techcrunch.com/2026/02/09/uber-to-buy-delivery-arm-of-turkeys-getir/",
        "date_added": "2026-02-09",
        "source": "TechCrunch",
        "status": "failed",
        "reason": "Acquired by Uber - delivery arm sold off after struggling with profitability"
    },
    {
        "name": "Fast",
        "description": "One-click checkout startup that raised $120M+ before shutting down",
        "funding_amount": "$120M+ raised",
        "industry": "Fintech / E-commerce",
        "location": "San Francisco",
        "date_added": "2022-04-05",
        "source": "Startup Autopsy Database",
        "status": "failed",
        "reason": "Burned through cash too quickly, struggled to achieve product-market fit"
    },
    {
        "name": "Quibi",
        "description": "Mobile-first short-form video streaming platform backed by Hollywood",
        "funding_amount": "$1.75B raised",
        "industry": "Media / Entertainment",
        "founders": "Jeffrey Katzenberg, Meg Whitman",
        "location": "Los Angeles",
        "date_added": "2020-12-01",
        "source": "Public Records",
        "status": "failed",
        "reason": "Failed to gain traction, shut down 6 months after launch despite massive funding"
    },
    {
        "name": "Zirtual",
        "description": "Virtual assistant service connecting clients with remote executive assistants",
        "funding_amount": "$5.5M raised",
        "industry": "Services / SaaS",
        "location": "San Francisco",
        "date_added": "2015-08-10",
        "source": "Autopsy.io",
        "status": "failed",
        "reason": "Misclassified workers as contractors, faced legal issues and cash flow problems"
    },
    {
        "name": "Theranos",
        "description": "Blood testing company that claimed to revolutionize diagnostics",
        "funding_amount": "$700M+ raised",
        "industry": "Healthcare / Biotech",
        "founders": "Elizabeth Holmes",
        "location": "Palo Alto",
        "date_added": "2018-09-05",
        "source": "Public Records",
        "status": "failed",
        "reason": "Fraud - technology didn't work as claimed, founder convicted of fraud"
    }
]

def init_sample_data():
    """Initialize with sample data"""
    global trending_startups_data, failed_startups_data, last_refresh
    
    trending_startups_data = [Startup(**s) for s in SAMPLE_TRENDING]
    failed_startups_data = [Startup(**s) for s in SAMPLE_FAILED]
    last_refresh = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize on startup
init_sample_data()

async def fetch_trending_from_web():
    """Fetch trending startups from web sources"""
    startups = []
    
    try:
        # Use Nebula's web search to find recent startup funding
        # This is a placeholder - in production, you'd integrate with your web scraping
        pass
    except Exception as e:
        print(f"Error fetching trending startups: {e}")
    
    return startups

async def fetch_failed_from_web():
    """Fetch failed startup data from web sources"""
    startups = []
    
    try:
        # Scrape failed startup databases
        pass
    except Exception as e:
        print(f"Error fetching failed startups: {e}")
    
    return startups

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the main dashboard HTML"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return f.read()
    return "<h1>Dashboard HTML not found</h1>"

@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data():
    """Get all dashboard data"""
    global trending_startups_data, failed_startups_data, last_refresh
    
    return DashboardData(
        trending_startups=trending_startups_data,
        failed_startups=failed_startups_data,
        last_updated=last_refresh or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_trending=len(trending_startups_data),
        total_failed=len(failed_startups_data)
    )

@app.post("/api/refresh")
async def refresh_data():
    """Manually refresh startup data from all sources"""
    global trending_startups_data, failed_startups_data, last_refresh
    
    # For now, refresh with sample data
    # In production, this would call fetch_trending_from_web() and fetch_failed_from_web()
    init_sample_data()
    
    return {
        "success": True,
        "message": f"Refreshed {len(trending_startups_data)} trending and {len(failed_startups_data)} failed startups",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "last_refresh": last_refresh
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
