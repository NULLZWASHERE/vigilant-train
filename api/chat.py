import os
from http.server import BaseHTTPRequestHandler
from openai import OpenAI
import json

# Initialize client outside the handler for connection pooling
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Expecting a list of messages from the frontend
        messages = data.get("messages", [])

        try:
            completion = client.chat.completions.create(
                model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
                messages=messages,
                temperature=0.6,
                extra_body={
                    "chat_template_kwargs": {"enable_thinking": True},
                    "reasoning_budget": 16384
                }
            )
            
            response_data = {
                "content": completion.choices[0].message.content,
                "reasoning": getattr(completion.choices[0].message, "reasoning_content", None)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))
