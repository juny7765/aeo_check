import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def analyze_aeo(url):
    """
    Analyze a given URL for Answer Engine Optimization (AEO) readiness.
    Evaluates 10 criteria, each worth 10 points. Total 100 points.
    """
    
    # Prepend http if missing
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Fetch Main Page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        parsed_url = urlparse(url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        results = []
        score = 0
        
        # 1. Structure Data (JSON-LD)
        json_ld = soup.find("script", {"type": "application/ld+json"})
        if json_ld:
            score += 10
            results.append({"title": "Structured Data (JSON-LD)", "status": "Pass", "icon": "✅", "desc": "Found. AI understands this content."})
        else:
            results.append({"title": "Structured Data (JSON-LD)", "status": "Fail", "icon": "❌", "desc": "Missing. Critical for AI understanding."})

        # 2. Meta Description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            score += 10
            results.append({"title": "Meta Description", "status": "Pass", "icon": "✅", "desc": "Good summary provided."})
        else:
            results.append({"title": "Meta Description", "status": "Fail", "icon": "❌", "desc": "Missing description."})

        # 3. Open Graph (Social/AI Context)
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title:
             score += 10
             results.append({"title": "Open Graph Tags", "status": "Pass", "icon": "✅", "desc": "Social context present."})
        else:
             results.append({"title": "Open Graph Tags", "status": "Fail", "icon": "❌", "desc": "Missing OpenGraph tags."})

        # 4. Header Hierarchy (H1/H2)
        h1 = soup.find_all("h1")
        h2 = soup.find_all("h2")
        if h1 and h2:
             score += 10
             results.append({"title": "Header Hierarchy (H1/H2)", "status": "Pass", "icon": "✅", "desc": "Clear content structure."})
        else:
             results.append({"title": "Header Hierarchy (H1/H2)", "status": "Fail", "icon": "❌", "desc": "Missing H1 or H2 tags."})

        # 5. Content Volume (> 500 chars)
        # Using characters as a proxy for words for simplicity in non-English
        text_content = soup.get_text()
        if len(text_content) > 500:
            score += 10
            results.append({"title": "Content Volume", "status": "Pass", "icon": "✅", "desc": "Sufficient content depth."})
        else:
            results.append({"title": "Content Volume", "status": "Fail", "icon": "⚠️", "desc": "Too thin. Add more text."})

        # 6. Internal Links
        links = soup.find_all("a", href=True)
        internal_links = [l for l in links if base_domain in urljoin(url, l['href'])]
        if len(internal_links) > 3:
            score += 10
            results.append({"title": "Internal Linking", "status": "Pass", "icon": "✅", "desc": "Good internal connectivity."})
        else:
             results.append({"title": "Internal Linking", "status": "Fail", "icon": "⚠️", "desc": "Few internal links found."})

        # 7. Image Alt Text
        images = soup.find_all("img")
        images_with_alt = [img for img in images if img.get("alt")]
        if images and (len(images_with_alt) / len(images) > 0.5):
             score += 10
             results.append({"title": "Image Alt Text", "status": "Pass", "icon": "✅", "desc": "Images have descriptions."})
        elif not images: # Pass if no images
             score += 10
             results.append({"title": "Image Alt Text", "status": "Pass", "icon": "✅", "desc": "No images to check."})
        else:
             results.append({"title": "Image Alt Text", "status": "Fail", "icon": "❌", "desc": "Many images missing Alt text."})

        # 8. Mobile Viewport
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if viewport:
            score += 10
            results.append({"title": "Mobile Friendly", "status": "Pass", "icon": "✅", "desc": "Mobile viewport tag found."})
        else:
            results.append({"title": "Mobile Friendly", "status": "Fail", "icon": "❌", "desc": "Not optimized for mobile."})

        # 9. Robots.txt
        robots_url = urljoin(base_domain, "/robots.txt")
        try:
            r_resp = requests.get(robots_url, headers=headers, timeout=5)
            if r_resp.status_code == 200:
                score += 10
                results.append({"title": "Robots.txt", "status": "Pass", "icon": "✅", "desc": "Crawling policy found."})
            else:
                results.append({"title": "Robots.txt", "status": "Fail", "icon": "⚠️", "desc": "Robots.txt unreachable."})
        except:
             results.append({"title": "Robots.txt", "status": "Fail", "icon": "⚠️", "desc": "Check failed."})

        # 10. Sitemap.xml
        # Simple check: try specific path or check robots.txt (simplified here to try common path)
        sitemap_url = urljoin(base_domain, "/sitemap.xml")
        try:
            s_resp = requests.get(sitemap_url, headers=headers, timeout=5)
            if s_resp.status_code == 200:
                score += 10
                results.append({"title": "Sitemap.xml", "status": "Pass", "icon": "✅", "desc": "Sitemap found."})
            else:
                 # Check if robots.txt mentions sitemap? (Skip for MVP complexity)
                 results.append({"title": "Sitemap.xml", "status": "Fail", "icon": "⚠️", "desc": "Sitemap not found at root."})
        except:
            results.append({"title": "Sitemap.xml", "status": "Fail", "icon": "⚠️", "desc": "Check failed."})


        return {
            "score": score,
            "url": url,
            "results": results
        }

    except Exception as e:
        return {
            "score": 0,
            "url": url,
            "error": str(e),
            "results": [{"title": "Analysis Failed", "status": "Fail", "icon": "❌", "desc": str(e)}]
        }

if __name__ == "__main__":
    # Internal Test
    test_url = "https://www.apple.com"
    print(f"Testing {test_url}...")
    # print(analyze_aeo(test_url))
