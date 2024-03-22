## Web Scraping Academy Application
You are expected to develop a database where the information of academic publications searched by web scraping method through academic search engines such as Dergi Park is saved, as well as a web interface that will allow this information to be searched, displayed and queried according to the desired features.

<b>Objective:</b> The project aims to provide access to information from a web page with web scraping, use MongoDB database and Elasticsearch query structures and develop web coding skills.

<b>Programming Language:</b> MongoDB and Elasticsearch structure should be used for the project database and queries. The web interface will be created using a desired web programming language.

The project consists of 3 main parts detailed below:

1. Web Scraping:
   
• The information of at least the first 10 academic publications listed according to the keywords to be entered by the user using web scraping from at least one academic search engine should be displayed on the web page you will create. The keywords that the user will use to search will be entered through a text field on your own web page.

• For web scraping, the desired data should be accessed by using the html information of the site or by making a request request to the site. (Ready-made web APIs for the site to be accessed should not be used.)

• Information about the requested publication can be obtained directly from the page of the academic search engine or from another web page that will be redirected via the link on the search engine page. (Bonus points will be awarded for web scraping by switching to secondary sites).

• The pdf file must be downloaded for each requested publication. Then, depending on preference, the publication information can be obtained either from the web page or from the content of the downloaded pdf file.

2. Database
   
• The data obtained by web scraping will be saved in the database using MongoDb.

• The information that should be kept in the database is as follows:

Publication id,  
Publication name,  
Names of authors,  
Type of publication (research article, review, conference, book, etc.),  
Date of publication,  
Name of the publisher (name of the conference where the publication was published; journal or book publishing house),  
Keywords (searched in the search engine),  
Keywords (for the article),  
Summary,  
References,  
Number of citations,  
Doi number (if available),  
URL address  

3. Web Page:
   
• You are expected to create a web page to display the information of the accessed publications to the user.

• A text field should be created for the publications to be searched on the web page and the relevant search engine should be enabled to search for the publications and bring their information to the web page through the keywords to be entered in this text field.

• When the web page is first opened, all records in the database should be brought to the page.

• In the listing process, the names of the publications should be listed in the proper order. When clicking on a listed article name, information specific to that article should be displayed on a separate page.

• It should be possible to perform a dynamic search for any study from the web page. In addition, in case of a spelling mistake during the search, the system should provide a corrected suggestion. Example: deep learning -- you see the corrected results: deep learning.

• The dynamic filtering process should also be included on the web page. The filtering process should be applicable both separately and together for all features of the publication in the database.

• It should be possible to sort according to the date of the most recent or earliest publication on the web page, and it should also be possible to sort according to the number of citations as the least or most.

### Development Process  

***I developed this project using flask, mongoDB and elasticsearch.***
