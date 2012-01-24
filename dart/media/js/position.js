(function($){
     $(function(){

		$("#id_size").change(function(){
		
			if ($("#id_size option:selected").val() == 1){
			
				$(".sizes").removeClass("closed");
				$(".sizes").addClass("open");
			
			}else {
				
				size = $("#id_size option:selected").text().split('|')[1].replace(/ /g,'');
				
				var width = size.split('x')[0];
				var height = size.split('x')[1];
				
				$("#id_width").val(width);
				$("#id_height").val(height);
		
			}
		
		});


     });
 }(django.jQuery));