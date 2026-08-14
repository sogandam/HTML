function validateRegisterForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (!email.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)) {
        alert('Geçersiz e-posta adresi!');
        return false;
    }
    if (password.length < 8) {
        alert('Şifre en az 8 karakter olmalidir!');
        return false;
    }
    localStorage.setItem('user', JSON.stringify({
        name: document.getElementById('name').value,
        surname: document.getElementById('surname').value,
        email: email,
        username: document.getElementById('username').value,
        password: password
    }));
    alert('Kayit başarili!');
    return true;
}

function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.username === username && user.password === password) {
        sessionStorage.setItem('loggedIn', 'true');
        alert('Giriş başarili!');
        window.location.href = 'profile.html';
    } else {
        alert('Kullanici adi veya şifre yanliş!');
    }
    return false;
}

function logoutUser() {
    sessionStorage.clear();
    alert('Çikiş yapildi.');
    window.location.href = 'index.html';
}

function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const user = JSON.parse(localStorage.getItem('user'));
    if (user.password === currentPassword) {
        user.password = newPassword;
        localStorage.setItem('user', JSON.stringify(user));
        alert('Şifre başariyla değiştirildi!');
    } else {
        alert('Mevcut şifre yanliş!');
    }
    return false;
}

function loadProfile() {
    const user = JSON.parse(localStorage.getItem('user'));
    document.getElementById('profileName').textContent = user.name;
    document.getElementById('profileSurname').textContent = user.surname;
    document.getElementById('profileEmail').textContent = user.email;
}
