import requests, pandas, json, os

api_key= os.environ["api_key"]
filters='&frequency=annual&data[0]=consumption-for-eg-btu&data[1]=total-consumption-btu&facets[sectorid][]=99&facets[fueltypeid][]=ALL&facets[fueltypeid][]=AOR&facets[fueltypeid][]=FOS&facets[fueltypeid][]=REN&facets[location][]=AK&facets[location][]=AL&facets[location][]=AR&facets[location][]=AZ&facets[location][]=CA&facets[location][]=CO&facets[location][]=CT&facets[location][]=DC&facets[location][]=DE&facets[location][]=FL&facets[location][]=GA&facets[location][]=HI&facets[location][]=IA&facets[location][]=ID&facets[location][]=IL&facets[location][]=IN&facets[location][]=KS&facets[location][]=KY&facets[location][]=LA&facets[location][]=MA&facets[location][]=MD&facets[location][]=ME&facets[location][]=MI&facets[location][]=MN&facets[location][]=MO&facets[location][]=MS&facets[location][]=MT&facets[location][]=NC&facets[location][]=ND&facets[location][]=NE&facets[location][]=NH&facets[location][]=NJ&facets[location][]=NM&facets[location][]=NV&facets[location][]=NY&facets[location][]=OH&facets[location][]=OK&facets[location][]=OR&facets[location][]=PA&facets[location][]=PR&facets[location][]=RI&facets[location][]=SC&facets[location][]=SD&facets[location][]=TN&facets[location][]=TX&facets[location][]=UT&facets[location][]=VA&facets[location][]=VT&facets[location][]=WA&facets[location][]=WI&facets[location][]=WV&facets[location][]=WY&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
response = requests.get("https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key="+api_key+filters)
data = response.json()
with open('output.txt','w') as f:
        json.dump(data, f, indent=4)
df = pandas.DataFrame(data['response']['data'])
df['year'] = df['year'].astype(int)
df['location'] = df['location'].astype(str)
df['consumption-for-eg-btu'] = df['consumption-for-eg-btu'].astype(float)
df['fueltypeid'] = df['fueltypeid'].astype(str)
df['total-consumption-btu'] = df['total-consumption-btu'].astype(float)

print(df['total-consumption-btu-units'].unique())
print(df['consumption-for-eg-btu-units'].unique())

print(df.head())
print(df.dtypes)
print(df.info())

