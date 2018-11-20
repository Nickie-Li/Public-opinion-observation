var cHeight,browserHeight;

window.onload = function () {
    cHeight = document.body.clientHeight;
    browserHeight=document.documentElement.clientHeight;
    setBodyHeight();
    
    if(cHeight<=browserHeight){
        setInterval(setBodyHeight,50);
    }
}

function setBodyHeight(){ 
    cHeight = document.body.clientHeight;
    browserHeight=document.documentElement.clientHeight;

    if(cHeight<=browserHeight){
        document.body.style.height = browserHeight+"px";
    }
    else{
        document.body.style.height ="auto";
    }
}
