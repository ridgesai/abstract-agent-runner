#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const REPOS_DIR = path.join(__dirname, 'repos');
const SWEBENCH_JSON = path.join(__dirname, 'swebench_verified.json');

async function main() {
    console.log('🔍 Checking repository setup...');
    
    // Check if repos/ directory exists
    if (!fs.existsSync(REPOS_DIR)) {
        console.log('📁 Creating repos/ directory...');
        fs.mkdirSync(REPOS_DIR, { recursive: true });
    } else {
        console.log('✅ repos/ directory already exists');
    }
    
    // Parse swebench_verified.json to get all unique repos
    console.log('📄 Parsing swebench_verified.json...');
    let swebenchData;
    try {
        const jsonContent = fs.readFileSync(SWEBENCH_JSON, 'utf8');
        swebenchData = JSON.parse(jsonContent);
    } catch (error) {
        console.error('❌ Failed to parse swebench_verified.json:', error.message);
        process.exit(1);
    }
    
    // Extract unique repository names
    const repoSet = new Set();
    swebenchData.forEach(item => {
        if (item.repo) {
            repoSet.add(item.repo);
        }
    });
    
    const uniqueRepos = Array.from(repoSet).sort();
    console.log(`📊 Found ${uniqueRepos.length} unique repositories to process:`);
    uniqueRepos.forEach(repo => console.log(`  - ${repo}`));
    
    // Check which repos are missing
    const missingRepos = [];
    const existingRepos = [];
    
    for (const repo of uniqueRepos) {
        // Convert "owner/repo" to "owner_repo" directory format
        const dirName = repo.replace('/', '_');
        const repoPath = path.join(REPOS_DIR, dirName);
        
        if (fs.existsSync(repoPath)) {
            existingRepos.push(repo);
        } else {
            missingRepos.push(repo);
        }
    }
    
    console.log(`\n📋 Repository Status:`);
    console.log(`✅ Existing: ${existingRepos.length} repositories`);
    console.log(`❌ Missing: ${missingRepos.length} repositories`);
    
    if (existingRepos.length > 0) {
        console.log('\n✅ Already cloned:');
        existingRepos.forEach(repo => console.log(`  ✓ ${repo}`));
    }
    
    if (missingRepos.length === 0) {
        console.log('\n🎉 All repositories are already available!');
        return;
    }
    
    console.log('\n📥 Missing repositories to clone:');
    missingRepos.forEach(repo => console.log(`  → ${repo}`));
    
    // Clone missing repositories
    console.log('\n🚀 Starting repository cloning process...');
    
    for (let i = 0; i < missingRepos.length; i++) {
        const repo = missingRepos[i];
        const dirName = repo.replace('/', '_');
        const repoUrl = `https://github.com/${repo}.git`;
        const targetPath = path.join(REPOS_DIR, dirName);
        
        console.log(`\n[${i + 1}/${missingRepos.length}] Cloning ${repo}...`);
        console.log(`📍 URL: ${repoUrl}`);
        console.log(`📁 Target: ${targetPath}`);
        
        try {
            await cloneRepository(repoUrl, targetPath);
            console.log(`✅ Successfully cloned ${repo}`);
        } catch (error) {
            console.error(`❌ Failed to clone ${repo}:`, error.message);
            // Continue with other repos even if one fails
        }
    }
    
    console.log('\n🏁 Repository cloning process completed!');
}

function cloneRepository(repoUrl, targetPath) {
    return new Promise((resolve, reject) => {
        const git = spawn('git', ['clone', repoUrl, targetPath], {
            stdio: 'inherit'
        });
        
        git.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`Git clone failed with code ${code}`));
            }
        });
        
        git.on('error', (error) => {
            reject(new Error(`Failed to spawn git: ${error.message}`));
        });
    });
}

// Run the main function
main().catch(error => {
    console.error('💥 Script failed:', error.message);
    process.exit(1);
});
