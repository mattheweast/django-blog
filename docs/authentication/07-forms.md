# Forms

## Django Forms Overview

Django provides two types of forms:
1. **Form** - Generic forms (any data)
2. **ModelForm** - Forms tied to models (database)

## UserCreationForm (Built-in)

### Import
```python
from django.contrib.auth.forms import UserCreationForm
```

### What It Provides

```python
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username",)
```

### Fields

**username**
- TextField
- Max 150 characters
- Required
- Validates uniqueness

**password1**
- PasswordInput widget (masked)
- Validates against password validators

**password2**
- Confirmation field
- Must match password1

### Validation

**Built-in checks:**
1. Username not already taken
2. Passwords match
3. Password at least 8 characters
4. Password not too similar to username
5. Password not in common password list
6. Password not all numeric

### Usage

```python
# In view
form = UserCreationForm(request.POST)
if form.is_valid():
    user = form.save()  # Automatically hashes password!
```

### Customizing

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user
```

## AuthenticationForm (Built-in)

### Used By LoginView

```python
from django.contrib.auth.forms import AuthenticationForm
```

### Fields

**username**
- CharField
- Required

**password**
- CharField with PasswordInput
- Required

### Validation

```python
def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    
    if username and password:
        self.user_cache = authenticate(
            self.request,
            username=username,
            password=password
        )
        if self.user_cache is None:
            raise forms.ValidationError("Invalid username or password")
    
    return self.cleaned_data
```

**Checks:**
- Both fields filled in
- Username exists
- Password matches hash
- User account is active

## CommentForm (Custom)

### Location
`blog/forms.py`

### Implementation

### Before Authentication

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')
```

### After Authentication

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)  # Only body - user comes from request
```

### Why Only body?

**The view sets user:**
```python
comment = form.save(commit=False)
comment.user = request.user  # Set from logged-in user
comment.post = post           # Set from URL
comment.save()
```

Form doesn't need to ask for:
- User (comes from `request.user`)
- Post (comes from URL parameter)

**Form only handles:** Comment text

## ModelForm Basics

### Simple Example

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']
```

**Automatically creates fields for:**
- `title` - CharField
- `body` - Textarea
- `categories` - Multiple choice (ManyToMany)

### With Widgets

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'body': 'Post Content',
        }
        help_texts = {
            'title': 'Choose a descriptive title',
        }
```

### Excluding Fields

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'post', 'created_on']
# Same as: fields = ['body']
```

## Form Validation

### Field-level Validation

```python
class UserCreationForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        
        if len(username) < 3:
            raise forms.ValidationError("Username too short")
        
        return username
```

### Form-level Validation

```python
class UserCreationForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
```

### In Views

```python
form = UserCreationForm(request.POST)
if form.is_valid():
    # All validation passed
    user = form.save()
else:
    # form.errors contains error messages
    print(form.errors)
    # Re-render form with errors
```

## Form Rendering Options

### as_p (Paragraphs)

```python
{{ form.as_p }}
```

```html
<p>
    <label for="id_username">Username:</label>
    <input type="text" name="username" id="id_username">
</p>
```

### as_table (Table Rows)

```python
<table>
    {{ form.as_table }}
</table>
```

```html
<tr>
    <th><label for="id_username">Username:</label></th>
    <td><input type="text" name="username" id="id_username"></td>
</tr>
```

### as_ul (List Items)

```python
<ul>
    {{ form.as_ul }}
</ul>
```

```html
<li>
    <label for="id_username">Username:</label>
    <input type="text" name="username" id="id_username">
</li>
```

### Manual Rendering

```django
<form method="post">
    {% csrf_token %}
    
    <div>
        <label for="id_username">Username:</label>
        {{ form.username }}
        {% if form.username.errors %}
            <ul class="errors">
                {% for error in form.username.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <div>
        <label for="id_password">Password:</label>
        {{ form.password }}
        {{ form.password.errors }}
    </div>
    
    <button type="submit">Submit</button>
</form>
```

## Form Fields

### Common Field Types

```python
from django import forms

class ExampleForm(forms.Form):
    # Text
    name = forms.CharField(max_length=100)
    
    # Email
    email = forms.EmailField()
    
    # Number
    age = forms.IntegerField(min_value=0, max_value=120)
    
    # Choice
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    
    # Multiple choice
    interests = forms.MultipleChoiceField(choices=[...])
    
    # Boolean
    agree = forms.BooleanField(required=True)
    
    # Date
    birthday = forms.DateField()
    
    # File
    avatar = forms.ImageField()
```

### Field Arguments

```python
username = forms.CharField(
    max_length=150,
    required=True,
    label="Username",
    help_text="150 characters max",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    initial="",
    error_messages={'required': 'Please enter a username'}
)
```

## Form Processing Pattern

### Standard Flow

```python
def my_view(request):
    if request.method == 'POST':
        # User submitted form
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            # Validation passed
            form.save()  # Or process data
            return redirect('success_page')
        # Validation failed - fall through to render form with errors
    else:
        # User just visiting - show empty form
        form = MyForm()
    
    return render(request, 'form.html', {'form': form})
```

### With Instance (Editing)

```python
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Updates existing comment
            return redirect('blog_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)  # Pre-filled with data
    
    return render(request, 'edit_comment.html', {'form': form})
```

## cleaned_data

After `form.is_valid()`:

```python
form = UserCreationForm(request.POST)
if form.is_valid():
    username = form.cleaned_data['username']  # Validated, cleaned data
    password = form.cleaned_data['password1']
    
    # Or just save the form
    user = form.save()
```

**cleaned_data provides:**
- Validated data
- Converted to Python types (strings, ints, dates)
- Sanitized (XSS protection)

## Form Errors

### Access Errors

```python
if not form.is_valid():
    # All errors
    print(form.errors)
    
    # Specific field
    print(form.errors['username'])
    
    # As JSON
    import json
    print(json.dumps(form.errors))
```

### Display in Template

```django
{% if form.errors %}
    <div class="errors">
        <ul>
            {% for field, errors in form.errors.items %}
                {% for error in errors %}
                    <li>{{ field }}: {{ error }}</li>
                {% endfor %}
            {% endfor %}
        </ul>
    </div>
{% endif %}
```

## Summary

- **UserCreationForm** - Built-in registration form with password validation
- **AuthenticationForm** - Built-in login form
- **ModelForm** - Automatically creates form from model
- Use `fields` or `exclude` to control which model fields appear
- `commit=False` lets you modify before saving
- `form.is_valid()` runs all validation
- `form.cleaned_data` contains validated data
- Forms automatically handle CSRF protection
- Can customize widgets, labels, help text, and error messages
