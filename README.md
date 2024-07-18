<h1>Free HRMS</h1>

<h2> Introduction </h2>

Free HRM is a free and open-source Human Resource Management System. It is a web-based application that allows you to manage your employees, payroll, and other HR-related tasks. It is built using the Django web framework and is designed to be easy to use and customize. The intent was to have a simple and easy-to-use HRMS that can be used by small and medium-sized businesses, and is free from clutter.
The technology stack used in this project is:
- Django
- HTML
- CSS
- JavaScript
- Bootstrap 5 with themes from https://bootswatch.com/
- SQLite

The main programming language used is Python, and the database used is SQLite. The project is hosted on GitHub and is free to use and modify.
The project is database-agnostic, and can be easily modified to use other databases like PostgreSQL, MySQL, or Oracle.
Python allows for easy integration with other systems and APIs, and the Django framework provides a robust and secure platform for building web applications. Python is also the preferred language for data science and machine learning, so the project can be easily extended to include data analytics and other advanced features.
The project is still in development, and new features are being added regularly. If you have any suggestions or feedback, please feel free to open an issue or submit a pull request.

***

<h2>Installation, Features, and Usage</h2>
Below are the instructions you can place in your `README.md` for users to install and run your project, including loading sample data using `db.json` fixtures.

---

## Installation and Running the Project

### Prerequisites

- Python (3.8 or newer)
- Django (3.2 or newer)
- Git

### Installation Steps

1. **Clone the Repository**

   First, clone the repository to your local machine using Git.

   ```bash
   git clone https://github.com/yourusername/yourprojectname.git
   cd yourprojectname
   ```

2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment for Python projects. This keeps dependencies required by different projects separate. To set up a virtual environment, run:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   Install the project dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**

   Before running the application, you'll need to apply migrations to set up the database schema:

   ```bash
   python manage.py migrate
   ```

5. **Load Sample Data**

   To load sample data into the database, use the `db.json` fixtures file:

   ```bash
   python manage.py loaddata db.json
   ```

### Running the Project

1. **Start the Development Server**

   You can start the Django development server using:

   ```bash
   python manage.py runserver
   ```

2. **Access the Application**

   Once the server is running, you can access the application by navigating to `http://127.0.0.1:8000/` in your web browser.

### Additional Information

- To access the admin panel, navigate to `http://127.0.0.1:8000/admin/`. You may need to create a superuser account if you haven't already:

  ```bash
  python manage.py createsuperuser
  ```

- For further customization and development, refer to the Django documentation: https://docs.djangoproject.com/

---

Feel free to adjust the instructions based on your specific project setup or additional requirements.

<h2>License</h2>

The project is licensed under the GPL v3 License. This means that you are free to use, modify, and distribute the software as long as you provide the source code and include the GPL v3 License with any distribution. You can read more about the GPL v3 License here: https://www.gnu.org/licenses/gpl-3.0.en.html
For advancement developments, please visit the website: https://freehrm.com/


<h2>Additional Resources</h2>

* https://github.com/iamswaroopp/django-scaffold-generator/tree/master
* https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
* https://www.javatpoint.com/django-crud-application
* https://testdriven.io/blog/django-permissions/
* https://getbootstrap.com/docs/4.0/components/navbar/
* https://dev.to/codeply/bootstrap-5-sidebar-examples-38pb
* https://djangosource.com/django-csv-upload
* https://github.com/marcanuy/django-dynamic-breadcrumbs
* pip install django-filter
* https://pypi.org/project/django-bootstrap-v5/
* https://github.com/clearspark/django-monthfield

