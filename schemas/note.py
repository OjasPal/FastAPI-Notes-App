from datetime import timezone


def noteEntity(item) -> dict:
    created = item.get("created_at")
    if created:
        created = created.replace(tzinfo=timezone.utc).astimezone()
        created = created.strftime("%d %b %Y, %I:%M %p")

    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "desc": item["desc"],
        "important": item.get("important", False),
        "created_at": created or "",
    }


def notesEntity(items) -> list:
    return [noteEntity(item) for item in items]