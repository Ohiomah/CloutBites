import json

data = [{
    "username": "feastwithfoo",
    "followersCount": 14974.0
},
{
    "username": "tedweitz",
    "followersCount": 148869.0
},
{
    "username": "muslimfoodies",
    "followersCount": 156255.0
},
{
    "username": "brunchnut",
    "followersCount": 78336.0
},
{
    "username": "johnnyeatsnyc",
    "followersCount": 217508.0
},
{
    "username": "allinikkinash",
    "followersCount": 15018.0
},
{
    "username": "outwithair_foodie_nyc",
    "followersCount": 21870.0
},
{
    "username": "piano_pastries",
    "followersCount": 19211.0
},
{
    "username": "elsafoodparadise",
    "followersCount": 115061.0
},
{
    "username": "spinx17",
    "followersCount": 16409.0
},
{
    "username": "jerica.feasts",
    "followersCount": 45414.0
},
{
    "username": "nycfoodie.nyc",
    "followersCount": 22249.0
},
{
    "username": "thequeenfoodie",
    "followersCount": 69161.0
},
{
    "username": "fahfahji",
    "followersCount": 21476.0
},
{
    "username": "comicsinmybirkin",
    "followersCount": 21167.0
},
{
    "username": "tofueeats",
    "followersCount": 10135.0
},
{
    "username": "nycmouth",
    "followersCount": 42102.0
},
{
    "username": "chungeats",
    "followersCount": 111757.0
},
{
    "username": "cindy_food_drink",
    "followersCount": 483786.0
},
{
    "username": "maxhoffmann",
    "followersCount": 146864.0
},
{
    "username": "__poshhh",
    "followersCount": 91343.0
},
{
    "username": "ms_new_foodie",
    "followersCount": 37700.0
},
{
    "username": "theeoverthinker",
    "followersCount": 11347.0
},
{
    "username": "worldeatsjen",
    "followersCount": 13250.0
},
{
    "username": "travelicious_d",
    "followersCount": 25986.0
},
{
    "username": "food_ilysm",
    "followersCount": 221384.0
},
{
    "username": "fooddrinksnyc",
    "followersCount": 23884.0
},
{
    "username": "itsasugarhighh",
    "followersCount": 12187.0
},
{
    "username": "taleitalei",
    "followersCount": 31845.0
},
{
    "username": "tastynybites",
    "followersCount": 40882.0
},
{
    "username": "whatsgoinganh",
    "followersCount": 37570.0
},
{
    "username": "foodieguynyc",
    "followersCount": 17604.0
},
{
    "username": "thehungryskipper",
    "followersCount": 23239.0
},
{
    "username": "bao_buddy",
    "followersCount": 48365.0
},
{
    "username": "foodieee.nycc",
    "followersCount": 24345.0
},
{
    "username": "the_fork_lift",
    "followersCount": 36086.0
},
{
    "username": "kosherjunkie",
    "followersCount": 21447.0
},
{
    "username": "airlinkadventures",
    "followersCount": 31412.0
},
{
    "username": "glamorousgrub",
    "followersCount": 16421.0
},
{
    "username": "kaitsplatess",
    "followersCount": 11928.0
},
{
    "username": "ariels_eats",
    "followersCount": 25385.0
},
{
    "username": "newyorkcity.adventures",
    "followersCount": 113328.0
},
{
    "username": "nychungry",
    "followersCount": 63002.0
},
{
    "username": "skirtsteak.nyc",
    "followersCount": 71490.0
},
{
    "username": "raicescolombianasnyc",
    "followersCount": 14555.0
},
{
    "username": "theexcursiondoctor",
    "followersCount": 120047.0
},
{
    "username": "pergolanyc",
    "followersCount": 52951.0
},
{
    "username": "hungryhippie_",
    "followersCount": 32700.0
},
{
    "username": "casalafemmenyc",
    "followersCount": 287538.0
},
{
    "username": "marivannanyc",
    "followersCount": 19183.0
},
{
    "username": "carrasnyc",
    "followersCount": 43034.0
},
{
    "username": "beijaflorlic",
    "followersCount": 11145.0
},
{
    "username": "loveskitchennyc",
    "followersCount": 13845.0
},
{
    "username": "dkrestaurantnyc",
    "followersCount": 10640.0
},
{
    "username": "aanganrestaurantnyc",
    "followersCount": 11941.0
},
{
    "username": "beijaflorlic",
    "followersCount": 11145.0
},
{
    "username": "loveskitchennyc",
    "followersCount": 13845.0
},
{
    "username": "aanganrestaurantnyc",
    "followersCount": 11941.0
},
{
    "username": "kosherjunkie",
    "followersCount": 21447.0
}]

# put length of data in a file

with open("data.json", "w") as file:
    json.dump(len(data), file)
    print("Data has been written to file")
    
    
    
    
    
    