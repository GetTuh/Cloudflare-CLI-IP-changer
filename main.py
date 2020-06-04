import requests #install
import json
current_ip = requests.get('https://api.ipify.org').text #pobiera zewnetrzne IP
print("Extenal IP: " + current_ip)
zone = ""
headers={}
def getDataFromCloudflare():
	response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records', headers=headers) #Pobieranie danych przy uzyciu curl(requests)
	return json.loads(response.content)['result']		#nie interesuje mnie nic poza wynikami lol

response_json= getDataFromCloudflare()
for x in response_json:
	z=0
	dns_ip=x["content"]			#content to IP. Czemu? Nie wiem kurwa
	print("Cloudflare DNS with name "+x["name"]+" status: ")
	while(dns_ip!=current_ip and z<20):					#Jezeli IP na ktore wskazuje serwer jest rozne od tego ktory jest teraz 
		print("Incorrect IP, changing")
		data = '{"type":"'+x["type"]+'","name":"'+x["name"]+'","content":"'+current_ip+'"}'		#API wymaga typu, nazwy oraz IP ale poniewaz zmieniam tylko IP reszte wklejam z pobranych wczesniej danych
		response = requests.put('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records/'+x["id"], headers=headers, data=data) #zmienam dane przy uzyciu API
		dns_response=json.loads(response.content)
		try:
			dns_response['error']
			print(dns_response['error'])
			break
		except:
			dns_ip=dns_response['result']
		z+=1
	else :print("Everything OK")
