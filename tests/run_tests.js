const { loadPlugin, PluginAPI } = require('./test_harness');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

// Setup temporary test directories
const testDir = path.join(__dirname, 'temp_test_env');
const mcpDir = path.join(testDir, 'mcp');
const cmdDir = path.join(mcpDir, 'plugin_commands');
const respDir = path.join(mcpDir, 'plugin_responses');

if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
fs.mkdirSync(cmdDir, { recursive: true });
fs.mkdirSync(respDir, { recursive: true });

async function runTests() {
    console.log('🚀 Starting Tests...');
    const plugin = loadPlugin();
    
    // Manually configure plugin to skip init() complexity
    plugin.config.mcpCommandDir = cmdDir;
    plugin.config.mcpResponseDir = respDir;

    // TEST 1: Security - Path Traversal (Regression Test)
    console.log('\n🧪 TEST 1: Path Traversal Security Check');
    const maliciousId = '../../evil_file';
    
    // We want to verify that writeCommandResponse DOES NOT write outside responseDir
    await plugin.writeCommandResponse(maliciousId, { secret: 'data' });
    
    // Check if evil file exists outside
    const evilFile = path.join(mcpDir, 'evil_file_response.json');
    const safeFile = path.join(respDir, 'evil_file_response.json');
    
    if (fs.existsSync(evilFile)) {
        console.error('❌ FAIL: Path Traversal Vulnerability exists! File written to:', evilFile);
        process.exit(1);
    } else if (fs.existsSync(safeFile)) {
        console.log('✅ PASS: Path Traversal prevented. File correctly sanitized to:', safeFile);
    } else {
        console.error('❓ UNKNOWN: File was not written anywhere? Check writeCommandResponse logic.');
    }

    // TEST 2: Feature - Delete Tag (TDD)
    console.log('\n🧪 TEST 2: Delete Tag Feature Check');
    
    const deleteCommand = {
        action: 'deleteTag',
        tagId: 'MY_TAG_ID'
    };
    
    const commandInfo = {
        command: deleteCommand,
        filename: 'test_cmd.json',
        path: path.join(cmdDir, 'test_cmd.json')
    };
    
    // Create dummy command file so deletion doesn't fail
    fs.writeFileSync(commandInfo.path, JSON.stringify(deleteCommand));
    
    try {
        await plugin.executeCommand(commandInfo);
        
        // Check if PluginAPI.deleteTag was called
        const call = PluginAPI.calls.find(c => c.method === 'deleteTag');
        if (call && call.args[0] === 'MY_TAG_ID') {
             console.log('✅ PASS: PluginAPI.deleteTag was called correctly.');
        } else {
             // We expect this to fail initially
             console.error('❌ FAIL: PluginAPI.deleteTag was NOT called.');
             console.log('Actual calls:', PluginAPI.calls);
             // We don't exit here because we want to see the fail
        }
    } catch (e) {
        console.error('❌ ERROR executing command:', e);
    }

    // Cleanup
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true });
}

runTests();
