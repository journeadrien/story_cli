# Character Management Guide

This guide covers creating and managing characters in Story CLI using the AI-powered wizard.

## Overview

Story CLI's character system helps you build detailed, consistent characters for your visual novel. The creation wizard guides you through five phases:

1. **Basics** - Name, age, role
2. **Appearance** - Physical description, hair, eyes
3. **Personality** - Traits and characteristics
4. **Backstory** - History and background
5. **Relationships** - Connections to other characters

Each phase can be enhanced with AI suggestions when Ollama is running.

## Creating a Character

Start the character creation wizard from within your project directory:

```bash
cd my-visual-novel
story new character
```

### Phase 1: Basics

> 🤖 **AI Feature**: The AI can suggest character names based on your story's genre and setting.

The basics phase collects fundamental information:

```text
═══════════════════════════════════════════════════════════════
                    Character Creation Wizard
                         Phase 1: Basics
═══════════════════════════════════════════════════════════════

Character name: _

Would you like AI name suggestions? [y/n]: y

Here are some name suggestions:
  1. Sakura Tanaka
  2. Yuki Nakamura
  3. Hana Yamamoto

Enter a number to select, or type your own name: 1

Age: 22

Role (protagonist/antagonist/supporting/minor): protagonist
```

### Phase 2: Appearance

> 🤖 **AI Feature**: The AI can expand brief appearance notes into detailed descriptions.

Describe your character's physical appearance:

```text
═══════════════════════════════════════════════════════════════
                         Phase 2: Appearance
═══════════════════════════════════════════════════════════════

Brief description: tall, long black hair, gentle eyes

Would you like AI to expand this description? [y/n]: y

Expanded description:
  Sakura stands at 5'8", notably tall for her age. Her long,
  silky black hair reaches her mid-back, often worn loose or
  in a simple ponytail. Her gentle, almond-shaped eyes are
  a warm brown that seem to soften when she smiles...

Accept this description? [y/n]: y

Hair color: Black
Hair style: Long, straight
Eye color: Brown
```

### Phase 3: Personality

> 🤖 **AI Feature**: The AI suggests personality traits based on the character's role and appearance.

Define your character's personality:

```text
═══════════════════════════════════════════════════════════════
                         Phase 3: Personality
═══════════════════════════════════════════════════════════════

Would you like AI trait suggestions? [y/n]: y

Suggested traits based on protagonist role:
  • Compassionate - deeply cares about others' wellbeing
  • Determined - pursues goals despite obstacles
  • Introspective - tends to reflect on experiences

Accept these traits? [y/n/edit]: y

Add additional traits (comma-separated, or press Enter to skip):
thoughtful, artistic
```

### Phase 4: Backstory

> 🤖 **AI Feature**: The AI asks guided questions to help develop your character's history.

Develop your character's background:

```text
═══════════════════════════════════════════════════════════════
                         Phase 4: Backstory
═══════════════════════════════════════════════════════════════

Would you like AI-guided backstory development? [y/n]: y

Let's explore Sakura's history...

Q: What was Sakura's childhood like?
A: She grew up in a small coastal town with her grandmother
   after her parents moved abroad for work.

Q: What event most shaped who she is today?
A: Winning an art competition at 15 gave her confidence
   to pursue her dreams.

Q: What does she fear most?
A: Being abandoned by the people she loves.

Generating backstory summary...
```

### Phase 5: Relationships

Define connections to other characters in your story:

```text
═══════════════════════════════════════════════════════════════
                         Phase 5: Relationships
═══════════════════════════════════════════════════════════════

Add relationships to existing characters:

Available characters:
  1. Kenji Watanabe (supporting)
  2. Mei Chen (supporting)

Select character number (or 0 to skip): 1

Relationship type:
  1. Friend
  2. Family
  3. Rival
  4. Romantic interest
  5. Other

Select type: 1

Describe the relationship: Childhood friends who lost touch
                          and recently reconnected.

Add another relationship? [y/n]: n
```

### Saving the Character

After completing all phases, you'll see a summary:

```text
═══════════════════════════════════════════════════════════════
                      Character Summary
═══════════════════════════════════════════════════════════════

Name: Sakura Tanaka
Age: 22
Role: Protagonist

Appearance: Tall with long black hair and gentle brown eyes...
Personality: Compassionate, determined, introspective...
Backstory: Grew up in a coastal town with her grandmother...

Relationships:
  • Kenji Watanabe - Friend (childhood friends who reconnected)

Save this character? [y/n]: y

✨ Character saved: Sakura Tanaka
   File: story_data/characters/sakura_tanaka.json
```

## Editing Characters

Edit an existing character with:

```bash
story edit character "Sakura Tanaka"
```

### Edit Specific Phase

Jump directly to a specific wizard phase:

```bash
# Edit only appearance
story edit character "Sakura Tanaka" --phase appearance

# Edit only personality
story edit character "Sakura Tanaka" --phase personality

# Edit only backstory
story edit character "Sakura Tanaka" --phase backstory

# Edit only relationships
story edit character "Sakura Tanaka" --phase relationships
```

The wizard opens at the specified phase with current values pre-filled.

## Listing Characters

View all characters in your project:

```bash
story list characters
```

Output:
```text
Characters in my-visual-novel:

Name              Role         Age
─────────────────────────────────────
Sakura Tanaka     protagonist  22
Kenji Watanabe    supporting   24
Mei Chen          supporting   21

Total: 3 characters
```

### Detailed View

Show full character information:

```bash
story list characters --detailed
```

### Filter by Role

List only specific character types:

```bash
# Only protagonists
story list characters --role protagonist

# Only supporting characters
story list characters --role supporting
```

### JSON Output

Export character data as JSON:

```bash
story list characters --json
```

## Deleting Characters

Remove a character from your project:

```bash
story delete character "Sakura Tanaka"
```

You'll be asked to confirm:

```text
Are you sure you want to delete "Sakura Tanaka"? [y/n]: y

✨ Deleted character: Sakura Tanaka
```

### Dependency Warnings

If other characters have relationships with the character you're deleting:

```text
⚠️  Warning: The following characters have relationships with "Sakura Tanaka":
    • Kenji Watanabe (Friend)
    • Mei Chen (Rival)

Deleting will remove these relationship references.
Continue anyway? [y/n]:
```

### Force Delete

Skip the confirmation prompt:

```bash
story delete character "Sakura Tanaka" --force
```

**Use with caution** - this immediately deletes without confirmation.

---

[Back to Documentation Index](./README.md)
