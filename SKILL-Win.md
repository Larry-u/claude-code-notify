---
name: notify
description: Toggle HTTP notifications for HITL prompts and task completion
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, AskUserQuestion, Glob
argument-hint: "[on|off]"
---

# HTTP Notification Manager (Windows)

Manage HTTP notification hooks in `~/.claude/settings.json`.

## Behavior

1. First, read `~/.claude/settings.json` to check current state (look for `# claude-notify` markers).

### Arguments

- **`$ARGUMENTS` is "off"**: Remove all notification-related hooks (with `# claude-notify` marker) and confirm.
- **`$ARGUMENTS` is "on"**: Add notification hooks with the default messages.
- **`$ARGUMENTS` is empty or anything else**: Show current status and ask user what to do:

Use AskUserQuestion to offer:
  1. Toggle on/off

## Hook Configuration

When enabling, add/update these hooks in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "curl.exe -s -X POST http://localhost:8888/send -H \"Content-Type: application/json\" -d '{\"msg\": \"需要确认权限\"}' & # claude-notify"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "curl.exe -s -X POST http://localhost:8888/send -H \"Content-Type: application/json\" -d '{\"msg\": \"任务完成\"}' & # claude-notify"
          }
        ]
      }
    ]
  }
}
```

## Important

- Preserve all existing non-notification hooks when editing settings.json.
- Merge hooks carefully -- don't overwrite other hook configurations.
- The `# claude-notify` comment is a marker to identify notification hooks for toggling.
- Uses `curl.exe` (mingw64 version on Windows) with `&` for background execution in bash.
- Always show the user the final result after changes.