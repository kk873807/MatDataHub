import sys

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_limit = """def _check_daily_limit(request: Request, current_user: Optional[User]):
    # Pro and Advanced get unlimited lookups
    if current_user and current_user.tier in ["pro", "advanced"]:
        return

    # Track by user_id if logged in, otherwise by IP
    key = f"user_{current_user.id}" if current_user else f"ip_{_get_ip(request)}"
    now = time.time()
    
    timestamps = _daily_lookups[key]
    # Remove timestamps older than 24 hours (86400 seconds)
    timestamps[:] = [t for t in timestamps if now - t < 86400]
    
    if len(timestamps) >= FREE_DAILY_LIMIT:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS, 
            "You have reached your free limit of 50 material lookups for today. Upgrade to Pro for unlimited access!"
        )
    timestamps.append(now)"""

new_limit = """def _check_daily_limit(request: Request, current_user: Optional[User]):
    # Assign specific daily limits based on tier
    is_api_key_request = bool(request.headers.get("X-API-Key"))
    
    if current_user:
        if current_user.tier == "advanced":
            daily_limit = 10000
        elif current_user.tier == "pro":
            # Pro gets UNLIMITED UI lookups! But they don't have programmatic access.
            # To protect against them stealing a JWT token to write a scraping script, we cap them at a high threshold.
            daily_limit = 1000
        else:
            daily_limit = 50
    else:
        daily_limit = 50

    key = f"user_{current_user.id}" if current_user else f"ip_{_get_ip(request)}"
    now = time.time()
    
    timestamps = _daily_lookups[key]
    # Clean up timestamps older than 24 hours (86400 seconds)
    timestamps[:] = [t for t in timestamps if now - t < 86400]
    
    if len(timestamps) >= daily_limit:
        msg = "You have reached your tier's daily lookup limit."
        if daily_limit == 50:
            msg = "You have reached your free limit of 50 material lookups for today. Upgrade to Pro for 1,000 daily lookups!"
        elif daily_limit == 1000:
            msg = "Pro tier limit of 1,000 lookups reached. Upgrade to Advanced for 10,000/day programmatic API limits."
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, msg)
        
    timestamps.append(now)"""

content = content.replace(old_limit, new_limit)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated materials.py daily limits.")
