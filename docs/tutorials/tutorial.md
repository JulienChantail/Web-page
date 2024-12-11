How to Use the Login Page
This tutorial explains how to interact with the login.html page for the Musicca project.

1. Clone the Repository
First, clone the project repository to your local machine using Git:

bash
Copier le code
git clone https://github.com/your-username/your-project.git
Replace your-username with your actual GitHub username and your-project with the name of the repository.

2. Run the Local Web Server
To view the login.html page locally, you need to run a small web server. At the root of your project, run the following Python script:

bash
Copier le code
python3 ./run_server.py
Make sure you have Python 3 installed on your machine.

3. Compile SCSS to CSS
The project uses SCSS for styling. To compile the SCSS into a CSS file, use the following script:

bash
Copier le code
./compile_css.sh
This will transform the style.scss into the output.css file, which is necessary for styling the page.

4. Access the Login Page
Once the server is running and the styles are compiled, open your browser and go to the following URL:

bash
Copier le code
http://localhost:8000/integration/login.html
This will load the login page in your browser.

5. Interact with the Login Form
On the login page, you will see two fields:

Username: Enter a valid email (e.g., admin@domain.com).
Password: Enter the password (e.g., rainbow).
The form includes validation feedback:

If the username or password fields are empty, a red border will appear around them, indicating that the fields are invalid.
If a valid email format is entered in the username field, and both fields are filled correctly, the borders will turn green, indicating the fields are valid.
You will not be able to submit the form if the fields are invalid.

6. Submit the Form
Once you have filled in the form with the correct information:

Username: admin@domain.com
Password: rainbow
Click the submit button to send the data. If the credentials are correct, you will see a confirmation message.

If the credentials are incorrect, you will be redirected to an error page.

7. Troubleshooting
If the page doesn't load, try the following:

Ensure the Python server is running.
Refresh the page using Ctrl + F5 (or Cmd + Shift + R on macOS) to clear any cache issues.
Check the browser's developer tools for any errors.