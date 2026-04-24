#!/usr/bin/env node

const { program } = require('commander');
const fs = require('fs');
const path = require('path');
const { bootstrap, HARNESS_CHOICES } = require('./bootstrap.js');

const packageJson = require('../package.json');
const TEMPLATE_DIR = path.join(__dirname, '..', 'template');

program
  .name('claude-sdlc')
  .description('Bootstrap a frozen Waterfall SDLC project. Runtime needs Python 3.11+.')
  .version(packageJson.version);

program
  .command('init')
  .description('Initialize a new SDLC project in the target directory')
  .option('-f, --force', 'Overlay non-empty directory without prompting')
  .option('--dir <path>', 'Target directory (default: current directory)', '.')
  .option(
    '--harness <name>',
    `Harness wrapper(s) to install. One of: ${HARNESS_CHOICES.join(', ')}`,
    'all',
  )
  .action(async (options) => {
    const targetDir = path.resolve(options.dir);

    try {
      const result = bootstrap({
        templateDir: TEMPLATE_DIR,
        targetDir,
        harness: options.harness,
      });
      for (const w of result.warnings) {
        console.error(w);
      }

      console.log(`\n✓ SDLC project initialized at ${targetDir}`);
      console.log(`  Harness selection: ${result.harness}`);
      console.log('\nLayout:');
      console.log('  docs/sdlc/01_requirement/ … docs/sdlc/06_maintenance/   ← phase doc tree');
      console.log('  skill/                              ← /sdlc-strict-waterfall protocol');
      console.log('  hooks/session_start.py              ← SessionStart harness hook');
      console.log('  .claude/settings.json               ← Claude Code hook registration (if --harness claude|all)');
      console.log('  CLAUDE.md                           ← project facts (fill in {{PLACEHOLDERS}})');

      console.log('\nNext steps:');
      console.log(`  1. cd ${targetDir}`);
      console.log('  2. Edit CLAUDE.md — fill {{PLACEHOLDER}} values');
      console.log('  3. Open docs/sdlc/01_requirement/srs.md and start the spec');

      if (result.harness === 'claude' || result.harness === 'all') {
        console.log(`  4. Start Claude Code in ${targetDir} — SessionStart hook auto-loads contract`);
      } else if (result.harness === 'cursor') {
        console.log(`  4. Open ${targetDir} in Cursor — plugin auto-registers on first agent session`);
      } else if (result.harness === 'gemini') {
        console.log(`  4. Run: (cd ${targetDir} && gemini extensions install .)`);
      } else if (result.harness === 'codex') {
        console.log('  4. Follow .codex/INSTALL.md for Codex CLI skill-discovery install');
      } else if (result.harness === 'opencode') {
        console.log('  4. Add plugin to your opencode.json — see .opencode/INSTALL.md');
      } else if (result.harness === 'copilot') {
        console.log(`  4. Run: (cd ${targetDir} && copilot plugin install .)`);
      }

      console.log('  5. First message to the agent:');
      console.log('       /sdlc-strict-waterfall');
      console.log('       Start.');
      console.log('     (Greenfield → Bootstrap mode Gate 1. Existing docs → Strict mode.)');
      console.log('\nRuntime reminder: hooks + scripts + tools use Python 3.11+.');
      console.log('Verify with:  python3 --version');
    } catch (err) {
      console.error(`error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
