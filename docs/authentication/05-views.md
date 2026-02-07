# Views & Logic

## Registration View

### Location
`blog/views.py`

### Implementation

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_index')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
```

### Line-by-Line Explanation

```python
def register(request):
```
Standard Django view function. Receives `HttpRequest`, returns `HttpResponse`.

```python
if request.method == 'POST':
```
**Two request types:**
- `GET` - User just visiting the page → Show empty form
- `POST` - User submitting form → Process it

```python
form = UserCreationForm(request.POST)
```
Creates form instance bound to submitted data.

**UserCreationForm includes:**
- `username` field
- `password1` field (password)
- `password2` field (confirmation)
- Built-in validation

```python
if form.is_valid():
```
**Validates:**
- Username not already taken
- Passwords match
- Password meets requirements (length, not too common, not all numeric)

**If invalid:**
- `form.errors` populated with error messages
- Form re-displayed with errors

```python
user = form.save()
```
**This line does a lot:**
1. Creates User object
2. **Hashes password** with PBKDF2-SHA256
3. Saves to database
4. Returns User instance

**Equivalent to:**
```python
user = User.objects.create_user(
    username=form.cleaned_data['username'],
    password=form.cleaned_data['password1']
)
```

```python
login(request, user)
```
**Logs user in immediately:**
1. Creates session in database
2. Sends session cookie to browser
3. Sets `request.session['_auth_user_id'] = user.id`

**What happens:**
- Browser now has cookie: `sessionid=abc123`
- Future requests will have `request.user` = this user

```python
return redirect('blog_index')
```
Sends 302 redirect to homepage. User sees URL change to `/`.

```python
else:
    form = UserCreationForm()
```
For GET requests, create empty form to display.

## Comment View (Updated)

### Implementation

```python
def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all().order_by('-created_on')
    
    # Handle comment form - only for authenticated users
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('blog_detail', pk=post.pk)
        else:
            form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog_detail.html', context)
```

### Key Changes from Before

**Before:**
```python
form = CommentForm(request.POST or None)
if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
```

**After:**
```python
form = None  # Start with no form
if request.user.is_authenticated:  # Check login
    # ... form logic here
    comment.user = request.user  # Link to user
```

### Authentication Check

```python
if request.user.is_authenticated:
```

**What is request.user?**

**Logged in:**
```python
request.user = User(
    id=5,
    username='alice',
    is_authenticated=True
)
```

**Not logged in:**
```python
request.user = AnonymousUser(
    is_authenticated=False
)
```

**How does it get there?**
- `AuthenticationMiddleware` runs on every request
- Reads session cookie
- Looks up user in database
- Attaches to `request.user`

### The save() Process

```python
comment = form.save(commit=False)  # Create object, don't save yet
comment.post = post                 # Set post relationship
comment.user = request.user         # Set user relationship
comment.save()                      # NOW save to database
```

**Why commit=False?**

Form only has `body` field:
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)  # Only body!
```

But Comment model needs:
- `body` - From form ✓
- `post` - Must set manually
- `user` - Must set manually

**commit=False** lets us set these before saving.

### Form = None for Anonymous Users

```python
form = None
if request.user.is_authenticated:
    # Create form
else:
    # Leave form as None
```

**In template:**
```django
{% if form %}
    <!-- Show form -->
{% else %}
    <p>Login to comment</p>
{% endif %}
```

## Authentication Helper Functions

### login()

```python
from django.contrib.auth import login

login(request, user)
```

**What it does:**
1. Creates session in `django_session` table
2. Stores user ID in session
3. Sends `sessionid` cookie to browser

**Session data:**
```json
{
    "_auth_user_id": "5",
    "_auth_user_backend": "django.contrib.auth.backends.ModelBackend",
    "_auth_user_hash": "..."
}
```

### logout()

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('blog_index')
```

**What it does:**
1. Deletes session from database
2. Clears session cookie
3. request.user becomes AnonymousUser

### authenticate()

```python
from django.contrib.auth import authenticate

user = authenticate(
    request,
    username='alice',
    password='secret123'
)

if user is not None:
    # Credentials valid
    login(request, user)
else:
    # Invalid credentials
    print("Login failed")
```

**What it does:**
1. Looks up user by username
2. Checks password hash matches
3. Returns User object if valid, None if not

**Django's LoginView uses this internally.**

## Protecting Views

### Using Decorator (Not implemented yet)

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')
```

**What it does:**
- If logged in: View runs normally
- If not logged in: Redirects to `/accounts/login/?next=/profile/`

### Manual Check (What we're doing)

```python
def blog_detail(request, pk):
    if request.user.is_authenticated:
        # Allow commenting
    else:
        # Don't show comment form
```

**Different approach:**
- Decorator: Blocks entire view
- Manual check: Conditionally shows/hides features

## Common View Patterns

### Check if staff

```python
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Staff only")
    
    # Admin dashboard code
```

### Check specific user

```python
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user != comment.user:
        return HttpResponseForbidden("Can only edit your own comments")
    
    # Edit logic
```

### Require POST

```python
@require_http_methods(["POST"])
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.user:
        comment.delete()
    
    return redirect('blog_detail', pk=comment.post.pk)
```

## Error Handling

### User doesn't exist

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Raises Http404 if not found
user = get_object_or_404(User, username='alice')

# Returns None if not found
user = User.objects.filter(username='alice').first()
if user:
    # User exists
```

### Invalid form

```python
if form.is_valid():
    # Process form
else:
    # form.errors contains error messages
    print(form.errors)
    # Re-render form with errors
```

## URL Reverse Lookup

```python
# By name
return redirect('blog_index')

# With arguments
return redirect('blog_detail', pk=post.pk)

# Absolute URL
from django.urls import reverse
url = reverse('blog_detail', kwargs={'pk': 5})
# Returns: '/post/5/'
```

## Summary

- Registration view uses `UserCreationForm` and `login()` function
- Comment view checks `request.user.is_authenticated` before showing form
- `commit=False` allows setting relationships before saving
- `login()` creates session and sends cookie
- `logout()` deletes session
- Views can check user permissions and ownership
- Forms automatically validate and provide error messages
