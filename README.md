# Twitter Sentiment Analysis Model

created by Danielle Martin, Jordan Roessle, Robert Gramlich, Sunwoo Kim

![Twitter Sentiment Image](https://miro.medium.com/max/1400/1*0P55fknrgWKxG0gfwAGCvw.png)

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

## Project Description

The Sentiment Analysis Model project aims to create a neural network that can predict the sentiment (positive - 1 or negative - 0) of tweets from Twitter. The model is trained and tested on a IMDB movie reviews dataset with prescribed positive or negative rankings. This model is then paired with Twitter's API to make sentiment predictions on tweets. 

Our Sentiment Analysis application includes a level of interactivity through Flask and JavaScript D3. Each tweet that is classified by the user is then pushed along with the classification and time stamp into a SQL database. This data is stored and will later be used to retrain the model to improve its predictive power.



## Data

* [IMDB Movie Review Dataset](http://ai.stanford.edu/~amaas/data/sentiment/) -- Citation: Maas, Andrew L., et al. “Learning Word Vectors for Sentiment Analysis.” Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies, June 2011, pp. 142–150., www.aclweb.org/anthology/P11-1015. 

* [Twitter API](https://developer.twitter.com/en/docs)

### Built With

* PostgreSQL/SQLAlchemy
* Pandas - tensorflow
* Flask
* HTML
* JavaScript - D3

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sunwoo-kim20/sentiment-analysis-final-project.git
   ```
2. Set up PostgreSQL database and establish connection 
   ```sh
   rds_connection_string = "postgres:password@localhost:5432/sentiment_db"
   engine = create_engine(f'postgresql://{rds_connection_string}')
   conn = engine.connect()
   session = Session(bind=engine)
   ```



<!-- USAGE EXAMPLES -->
## Usage

User grabs a tweet by giving the keyword selection an input. Once the tweet has been loaded onto the webpage, the user selects whether they consider the tweet to be positive or negative in sentiment. The model then makes a prediction on the same tweet thereafter to compare to the user's selection. 

![Screenshot of Sentiment Analysis Application](https://github.com/sunwoo-kim20/sentiment-analysis-final-project/blob/main/static/images/voting_page.png?raw=true)


![Screenshot of Neural Network Structure](https://github.com/sunwoo-kim20/sentiment-analysis-final-project/blob/main/static/images/the_model.PNG?raw=true)



<!-- CONTACT -->
## Contact


[Project Link](https://github.com/sunwoo-kim20/sentiment-analysis-final-project)

