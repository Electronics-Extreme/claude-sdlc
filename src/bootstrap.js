const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const HARNESS_CHOICES = ['claude', 'cursor', 'codex', 'gemini', 'copilot', 'opencode', 'all'];

const HARNESS_FILES = {
  claude:   ['.claude/settings.json', '.claude/sdlc-contract.md',
             '.claude-plugin/plugin.json',
             'CLAUDE.template.md'],
  cursor:   ['.cursor-plugin/plugin.json',
             '.cursor-plugin/hooks/hooks-cursor.json',
             '.cursor-plugin/rules/sdlc-contract.mdc',
             'AGENTS.md'],
  codex:    ['AGENTS.md'],
  gemini:   ['gemini-extension.json', 'GEMINI.md'],
  copilot:  ['.claude-plugin/plugin.json', 'AGENTS.md'],
  opencode: ['.opencode/plugins/sdlc-contract-loader.js', 'AGENTS.md'],
};

const ALWAYS_COPY_DIRS = [
  'docs/sdlc',
  'skill', 'hooks', 'scripts', 'config', 'schemas', 'tools',
  '.github',
];
const ALWAYS_COPY_FILES = ['.gitattributes', 'README.md'];

function copyTree(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.cpSync(src, dest, { recursive: true });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function sha256Of(file) {
  const buf = fs.readFileSync(file);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function bootstrap({ templateDir, targetDir, harness = 'all' }) {
  const warnings = [];

  if (!fs.existsSync(templateDir)) {
    throw new Error(`Template directory not found: ${templateDir}`);
  }
  if (!HARNESS_CHOICES.includes(harness)) {
    throw new Error(`Unknown harness '${harness}' (choose: ${HARNESS_CHOICES.join(', ')})`);
  }

  fs.mkdirSync(targetDir, { recursive: true });

  // Always-copy dirs + files.
  for (const d of ALWAYS_COPY_DIRS) {
    copyTree(path.join(templateDir, d), path.join(targetDir, d));
  }
  for (const f of ALWAYS_COPY_FILES) {
    copyTree(path.join(templateDir, f), path.join(targetDir, f));
  }

  // Harness-specific wrapper files.
  const harnesses = harness === 'all' ? HARNESS_CHOICES.slice(0, -1) : [harness];
  for (const h of harnesses) {
    for (const rel of HARNESS_FILES[h] || []) {
      copyTree(path.join(templateDir, rel), path.join(targetDir, rel));
    }
  }

  // Claude Code skill-discoverability: replicate skill/ into
  // .claude/skills/sdlc-strict-waterfall/.
  if (harness === 'claude' || harness === 'all') {
    const skillSrc = path.join(targetDir, 'skill');
    const skillDst = path.join(targetDir, '.claude', 'skills', 'sdlc-strict-waterfall');
    if (fs.existsSync(skillSrc) && !fs.existsSync(skillDst)) {
      fs.cpSync(skillSrc, skillDst, { recursive: true });
    }
  }

  // Promote CLAUDE.template.md → CLAUDE.md if safe.
  const tpl = path.join(targetDir, 'CLAUDE.template.md');
  const live = path.join(targetDir, 'CLAUDE.md');
  if (fs.existsSync(tpl) && !fs.existsSync(live)) {
    fs.renameSync(tpl, live);
  }

  // Pin SHA256 for hook-critical files to whatever was just copied. Adopter
  // re-pins later if they amend the contract.
  for (const rel of ['skill/sdlc-contract.md', 'hooks/session_start.py']) {
    const src = path.join(targetDir, rel);
    if (fs.existsSync(src)) {
      const sha = sha256Of(src);
      const base = path.basename(rel);
      fs.writeFileSync(`${src}.sha256`, `${sha}  ${base}\n`, 'utf8');
    }
  }

  // Sanity checks.
  if ((harness === 'claude' || harness === 'all') &&
      !fs.existsSync(path.join(targetDir, '.claude', 'settings.json'))) {
    warnings.push('warning: .claude/settings.json missing — SessionStart hook will not fire.');
  }
  if (['all', 'codex', 'copilot', 'opencode'].includes(harness) &&
      !fs.existsSync(path.join(targetDir, 'AGENTS.md'))) {
    warnings.push('warning: AGENTS.md missing — Codex/Copilot/OpenCode/generic readers may not load the contract.');
  }
  if ((harness === 'claude' || harness === 'all') &&
      !fs.existsSync(path.join(targetDir, '.claude', 'skills', 'sdlc-strict-waterfall', 'SKILL.md'))) {
    warnings.push('warning: .claude/skills/sdlc-strict-waterfall/ missing — /sdlc-strict-waterfall skill will not load.');
  }

  return { warnings, targetDir, harness };
}

module.exports = { bootstrap, HARNESS_CHOICES };
