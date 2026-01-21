// Debug script to inspect raw task data
const fs = require('fs');
const path = require('path');

// This mimics the plugin's environment to inspect data
async function debugTask(taskId) {
  // In a real scenario, we'd use the PluginAPI. 
  // Since we are outside, we will instruct the user to check the "raw" data 
  // by creating a special "Debug" task that dumps its own full content.
  
  console.log("To debug Trello assignee data:");
  console.log("1. Open Super Productivity DevTools (Ctrl+Shift+I)");
  console.log("2. Go to Console");
  console.log("3. Type: `const t = this.store.select(state => state.task.ids.map(id => state.task.entities[id]).find(t => t.issueType === 'TRELLO')); console.log(t);`");
  console.log("4. Check if the logged object has `issueData` or `originalIssue` fields.");
}

console.log("Please run the DevTools check described above.");
