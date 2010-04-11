var state = {};

function zoomIn() {
    var w = $("table").css('width'),
	h = $("table").css('height');
    $("table").css('width', parseInt(w)*2 + "px");
    $("table").css('height', parseInt(h)*2 + "px");
};

function zoomOut() {
    var w = $("table").css('width'),
	h = $("table").css('height');
    $("table").css('width', parseInt(w)/2 + "px");
    $("table").css('height', parseInt(h)/2 + "px");
};

function findCellCoordinates(cell) {
    var afterMe = $(cell).nextAll("td");
    var onMyRow = $(cell).siblings("td");
    var myX = onMyRow.length - afterMe.length;
    
    afterMe = $(cell).parent("tr").nextAll("tr");
    onMyRow = $(cell).parent("tr").siblings("tr");
    var myY = onMyRow.length - afterMe.length;

    return {col: myX, row: myY};
};

function stepsBack(x, y) {
    //var cur = state[x+':'+y];
    //if( typeof(cur) != 'undefined' )
    //return parseInt(cur);
    return parseInt($.jqURL.get(x+':'+y)) || 0;
};

function rewindBit() {
    var pos = findCellCoordinates(this);
    var x = pos.col, y = pos.row;
    var r = stepsBack(x, y);
    var key = '' + x + ':' + y;
    var hash = {};
    hash[key] = r+1;
    var href = $.jqURL.set(hash);
    window.location = href;
    $.get(href, function(res) { rebuild(res, key, r) });
};

function rebuild(res, key, r) {
    $("table").html(res);
    $("td").click(rewindBit);
    //    state[key] = r+1;
};

$(window).keydown(function(e) {
	if( e.which == 65 ) zoomIn();
	if( e.which == 68 ) zoomOut();
    });

var mousedown = 0;
$(window).load(function() {
	$("<button>Zoom in</button>").click(zoomIn).appendTo("body");
	$("<button>Zoom out</button>").click(zoomOut).appendTo("body");
	$("<input id='color' value='blue'/>").appendTo("body");
	$("td").click(rewindBit);
	$(window).mousedown(function() { mousedown = 1; });
	$(window).mouseup(function() { mousedown = 0; });
	$("td").mouseover(function() {
		if( !mousedown ) return;
		var color = $("#color").val();
		$(this).css("backgroundColor", color);
	    });
    });