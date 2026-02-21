#!/bin/bash
# Simple script to rebuild the plugin.zip for Super Productivity
echo "Zipping plugin.js, manifest.json, and package.json..."
zip -r plugin.zip plugin.js manifest.json package.json
echo "Done! plugin.zip has been rebuilt."
