# Book-Recommend
Book recommender, rating and shopping web project based on collaborative filtering algorithm

## Environment configuration
-	Python 3.6
-	Flask
-	Mysql 5.7
-	Pymysql
-	Yaml

## Run configuration

1.	Create a new database in mysql, and import the data into the database from book.sql in the decompressed folder

2.	Open the project with pycharm, the configuration file of the database is web/config.yml, change the database password to your own password

3.	Select the running environment of python, and pip install the relevant dependencies in the first step of the environment configuration

4.	Finally, open the app.py file, pull the file to the end, and click the small green arrow to run

5.	There are two different types of users in the system. One is a normal user and the other is an administrator user. The username of an ordinary user is the UserID field of the user table in the database, and the password is the Location field. The administrator username and password are both admin.

## CF Algorithm

### Description

For collaborative filtering, you can read the following blog post: 
https://www.cnblogs.com/NeilZhang/p/9900537.html

Dataset download link (which has a detailed introduction to the dataset): 
http://www2.informatik.uni-freiburg.de/~cziegler/BX/

In this dataset, the User table has 278,858 pieces of data, the Ratings table has 1,149,780 pieces of data, and the Book table has 271,360 pieces of data.

The function of this program is to calculate the 10 recommended books for these users through the collaborative filtering algorithm from the 1 million rating data.

### Class UserCf

#### _cosine_sim()

Calculate Cosine similarity, refer to the blog: https://blog.csdn.net/MassiveStars/article/details/79601666

For example, there are 2 points A and B on the subspace. The AOB triangle is formed with the coordinate origin (0,0), the smaller the degree of the angle AOB, Then it means that the two coordinate points are closer. Substitute this book recommendation above. We understand it this way:
	User A=['Book 1', 'Book 2', 'Book 3']=['1','2','3'] ID represents the number of the book
	User B=['Book 4', 'Book 2', 'Book 6']=['4','2','6'] ID represents the number of the book
	User C=['Book 7', 'Book 8', 'Book 9']=['21','2','6'] ID represents the number of the book

If user A logs in to the website and thinks about a question, do we recommend user B's book, or user C's book to A?
Find cosAOB = X = 26/(3.74*7.48) = 0.92 ; cosAOC = Y = 43/(3.74*21.9) = 0.525
The larger the cos value, the smaller the angle, the more similar. 

Obviously X > Y, then it proves that user B is closer to user A, that is, B's reading interest is similar to that of user A, so We can recommend books read by B to A. We can use this method to get the most similar users, but we can't get the most suitable books for recommendation. This can be in get_topn_items is resolved in this method.

#### _get_top_n_users()

Calculate the top_n users who are most similar to the current user (top_n is 10 at this time)
	:param target_user_id: The currently calculated user ID
	:param top_n: The number of similar users to be calculated
	:return: top_n users most similar to the current user

#### _get_candidates_items()

Find all books in source data and target_user did not meet before.

#### _get_top_n_items()

This function is used to calculate the top_n books with the highest recommendation to the current user

The above 2 methods, relying on the content of the above comments, we get the most similar users, so how do we recommend books among the users?

First we have the ratings of all users for different books, then we can calculate the average score for each book. This as a weight. Then multiply by the similarity of previous users. Then this value takes the example above
        User A=['Book 1', 'Book 2', 'Book 3']=['1','2','3'] ID represents the number of the book
        User B=['Book 4', 'Book 2', 'Book 6']=['4','2','6'] ID represents the number of the book
        User C=['Book 7', 'Book 8', 'Book 9']=['21','2','6'] ID represents the number of the book

User A logs in, he reads 'Book 1', 'Book 2', 'Book 3', assuming that the database only has user A, user B, and user C. It is found that both B and C have common interests with A, that is, read book 2, then we need to push 4, 6, 21, and we need to calculate 4, 6, 21. The recommendation degree is returned to A in order.

So how to calculate it?
First, we found the similarity between A and B and C earlier. This value is multiplied by the average of the book rating data for each book. In this way, 4 and 21 can be directly, and for 6, we need to add the match of B to the match of C (since B and C both rate 6).Finally we get a form as

​        【 Book ID, matching degree 】
​        【xxxxx 1.223】
​        【xxxxx 1.223】
​        【xxxxx 0.423】
​        【xxxxx 1.323】
​        【xxxxx 0.023】
​        【xxxxx 0.000】

We then sort this table and recommend the top TOPN to user A.

#### calculate()

User-Based Collaborative Filtering
         :param target_user_id: User ID
         :param top_n: number of recommended books
         :return: The BookID of the book recommended to the current user is based on the score of the book

#### run()

The run function can perform multi-threaded calculations, call the calculate function to calculate the book recommendation table DF of a single user, and merge the DF into res after the calculation is completed.
     :param i: user number

## App design

| Func                    | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| root()                  | Main page                                                    |
| guess()                 | Real-time recommendation module. Guess you like              |
| recommend()             | Collaborative filtering calculation---recommended book pages |
| loginForm()             | Jump to login page                                           |
| registrationForm()      | Jump to the registration page                                |
| register()              | Registration                                                 |
| is_valid()              | Login authentication                                         |
| login()                 | Login page submission                                        |
| logout()                | Log out                                                      |
| update_recommend_book() | Update recommendation data. If the score exists, judge whether (score+0.5) is greater than 10, and if it is greater, assign the score to 10, otherwise, score+=0.5. If score does not exist, then score=0.5 |
| bookinfo()              | Book Details                                                 |
| user()                  | Personal information                                         |
| search()                | Book Search                                                  |
| rating()                | .html                                                        |
| historical()            | Historical rating                                            |
| order()                 | Check the shopping cart                                      |
| add()                   | Add items to cart                                            |
| delete()                | Delete items in cart                                         |
| editinfo()              | Modify Personal Information                                  |
| editpassword()          | Change account password                                      |
| admin()                 | The main page of the background management page              |
| adminuser()             | Manage User Pages                                            |
| keyword()               | Use keyword to query users                                   |
| delete_user()           | Delete user                                                  |
| adminbook()             | Manage book pages                                            |
| keyword_book()          | Use keyword to query books                                   |
| delete_book()           | Delete books                                                 |
| addbook()               | Add books                                                    |

