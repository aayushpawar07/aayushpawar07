import urllib.request
import json
import os

def get_stats():
    url = "https://leetcode-api-faisalshohag.vercel.app/aayushparadkar99"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching LeetCode stats: {e}")
        return None

def generate_svg(solved, total_ques, easy, total_easy, med, total_med, hard, total_hard, rank):
    # Calculate progress bar percentages
    easy_pct = min(100, int((easy / total_easy) * 100)) if total_easy > 0 else 0
    med_pct = min(100, int((med / total_med) * 100)) if total_med > 0 else 0
    hard_pct = min(100, int((hard / total_hard) * 100)) if total_hard > 0 else 0
    total_pct = min(100, int((solved / total_ques) * 100)) if total_ques > 0 else 0
    
    # Circle calculations
    r = 28
    circ = 2 * 3.14159 * r # ~175.9
    stroke_offset = circ - (total_pct / 100) * circ
    
    svg = f"""<svg width="450" height="120" viewBox="0 0 450 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .title {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 14px; fill: #FFA116; }}
        .rank {{ font-family: 'Fira Code', monospace; font-weight: 700; font-size: 13px; fill: #FFFFFF; }}
        .rank-lbl {{ font-family: 'Inter', sans-serif; font-weight: 500; font-size: 10px; fill: #8B949E; }}
        .stat-name {{ font-family: 'Inter', sans-serif; font-weight: 600; font-size: 11px; fill: #FFFFFF; }}
        .stat-val {{ font-family: 'Fira Code', monospace; font-weight: 600; font-size: 11px; fill: #8B949E; }}
        .solved-count {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 20px; fill: #FFFFFF; }}
        .solved-lbl {{ font-family: 'Inter', sans-serif; font-weight: 500; font-size: 9px; fill: #8B949E; }}
        .border-glow {{ stroke: url(#border-grad); stroke-width: 1.5; }}
    </style>
    
    <defs>
        <linearGradient id="border-grad" x1="0" y1="0" x2="450" y2="120" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FFA116" stop-opacity="0.8"/>
            <stop offset="0.5" stop-color="#30363D" stop-opacity="0.3"/>
            <stop offset="1" stop-color="#FF6B6B" stop-opacity="0.8"/>
        </linearGradient>
        <linearGradient id="ring-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#FFA116"/>
            <stop offset="100%" stop-color="#FF6B6B"/>
        </linearGradient>
        <filter id="glow" x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
    </defs>

    <!-- Background card -->
    <rect x="1" y="1" width="448" height="118" rx="8" fill="#0D1117" class="border-glow"/>

    <!-- Left: Solved Circle Progress -->
    <g transform="translate(55, 60)">
        <!-- Underlay circle -->
        <circle r="{r}" stroke="#1F2937" stroke-width="5" fill="none" />
        <!-- Active circle -->
        <circle r="{r}" stroke="url(#ring-grad)" stroke-width="5" fill="none" 
                stroke-dasharray="{circ}" stroke-dashoffset="{stroke_offset}" 
                stroke-linecap="round" transform="rotate(-90)" />
        <!-- Solved Count Text -->
        <text x="0" y="2" text-anchor="middle" class="solved-count">{solved}</text>
        <text x="0" y="14" text-anchor="middle" class="solved-lbl">SOLVED</text>
    </g>

    <!-- Middle: Easy, Medium, Hard stats -->
    <g transform="translate(125, 14)">
        <!-- Easy Row -->
        <g transform="translate(0, 10)">
            <text x="0" y="0" class="stat-name" fill="#2cbb5d">Easy</text>
            <text x="145" y="0" class="stat-val" text-anchor="end">{easy}<tspan fill="#4B5563">/{total_easy}</tspan></text>
            <rect x="0" y="6" width="145" height="4" rx="2" fill="#1F2937" />
            <rect x="0" y="6" width="{int(145 * easy_pct / 100)}" height="4" rx="2" fill="#2cbb5d" />
        </g>
        
        <!-- Medium Row -->
        <g transform="translate(0, 36)">
            <text x="0" y="0" class="stat-name" fill="#ffb700">Medium</text>
            <text x="145" y="0" class="stat-val" text-anchor="end">{med}<tspan fill="#4B5563">/{total_med}</tspan></text>
            <rect x="0" y="6" width="145" height="4" rx="2" fill="#1F2937" />
            <rect x="0" y="6" width="{int(145 * med_pct / 100)}" height="4" rx="2" fill="#ffb700" />
        </g>
        
        <!-- Hard Row -->
        <g transform="translate(0, 62)">
            <text x="0" y="0" class="stat-name" fill="#ef4743">Hard</text>
            <text x="145" y="0" class="stat-val" text-anchor="end">{hard}<tspan fill="#4B5563">/{total_hard}</tspan></text>
            <rect x="0" y="6" width="145" height="4" rx="2" fill="#1F2937" />
            <rect x="0" y="6" width="{int(145 * hard_pct / 100)}" height="4" rx="2" fill="#ef4743" />
        </g>
    </g>

    <!-- Right Side: LeetCode Brand and Ranking -->
    <g transform="translate(295, 14)">
        <!-- Custom Leetcode Hex Logo -->
        <g transform="translate(0, 6)">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z" fill="#FFA116" opacity="0.1"/>
            <path d="M12 4.5l6.5 3.8v7.5L12 19.5l-6.5-3.8v-7.5L12 4.5z" stroke="#FFA116" stroke-width="1.5" fill="none" opacity="0.3"/>
            <path d="M8.2 12.3c-.2.2-.2.5 0 .7l2.8 2.8c.2.2.5.2.7 0l4.2-4.2c.2-.2.2-.5 0-.7l-.7-.7c-.2-.2-.5-.2-.7 0l-2.8 2.8-1.4-1.4c-.2-.2-.5-.2-.7 0l-.7.7z" fill="#FFA116" />
        </g>
        
        <g transform="translate(25, 5)">
            <text x="0" y="10" class="title">LeetCode Profile</text>
            <text x="0" y="23" class="rank-lbl">Global Ranking</text>
            <text x="0" y="38" class="rank" filter="url(#glow)">#{rank:,}</text>
            <text x="0" y="52" class="rank-lbl">Submission Streak</text>
            <text x="0" y="67" class="rank" fill="#ffb700" style="font-size:11px;">100 Days Badge 🔥</text>
        </g>
    </g>
</svg>"""
    return svg

def main():
    print("Fetching stats for aayushparadkar99...")
    stats = get_stats()
    
    if not stats:
        print("Failed to get LeetCode stats. Using fallback.")
        # Fallback values
        solved, total_ques = 377, 3935
        easy, total_easy = 295, 944
        med, total_med = 82, 2057
        hard, total_hard = 0, 934
        rank = 320819
    else:
        solved = stats.get('totalSolved', 377)
        total_ques = stats.get('totalQuestions', 3935)
        easy = stats.get('easySolved', 295)
        total_easy = stats.get('totalEasy', 944)
        med = stats.get('mediumSolved', 82)
        total_med = stats.get('totalMedium', 2057)
        hard = stats.get('hardSolved', 0)
        total_hard = stats.get('totalHard', 934)
        rank = stats.get('ranking', 320819)
        
    svg_content = generate_svg(solved, total_ques, easy, total_easy, med, total_med, hard, total_hard, rank)
    
    os.makedirs("assets/leetcode", exist_ok=True)
    output_path = "assets/leetcode/stats.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"LeetCode SVG successfully written to {output_path}")

if __name__ == "__main__":
    main()
