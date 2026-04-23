# Version Support & End-of-Life Policy

## Supported Versions

| Line  | Status                | Security patches | Bug fixes      | Notes              |
|-------|-----------------------|------------------|----------------|--------------------|
| 1.x   | Current               | Yes              | Yes            | Active development |
| 0.x   | Maintenance           | Yes              | Critical only  | Sunset {{date}}    |

## Deprecation Flow

1. **Announce** deprecation ≥ {{90 days}} before removal. Post to release notes + changelog + customer email.
2. **Emit warnings** from the deprecated path (logs, response header, UI banner).
3. **Provide migration guide** with concrete examples.
4. **Remove** at the announced date. Major version bump.

## API Version Policy

- `/v1` supported for {{12 months}} after `/v2` goes GA.
- Breaking changes only at major bumps.
- Additive changes (new optional fields) allowed within a version.

## Dependency EOL

- Track upstream EOL dates in {{sheet / tool}}.
- Upgrade path begins {{6 months}} before upstream EOL.
- Running on EOL dependencies in production requires documented risk acceptance.

## Data Retention on Deprecation

- When a feature is removed, associated data follows retention policy in `docs/sdlc/02_design/database_design.md`.
- Users notified if their data will be deleted; offered export.

## Sunset Checklist

- [ ] Deprecation announced
- [ ] Warnings live
- [ ] Migration path documented and tested
- [ ] All internal callers migrated
- [ ] Telemetry confirms zero traffic on deprecated path
- [ ] Removal PR approved
- [ ] Release notes updated
