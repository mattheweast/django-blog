# Complete Request Flow

This document shows complete examples of authentication requests from browser to database and back.

## Example 1: User Registration

### Step-by-Step Flow

```
1. User visits /register/
    ↓
2. Browser sends: GET /register/ HTTP/1.1
    ↓
3. Django's URL router
    personal_blog/urls.py includes blog.urls
    blog/urls.py matches 'register/' → views.register
    ↓
4. register(request) view executes
    request.method = 'GET'
    ↓
5. View creates empty form
    form = UserCreationForm()
    ↓
6. View renders template
    render(request, 'registration/register.html', {'form': form})
    ↓
7. Template engine processes
    {% extends 'base.html' %}
    {{ form.as_p }}  # Generates HTML form fields
    ↓
8. HTTP response sent
    HTTP/1.1 200 OK
    Content-Type: text/html
    
    <html>
        <form method="post">
            <input type="text" name="username">
            <input type="password" name="password1">
            <input type="password" name="password2">
            <button>Sign Up</button>
        </form>
    </html>
    ↓
9. Browser renders page
```

### User Submits Form

```
1. User fills form and clicks "Sign Up"
    Username: alice
    Password: secret123
    Password confirm: secret123
    ↓
2. Browser sends: POST /register/ HTTP/1.1
   Cookie: csrftoken=abc123
   Content-Type: application/x-www-form-urlencoded
   
   csrfmiddlewaretoken=abc123&username=alice&password1=secret123&password2=secret123
    ↓
3. Django middleware processes request
    CsrfViewMiddleware: Checks CSRF token ✓
    SessionMiddleware: Loads session (none yet)
    AuthenticationMiddleware: Sets request.user = AnonymousUser
    ↓
4. URL router → views.register(request)
    ↓
5. View processes POST
    request.method = 'POST'
    form = UserCreationForm(request.POST)
    ↓
6. Form validation
    form.is_valid()
        ↓
        Check username field:
        - Not empty? ✓
        - Length <= 150? ✓
        - Valid characters? ✓
        ↓
        Check username unique:
        User.objects.filter(username='alice').exists() → False ✓
        ↓
        Check password1:
        - At least 8 characters? ✓
        - Not similar to username? ✓
        - Not in common passwords list? ✓
        - Not all numeric? ✓
        ↓
        Check password2:
        - Matches password1? ✓
        ↓
        All valid! Return True
    ↓
7. Create user
    user = form.save()
        ↓
        Internally does:
        user = User()
        user.username = 'alice'
        user.set_password('secret123')  # Hashes password!
            ↓
            Password hasher:
            - Generates random salt
            - Runs PBKDF2-SHA256 with 260,000 iterations
            - Produces hash: pbkdf2_sha256$260000$salt$hash
        user.save()
            ↓
            SQL: INSERT INTO auth_user (username, password, ...)
                 VALUES ('alice', 'pbkdf2_sha256$...', ...)
        ↓
        Returns User(id=2, username='alice')
    ↓
8. Log user in
    login(request, user)
        ↓
        Create session:
        session_key = generate_random_string()  # 'xyz789'
        session_data = {
            '_auth_user_id': '2',
            '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
            '_auth_user_hash': hash(user.password)
        }
        SQL: INSERT INTO django_session (session_key, session_data, expire_date)
             VALUES ('xyz789', encrypted_data, '2026-02-21')
        ↓
        Add cookie to response: sessionid=xyz789
    ↓
9. Redirect to homepage
    return redirect('blog_index')
        ↓
        HTTP/1.1 302 Found
        Location: /
        Set-Cookie: sessionid=xyz789; HttpOnly; SameSite=Lax
    ↓
10. Browser follows redirect
    GET / HTTP/1.1
    Cookie: sessionid=xyz789
    ↓
    Now authenticated! (see Example 2)
```

## Example 2: Authenticated User Visits Homepage

```
1. Browser sends: GET / HTTP/1.1
   Cookie: sessionid=xyz789
    ↓
2. Middleware processes request
    ↓
    SessionMiddleware:
    - Reads cookie: sessionid=xyz789
    - SQL: SELECT * FROM django_session WHERE session_key='xyz789'
    - Decrypts session_data
    - Stores in request.session
    ↓
    AuthenticationMiddleware:
    - Reads request.session['_auth_user_id'] → '2'
    - SQL: SELECT * FROM auth_user WHERE id=2
    - Gets User(id=2, username='alice')
    - Sets request.user = this User object
    ↓
3. URL router → views.blog_index(request)
    ↓
4. View executes
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog_index.html', context)
    ↓
5. Context processors add to context
    auth processor adds:
    context['user'] = request.user  # User(username='alice')
    ↓
6. Template renders
    {% if user.is_authenticated %}  ← True
        Welcome, {{ user.username }}!  ← "Welcome, alice!"
    ↓
7. Response sent
    HTTP/1.1 200 OK
    
    <html>
        <nav>Welcome, <strong>alice</strong>! | Logout</nav>
        <!-- Posts here -->
    </html>
```

## Example 3: Login Process

```
1. Browser: POST /accounts/login/
   Data: username=alice&password=secret123
   Cookie: csrftoken=abc123
    ↓
2. Middleware → URL router → Django's LoginView
    ↓
3. LoginView processes
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        ↓
        Form validation:
        - Calls authenticate(request, username='alice', password='secret123')
            ↓
            SQL: SELECT * FROM auth_user WHERE username='alice'
            Gets: User(id=2, password='pbkdf2_sha256$260000$...')
            ↓
            Check password:
            user.check_password('secret123')
                ↓
                Extract salt from stored hash
                Hash input password with same salt and iterations
                Compare hashes → Match! ✓
            ↓
            Return User object
        ↓
        User found and password valid!
        form.is_valid() returns True
    ↓
4. LoginView logs user in
    login(request, user)
    # (Same session creation as registration)
    ↓
5. Redirect
    Check for ?next= parameter
    If present: redirect(next)
    Else: redirect(LOGIN_REDIRECT_URL)  # '/'
```

## Example 4: Posting a Comment (Authenticated)

```
1. User on /post/1/ (logged in)
   Browser: POST /post/1/
   Cookie: sessionid=xyz789
   Data: body=Great post!
    ↓
2. Middleware chain
    SessionMiddleware → finds session
    AuthenticationMiddleware → request.user = User(username='alice', id=2)
    ↓
3. URL router → views.blog_detail(request, pk=1)
    ↓
4. View executes
    post = Post.objects.get(pk=1)
    
    if request.user.is_authenticated:  ← True (user logged in)
        if request.method == 'POST':  ← True
            form = CommentForm(request.POST)
            if form.is_valid():  ← Validates body field
                comment = form.save(commit=False)
                # comment.body = 'Great post!'
                
                comment.post = post  # Link to Post #1
                comment.user = request.user  # Link to User #2 (alice)
                
                comment.save()
                ↓
                SQL: INSERT INTO blog_comment (body, post_id, user_id, created_on)
                     VALUES ('Great post!', 1, 2, NOW())
                ↓
                return redirect('blog_detail', pk=1)
    ↓
5. Browser redirected to /post/1/ (to clear POST data)
    ↓
6. Page reloads with new comment showing
```

## Example 5: Anonymous User Tries to Comment

```
1. User on /post/1/ (NOT logged in)
   Browser: GET /post/1/
   (No session cookie)
    ↓
2. Middleware chain
    SessionMiddleware → no session
    AuthenticationMiddleware → request.user = AnonymousUser
    ↓
3. View executes
    post = Post.objects.get(pk=1)
    comments = post.comment_set.all()
    
    form = None
    if request.user.is_authenticated:  ← False!
        # This block doesn't run
    
    context = {'post': post, 'comments': comments, 'form': None}
    ↓
4. Template renders
    {% if user.is_authenticated %}
        <!-- Comment form -->
    {% else %}
        <p>Login to leave a comment.</p>  ← This shows
    {% endif %}
```

## Example 6: Logout

```
1. Browser: GET /accounts/logout/
   Cookie: sessionid=xyz789
    ↓
2. Middleware → URL router → Django's LogoutView
    ↓
3. LogoutView executes
    logout(request)
        ↓
        SQL: DELETE FROM django_session WHERE session_key='xyz789'
        Clear request.session
        request.user = AnonymousUser
    ↓
4. Response with cookie deletion
    HTTP/1.1 302 Found
    Location: /
    Set-Cookie: sessionid=""; Max-Age=0  # Delete cookie
    ↓
5. Browser deletes cookie
   Future requests have no sessionid → anonymous
```

## Request Object Anatomy

During a request, `request` contains:

```python
request.method          # 'GET', 'POST', etc.
request.path            # '/post/1/'
request.GET             # Query parameters: ?name=value
request.POST            # Form data from POST
request.FILES           # Uploaded files
request.COOKIES         # Browser cookies
request.META            # HTTP headers
request.user            # User object or AnonymousUser
request.session         # Session dictionary
request.is_secure()     # Using HTTPS?
```

## Response Object

Views return HttpResponse:

```python
from django.http import HttpResponse

# Simple response
return HttpResponse("Hello")

# Rendered template
return render(request, 'template.html', context)

# Redirect
return redirect('url_name')

# JSON response
return JsonResponse({'status': 'ok'})

# 404
return HttpResponseNotFound("Not found")
```

## Summary

Authentication flow involves:
1. **Middleware** - Processes every request, loads user
2. **Forms** - Validate input, check credentials
3. **Password hashing** - Secure password storage
4. **Sessions** - Remember logged-in users
5. **Cookies** - Browser stores session ID
6. **Database** - Store users, sessions, content
7. **Templates** - Display conditional content

Each request goes through: Middleware → URL Router → View → Template → Response
