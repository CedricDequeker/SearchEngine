/*--------------------------------------------------*/
/* Dark & White Theme */

const themeBtn = document.getElementById('theme-btn');
const currentTheme = localStorage.getItem('theme') || 'light';

if (currentTheme === 'dark') {
    document.body.classList.add('dark-theme');
    themeBtn.textContent = 'White Theme';
}

themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    if (document.body.classList.contains('dark-theme')) {
        themeBtn.textContent = 'White Theme';
        localStorage.setItem('theme', 'dark');
    } else {
        themeBtn.textContent = 'Dark Theme';
        localStorage.setItem('theme', 'light');
    }
});


/*--------------------------------------------------*/
/* Side bar */

let btn = document.querySelector("#btn");
        let sidebar = document.querySelector(".sidebar");
    
        btn.onclick = function() {
            sidebar.classList.toggle("active");
        }


/*--------------------------------------------------*/
/* Contact Pop up */

document.getElementById('contact-link').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('contact-popup').style.display = 'block';
});

document.getElementById('close-btn').addEventListener('click', function() {
    document.getElementById('contact-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('contact-popup')) {
        document.getElementById('contact-popup').style.display = 'none';
    }
});


/*--------------------------------------------------*/
/* Search code */
const sendBtn = document.getElementById('send-btn');
const inputField = document.querySelector('.input-container input');

sendBtn.addEventListener('click', () => {
    const userInput = inputField.value;
    console.log(userInput);

    fetch('/process_query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
