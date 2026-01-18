const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Mock Browser Environment
global.window = {};
global.console = console;

// Mock PluginAPI
global.PluginAPI = {
    calls: [],
    
    executeNodeScript: async ({ script, args }) => {
        try {
            // Create a context with fs/path available
            const sandbox = {
                require: require,
                args: args,
                console: console
            };
            
            // Wrap script in an async function to allow 'return'
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
    
    deleteTag: async (tagId) => {
        global.PluginAPI.calls.push({ method: 'deleteTag', args: [tagId] });
        return { success: true };
    },
    
    updateTag: async (tagId, data) => {
         global.PluginAPI.calls.push({ method: 'updateTag', args: [tagId, data] });
         return { success: true };
    },

    registerHook: () => {},
    registerMenuEntry: () => {},
    showSnack: () => {},
    log: () => {}
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
    // Do NOT call init() to avoid starting intervals/filesytem checks
    
    return plugin;
}

module.exports = { loadPlugin, PluginAPI: global.PluginAPI };