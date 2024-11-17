-- SQL to get threads by message ID
SELECT 
    t.id AS thread_id,
    t.sender_id,
    t.content,
    t.isBookmarked,
    t.hasRead,
    t.createdAt,
    t.updatedAt,
    u.username AS sender_username,
    r.emoji AS reaction_emoji,
    u_reacted.username AS reacted_by_username
FROM 
    Threads t
LEFT JOIN 
    Users u ON t.sender_id = u.id
LEFT JOIN 
    Reactions r ON t.id = r.message_id
LEFT JOIN 
    Users u_reacted ON r.reactedToBy = u_reacted.id
WHERE 
    t.message_id = ?; -- Replace ? with the actual message ID parameter

-- User Registration
INSERT INTO Users (username, email, googleId, loginVerificationCode, loginVerificationCodeExpires)
VALUES (?, ?, NULL, NULL, NULL)
ON CONFLICT(email) DO NOTHING;

-- Send Verification Email (this is typically handled in application logic, not SQL)
-- Generate verification code and send email would be application logic

-- User Sign-in
SELECT *
FROM Users
WHERE email = ?;

-- Verify User
SELECT *
FROM Users
WHERE loginVerificationCode = SHA2(?, 256)
AND loginVerificationCodeExpires > NOW();

-- Update user to clear verification code after verification
UPDATE Users
SET loginVerificationCode = NULL,
    loginVerificationCodeExpires = NULL
WHERE email = ?;

-- Google OAuth Callback (Insert or Update user based on Google profile)
INSERT INTO Users (googleId, username, email)
VALUES (?, ?, ?)
ON CONFLICT (googleId) 
DO UPDATE SET username = EXCLUDED.username, email = EXCLUDED.email;

-- Generate JWT Token (this is typically handled in application logic, not SQL)

-- Create Channel
INSERT INTO Channels (name, organisationId, collaborators)
VALUES (?, ?, ARRAY[?])
RETURNING *;

-- Get Channels by Organisation ID
SELECT *
FROM Channels
WHERE organisationId = ?
ORDER BY id DESC;

-- Get a Single Channel by ID
SELECT *
FROM Channels
WHERE id = ?;

-- If channel is found, add the 'isChannel' attribute in application logic

-- Update Channel to Add Collaborator
UPDATE Channels
SET collaborators = array_append(collaborators, ?)
WHERE id = ?
RETURNING *;

-- Get Conversations by Organisation ID
SELECT *
FROM Conversations
WHERE organisationId = ?
ORDER BY id DESC;

-- Get a Single Conversation by ID
SELECT c.*, 
       ARRAY(SELECT u.username 
             FROM Users u 
             WHERE u.id = ANY(c.collaborators)) AS collaborator_usernames
FROM Conversations c
WHERE c.id = ?;

-- Get Messages by Channel ID
SELECT *
FROM Messages
WHERE channelId = ? 
  AND organisationId = ?
ORDER BY createdAt DESC;

-- Get Messages by Conversation ID (with optional filter for isSelf)
SELECT *
FROM Messages
WHERE organisationId = ? 
  AND conversationId = ?
  AND (isSelf = ? OR ? IS NULL)  -- Adjusting for optional filtering
ORDER BY createdAt DESC;

-- Get a Single Message by ID
SELECT m.*, 
       u.username AS sender_username,
       ARRAY(SELECT u.username 
             FROM Users u 
             WHERE u.id = ANY(m.reactions->>'reactedToBy')) AS reacted_usernames,
       ARRAY(SELECT r.* 
             FROM Replies r 
             WHERE r.messageId = m.id) AS threadReplies
FROM Messages m
WHERE m.id = ?;

-- Get Organisation by ID
SELECT o.*, 
       ow.username AS owner_username, 
       ARRAY(SELECT cw.username 
             FROM Users cw 
             WHERE cw.id = ANY(o.coWorkers)) AS coworkers,
       ARRAY(SELECT c.* 
             FROM Channels c 
             WHERE c.organisationId = o.id) AS channels,
       ARRAY(SELECT con.* 
             FROM Conversations con 
             WHERE con.organisationId = o.id) AS conversations
FROM Organisations o
JOIN Users ow ON ow.id = o.ownerId
WHERE o.id = ?;

-- Get updated conversations for the current user
WITH UpdatedConversations AS (
  SELECT c.*, 
         ARRAY(SELECT cw.username 
               FROM Users cw 
               WHERE cw.id = ANY(c.collaborators)) AS collaborators,
         (SELECT username 
          FROM Users cw 
          WHERE cw.id = (SELECT id 
                         FROM Users 
                         WHERE id = ANY(c.collaborators) 
                         AND id != ? LIMIT 1)) AS other_username
  FROM Conversations c
  WHERE c.organisationId = ?
)
SELECT *, 
       CASE 
         WHEN EXISTS (SELECT 1 
                      FROM UpdatedConversations uc 
                      WHERE uc.id = c.id 
                      AND c.collaborators @> ARRAY[?]) THEN TRUE 
         ELSE FALSE 
       END AS current_user_is_co_worker
FROM UpdatedConversations c;

-- Create Organisation
INSERT INTO Organisations (ownerId, coWorkers)
VALUES (?, ARRAY[?])
RETURNING *;