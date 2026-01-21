# Phase III Data Model Extension

## 1. Entity Definitions

### 1.1 Conversation Entity
```python
class Conversation(SQLModel, table=True):
    """
    Represents a conversation between user and AI assistant
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    title: str | None = Field(max_length=200, default=None)  # Auto-generated from first message
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow())
    updated_at: datetime.datetime = Field(default=datetime.datetime.utcnow())
    is_active: bool = Field(default=True)
    
    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
    
    # Indexes
    # IDX: user_id (foreign key)
    # IDX: (user_id, created_at DESC) for efficient user history queries
    # IDX: (is_active, updated_at DESC) for active conversation queries
```

### 1.2 Message Entity
```python
class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    role: str = Field(max_length=20, sa_column=sa.Column(sa.Enum("user", "assistant", "system", name="message_role")))  # Enum for message roles
    content: str = Field(sa_column=sa.Column(sa.Text))  # Message content
    timestamp: datetime.datetime = Field(default=datetime.datetime.utcnow())
    metadata: dict | None = Field(default=None, sa_column=sa.Column(sa.JSON))  # AI-related metadata
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    
    # Indexes
    # IDX: conversation_id (foreign key)
    # IDX: (conversation_id, timestamp ASC) for chronological message retrieval
    # IDX: (timestamp DESC) for recent message queries
```

## 2. Relationship Mapping

### 2.1 User-Conversation Relationship
- **Relationship**: One-to-Many (User → Conversations)
- **Cardinality**: One user can have many conversations
- **Cascade Behavior**: Conversations cascade delete when user is deleted
- **Indexing**: Foreign key on user_id for efficient user-based queries

### 2.2 Conversation-Message Relationship
- **Relationship**: One-to-Many (Conversation → Messages)
- **Cardinality**: One conversation contains many messages
- **Cascade Behavior**: Messages cascade delete when conversation is deleted
- **Indexing**: Foreign key on conversation_id for efficient conversation-based queries

## 3. Database Schema Changes

### 3.1 New Tables
- **conversations**: Stores conversation metadata and user associations
- **messages**: Stores individual message records with roles and content

### 3.2 Modified Tables
- **users**: No structural changes needed; foreign key relationships established
- **tasks**: No structural changes needed; AI tools will use existing API endpoints

## 4. Index Strategy

### 4.1 Query Optimization
- **User Conversations**: Index on (user_id, created_at DESC) for history retrieval
- **Active Conversations**: Index on (is_active, updated_at DESC) for active session queries
- **Message Retrieval**: Index on (conversation_id, timestamp ASC) for chronological display
- **Recent Activity**: Index on (timestamp DESC) for recent message queries

### 4.2 Performance Considerations
- **Selectivity**: High-selectivity indexes for optimal query performance
- **Covering Indexes**: Include frequently selected columns in indexes where appropriate
- **Maintenance**: Regular index maintenance to prevent performance degradation

## 5. Data Integrity

### 5.1 Constraints
- **Foreign Key Constraints**: Ensure referential integrity between entities
- **Check Constraints**: Validate message role enum values
- **Not Null Constraints**: Enforce required fields for data completeness
- **Unique Constraints**: Prevent duplicate critical combinations

### 5.2 Validation Rules
- **Conversation Title**: Max length of 200 characters
- **Message Content**: Text field to accommodate varying lengths
- **Timestamps**: Automatically managed with default values
- **Role Values**: Restricted to "user", "assistant", or "system"

## 6. Migration Path

### 6.1 Schema Evolution
- **Version Control**: Alembic-managed migration scripts
- **Rollback Capability**: Fully reversible migration operations
- **Data Preservation**: Migration scripts preserve existing data
- **Testing**: Migration scripts tested in staging environment

### 6.2 Data Migration
- **Initial Data**: Create seed data if required
- **Transformation**: Scripts to transform existing data if needed
- **Validation**: Post-migration data validation checks
- **Backup**: Full backup before migration execution

## 7. Security Considerations

### 7.1 Data Privacy
- **Encryption**: Data encryption at rest for sensitive information
- **Access Control**: Row-level security through user_id foreign keys
- **Audit Trail**: Timestamps for all data changes
- **Retention Policy**: Automatic cleanup of inactive conversations

### 7.2 User Isolation
- **Foreign Key Enforcement**: Database-level enforcement of user isolation
- **Query Filtering**: All queries must filter by user_id
- **API Validation**: Double-validation at API layer for additional security
- **Session Context**: User context maintained throughout operations