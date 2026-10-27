# Shared connection and external action policy

A skill can **describe** its needed information. The environment determines whether an installed, authorized tool can supply it. Agent Skills metadata does not grant permissions and a shared Bot template cannot transfer the author's credentials.

## Progressive authorization

For public X posts and threads, use available public read-only tools without a connection prompt. For a request about the user's **own** bookmarks, DMs, timeline or likes, first inspect the X plugin's actual available resources and connection state. If the relevant source is unavailable because the user has not connected X, explain the immediate research benefit and ask them to connect the X plugin using the supported app flow. After authorization verify the requested operation; if unsupported, say so and offer a public search or user-supplied export. Don't request a password, cookie or token in chat.

A link between an X account and Grok for `@bot` handoff is not the same as authorizing the X plugin to access account-specific resources. Sharing a Bot template does not bring the creator's conversations, files, account permissions or histories.

## Sending invitations

Drafts are the safe default. **Read access is not send access.** Verify whether the runtime exposes the specific reply, DM or post action before offering to execute it. For any supported external write, show the exact recipient, X account and message, and require explicit approval for that specific action. Do not bulk-send unsolicited invitations, follow people or add members to groups automatically. If a tool is unavailable, provide a copyable draft without claiming it was sent.

## Sensitive material

Use only the relevant account-specific sources the user requested. Private communications and research participant notes must not be included in a published repo, public skill bundle, demo or shareable Bot template. A person posting publicly about work has not agreed to become a research participant.

## Runtime caution

Grok Bots on one user account can share the same cloud computer and connected apps. They are not separate security boundaries. The user must be able to revoke a connection without making the Bot fabricate missing data.
