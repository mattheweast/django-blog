# Security Features

Django's authentication system includes multiple layers of security by default.

## 1. Password Hashing

### Never Plain Text

Django **never** stores passwords as plain text.

```python
# When user registers
user.set_password('secret123')
user.save()

# Database stores:
# 'pbkdf2_sha256$260000$salt$hash'
# NOT: 'secret123'
```

### PBKDF2-SHA256 Algorithm

**PBKDF2** = Password-Based Key Derivation Function 2

**How it works:**
```
1. Generate random salt (unique per password)
2. Combine password + salt
3. Hash with SHA-256
4. Repeat 260,000 times (iterations)
5. Store: algorithm$iterations$salt$final_hash
```

**Example stored password:**
```
pbkdf2_sha256$260000$gqCY8XImLWXf$7FvT+w3s/rXnI1A...
     ↓         ↓         ↓           ↓
 algorithm iterations  salt      final hash
```

### Why This Is Secure

**Brute force is slow:**
- Each guess requires 260,000 hash operations
- Testing 1 million passwords takes ~43 minutes
- Makes cracking infeasible

**Salt prevents rainbow tables:**
- Each password has unique salt
- Same password → different hash for different users
- Attacker can't pre-compute hashes

### Checking Passwords

```python
# User logs in
user.check_password('secret123')
    ↓
1. Extract salt from stored hash
2. Hash input password with same salt + iterations
3. Compare result to stored hash
4. Return True if match, False if not
```

**Constant time comparison** - prevents timing attacks.

### Other Hashers Available

```python
# settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',      # Default
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',  # SHA1 variant
    'django.contrib.auth.hashers.Argon2PasswordHasher',      # More secure, needs argon2-cffi
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',# Needs bcrypt
]
```

**Argon2** is recommended for high-security applications (requires extra package).

## 2. CSRF Protection

### What is CSRF?

**Cross-Site Request Forgery** - tricking a user into submitting a request.

**Example attack without CSRF protection:**
```html
<!-- Malicious site -->
<form action="https://yourblog.com/comment/" method="post">
    <input type="hidden" name="body" value="SPAM!">
</form>
<script>document.forms[0].submit()</script>
```

If user visits malicious site while logged into your blog → spam comment posted!

### How Django Prevents This

**1. Token Generation**
```django
{% csrf_token %}
```
Generates:
```html
<input type="hidden" name="csrfmiddlewaretoken" value="abc123xyz...">
```

**2. Token Stored in Cookie**
```
Set-Cookie: csrftoken=abc123xyz; HttpOnly
```

**3. Validation on POST**
```
POST /comment/
Cookie: csrftoken=abc123xyz
Data: csrfmiddlewaretoken=abc123xyz&body=Comment
        ↓
Middleware checks: Cookie matches POST data? ✓
```

**4. Domain-specific**
- Token tied to your domain
- Malicious site can't read your cookies
- Can't forge valid request

### CSRF in AJAX

```javascript
// Get CSRF token from cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Include in AJAX request
fetch('/api/comment/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({body: 'Comment'})
});
```

## 3. Session Security

### Session Lifecycle

```
1. User logs in
2. Server creates session in database
3. Browser receives session cookie: sessionid=xyz789
4. Cookie sent with every request
5. Server looks up session, loads user
6. User logs out → session deleted
```

### Session Settings

```python
# How long until session expires (2 weeks default)
SESSION_COOKIE_AGE = 1209600  # seconds

# Delete session when browser closes?
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Only send cookie over HTTPS? (production)
SESSION_COOKIE_SECURE = True

# Prevent JavaScript access?
SESSION_COOKIE_HTTPONLY = True  # Default

# Only send to same site?
SESSION_COOKIE_SAMESITE = 'Lax'  # 'Strict', 'Lax', or None
```

### Session Hijacking Prevention

**HttpOnly flag:**
```
Set-Cookie: sessionid=xyz; HttpOnly
```
JavaScript cannot read cookie → prevents XSS attacks from stealing sessions.

**Secure flag (production):**
```
Set-Cookie: sessionid=xyz; Secure
```
Only sent over HTTPS → prevents man-in-the-middle attacks.

**SameSite:**
```
Set-Cookie: sessionid=xyz; SameSite=Lax
```
Cookie not sent on cross-site requests → prevents CSRF.

### Session Regeneration

After login, Django creates new session ID:

```python
login(request, user)
# Old session deleted
# New session created with new ID
# Prevents session fixation attacks
```

## 4. SQL Injection Prevention

### Django ORM Escapes Everything

**Safe (Django ORM):**
```python
User.objects.filter(username=user_input)
```

Django generates:
```sql
SELECT * FROM auth_user WHERE username = %s
-- Parameter: user_input (safely escaped)
```

**Unsafe (raw SQL):**
```python
# DON'T DO THIS!
cursor.execute(f"SELECT * FROM auth_user WHERE username = '{user_input}'")
```

If `user_input = "alice' OR '1'='1"`:
```sql
SELECT * FROM auth_user WHERE username = 'alice' OR '1'='1'
-- Returns all users!
```

### Parameterized Queries

Even with raw SQL, use parameters:

```python
# Safe
cursor.execute(
    "SELECT * FROM auth_user WHERE username = %s",
    [user_input]
)
```

Django/database driver handles escaping.

## 5. XSS Protection

### Auto-Escaping in Templates

Django templates automatically escape HTML:

```django
{{ comment.body }}
```

If `comment.body = "<script>alert('XSS')</script>"`:

**Rendered:**
```html
&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

Displayed as text, not executed as code.

### Marking Safe HTML

```django
{{ content|safe }}
```

Only use when content is trusted (e.g., admin-created HTML).

### Example Attack Prevented

**Without escaping:**
```html
<!-- Comment body: <script>steal_cookies()</script> -->
<p></p>
<!-- Runs malicious JavaScript! -->
```

**With escaping:**
```html
<!-- Comment body rendered as text -->
<p>&lt;script&gt;steal_cookies()&lt;/script&gt;</p>
<!-- Just displays the text, safe! -->
```

## 6. Clickjacking Protection

### X-Frame-Options Header

Django sets:
```
X-Frame-Options: DENY
```

Prevents your site from being loaded in an `<iframe>`.

**Prevents:**
```html
<!-- Malicious site -->
<iframe src="https://yourblog.com/admin/"></iframe>
<div style="position:absolute; opacity:0; top:0; left:0; width:100%; height:100%">
    <!-- Invisible layer to intercept clicks -->
</div>
```

User thinks they're clicking malicious site, actually clicking your site!

## 7. Password Validation

### Built-in Validators

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Prevents:**
- Password similar to username/email
- Too short passwords
- Common passwords (password, 12345678, etc.)
- All-numeric passwords

### Custom Validator

```python
from django.core.exceptions import ValidationError

class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not any(char in '!@#$%^&*' for char in password):
            raise ValidationError("Password must contain special character")
    
    def get_help_text(self):
        return "Your password must contain at least one: !@#$%^&*"
```

## 8. Rate Limiting (Not built-in)

Django doesn't include rate limiting, but you can add it:

### Using django-ratelimit

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Max 5 login attempts per minute per IP
    pass
```

### Manual Implementation

```python
from django.core.cache import cache

def login_view(request):
    key = f'login_attempts_{request.META["REMOTE_ADDR"]}'
    attempts = cache.get(key, 0)
    
    if attempts >= 5:
        return HttpResponse("Too many attempts. Try again later.", status=429)
    
    # ... login logic ...
    
    if login_failed:
        cache.set(key, attempts + 1, 300)  # 5 minutes
```

## Security Checklist

### Development
- ✅ DEBUG = True (OK for dev)
- ✅ SECRET_KEY in .env
- ✅ .env in .gitignore
- ✅ CSRF protection enabled
- ✅ Session cookies HttpOnly

### Production
- ☐ DEBUG = False
- ☐ SECRET_KEY strong and secret
- ☐ ALLOWED_HOSTS configured
- ☐ SESSION_COOKIE_SECURE = True (HTTPS)
- ☐ CSRF_COOKIE_SECURE = True (HTTPS)
- ☐ Use HTTPS
- ☐ Keep Django updated
- ☐ Use strong database password
- ☐ Enable rate limiting
- ☐ Regular backups
- ☐ Monitor failed login attempts

## Common Vulnerabilities Prevented

| Attack | Django Protection |
|--------|-------------------|
| SQL Injection | ORM parameterized queries |
| XSS | Template auto-escaping |
| CSRF | CSRF tokens |
| Password Leaks | Password hashing |
| Session Hijacking | HttpOnly, Secure cookies |
| Clickjacking | X-Frame-Options header |
| Broken Auth | Session management |
| Timing Attacks | Constant-time comparison |

## Summary

Django provides strong security by default:
- Passwords hashed with PBKDF2-SHA256
- CSRF tokens on all POST requests
- Sessions secured with HttpOnly cookies
- SQL injection prevented by ORM
- XSS prevented by template escaping
- Clickjacking prevented by X-Frame-Options
- Password validators enforce strong passwords

**Most security features are automatic** - you just need to:
1. Use `{% csrf_token %}` in forms
2. Use Django ORM (don't write raw SQL)
3. Keep Django updated
4. Configure production settings properly
