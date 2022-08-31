Blog Project.

* Create Customized Adminstration site For Blog app.

* create superuser for the Adminstration (Blogger).

* Design Schama and Model of the Blog.

* Post:
  * Post should have a title, slug, author, body, publish ,created, updated, status.

  * Publish: the datetime indicates when the post was published.

  * created: the datetime iindicates when the post was created.

  * updated: the datetime indicates the last time the post was updated.

  * status : have two choices ( Draft, Published)

* Structure The app with Model-View-Template (MVT) Design Pattern.

* Create View for all Posts in the Blog.

* Create View for each Post.

* Create custom Manger to retrive only Published Posts.

* Post will be Created From the Blogger (Admin) site 

* Create a comments system.

  * use Django Forms to submit the comment for each Posts.

  * Forms content: name,email,body,created time, updated time, active.

  * each email can submit a comment each 30s to prevent spamming bots.

  * Detect and censor bad words.

* Create Templates to view all Posts and comments.

* Posts Page

  * use django pagination to show only 3 Posts in each Page.

  * If we click on a post it should go to Post-detail page.

* Post-details

  * Show the Post detail

  * Show all prevoius comments

  * Show form to sumbit new comment


* User system
  * Create user system ( login, logout, register, forget password).
  * Create add/edit post views
    * Each user can edit his own post only.
    * Put the <add post>, login/logout in the header.

* API Utilization
  * Utilize muffin_example API to feed the blog with Users/Posts/Comments.
  * Make a distinction between the posts from your blog and the one comming from the API.
   

* Blog API
  * Create an API for the Blog models.
  * Create serializers for each models.
  * Create an API endpoints.
  * Use the Token Authentication to Auth Read/Write operation.
    * Only authenticated users can add posts.
    * Only authenticeted author user can edit the posts that he/she created.
    
  * Gust User ( Anonymous User).
    * Can't read/write Users.
    * Can read-only the post ( can't add/edit).
    * Can read/create Comments.
    
  * API Utilizer client (script).
    * Create a small script that utilize the Blog API.

