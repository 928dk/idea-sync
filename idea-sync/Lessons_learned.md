# Lessons Learned

## Mobile-Desktop Sync

### Problem
Sync conflicts can lose data.

### Solution
Implement last-write-wins with conflict logging:
```python
def sync_ideas(local_ideas, remote_ideas):
    merged = {}
    for idea in {**local_ideas, **remote_ideas}.values():
        merged[idea.id] = idea
    
    # Log conflicts
    for id in set(local_ideas) & set(remote_ideas):
        if local_ideas[id].modified != remote_ideas[id].modified:
            log_conflict(id, local_ideas[id], remote_ideas[id])
    
    return merged
```

### Lesson
Always log conflicts for manual review.

---

## Pre-Flight Checks

```bash
# Syntax check
find . -name "*.py" -exec python3 -m py_compile {} \;

# Check hub is accessible
curl -s http://localhost:5000/health || echo "Hub not running"

# Verify mobile/desktop can reach hub
ping -c 1 hub.local

# Check sync directory
ls -la sync/ || mkdir -p sync
```

---

## Future Improvements

1. Add encrypted sync
2. Implement offline-first mode
3. Add real-time collaboration