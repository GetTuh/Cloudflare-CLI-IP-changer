import requests #install
import json
current_ip = requests.get('https://api.ipify.org').text #Check current IP
print("Extenal IP: " + current_ip)
zone = ""
headers={}

def getDataFromCloudflare():
	response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records', headers=headers) #Getting data using curl(requests)
	return json.loads(response.content)['result']		

response_json= getDataFromCloudflare()
for x in response_json:
	z=0
	dns_ip=x["content"]			#content is the IP
	print("Cloudflare DNS with name "+x["name"]+" status: ")
	while(dns_ip!=current_ip and z<20):					#If the IP of the DNS is different than current IP 
		print("Incorrect IP, changing")
		data = '{"type":"'+x["type"]+'","name":"'+x["name"]+'","content":"'+current_ip+'"}'		#Pasting data with required changes
		response = requests.put('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records/'+x["id"], headers=headers, data=data) #Pushing changes
		dns_response=json.loads(response.content)
		try:
			print(dns_response['error'])
			break
		except:
			dns_ip=dns_response['result']
		z+=1
	else :print("Everything OK")
