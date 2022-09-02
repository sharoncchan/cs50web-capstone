# Capstone Project

My capstone project is a web application of a blogging community for developers. Users are able to register for an account for this web application. They can view all the articles posted by other users, and also post articles to teach others on topics such as HTML, CSS , Javascript and Python. Users are able to edit the articles which they have published, "like and unlike" other users' articles and write and reply to comments in the discussion section of each article. They are also able to save articles to their bookmarks for their future reading.
Users who are not logged in will not be able to like or bookmark articles and will be prompted to log in or sign up.

This project was built using Django as a backend framework and HTML, CSS , Bootstrap and JavaScript as frontend programming tools. All generated details are saved in a database, which is SQLite by default.

All webpages of the project are mobile-responsive.

#### Features of the project

This project contains the features below:

- Allows users to post their content of their aricles in markdown format which will be converted and displayed as HTML using the markdown package
- Utilizes the Django MPTT (Modified Preorder Tree Transversal) to create the models and interface for user to comment and reply to other user's comments
- Boostrap features such as modal forms is tapped on to prompt users to log in or sign up if they are not logged in and attempt to like or bookmark an article
- Using Javascript, user can like/bookmark/edit and save an article without refreshing the page and the color of these icons change accordingly to signify the change made
- Utilizes the Waypoints library to implement infinite scrolling. Posts are loaded as the user scrolls down the page

#### Running the application

- Install project dependencies by running `pip install -r requirements.txt`. Dependencies include Markdown , Django and Django MPTT module that allows Django to work with nested comments and replies.
- Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
- Create superuser with `python manage.py createsuperuser`. This will create a user with admin privileges, with permissions to create, read, update and delete data in the Django admin
- Run the django server using `python manage.py runserver` to enter the homepage of the web application.

#### Files and directories

- `blog` - main application directory.

  - `static/blog` contains all static content.
    - `css` contains compiled CSS file
    - `index.js` - script that run in all the templates
  - `templates/blog` contains all application templates.

    - `layout.html` - Base templates. Other templates extend it.
    - `register.html` - The page that show the register page for user to register for a new account
    - `login.html` - The page that show the login page for user to log in
    - `index.html` - The homepage of the webpage, displays all the articles that users have published
    - `create.html` - The page for user to publish an article, by inputting details such as title, category , the content of the article, image and the reading duration
    - `post.html` - The page that show the individual article that is published, user can like the article. Under the discussion section, user can comment and reply to other comments.
    - `bookmarks.html` - The page that show all the articles the user has saved in their bookmarks list
    - `category.html` - The page that show all the articles under each category
    - `profile.html` - The page that show the details of an individual user such as all the articles they have published and the number of articles they have published

  - `admin.py` -admin settings for model view
  - `forms.py` - contains the django form for the Comment model
  - `models.py` contains the four models that I have used in the project- User, Category, Post and Comment
  - `urls.py` - contains all application URLs.
  - `views.py` contains all application views.

My project's video : https://www.youtube.com/watch?v=981zmf09S80
