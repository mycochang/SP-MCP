const { loadPlugin, PluginAPI } = require('./test_harness');

// Helper for delays
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function runCleanup() {
    console.log("🚀 Starting Organization & Cleanup Sequence...");
    
    // IDs
    const CEO_PROJECT = '1b4f3e39-149a-4b57-b9e2-8a4de070b59f';
    const OPTIMIZATIONS_PROJECT = 'wZMuq-PbrcOFaOQzQtLhG';
    const LINKEDIN_PROJECT = '_vjBDlTo8wLBnK5EBUjA8';
    const INBOX_PROJECT = 'INBOX_PROJECT';

    // 1. Create New Task
    console.log("1. Creating 'Verify Trello 2-way sync' in CEO...");
    await PluginAPI.addTask({
        title: 'Verify Trello 2-way sync',
        projectId: CEO_PROJECT
    });

    // 2. Mark Done (Specific Requests)
    console.log("2. Marking user-specified tasks as DONE...");
    const tasksToComplete = [
        'j4MVIBrQ4tDmxWj7T4922', // PhD Post
        '3zf4A4ipDeamxreLv9pJZ', // Post 44
        'RtE_fcUGRv_zEuJyJYZwv'  // Pay Office Bill
    ];
    for (const tid of tasksToComplete) {
        await PluginAPI.updateTask(tid, { isDone: true, doneOn: Date.now() });
    }

    // 3. Move Tasks to Projects
    console.log("3. Moving Inbox items to Projects...");
    
    // To LinkedIn (Also ensure these are done since they are the posts mentioned)
    await PluginAPI.updateTask('j4MVIBrQ4tDmxWj7T4922', { projectId: LINKEDIN_PROJECT });
    await PluginAPI.updateTask('3zf4A4ipDeamxreLv9pJZ', { projectId: LINKEDIN_PROJECT });

    // To CEO
    const toCEO = [
        'NWBXc450JfCfq5HJhPg6T', // Review Quote
        '5d6BpUcKTEWSjRYr7gdPw', // Pitch Deck
        'P7OY7PmSK8TMhtqq1ReBd', // PaulAndi
        'XC2BpLa9iHkHFLiqDUL9_', // Fruitservice
        'RtE_fcUGRv_zEuJyJYZwv'  // Pay Office Bill (Move after completing)
    ];
    for (const tid of toCEO) {
        await PluginAPI.updateTask(tid, { projectId: CEO_PROJECT });
    }

    // To Optimizations
    const toOpt = [
        'nRQiepMaQ5mP06mwsWhC1', // NOI Login
        'pr-uJwlgQv7OE0OR07ftQ', // Cachy
        'ordZ822iEEiQwKHRVeQiD'  // selfh.st
    ];
    for (const tid of toOpt) {
        await PluginAPI.updateTask(tid, { projectId: OPTIMIZATIONS_PROJECT });
    }

    // 4. Group Scheduling
    console.log("4. Grouping Scheduling tasks...");
    const parentId = await PluginAPI.addTask({
        title: '📅 Scheduling Batch',
        projectId: INBOX_PROJECT
    });
    
    const schedulingTasks = [
        'dBhAjRsko2yIX2tzjo1Xt', // Luis G 41
        'CPQMQ72rtiDuGC_8Tew7v', // Ginetti 42
        'HVCwKP_Ft0jLP6fIT7mHN', // Laimburg 24
        'wrwcn6KHQmiHHuiJN3ImS'  // Luis G 38
    ];
    for (const tid of schedulingTasks) {
        await PluginAPI.updateTask(tid, { parentId: parentId });
    }

    console.log("✅ Cleanup Complete!");
}

runCleanup().catch(console.error);
