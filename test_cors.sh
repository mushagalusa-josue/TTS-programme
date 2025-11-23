#!/bin/bash
# Test des headers CORS
echo "Testing OPTIONS request:"
curl -X OPTIONS https://tts-programme.onrender.com/tts \
  -H "Origin: https://tts-programme.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

echo -e "\n\nTesting POST request:"
curl -X POST https://tts-programme.onrender.com/tts \
  -H "Origin: https://tts-programme.vercel.app" \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}' \
  -v

