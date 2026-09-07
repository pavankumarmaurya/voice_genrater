from flask import Flask, render_template, request, jsonify
import edge_tts
import asyncio
import os
import time
import sys

# Windows Event Loop Error को फिक्स करने के लिए 
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)

# ऑडियो सेव करने के लिए फोल्डर बनाना
os.makedirs('static/audio', exist_ok=True)

async def generate_audio(text, output_path):
    # 👩‍🦰 फीमेल वॉयस सेटिंग्स (SwaraNeural)
    communicate = edge_tts.Communicate(
        text=text, 
        voice="hi-IN-SwaraNeural",  # यहाँ Madhur की जगह Swara कर दिया गया है
        rate="+2%",       
        volume="+10%",    
        pitch="+0Hz"      
    )
    await communicate.save(output_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    filename = f"youtube_voice_{int(time.time())}.mp3"
    filepath = os.path.join('static', 'audio', filename)
    
    # एरर से बचने के लिए Async तरीका
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(generate_audio(text, filepath))
    finally:
        loop.close()
    
    return jsonify({'audio_url': f'/{filepath}'})

if __name__ == '__main__':
    print("👩‍🦰 फीमेल वॉयस जनरेटर तैयार है! ब्राउज़र में http://127.0.0.1:5000/ खोलें")
    app.run(debug=True)