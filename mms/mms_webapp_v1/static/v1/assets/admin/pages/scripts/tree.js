var Tree = function () {

	var tree = function () {

		$('#tree').jstree({
			"core" : {
				"themes" : {
					"responsive": false
				}
			},
			"types" : {
				"default" : {
					"icon" : "fa fa-tree icon-state-warning icon-lg"
				},
				"file" : {
					"icon" : "fa fa-tree icon-state-warning icon-lg"
				}
			},
			"plugins": ["types"]
		});

		// handle link clicks in tree nodes(support target="_blank" as well)
		$('#tree').on('select_node.jstree', function(e,data) { 
			var link = $('#' + data.selected).find('a');
			if (link.attr("href") != "#" && link.attr("href") != "javascript:;" && link.attr("href") != "") {
				if (link.attr("target") == "_blank") {
					link.attr("href").target = "_blank";
				}
				document.location.href = link.attr("href");
				return false;
			}
		});
	}

	return {
		//main function to initiate the module
		init: function () {
		tree();
	}
};
}();