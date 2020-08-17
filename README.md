![image](https://user-images.githubusercontent.com/1292230/90389392-29d6a000-e092-11ea-8752-eb5a935ec1e1.png)

Amazon reviews summarisation engine and user interface. [Hackathon Juction 2017](https://devpost.com/software/reviewsmark)

##Inspiration
We picked AI summarizing text track because we think it is challenged work and we came up with the idea of making something useful in the real world. We want to build a tool of summarizing Amazon reviews which will benefit both customers and sellers.

##What it does
Given a URL of an Amazon product, our tool will summarize its positive and negative reviews made by customers. The outcome will be a list of pros and cons of the product.

##How we built it
First, we use ´beautiful soup´ package to get all the reviews from the HTML file which contains all the information about the product we are analyzing.

Then, we train 2 word2vec models which are positive model and negative model respectively

Finally, we use K-means method to do clustering and find the centroids of clusters and the centroids are the representatives of the positive and negative reviews separately

##Challenges we ran into
Considering our background, we figure out how to build an efficient model. Part of a team learned new technologies in a short time and how to adapt it to our solution.

##Accomplishments that we're proud of
We are proud of having built a functional tool which could be used on any on-line shopping website.

##What we learned
We learned flask. Got more experience at python programming language.

##What's next for ReviewsMark
The next step would be to build a chrome extension which implements the same functionalities.

##Built With
flask
python

Try it out!
