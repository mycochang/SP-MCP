const { loadPlugin, PluginAPI } = require('./test_harness');
const assert = require('assert');

async function test() {
    console.log('--- Reproduction Test: Project Listing (Simulation of Bug) ---');
    const plugin = loadPlugin();

    // Mock Data
    const mockProjects = [
        { id: 'p1', title: 'Active with Tasks', isArchived: false },
        { id: 'p2', title: 'Active NO Tasks', isArchived: false }, // The problematic one
    ];

    // Mock getAllProjects to simulate the BUG (missing p2)
    PluginAPI.getAllProjects = async () => {
        return [mockProjects[0]];
    };

    // Mock loadSyncedData to return ALL data (the source of truth)
    PluginAPI.loadSyncedData = async (key) => {
        if (key === 'PROJECT') {
            return {
                ids: ['p1', 'p2'],
                entities: {
                    'p1': mockProjects[0],
                    'p2': mockProjects[1]
                }
            };
        }
        return null;
    };

    const command = {
        action: 'getAllProjects',
        id: 'test_cmd_1',
        timestamp: Date.now()
    };

    let capturedResponse = null;
    plugin.writeCommandResponse = async (id, response) => {
        capturedResponse = response;
    };
    plugin.deleteCommandFile = async () => {};

    await plugin.executeCommand({
        command: command,
        filename: 'test.json',
        path: '/tmp/test.json'
    });

    console.log('Result:', JSON.stringify(capturedResponse, null, 2));

    if (!capturedResponse || !capturedResponse.success) {
        console.error('Command failed');
        process.exit(1);
    }

    const projects = capturedResponse.result;
    
    // Check if p2 is present
    const p2 = projects.find(p => p.id === 'p2');
    if (!p2) {
        console.error('FAIL: Project p2 (Active NO Tasks) is missing! The bug is reproduced.');
        process.exit(1); // Fail intentionally to confirm reproduction
    }
    
    console.log('PASS: Project p2 is present.');
}

test().catch(e => {
    console.error(e);
    process.exit(1);
});