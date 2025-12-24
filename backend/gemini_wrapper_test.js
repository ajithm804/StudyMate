import { GoogleGenerativeAI } from "@google/generative-ai";
import { readFileSync } from 'fs';

// Read .env file manually
let envContent = readFileSync('.env', 'utf8');

// Remove BOM if present
if (envContent.charCodeAt(0) === 0xFEFF) {
  envContent = envContent.slice(1);
}

console.log("Raw .env content:");
console.log(envContent.replace(/GEMINI_API_KEY=.*/g, 'GEMINI_API_KEY=***hidden***'));
console.log("\n---\n");

// Parse manually
const lines = envContent.split(/\r?\n/);
let apiKey = null;

for (const line of lines) {
  const trimmedLine = line.trim();
  if (!trimmedLine || trimmedLine.startsWith('#')) continue;
  
  const [key, ...valueParts] = trimmedLine.split('=');
  const value = valueParts.join('=').trim();
  
  if (key.trim() === 'GEMINI_API_KEY') {
    apiKey = value;
    console.log("✅ Found API Key:", apiKey.substring(0, 10) + "...");
    break;
  }
}

async function testGemini() {
  try {
    if (!apiKey || apiKey === 'your_actual_key_here') {
      console.error("❌ GEMINI_API_KEY not set properly in .env");
      return;
    }

    console.log("\nTesting Gemini API...");
    const genAI = new GoogleGenerativeAI(apiKey);
    
    // Try different model names
    const modelNames = [
      "gemini-pro",
      "gemini-1.5-pro",
      "gemini-1.5-flash-latest"
    ];
    
    for (const modelName of modelNames) {
      try {
        console.log(`\nTrying model: ${modelName}...`);
        const model = genAI.getGenerativeModel({ model: modelName });
        
        const result = await model.generateContent("Say 'Hello, I am working!' if you can respond.");
        const response = await result.response;
        const text = response.text();

        console.log(`✅ Success with ${modelName}!`);
        console.log("Gemini Response:", text);
        console.log("\n✅ Gemini wrapper is working correctly!");
        return;
        
      } catch (error) {
        console.log(`❌ ${modelName} failed:`, error.message);
      }
    }
    
    console.error("\n❌ All models failed. Check your API key permissions.");
    
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

testGemini();