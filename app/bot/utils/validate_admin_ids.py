from typing import Set

def validate(admin_ids: str) -> Set[int]:
    return set(int(admin.strip()) for admin in admin_ids.split(", ") if admin.strip() != "" and admin.isnumeric())
