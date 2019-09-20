import gmplot

# Initialize two empty lists to hold the latitude and longitude values
latitude = [54.859997]
longitude = [83.108686] 

# Initialize the map to the first location in the list
gmap = gmplot.GoogleMapPlotter(latitude[0],longitude[0],18)

# Draw the points on the map. I created my own marker for '#FF66666'. 
# You can use other markers from the available list of markers. 
# Another option is to place your own marker in the folder - 
# /usr/local/lib/python3.5/dist-packages/gmplot/markers/
gmap.apikey="AIzaSyCEL8gvWxru0d2RLsGBU4BScU-SEcE1VLM"
gmap.scatter(latitude, longitude, '#FF6666', edge_width=10)

# Write the map in an HTML file
gmap.draw('map.html')
