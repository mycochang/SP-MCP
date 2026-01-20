const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Mock Browser Environment
global.window = {};
global.console = console;

// Mock PluginAPI
global.PluginAPI = {
    calls: [],
    
    // Core execution mock
    executeNodeScript: async ({ script, args }) => {
        try {
            // Create a context with fs/path available
            const sandbox = {
                require: require,
                args: args,
                console: console
            };
            
            // Wrap script in an async function to allow 'return' at top level
            const wrappedScript = `(async () => { 
                ${script} 
            })()`;
            
            // Execute the script string
            const result = await vm.runInNewContext(wrappedScript, sandbox);
            return { success: true, result: result };
        } catch (e) {
            console.error('Mock executeNodeScript error:', e);
            return { success: false, error: e.message };
        }
    },
    
    // Feature mocks - to be expanded as needed
    deleteTag: async (tagId) => {
        global.PluginAPI.calls.push({ method: 'deleteTag', args: [tagId] });
        return { success: true };
    },
    
    updateTag: async (tagId, data) => {
         global.PluginAPI.calls.push({ method: 'updateTag', args: [tagId, data] });
         return { success: true };
    },

    dispatchAction: async (action) => {
        global.PluginAPI.calls.push({ method: 'dispatchAction', args: [action] });
        return { success: true };
    },
    
    loadSyncedData: async (key) => {
        global.PluginAPI.calls.push({ method: 'loadSyncedData', args: [key] });
        // Return null by default, can be overridden in tests
        return null;
    },

    // Stubs to prevent crashes
    registerHook: () => {},
    registerMenuEntry: () => {},
    showSnack: () => {},
    log: () => {},
    getTasks: async () => [], 
    updateTask: async (taskId, data) => {
        global.PluginAPI.calls.push({ method: 'updateTask', args: [taskId, data] });
        return { success: true };
    },
    addProject: async () => {},
    addTask: async () => {}
};

function loadPlugin() {
    let pluginCode = fs.readFileSync(path.join(__dirname, '../plugin.js'), 'utf8');
    
    // STRIP the automatic initialization at the end
    // Look for "const mcpBridge = new MCPBridgePlugin();"
    const initStart = pluginCode.indexOf('const mcpBridge = new MCPBridgePlugin();');
    if (initStart !== -1) {
        pluginCode = pluginCode.substring(0, initStart);
    }
    
    // Add code to export the class
    pluginCode += '\nglobal.MCPBridgePlugin = MCPBridgePlugin;';
    
    // Eval in global context
    eval(pluginCode);
    
    // Manually instantiate
    const plugin = new global.MCPBridgePlugin();
    
    return plugin;
}

module.exports = { loadPlugin, PluginAPI: global.PluginAPI };
