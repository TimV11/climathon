import openeo
connection = openeo.connect("openeo.dataspace.copernicus.eu")   
connection.authenticate_oidc()