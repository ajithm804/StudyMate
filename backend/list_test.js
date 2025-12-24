import { readFileSync } from 'fs';

let envContent = readFileSync('.env', 'utf8');
if (envContent.charCodeAt(0) === 0xFEFF) {
  envContent = envContent.slice(1);
}

const lines = envContent.split(/\r?\n/);
let apiKey = null;

for (const line of lines) {
  const trimmedLine = line.trim();
  if (!trimmedLine) continue;
  
  const [key, ...valueParts] = trimmedLine.split('=');
  const value = valueParts.join('=').trim();
  
  if (key.trim() === 'GEMINI_API_KEY') {
    apiKey = value;
    break;
  }
}

async function testGemini2() {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${apiKey}`;
  
  const body = JSON.stringify({
    contents: [{
      parts: [{
        text: "Say 'Hello, Gemini 2.0 is working!'"
      }]
    }]
  });

  try {
    console.log("Testing Gemini 2.0 Flash...\n");
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body
    });

    const data = await response.json();

    if (response.ok) {
      console.log("✅ SUCCESS! Gemini 2.0 is working!");
      console.log("Response:", data.candidates[0].content.parts[0].text);
      console.log("\n📝 Use this model in your chatbot:");
      console.log("   Model: gemini-2.0-flash-exp");
      console.log("   API Version: v1beta");
    } else {
      console.log(`❌ Status ${response.status}:`, data.error?.message);
      
      if (response.status === 429) {
        console.log("\n⏰ Quota exceeded. Please wait 2-3 minutes and try again.");
        console.log("   Or enable billing for higher limits.");
      }
    }
    
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

testGemini2();