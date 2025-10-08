// Simple test to check if imports work
console.log("Testing imports...");

try {
  const React = require('react');
  console.log("✅ React import OK");
} catch (e) {
  console.log("❌ React import failed:", e.message);
}

try {
  const ReactDOM = require('react-dom/client');
  console.log("✅ ReactDOM import OK");
} catch (e) {
  console.log("❌ ReactDOM import failed:", e.message);
}

try {
  const App = require('./src/App.tsx');
  console.log("✅ App import OK");
} catch (e) {
  console.log("❌ App import failed:", e.message);
}

console.log("Import test complete.");
