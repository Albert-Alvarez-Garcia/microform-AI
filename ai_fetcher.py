from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import google.generativeai as genai

class SimpleProxy(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Proxy activo y esperando...")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_data = self.rfile.read(content_length)
        post_data = json.loads(raw_data)
        
        try:
            # 1. Usamos la API Key del frontend o una fija de seguridad
            genai.configure(api_key=post_data.get('apiKey'))
            
            # 2. CAMBIO CLAVE: Usar el modelo que SÍ tiene cuota para ti
            model = genai.GenerativeModel('gemini-3.1-flash-lite')
            
            # 3. Extracción robusta del prompt
            # Asegúrate de que el frontend envíe el JSON con esta estructura
            prompt = post_data.get('contents')[0]['parts'][0]['text']
            
            print(f"Procesando prompt: {prompt}") # Debug en terminal
            
            response = model.generate_content(prompt)
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # 4. Construcción del JSON de respuesta idéntica a la estructura oficial de Gemini
            data = {"candidates": [{"content": {"parts": [{"text": response.text}]}}]}
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        except Exception as e:
            print(f"Error procesando IA: {e}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

print("Servidor listo en puerto 8000...")
HTTPServer(('localhost', 8000), SimpleProxy).serve_forever()