const { loadPlugin, PluginAPI } = require('./test_harness');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

// Setup temp env (copied from run_tests.js pattern)
const testDir = path.join(__dirname, 'temp_habit_test');
const cmdDir = path.join(testDir, 'plugin_commands');
const respDir = path.join(testDir, 'plugin_responses');

function setup() {
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
    fs.mkdirSync(cmdDir, { recursive: true });
    fs.mkdirSync(respDir, { recursive: true });
    
    PluginAPI.calls = [];
    
    const plugin = loadPlugin();
    plugin.config.mcpCommandDir = cmdDir;
    plugin.config.mcpResponseDir = respDir;
    return plugin;
}

async function test() {
    console.log('--- Exploring/Verifying Habit API Integration ---');
    const plugin = setup();

    // 1. Test addHabit
    console.log('1. Testing addHabit dispatch...');
    const addCmd = {
        action: 'addHabit',
        data: { title: 'Test Habit', streakMinValue: 1 }
    };
    // Mock the file existence for executeCommand logic
    fs.writeFileSync(path.join(cmdDir, 'add.json'), JSON.stringify(addCmd));

    await plugin.executeCommand({
        command: addCmd,
        filename: 'add.json',
        path: path.join(cmdDir, 'add.json')
    });

    const addCall = PluginAPI.calls.find(c => c.method === 'addHabit');
    if (!addCall) {
        console.error('FAIL: addHabit was not called on PluginAPI');
        // Don't exit yet, let's see other failures
    } else {
        console.log('PASS: addHabit called');
    }

    // 2. Test checkHabit
    console.log('2. Testing checkHabit dispatch...');
    const checkCmd = {
        action: 'checkHabit',
        habitId: 'HABIT_123'
    };
    fs.writeFileSync(path.join(cmdDir, 'check.json'), JSON.stringify(checkCmd));

    await plugin.executeCommand({
        command: checkCmd,
        filename: 'check.json',
        path: path.join(cmdDir, 'check.json')
    });
    
    const checkCall = PluginAPI.calls.find(c => c.method === 'checkHabit');
    if (!checkCall) {
        console.error('FAIL: checkHabit was not called on PluginAPI');
    } else {
        console.log('PASS: checkHabit called');
    }

    if (!addCall || !checkCall) {
        process.exit(1);
    }

    console.log('All Habit API tests passed!');
    
    // Cleanup
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
}

test().catch(e => {
    console.error(e);
    process.exit(1);
});
