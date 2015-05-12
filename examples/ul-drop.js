$(document).ready(function(){


	$(".ul-dropfree").find("li:has(ul)").prepend('<div class="drop"></div>');
	$(".ul-dropfree div.drop").click(function() {
		if ($(this).nextAll("ul").css('display')=='none') {
			$(this).nextAll("ul").slideDown(400);
			$(this).css({'background-position':"-15px 0"});
		} else {
			$(this).nextAll("ul").slideUp(400);
			$(this).css({'background-position':"0 0"});
		}
	});

    $(".ul-dropfree li input").click(function(){
        rec_check(this);
    });

    function rec_check(node) {
        var current = $(node);
        //Check or uncheck all child nodes from this one
        var children = $(node).parent('li').children('ul').children('li').children('input');
        var chk = false;
        if (current[0].checked) {
            chk = true;
            children.attr('checked', 'checked');
        } else {
            children.removeAttr('checked');
        }
        for (var i = 0; i < children.length; i++) {
            children[i].checked = chk;
            rec_check(children[i])
        }

    }

	$(".ul-dropfree").find("ul").slideUp(400).parents("li").children("div.drop").css({'background-position':"0 0"});


	$(".ul-drop").find("li:has(ul)").prepend('<div class="drop"></div>');
	$(".ul-drop div.drop").click(function() {
		if ($(this).nextAll("ul").css('display')=='none') {
			$(this).nextAll("ul").slideDown(400);
			$(this).css({'background-position':"-15px 0"});
		} else {
			$(this).nextAll("ul").slideUp(400);
			$(this).css({'background-position':"0 0"});
		}
	});
	$(".ul-drop").find("ul").slideUp(400).parents("li").children("div.drop").css({'background-position':"0 0"});



    $(".lasttreedrophide").click(function(){
		$("#lasttree").find("ul").slideUp(400).parents("li").children("div.drop").css({'background-position':"0 0"});
	});
    $(".lasttreedropshow").click(function(){
		$("#lasttree").find("ul").slideDown(400).parents("li").children("div.drop").css({'background-position':"-15px 0"});
	});

// получуть все варианты выбора для списка select_box
// и активировать только те, родитель которых id
    function enable_opts(select_box, id) {
        var box = $(select_box);
        var opts = box.children('option');
        // начинаем с 1 - тк 0  - это "Все"
        for(var i = 1; i < opts.length; i++) {
            if (opts[i].getAttribute("par_id") != id) {
                $(opts[i]).remove();
            }
        }
    }

    var $dcs_data = $('select.dcs_sel');
    $dcs_data.data("original_dcs_HTML", $dcs_data.html());

    var $cpo_data = $('select.cpo_sel');
    $cpo_data.data("original_cpo_HTML", $cpo_data.html());


    function update_box(box_id, par_value){
        var box = document.getElementById(box_id);
        switch(par_value){
            case "Все":
                box.selectedIndex = 0;
                box.disabled = true;
                break;
            case "ЦД":
                box.selectedIndex = 0;
                box.disabled = true;
                break;
            case "ДЦУП":
                box.selectedIndex = 0;
                box.disabled = true;
                break;
            default:
                box.selectedIndex = 0;
                box.disabled = false;
                break;
        }
    }

    $("select.dir_sel").change(function(){
        var dcs_box = document.getElementById("dcs_sel");
        var i = this.selectedIndex;
        var dir = this.options[i].value;
        // восстановим варианты выбора ДЦС
        $dcs_data.html($dcs_data.data("original_dcs_HTML"));
        enable_opts(dcs_box, dir);
        update_box("dcs_sel", dir);
        var j = dcs_box.selectedIndex;
        var dcs = dcs_box.options[j].value;
        update_box("cpo_sel", dcs);
    });

    $("select.dcs_sel").change(function(){
        var cpo_box = document.getElementById("cpo_sel");
        var i = this.selectedIndex;
        var dcs = this.options[i].value;
        var dir_box = document.getElementById("dir_sel");
        var j = dir_box.selectedIndex;
        var dir = dir_box.options[j].value;
        $cpo_data.html($cpo_data.data("original_cpo_HTML"));
        enable_opts(cpo_box, dcs+dir);
        update_box("cpo_sel", dcs);
    });

    $("select.cpo_sel").change(function(){

    });
});