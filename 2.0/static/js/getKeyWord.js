
// we will get url like this:"/tag?tag=你好&freq=1"
//aryPara's data --> aryPara[0]=tag  aryPara[1]=freq

function getKey(){
    var strUrl = location.search;
    var getPara, ParaVal;
    var aryPara = [];
    
    if (strUrl.indexOf("?") != -1) {
        var getSearch=strUrl.split('?');
        getPara=getSearch[1].split('&');
        for(i=0; i<getPara.length; i++){
            ParaVal=getPara[i].split('=');
            aryPara.push(paraVal[1]);
        }
    }
    return aryPra
}

