/**
 * Created by mac on 11.05.15.
 */


function show_sel(name, value){
    var sels=document.getElementsByName("sel_" + name);
    for( var i = 0; i < sels.length; i++){
        if( value == "header"){
            sels[i].style.display = "block"
        }else{
            sels[i].style.display = "none"
        }

    }
}
