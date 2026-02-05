const { loadPlugin, PluginAPI } = require('./test_harness');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

// Setup temporary test directories
const testDir = path.join(__dirname, 'temp_test_env');
const mcpDir = path.join(testDir, 'mcp');
const cmdDir = path.join(mcpDir, 'plugin_commands');
const respDir = path.join(mcpDir, 'plugin_responses');

// Helper to reset env
function setupEnv() {
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
    fs.mkdirSync(cmdDir, { recursive: true });
    fs.mkdirSync(respDir, { recursive: true });
    
    // Reset calls
    PluginAPI.calls = [];
    
    const plugin = loadPlugin();
    plugin.config.mcpCommandDir = cmdDir;
    plugin.config.mcpResponseDir = respDir;
    
    return plugin;
}

async function runTests() {
    console.log('🚀 Starting Node.js Tests...');
    let passed = 0;
    let failed = 0;

    // --- TEST 1: Path Traversal Security Check ---
    try {
        console.log('\n🧪 TEST 1: Path Traversal Security Check');
        const plugin = setupEnv();
        const maliciousId = '../../evil_file';
        
        await plugin.writeCommandResponse(maliciousId, { secret: 'data' });
        
        const evilFile = path.join(mcpDir, 'evil_file_response.json');
        const safeFile = path.join(respDir, 'evil_file_response.json');
        
        if (fs.existsSync(evilFile)) {
            throw new Error('Path Traversal Vulnerability exists! File written outside directory.');
        } 
        if (!fs.existsSync(safeFile)) {
            throw new Error('File was not written to safe location (or sanitization failed unexpectedly).');
        }
        console.log('✅ PASS');
        passed++;
    } catch (e) {
        console.error('❌ FAIL:', e.message);
        failed++;
    }

    // --- TEST 2: Feature - Delete Tag (TDD) ---
    try {
        console.log('\n🧪 TEST 2: Delete Tag Feature Check');
        const plugin = setupEnv();
        const deleteCommand = {
            action: 'deleteTag',
            tagId: 'MY_TAG_ID'
        };
        const cmdInfo = {
            command: deleteCommand,
            filename: 'test_cmd.json',
            path: path.join(cmdDir, 'test_cmd.json')
        };
        // Mock file existence
        fs.writeFileSync(cmdInfo.path, JSON.stringify(deleteCommand));
        
        await plugin.executeCommand(cmdInfo);
        
        const call = PluginAPI.calls.find(c => c.method === 'deleteTag');
        if (!call) {
            throw new Error('PluginAPI.deleteTag was NOT called.');
        }
        if (call.args[0] !== 'MY_TAG_ID') {
            throw new Error(`Called with wrong ID: ${call.args[0]}`);
        }
        
        console.log('✅ PASS');
        passed++;
    } catch(e) {
        console.error('❌ FAIL:', e.message);
        failed++; // We expect this to fail now
    }

    // --- TEST 3: Feature - Update Tag (TDD) ---
    try {
        console.log('\n🧪 TEST 3: Update Tag Feature Check');
        const plugin = setupEnv();
        const updateCommand = {
            action: 'updateTag',
            tagId: 'TAG_123',
            data: { title: 'New Title', theme: { primary: '#ff0000' } }
        };
        const cmdInfo = {
            command: updateCommand,
            filename: 'update_cmd.json',
            path: path.join(cmdDir, 'update_cmd.json')
        };
        fs.writeFileSync(cmdInfo.path, JSON.stringify(updateCommand));
        
        await plugin.executeCommand(cmdInfo);
        
        const call = PluginAPI.calls.find(c => c.method === 'updateTag');
        if (!call) throw new Error('PluginAPI.updateTag was NOT called.');
        if (call.args[0] !== 'TAG_123') throw new Error(`Wrong ID: ${call.args[0]}`);
        if (call.args[1].title !== 'New Title') throw new Error(`Wrong Data: ${JSON.stringify(call.args[1])}`);
        
        console.log('✅ PASS');
        passed++;
    } catch(e) {
        console.error('❌ FAIL:', e.message);
        failed++;
    }

    // --- TEST 4: Feature - Create Board (TDD) ---
    try {
        console.log('\n🧪 TEST 4: Create Board Feature Check');
        const plugin = setupEnv();
        const boardCommand = {
            action: 'addBoard',
            data: { title: 'New Board', cols: 3, panels: [] }
        };
        const cmdInfo = {
            command: boardCommand,
            filename: 'board_cmd.json',
            path: path.join(cmdDir, 'board_cmd.json')
        };
        fs.writeFileSync(cmdInfo.path, JSON.stringify(boardCommand));
        
        await plugin.executeCommand(cmdInfo);
        
        const call = PluginAPI.calls.find(c => c.method === 'dispatchAction');
        if (!call) throw new Error('PluginAPI.dispatchAction was NOT called.');
        
        const action = call.args[0];
        if (action.type !== '[Boards] Add Board') throw new Error(`Wrong Action Type: ${action.type}`);
        if (action.board.title !== 'New Board') throw new Error(`Wrong Data: ${JSON.stringify(action.board)}`);
        
        console.log('✅ PASS');
        passed++;
    } catch(e) {
        console.error('❌ FAIL:', e.message);
        failed++;
    }

    // --- TEST 5: Feature - Update Task Tags (Probe) ---
    try {
        console.log('\n🧪 TEST 5: Update Task Tags Feature Check (Probe)');
        const plugin = setupEnv();
        const updateTaskCommand = {
            action: 'updateTask',
            taskId: 'TASK_1',
            data: { tagIds: ['TAG_A', 'TAG_B'] }
        };
        const cmdInfo = {
            command: updateTaskCommand,
            filename: 'update_task_tags.json',
            path: path.join(cmdDir, 'update_task_tags.json')
        };
        fs.writeFileSync(cmdInfo.path, JSON.stringify(updateTaskCommand));
        
        await plugin.executeCommand(cmdInfo);
        
        const call = PluginAPI.calls.find(c => c.method === 'updateTask');
        if (!call) throw new Error('PluginAPI.updateTask was NOT called.');
        if (call.args[0] !== 'TASK_1') throw new Error(`Wrong ID: ${call.args[0]}`);
        if (!call.args[1].tagIds || call.args[1].tagIds.length !== 2) {
            throw new Error(`tagIds NOT passed correctly: ${JSON.stringify(call.args[1])}`);
        }
        
        console.log('✅ PASS');
        passed++;
    } catch(e) {
        console.error('❌ FAIL:', e.message);
        failed++;
    }

    // --- TEST 6: Feature - Update Task Tags (Explicit Support) ---
    try {
        console.log('\n🧪 TEST 6: Update Task Tags (Explicit Logging Check)');
        const plugin = setupEnv();
        const updateTaskCommand = {
            action: 'updateTask',
            taskId: 'TASK_1',
            data: { tagIds: ['TAG_A'] }
        };
        const cmdInfo = {
            command: updateTaskCommand,
            filename: 'update_tags_log.json',
            path: path.join(cmdDir, 'update_tags_log.json')
        };
        fs.writeFileSync(cmdInfo.path, JSON.stringify(updateTaskCommand));
        
        // Intercept console.log
        const originalLog = console.log;
        let logFound = false;
        console.log = (...args) => {
            if (args.join(' ').includes('Updating task tags for TASK_1')) {
                logFound = true;
            }
            // originalLog(...args); // Optional: keep output
        };

        await plugin.executeCommand(cmdInfo);
        
        // Restore
        console.log = originalLog;

        if (!logFound) {
            throw new Error('Explicit log for tag update was NOT found in console output.');
        }
        
        console.log('✅ PASS');
        passed++;
    } catch(e) {
        console.error('❌ FAIL:', e.message);
        failed++;
    }

    // --- Cleanup ---
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
    
    console.log(`\nResults: ${passed} Passed, ${failed} Failed`);
    if (failed > 0) process.exit(1);
}

runTests();
