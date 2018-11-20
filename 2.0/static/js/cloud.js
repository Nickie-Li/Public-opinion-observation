
function wCloud(jData){
    jlist = [];
    for (var i=0;i<jData.length;i++) {
        jlist.push([jData[i].words, jData[i].wordsCount]);
    }
    var options = eval({
        "list": [jlist],
        "gridSize": 16, // size of the grid in pixels
        "weightFactor": 10, // number to multiply for size of each word in the list
        "fontWeight": 'normal', // 'normal', 'bold' or a callback
        "fontFamily": 'Microsoft JhengHei', // font to use
        "color": 'random-light', // 'random-dark' or 'random-light'
        "backgroundColor": '#333', // the color of canvas
        "rotateRatio": 1 // probability for the word to rotate. 1 means always rotate
    });
    var canvas = document.getElementById('word_cloud');
    WordCloud(canvas, options);
}