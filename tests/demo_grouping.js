const { loadPlugin, PluginAPI } = require('./test_harness');

// 1. Setup Data
const MOCK_PROJECTS = [
    { id: 'P1', title: 'Website Redesign' },
    { id: 'P2', title: 'Mobile App' }
];

const MOCK_TAGS = [
    { id: 'T1', title: 'Urgent', color: '#ff0000' },
    { id: 'T2', title: 'Backend', color: '#0000ff' }
];

const MOCK_TASKS = [
    { id: 'TASK1', title: 'Fix Header', projectId: 'P1', tagIds: ['T1'] },
    { id: 'TASK2', title: 'API Setup', projectId: 'P2', tagIds: ['T2', 'T1'] },
    { id: 'TASK3', title: 'Email config', projectId: null, tagIds: ['T2'] }, // No project
    { id: 'TASK4', title: 'Misc Todo', projectId: null, tagIds: [] } // No project, no tags
];

// 2. Mock API
PluginAPI.getAllProjects = async () => MOCK_PROJECTS;
PluginAPI.getAllTags = async () => MOCK_TAGS;
PluginAPI.getTasks = async () => MOCK_TASKS;

async function runDemo() {
    console.log("--- Simulating User Request: 'Get tags, projects, and tasks in each' ---\n");

    const plugin = loadPlugin(); // We don't strictly need the plugin instance for this read-only demo, but good practice
    
    // 3. Fetch Data (The "Tools")
    console.log("1. Calling get_projects...");
    const projects = await PluginAPI.getAllProjects();
    
    console.log("2. Calling get_tags...");
    const tags = await PluginAPI.getAllTags();
    
    console.log("3. Calling get_tasks...");
    const tasks = await PluginAPI.getTasks();

    console.log(`\nFetched: ${projects.length} projects, ${tags.length} tags, ${tasks.length} tasks.\n`);

    // 4. Organize Data (The "Reasoning")
    
    // Group by Project
    console.log("=== TASKS BY PROJECT ===");
    const projectMap = {};
    projects.forEach(p => projectMap[p.id] = { ...p, tasks: [] });
    projectMap['Unassigned'] = { title: 'Unassigned (No Project)', tasks: [] };

    tasks.forEach(t => {
        if (t.projectId && projectMap[t.projectId]) {
            projectMap[t.projectId].tasks.push(t);
        } else {
            projectMap['Unassigned'].tasks.push(t);
        }
    });

    Object.values(projectMap).forEach(p => {
        if (p.tasks.length > 0) {
            console.log(`\n📂 Project: ${p.title}`);
            p.tasks.forEach(t => console.log(`   - [${t.id}] ${t.title}`));
        }
    });

    // Group by Tag
    console.log("\n\n=== TASKS BY TAG ===");
    const tagMap = {};
    tags.forEach(t => tagMap[t.id] = { ...t, tasks: [] });
    tagMap['NoTag'] = { title: 'No Tags', tasks: [] };

    tasks.forEach(t => {
        if (t.tagIds && t.tagIds.length > 0) {
            t.tagIds.forEach(tagId => {
                if (tagMap[tagId]) {
                    tagMap[tagId].tasks.push(t);
                }
            });
        } else {
            tagMap['NoTag'].tasks.push(t);
        }
    });

    Object.values(tagMap).forEach(t => {
        if (t.tasks.length > 0) {
            console.log(`\n🏷️  Tag: ${t.title}`);
            t.tasks.forEach(task => console.log(`   - [${task.id}] ${task.title}`));
        }
    });
}

runDemo();
