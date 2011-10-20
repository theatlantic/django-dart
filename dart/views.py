from coffin.shortcuts import render_to_response
from coffin.template import RequestContext

def ad(request, ad_url):
	"""Function to display an ad.  Currently customized for the thankyou for sharing iframe ad."""
	# truncating this so it can't be passed an arbitrarily long string
	ad_url = 'http://ad.doubleclick.net/adj/'+ad_url[:500]
	return render_to_response("dart/sharing_iframe.html", {'ad_url':ad_url}, context_instance=RequestContext(request))

