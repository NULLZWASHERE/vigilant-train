import json
from http.server import BaseHTTPRequestHandler
from openai import OpenAI

# Hardcoded API key as requested
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))
        
        # Standard completion call
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            messages=body['messages'],
            stream=False,
            extra_body={"chat_template_kwargs":{"enable_thinking":True}}
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "content": completion.choices[0].message.content,
            "reasoning": getattr(completion.choices[0].message, "reasoning_content", None)
        }
        self.wfile.write(json.dumps(response).encode())
