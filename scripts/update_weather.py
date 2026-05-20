import urllib.request
import json
import os
from datetime import datetime, timedelta

def get_weather():
    url = "https://wttr.in/Bhopal?format=j1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def select_icon(desc):
    desc = desc.lower()
    if any(word in desc for word in ["thunder", "storm"]):
        return """
        <g transform="translate(45, 60)">
            <path d="M-12,8 a10,10 0 0,1 10,-10 a12,12 0 0,1 22,2 a8,8 0 0,1 2,16 a8,8 0 0,1 -8,8 l-20,0 a10,10 0 0,1 -6,-16 z" fill="#37474F" fill-opacity="0.4" stroke="#455A64" stroke-width="2" stroke-linejoin="round"/>
            <polygon points="2,12 -4,22 1,22 -2,30 6,18 1,18" fill="#FFD54F" stroke="#FFCA28" stroke-width="1"/>
        </g>
        """
    elif any(word in desc for word in ["rain", "drizzle", "shower"]):
        return """
        <g transform="translate(45, 60)">
            <path d="M-12,8 a10,10 0 0,1 10,-10 a12,12 0 0,1 22,2 a8,8 0 0,1 2,16 a8,8 0 0,1 -8,8 l-20,0 a10,10 0 0,1 -6,-16 z" fill="#78909C" fill-opacity="0.4" stroke="#90A4AE" stroke-width="2" stroke-linejoin="round"/>
            <g stroke="#64B5F6" stroke-width="2.5" stroke-linecap="round">
                <line x1="-5" y1="16" x2="-9" y2="24" />
                <line x1="5" y1="16" x2="1" y2="24" />
                <line x1="15" y1="16" x2="11" y2="24" />
            </g>
        </g>
        """
    elif any(word in desc for word in ["snow", "ice", "hail"]):
        return """
        <g transform="translate(45, 60)">
            <path d="M-12,8 a10,10 0 0,1 10,-10 a12,12 0 0,1 22,2 a8,8 0 0,1 2,16 a8,8 0 0,1 -8,8 l-20,0 a10,10 0 0,1 -6,-16 z" fill="#E0F7FA" fill-opacity="0.4" stroke="#B2EBF2" stroke-width="2" stroke-linejoin="round"/>
            <g fill="#E0F7FA">
                <circle cx="-5" cy="20" r="1.5" />
                <circle cx="5" cy="22" r="1.5" />
                <circle cx="15" cy="20" r="1.5" />
            </g>
        </g>
        """
    elif any(word in desc for word in ["cloud", "overcast"]):
        return """
        <g transform="translate(45, 60)">
            <path d="M-12,8 a10,10 0 0,1 10,-10 a12,12 0 0,1 22,2 a8,8 0 0,1 2,16 a8,8 0 0,1 -8,8 l-20,0 a10,10 0 0,1 -6,-16 z" fill="#B0BEC5" fill-opacity="0.4" stroke="#ECEFF1" stroke-width="2" stroke-linejoin="round"/>
        </g>
        """
    elif any(word in desc for word in ["fog", "mist", "haze"]):
        return """
        <g transform="translate(45, 65)" stroke="#B0BEC5" stroke-width="3" stroke-linecap="round" stroke-opacity="0.8">
            <line x1="-20" y1="-8" x2="20" y2="-8" />
            <line x1="-25" y1="0" x2="25" y2="0" />
            <line x1="-15" y1="8" x2="15" y2="8" />
        </g>
        """
    else:  # Sunny / Clear / default
        return """
        <g transform="translate(45, 60)" stroke="#FFB000" stroke-width="2.5" stroke-linecap="round">
            <circle cx="0" cy="0" r="14" fill="#FFE082" fill-opacity="0.3" stroke="#FFA000" stroke-width="3"/>
            <line x1="0" y1="-20" x2="0" y2="-25" />
            <line x1="0" y1="20" x2="0" y2="25" />
            <line x1="-20" y1="0" x2="-25" y2="0" />
            <line x1="20" y1="0" x2="25" y2="0" />
            <line x1="-14" y1="-14" x2="-18" y2="-18" />
            <line x1="14" y1="14" x2="18" y2="18" />
            <line x1="-14" y1="14" x2="-18" y2="18" />
            <line x1="14" y1="-14" x2="18" y2="-18" />
        </g>
        """

def generate_svg(temp, feels_like, humidity, wind, desc, time_str, date_str):
    icon_svg = select_icon(desc)
    
    svg = f"""<svg width="450" height="120" viewBox="0 0 450 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .title {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 15px; fill: #6C63FF; }}
        .location {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 500; font-size: 12px; fill: #8B949E; }}
        .temp {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; font-size: 32px; fill: #FFFFFF; }}
        .feels-like {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 400; font-size: 11px; fill: #8B949E; }}
        .desc {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 600; font-size: 12px; fill: #FF6B6B; }}
        .stat-lbl {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 500; font-size: 11px; fill: #8B949E; }}
        .stat-val {{ font-family: 'Fira Code', monospace; font-weight: 600; font-size: 11px; fill: #FFFFFF; }}
        .time-label {{ font-family: 'Fira Code', monospace; font-weight: 700; font-size: 13px; fill: #22c55e; }}
        .border-glow {{ stroke: url(#border-grad); stroke-width: 1.5; }}
    </style>
    
    <defs>
        <linearGradient id="border-grad" x1="0" y1="0" x2="450" y2="120" gradientUnits="userSpaceOnUse">
            <stop stop-color="#6C63FF" stop-opacity="0.8"/>
            <stop offset="0.5" stop-color="#30363D" stop-opacity="0.3"/>
            <stop offset="1" stop-color="#FF6B6B" stop-opacity="0.8"/>
        </linearGradient>
        <filter id="glow" x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
    </defs>

    <!-- Background card -->
    <rect x="1" y="1" width="448" height="118" rx="8" fill="#0D1117" class="border-glow"/>

    <!-- Left: Weather Icon -->
    {icon_svg}

    <!-- Middle: Temp and Description -->
    <g transform="translate(100, 0)">
        <text x="0" y="55" class="temp">{temp}°C</text>
        <text x="0" y="74" class="feels-like">Feels like {feels_like}°C</text>
        <text x="0" y="96" class="desc">{desc}</text>
    </g>

    <!-- Right: Stats & Local Info -->
    <g transform="translate(255, 0)">
        <text x="0" y="32" class="title">Bhopal, India</text>
        <text x="0" y="48" class="location">Local Time &amp; Date</text>
        <text x="0" y="68" class="time-label" filter="url(#glow)">{time_str} IST</text>
        <text x="0" y="86" class="location" font-size="10">{date_str}</text>
    </g>

    <!-- Far Right Statistics -->
    <g transform="translate(370, 48)">
        <text x="0" y="0" class="stat-lbl">💧 Humidity</text>
        <text x="0" y="15" class="stat-val">{humidity}%</text>
        
        <text x="0" y="35" class="stat-lbl">💨 Wind</text>
        <text x="0" y="50" class="stat-val">{wind} km/h</text>
    </g>
</svg>"""
    return svg

def main():
    print("Fetching weather for Bhopal...")
    data = get_weather()
    
    if not data:
        print("Failed to get weather data. Writing fallback SVG.")
        # Fallback values
        temp, feels_like, humidity, wind, desc = "28", "28", "45", "10", "Clear", "12:00 PM", "Bhopal, India"
    else:
        current = data['current_condition'][0]
        temp = current['temp_C']
        feels_like = current['FeelsLikeC']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        desc = current['weatherDesc'][0]['value'].strip()
    
    # Calculate IST time
    utc_time = datetime.utcnow()
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    time_str = ist_time.strftime("%I:%M %p")
    date_str = ist_time.strftime("%d %b %Y")
    
    svg_content = generate_svg(temp, feels_like, humidity, wind, desc, time_str, date_str)
    
    # Ensure directories exist
    os.makedirs("assets/weather", exist_ok=True)
    
    output_path = "assets/weather/bhopal.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Weather SVG successfully written to {output_path}")

if __name__ == "__main__":
    main()
