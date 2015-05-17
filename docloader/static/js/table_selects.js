/**
 * Created by mac on 11.05.15.
 */


function show_sel(tbl_name, row_num, fields_num,  value){
    for( var i =0; i < fields_num; i++){
        var sels=document.getElementsByName("sel_" + tbl_name + '_' + row_num + '_' + i);
        if( value == "header"){
            sels[0].style.display = "block"
        }else{
            sels[0].style.display = "none"
        }
    }
}
