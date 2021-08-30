function clickedFace(choice) {
    var data = d3.select(".tweetholder").data()[0]
    
    // call route to give vote to flask 
    if (choice === 'Positive') {
        $.post("/positive_update", data);
    }
    if (choice === 'Negative') {
        $.post( "/negative_update", data);
    }

    // update tweet
    updateTweet();
}

function updateTweet() {
    d3.json("/load_tweet").then(data =>{
        // give data to the tweet and change the tweet text
        d3.select(".tweetholder").data([data]).text(data.tweet)

        // make prediction 
        var prediction;
        if (data.sentiments >= .5) {
            prediction = "POSITIVE"
        }
        else {
            prediction = "NEGATIVE"
        }
        updatePrediction(prediction)
    })
}

function updatePrediction(choice) {
    d3.select(".modelPredict").text(`Our model predicts this tweet has a ${choice} sentiment.`)
}

// grab a tweet when webpage is opened
updateTweet();