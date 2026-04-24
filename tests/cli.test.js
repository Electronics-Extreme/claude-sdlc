const { describe, it } = require('node:test');
const assert = require('node:assert');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('cli init', () => {
  it('defaults to current directory when no --dir provided', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-test-'));
    try {
      execSync(
        `node ${path.resolve('src/cli.js')} init --harness claude`,
        { cwd: tmpDir, encoding: 'utf8' }
      );
      assert.ok(fs.existsSync(path.join(tmpDir, 'docs', 'sdlc', '01_requirement')));
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  it('uses --dir override when provided', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-test-'));
    const targetDir = path.join(tmpDir, 'target');
    try {
      execSync(
        `node ${path.resolve('src/cli.js')} init --dir "${targetDir}" --harness claude`,
        { cwd: tmpDir, encoding: 'utf8' }
      );
      assert.ok(fs.existsSync(path.join(targetDir, 'docs', 'sdlc', '01_requirement')));
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  });
});
