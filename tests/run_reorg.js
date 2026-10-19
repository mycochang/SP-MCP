const { loadPlugin, PluginAPI } = require('./test_harness');

async function runReorg() {
    console.log("🚀 Starting Build Mode Reorganization...");

    // IDs from context
    const OPTIMIZATIONS_PROJECT = 'wZMuq-PbrcOFaOQzQtLhG';
    const GCAL_TASK_ID = '4k_ED2wroiKWeVdO7Rx0C';
    
    // 1. Mark Completed Tasks
    const doneTasks = [
        'nRQiepMaQ5mP06mwsWhC1', // NOI Login
        'pr-uJwlgQv7OE0OR07ftQ', // CachyOS
        'bGYE_cza4AUJCJg2YDPpu'  // Validate Taiga
    ];
    
    console.log("1. Completing user-identified tasks...");
    for (const tid of doneTasks) {
        await PluginAPI.updateTask(tid, { isDone: true, doneOn: Date.now() });
    }

    // 2. Consolidate Discord/Tech Debt
    console.log("2. Consolidating Discord & Low-pri items...");
    const parentId = await PluginAPI.addTask({
        title: '🧊 Integrations & Tech Debt (On Hold)',
        projectId: OPTIMIZATIONS_PROJECT
    });
    
    const lowPriTasks = [
        'CStM96lMrUh6mE3lJuUqy', // Trello -> Discord
        'bENu9iWjOkTH2uTyinjFF', // Taiga -> Discord
        '2kxhONHQgatI_yHmiqHg0'  // WebSocket IPC
    ];
    
    for (const tid of lowPriTasks) {
        await PluginAPI.updateTask(tid, { parentId: parentId });
    }

    // 3. Prioritize GCal Sync
    console.log("3. Prioritizing GCal Sync...");
    // Add subtasks for the agent workflow
    await PluginAPI.addTask({ title: 'Install Google Workspace MCP', parentId: GCAL_TASK_ID, projectId: OPTIMIZATIONS_PROJECT });
    await PluginAPI.addTask({ title: 'Verify Agent Access to GCal', parentId: GCAL_TASK_ID, projectId: OPTIMIZATIONS_PROJECT });
    await PluginAPI.addTask({ title: 'Define "Daily Briefing" skill in instructions.md', parentId: GCAL_TASK_ID, projectId: OPTIMIZATIONS_PROJECT });
    
    // Tag as URGENT (Tag ID fHH5wla3YDQR6yTTipusa from previous 'get_tags' output)
    await PluginAPI.updateTask(GCAL_TASK_ID, { tagIds: ['fHH5wla3YDQR6yTTipusa'] });

    console.log("✅ Reorganization Complete.");
}

runReorg().catch(console.error);
