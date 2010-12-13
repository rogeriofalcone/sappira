$(document).ready(function() {
	// Sizing Functions
	
	$(".hidse").hide();
	
	$("textarea").each(function() {
		//FIXME Inelegant Solution
		$(this).width(($(this).parent(".unit-content").outerWidth())-22);
		$(this).autoResize({
			extraSpace: 10,
		});
		$(this).keyup();
	});	

	$(".submit").click(function() {
	  $(this).closest("form").submit();
	});

	$("li, dd").live("click", function(event){
		$(this).next(".hide").toggle("blind");
	});
/*
	$("#prescription-list li, #problem-list li").live("mouseenter", function(event){
		$(this).children(".button").show();
	});
	$("#prescription-list li, #problem-list li").live("mouseleave", function(event){
		$(this).children(".button").hide();
	});
*/	
	$("#problem-add-form").live("keypress", function (e) {
	   if ( e.keyCode == 13 ){
			e.preventDefault();
			$.post(
				"/ajax/problem/add/", 
				$(this).closest("form").serialize(),			 
				function(html_data){
					$("#problem-list").html(html_data);
				}
			);
			$("#problem-add-form").get(0).reset();
		}
	});

	$("#prescription-add-form").live("keypress", function (e) {
		$("#ajax_medication").autocomplete({
			source: "/ajax/medication/",
			minLength: 3,
			select: function(event, ui) {
				}
		});
		if ( e.keyCode == 13 ){
			e.preventDefault();
			$.post(
				"/ajax/prescription/add/", 
				$(this).closest("form").serialize(),			 
				function(html_data){
					$("#prescription-list").html(html_data);
								$("#problem").focus();
				}
			);
			$("#prescription-add-form").get(0).reset();
		}
	});
	
	// FIXME should be done as CSS pseudoclasses not javascript
	$("input, textarea").live("mouseenter mouseleave", function(event){
		$(this).toggleClass("highlight");
	});
	
	$(".prescription-stop").live("click", function(){
		$.post(
			"/prescription/stop/", 
			$(this).closest("form").serialize(),			 
			function(html_data){
				$("#prescription-list").html(html_data);
			}
		);
	});
	
	$("#problem-add").live("click", function(){
		$.post(
			"/problem/add/", 
			$(this).closest("form").serialize(),			 
			function(html_data){
				$("#problem-list").html(html_data);
			}
		);
	});
	
	$(".problem-stop").live("click", function(){
		patient = $(this).siblings(".patient-value").val();
		$.post(
			"/problem/stop/", 
			$(this).closest("form").serialize(),			 
			function(html_data){
				$("#problem-list").html(html_data);
			}
		);
	});
});