/**
 * OpenCode plugin — session-start context injection for the SDLC contract.
 *
 * API STABILITY: relies on experimental.chat.messages.transform, which is NOT in
 * OpenCode's documented stable hook list as of 2026-04-23. If the API is removed,
 * switch the fallback branch (session.created + tui.prompt.append) — see comment
 * below.
 */
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const stripFrontmatter = (content) => {
  const match = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
  return match ? match[1] : content;
};

export const SdlcContractLoader = async ({ directory }) => {
  // Resolve the contract file — try repo-local first, then kit install location.
  const candidates = [
    path.resolve(directory || process.cwd(), 'skill/sdlc-contract.md'),
    path.resolve(__dirname, '../../skill/sdlc-contract.md'),
  ];

  const buildContext = () => {
    for (const p of candidates) {
      if (fs.existsSync(p)) {
        const body = stripFrontmatter(fs.readFileSync(p, 'utf8'));
        const now = new Date().toISOString();
        const versionFile = path.resolve(path.dirname(p), '..', 'VERSION');
        let version = 'unknown';
        try {
          if (fs.existsSync(versionFile)) {
            version = fs.readFileSync(versionFile, 'utf8').trim();
          }
        } catch { /* ignore */ }
        return `── SDLC contract v${version} loaded at ${now} · harness=opencode ──\n\n${body}`;
      }
    }
    return null;
  };

  return {
    // Primary hook — experimental API.
    'experimental.chat.messages.transform': async (_input, output) => {
      const ctx = buildContext();
      if (!ctx || !output.messages?.length) return;
      const firstUser = output.messages.find((m) => m.info?.role === 'user');
      if (!firstUser || !firstUser.parts?.length) return;
      // Injection idempotency — don't double-inject if the context is already present.
      if (firstUser.parts.some((p) => p.type === 'text' && p.text.includes('SDLC contract'))) return;
      const ref = firstUser.parts[0];
      firstUser.parts.unshift({ ...ref, type: 'text', text: ctx });
    },

    // Fallback stable hook — fires when a new session is created.
    // Kept as a non-injecting trace so logs confirm the plugin loaded even when
    // experimental.* is renamed or removed. If experimental.* goes away, adapt this
    // to persist the contract in session state instead.
    'session.created': async ({ session }) => {
      const ctx = buildContext();
      if (ctx) {
        // No-op beyond log visibility; injection must happen on the message path.
        console.debug(`[sdlc-contract-loader] session ${session?.id ?? '?'} created; contract ${ctx.length} chars ready`);
      }
    },
  };
};
