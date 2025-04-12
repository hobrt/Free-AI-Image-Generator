from flask import Flask, render_template, request, send_file, Response
from urllib.parse import quote
import requests
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    error = None
    prompt = None
    width = None
    height = None
    Seed = None
    
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            width = int(request.form['width'])
            height = int(request.form['height'])
            Seed = int(request.form['Seed'])
            
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
                
            encoded_prompt = quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={Seed}"
            
        except ValueError as e:
            error = f"Invalid input: {str(e)}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    
    return render_template(
        'index.html',
        image_url=image_url,
        error=error,
        prompt=prompt,
        width=width,
        height=height,
        Seed=Seed
    )

@app.route('/download')
def download_image():
    url = request.args.get('url')
    if not url:
        return "Image URL not provided", 400
    
    try:
        response = requests.get(url)
        content_type = response.headers.get('Content-Type', '')
        
        # Determine file extension from content type
        if 'jpeg' in content_type:
            ext = 'jpg'
        elif 'png' in content_type:
            ext = 'png'
        else:
            ext = 'bin'
            
        return Response(
            response.content,
            mimetype=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=image.{ext}"
            }
        )
    except Exception as e:
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)