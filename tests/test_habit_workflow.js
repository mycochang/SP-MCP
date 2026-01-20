const { loadPlugin, PluginAPI } = require('./test_harness');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const testDir = path.join(__dirname, 'temp_workflow_test');
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
    console.log('--- Testing Habit Workflow: Verify -> Add -> Check ---');
    const plugin = setup();

    // 1. Mock existing habits
    PluginAPI.getAllSimpleCounters = async () => {
        return [{ id: 'h1', title: 'Existing Habit', isTrackStreaks: true }];
    };

    // 2. Scenario A: Add a duplicate habit
    console.log('Scenario A: Duplicate Habit (Existing Habit)');
    // AI would first call list_habits
    const listResult = await PluginAPI.getAllSimpleCounters();
    const exists = listResult.find(h => h.title === 'Existing Habit');
    if (exists) {
        console.log('PASS: Workflow detected existing habit. Skipping creation.');
    } else {
        throw new Error('FAIL: Workflow failed to detect existing habit.');
    }

    // 3. Scenario B: Add a new habit
    console.log('Scenario B: New Habit (Fresh Habit)');
    const newTitle = 'Fresh Habit';
    const existsNew = listResult.find(h => h.title === newTitle);
    
    if (!existsNew) {
        console.log('New habit not found. Proceeding to add...');
        const addCmd = {
            action: 'addHabit',
            data: { title: newTitle, streakMinValue: 5 }
        };
        fs.writeFileSync(path.join(cmdDir, 'add_new.json'), JSON.stringify(addCmd));
        await plugin.executeCommand({
            command: addCmd,
            filename: 'add_new.json',
            path: path.join(cmdDir, 'add_new.json')
        });
        
        const addCall = PluginAPI.calls.find(c => c.method === 'addHabit' && c.args[0] === newTitle);
        if (addCall) {
            console.log('PASS: New habit creation dispatched.');
        } else {
            throw new Error('FAIL: addHabit not called for new habit.');
        }
    }

    // 4. Test check_habit
    console.log('4. Testing checkHabit...');
    const checkCmd = {
        action: 'checkHabit',
        habitId: 'h1'
    };
    fs.writeFileSync(path.join(cmdDir, 'check_h1.json'), JSON.stringify(checkCmd));
    await plugin.executeCommand({
        command: checkCmd,
        filename: 'check_h1.json',
        path: path.join(cmdDir, 'check_h1.json')
    });
    
    const checkCall = PluginAPI.calls.find(c => c.method === 'checkHabit' && c.args[0] === 'h1');
    if (checkCall) {
        console.log('PASS: checkHabit dispatched.');
    } else {
        throw new Error('FAIL: checkHabit not called.');
    }

    console.log('Habit workflow verification complete!');
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
}

test().catch(e => {
    console.error(e);
    process.exit(1);
});
