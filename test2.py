import json



with open('response.json') as f:
  data = json.load(f)

#print(data, '\n\n\n')

print('this is a', type(data))

status = data.get("status")
print(f"\nStatus: {status}\n")
# Print json data using loop 
for key in data:{ 
    print(key,":", data[key])

}


chosen = data.get('result').get('urls')[3].get('url')
print('\n\n\n')
print('chosen url is:', chosen)