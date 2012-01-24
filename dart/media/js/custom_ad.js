(function($){
     $(function(){

		if (typeof(CKEDITOR) != "undefined"){
			CKEDITOR.replace("id_embed", {
				"filebrowserWindowWidth": 940, 
				"filebrowserBrowseUrl": "/admin/filebrowser/browse/?pop=3&type=Image", 
				"filebrowserUploadUrl": "/ckeditor/upload/", 
				"height": 150, 
				"width": 760, 
				"skin": "kama", 
				"filebrowserWindowHeight": 147, 
				"toolbar": [ ["Source", "Bold", "Italic", "Font", "FontSize", "Strike", "Subscript", "Superscript", "RemoveFormat" , "Link", "Unlink", "Anchor"] ],
				"autoParagraph":false,
				"enterMode" : CKEDITOR.ENTER_BR
			});
		}
		

     });
}(django.jQuery));