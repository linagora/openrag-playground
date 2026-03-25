# User Manual

**OpenRAG Playground** is a demo interface for [Open-RAG](https://open-rag.ai), the sovereign Retrieval-Augmented Generation platform by [LINAGORA](https://linagora.com). It lets operators run live demos using persona-based logins, each backed by a real OpenRAG API token.

## Getting Started

### First Setup

When OpenRAG Playground is launched for the first time, it displays a setup wizard. The wizard guides you through five steps:

1. **Master password** -- Choose a strong password. This password protects all access to the application and is used to encrypt API tokens. It cannot be recovered if lost; the only reset mechanism is to delete the configuration file.
2. **Groups** -- Define groups to organize demo users (e.g. departments, teams). Each group has a name, a color, and a Lucide icon.
3. **Demo users** -- Create persona accounts. Each user needs a name, job title, group, avatar style (male/female/neutral), avatar color, an OpenRAG API URL, and a real API token.
4. **Demo prompts** -- Pre-configure prompts that users can quickly access with the `/` shortcut. Each prompt has a label, a scope (global, group-specific, or user-specific), optional tags, and the prompt text.
5. **Review and confirm** -- Review all settings and create the configuration.

The configuration is saved to `config.yaml`. Tokens are encrypted with AES-256-GCM using a key derived from the master password.

### Unlocking the Application

Every visit requires entering the master password. Once entered, a session is created that lasts 24 hours. All pages are protected behind this gate.

## Login Page

After unlocking, the login page displays a grid of persona cards organized by group. Each card shows the user's avatar, name, job title, and group badge.

- **Single click** on a card to open the sign-in modal. The modal shows a decorative pre-filled password field and a "Sign in" button.
- **Double-click** on a card to hide that user from the grid for the current session. This is useful during demos to show only relevant personas.
- Press **Escape** to close the sign-in modal.

## Chat Interface

### Layout

The chat interface has two main areas:

- **Sidebar** (left) -- Contains the partition tree, file browser, and message history.
- **Chat area** (right) -- Contains the chat header, message stream, and input bar.

### Sending Messages

Type your message in the input bar at the bottom and press **Enter** to send. Responses are streamed in real time using Server-Sent Events -- tokens appear one by one as they are generated.

Responses are rendered with full markdown support: headings, bold, italic, code blocks, lists, and tables are all formatted.

### Sources

After each response, the system displays the source documents that were used to generate the answer. Each source shows the filename, a relevance score, and an excerpt. Click on a source to open the source viewer, which supports:

- PDF documents (embedded viewer)
- Images (inline display)
- Audio files (audio player)
- Video files (video player)
- Text and markdown files (rendered content)
- Other file types (download link)

### Clear Conversation

Click the eraser icon in the top-left corner of the chat area to clear the current conversation.

## Semantic Search

Prefix your message with `#` to perform a semantic search instead of a chat query. For example:

```
# employment contract termination clauses
```

This returns the most relevant document chunks from the active partition without generating an AI response. Results are displayed as clickable source cards.

## Prompt Suggestions

Type `/` in the input bar to open the prompt suggestions dropdown. This displays all pre-configured demo prompts available to the current user based on scope (global, group, user, or partition). Use **Up/Down** arrow keys to navigate and **Enter** to select a prompt.

Prompts can also be saved from the message history: hover over a message in the history sidebar and click the bookmark icon to save it as a demo prompt with a chosen scope (for everyone, for my group, for this partition, or for me only).

## Partition Tree

The sidebar displays all available partitions as a folder tree. Partitions are data repositories that organize documents by topic or department.

- **all** is always listed first and aggregates all partitions.
- Click a partition to select it. The chat and file browser will reflect the selected partition.
- Click the arrow next to a partition to expand it and see its files and chunks.
- Files are displayed as a tree structure under each partition. Click a file to view it. Click the arrow next to a file to see its indexed chunks.
- Each partition shows a role badge (owner, editor, or viewer) indicating your access level.

### Browsing Files and Chunks

When a partition is expanded, its files appear as a sub-tree. Each file shows its name and a type icon. Expanding a file reveals the individual chunks that were indexed from it.

- Click a file name to open it in the source viewer.
- Click a chunk to view that specific chunk's content.
- Hover over a file to reveal action buttons: view in source viewer, open in new tab, and delete (if you have editor or owner access).

## File Upload

If you have editor or owner access to a partition, an upload button appears in the sidebar header. Click it to select a file to upload. Supported file types depend on the OpenRAG server configuration.

After uploading, the file is queued for indexing. The interface polls the task status and updates the display when indexing is complete.

## Partition Access Management

For partitions where you have owner access, hover over the partition name and click the shield icon to manage user access. This opens a panel showing all users with access to the partition and their roles. Owners can modify user roles for that partition.

## Admin Panel

The admin panel is accessible at [/admin](/admin) (not linked in the main navigation). It requires the same master session as the main application.

The admin panel provides four sections accessible via tabs:

- **Groups** -- Add, edit, or delete groups. Each group has a name, color, and icon.
- **Demo Users** -- Add, edit, or delete demo user personas. You can use the "Fetch user info" button to auto-fill user details from the API. Changing the master password re-encrypts all tokens.
- **Demo Prompts** -- Add, edit, or delete pre-configured prompts with labels, scopes, tags, and text.
- **Settings** -- Export and import configuration files.

The admin panel also provides a [logout](/logout) link to end the master session and return to the unlock screen.

## User Menu

Click your avatar and name in the top-right corner of the chat header to open the user menu. From here you can:

- **Switch language** between English and French.
- **Switch theme** between dark and light mode.
- **Log out** to return to the persona login screen.

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Enter | Send message |
| Escape | Close modal, close sign-in overlay, close source viewer |
| Up / Down | Navigate prompt suggestions |
| / | Open prompt suggestions (when input is empty) |
| # | Start a semantic search (when input is empty) |
