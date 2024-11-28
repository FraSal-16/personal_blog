from django.shortcuts import get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Post
from .forms import PostForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Imposta l'autore
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Controlla se l'utente è l'autore del post o un superuser
    if request.user != post.author and not request.user.is_superuser:
        return render(request, 'blog/not_authorized.html')  # Reindirizza alla pagina di errore

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post modificato con successo!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Controlla se l'utente è l'autore del post o un superuser
    if request.user != post.author and not request.user.is_superuser:
        return render(request, 'blog/not_authorized_delete.html')  # Reindirizza alla pagina di errore

    if request.method == 'POST':
        post.delete()
        #messages.success(request, "Post eliminato con successo!")
        return redirect('post_list')  # Reindirizza alla lista dei post

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def index(request):
    return render(request, 'blog/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            #messages.warning(request, "Le password non corrispondono.")
            return redirect('register')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            #messages.success(request, "Registrazione avvenuta con successo!")
            return redirect('success')
        except Exception as e:
            #messages.error(request, "Errore nella registrazione: " + str(e))
            return redirect('register')

    return render(request, 'blog/register.html')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Accesso avvenuto con successo!")
#             return redirect('home')  # Modifica l'URL in base alla tua configurazione
#         else:
#             messages.error(request, "Nome utente o password errati.")
#             return redirect('user_login')  # Modifica l'URL in base alla tua configurazione

#     return render(request, 'blog/login.html')  # Assicurati che il percorso sia corretto

def user_login(request):
    if request.user.is_authenticated:
        # Reindirizza a una pagina informativa se l'utente è già loggato
        return redirect('already_logged_in')  # Assicurati di avere questa vista configurata
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login effettuato con successo.")
            return redirect('home')
        else:
            messages.error(request, "Credenziali non valide. Riprova.")
    
    return render(request, 'blog/login.html')

def after_log_out(request):
    print("Request method:", request.method)  # Debug
    print("User authenticated:", request.user.is_authenticated)  # Debug

    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)  # Esegui il logout dell'utente
            return render(request, 'blog/logged_out.html')  # Reindirizza alla pagina di logout personalizzata
        else:
            return render(request, 'blog/not_logged_in.html')  # Mostra la pagina di avviso se non c'è nessuno loggato
    else:
        return render(request, 'blog/not_logged_in.html')  # Se non è una richiesta POST, mostra la pagina di avviso
    
def not_logged_in(request):
    return render(request, 'blog/not_logged_in.html')

def success(request):
    return render(request, 'blog/success.html')