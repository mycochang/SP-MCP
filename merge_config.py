import json
import sys
import os

def merge_claude_config(config_file, mcp_dir):
    backup_file = config_file + '.backup'
    
    try:
        # Load existing config if it exists
        config = {}
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                config = json.load(f)
        elif os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        
        # Ensure mcpServers exists
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        # Add or update super-productivity server
        config['mcpServers']['super-productivity'] = {
            'command': 'python',
            'args': [os.path.join(mcp_dir, 'mcp_server.py')]
        }
        
        # Write back the merged config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print('Successfully merged Super Productivity MCP server into existing configuration')
        return True
        
    except Exception as e:
        print(f'Error merging config: {e}')
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python merge_config.py <config_file> <mcp_dir>')
        sys.exit(1)
    
    config_file = sys.argv[1]
    mcp_dir = sys.argv[2]
    
    success = merge_claude_config(config_file, mcp_dir)
    sys.exit(0 if success else 1)